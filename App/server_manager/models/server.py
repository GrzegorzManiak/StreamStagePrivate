from django.db import models
from ip3country import CountryLookup
from StreamStage.secrets import CLOUDFLARE_TOKEN
from StreamStage.settings import DOMAIN_NAME, USE_CLOUDFLARE, acf
from django.core.validators import (
    MinLengthValidator, 
    validate_ipv4_address
)
from server_manager.library.common import ServerMode
from server_manager.models import Publisher

import uuid
import secrets
import CloudFlare
import country_converter

lookup = CountryLookup()

class Server(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    server_uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    region = models.CharField(
        max_length=3,
    )

    country = models.CharField(
        max_length=2,
    )
    

    slug = models.CharField(
        max_length=64,
        unique=True,
    )

    name = models.CharField(
        validators=[
            MinLengthValidator(3)
        ],
        max_length=64,
    )

    mode = models.CharField(
        max_length=2,
        choices=[
            ('I', 'Ingest'),
            ('R', 'Relay'),
            ('RR', 'Root Relay'),
        ],
        default='I',
    )

    secret = models.CharField(
        validators=[
            MinLengthValidator(3),
        ],
        max_length=64,
        default=secrets.token_urlsafe,
    )


    rtmp_ip = models.GenericIPAddressField(
        protocol='IPv4', null=True, blank=True)
    rtmp_port = models.PositiveIntegerField(
        null=True, blank=True)

    http_ip = models.GenericIPAddressField(
        protocol='IPv4', null=True, blank=True)
    http_port = models.PositiveIntegerField(
        null=True, blank=True)

    rtmp_url = models.URLField(
        null=True, blank=True
    )
    http_url = models.URLField(
        null=True, blank=True
    )


    live = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name


    # ========= Functions ========= #
    def set_mode(self, mode: ServerMode) -> None:
        # Make sure no other servers are using this mode
        for pub in Publisher.objects.all():
            if pub.ingest_server == self:
                raise ValueError('Cannot change the mode of an ingest server')

            if self in pub.server_list.all():
                raise ValueError('Cannot change the mode of a publisher server')
        
        mode = mode.to_string()
    
        if mode is not None: self.mode = mode
        else: raise ValueError('Invalid server mode')

        self.save()

    def get_mode(self) -> ServerMode or ValueError:
        mode = ServerMode.from_string(self.mode)

        if mode is not None: return mode
        else: raise ValueError('Invalid server mode')

    def regenerate_secret(self) -> None:
        self.secret = secrets.token_urlsafe()
        self.save()

    def announce(self, ip, port, hb_id) -> None:
        self.live = True
        
        # Validate the IP and port
        try: validate_ipv4_address(ip)
        except: raise ValueError('Invalid IP address')

        # Validate the port
        if port < 0 or port > 65535:
            raise ValueError('Invalid port')

        # TODO: Here we would spawn a thread to
        # monitor the heartbeat of the server
        # but we haven't implemented the 
        # heartbeat system yet

        self.ip = ip
        self.port = port

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'mode': self.mode,
            'slug': self.slug,
            'region': self.region,
            'rtmp_ip': self.rtmp_ip,
            'rtmp_port': self.rtmp_port,
            'http_ip': self.http_ip,
            'http_port': self.http_port,
            'secret': self.secret,
            'live': self.live,
            'rtmp_url': self.rtmp_url,
            'http_url': self.http_url,
        }

    def display(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'mode': self.mode,
            'slug': self.slug,
            'region': self.region,
            'rtmp_url': self.rtmp_url,
            'http_url': self.http_url,
            'live': self.live,
        }

    def set_region(self) -> None:
        try: 
            cc = lookup.lookupStr(self.rtmp_ip)
            continent = country_converter.convert(names=cc, to='continent')
            continent = continent[:2]
            self.region = continent.upper()
            self.country = cc.upper()

        except: 
            self.region = 'UNK'
            self.country = 'UNK'
        
    def update_slug(self) -> None:
        """
            We need to count all other servers
            with the same region so we can 
            generate a unique slug for this node

            This method of looping through all the
            same region servers is the most efficient
            as it gets the lowest number that is not
            taken, and it only has to loop through
            the servers once.
        """
        regions = Server.objects.filter(region=self.region).all()
        count = 0

        # -- If the count is None, we need to generate a new one
        for region in regions:
            if region.slug.startswith(f'{count}'): count += 1
            else: break
                

        self.slug = f'{count}.{self.country}.{self.region}'.upper()
    
    def update_cloudflare(self) -> bool:
        """
            This function will update the cloudflare
            DNS records for this server, my initial
            intention was to have a single wildcard
            DNS record for the nodes, but this would
            require me to redirect RTMP traffic,
            which is not a thing in the RTMP Spec.

            It took me a very very long time to figure
            that out, and im incredibly salty about it.
        """
        if not USE_CLOUDFLARE: return True

        # Get the zone ID
        zone = acf.zones.get(params={'name': DOMAIN_NAME})
        name = f'{self.slug.lower()}.rtmp'
        zone_id = zone[0]['id']
        records = acf.zones.dns_records.get(zone_id, params={
            "type": "A"
        })

        # Get the DNS records
        dns_entry = {
            'type': 'A',
            'content': self.rtmp_ip,
            'name': name.lower(),
            'ttl': 120,
            'proxied': False, # Can't proxy RTMP.
            'comment': f'{self.id}',
        }

        try: 
            # Check if the record exists
            for record in records:
                if record['name'].lower() == dns_entry['name'].lower() + '.' + DOMAIN_NAME.lower():
                    acf.zones.dns_records.put(zone_id, record['id'], data=dns_entry)
                    return True

            # If it doesn't exist, create it
            acf.zones.dns_records.post(zone_id, data=dns_entry)
            return True

        except Exception as e:
            print(e)
            return False

    # ========= Overrides ========= #
    def save(self, *args, **kwargs):
        self.set_region()
        self.update_slug()

        # -- Set the node url
        self.rtmp_url = f'rtmp://{self.rtmp_ip}:{self.rtmp_port}/live'
        self.http_url = f'http://{self.http_ip}:{self.http_port}/public'

        super(Server, self).save(*args, **kwargs)