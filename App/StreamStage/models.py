from typing import Union
from django.db import models
import psutil
import uuid
import time
import datetime

MINUTE = 60
HOUR = 3600
DAY = 86400
WEEK = 604800
MONTH = 2592000
YEAR = 31536000

network_tx = []
network_rx = []
cpu = []
memory = []

kb = float(1024)
mb = float(kb ** 2)
gb = float(kb ** 3)

class SentEmail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email_id = models.UUIDField(default=uuid.uuid4, editable=False)
    member_id = models.UUIDField(null=True, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Statistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    statistic = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    value = models.IntegerField()
    created = models.IntegerField(default=time.time())

    def log(
        group: str, 
        statistic: str, 
        value: int = 1
    ):  
        """
            Logs a statistic
        """
        stat = Statistics(
            statistic=statistic,
            group=group,
            value=value
        )
        stat.save()



    def build_statistic(
        group: str, 
        statistic: str,
        time_frame: Union[int, int],
        frame_type: str = 'minute'
    ):
        """
            Builds a statistic dict between the two times
            format: {
                'lables': [ '1', '2', '3' ],
                'data': [ 1, 2, 3 ]
            }
        """
        time_frame = [ int(time_frame[0]), int(time_frame[1]) ]
        data = { 'labels': [], 'data': [] }

        # -- Create the labels and data
        dif = (time_frame[0] - time_frame[1])
        for i in range(dif):
            data['labels'].append(generate_lable(time_frame, frame_type, i))

        # -- Get the statistics (not system)
        if group == 'system':
            match statistic:
                case 'cpu': stats = cpu
                case 'memory': stats = memory
                case 'network_tx': stats = network_tx
                case 'network_rx': stats = network_rx

            # -- Process the statistics
            for i in range(dif):
                # -- Get the data
                stat = stats[i]

                # -- Add the data
                data['data'].append(stat)


        else: 
            stats = Statistics.objects.filter(
                group=group,
                statistic=statistic,
                created__gte=get_time(frame_type, time_frame[0]),
                created__lte=get_time(frame_type, time_frame[1])
            ).order_by('created')


            for i in range(dif):
                # -- Get the data
                stat = stats.filter( 
                    created__gte=get_time(frame_type, time_frame[0] - i),
                    created__lte=get_time(frame_type, time_frame[1] + i)
                )

                # -- Add the data
                data['data'].append(stat.count())



        data['labels'].reverse()
        data['data'].reverse()

        return data



def get_time(
    frame_type: str = 'minute',
    frame: int = 1,
) -> int:
    current_time = int(time.time())
    frame = int(frame)

    match frame_type:
        case 'minute': return current_time - int(frame * MINUTE)
        case 'hour': return current_time - int(frame * HOUR)
        case 'day': return current_time - int(frame * DAY)
        case 'week': return current_time - int(frame * WEEK)
        case 'month': return current_time - int(frame * MONTH)
        case 'year': return current_time - int(frame * YEAR)
        case _: raise Exception('Invalid frame')



def generate_lable(
    time_frame: Union[int, int],
    frame_type: str,
    frame: int,
) -> str:
    match frame_type:
        case 'minute': return f'{frame}m'
        case 'hour': return f'{frame}h' if frame > 9 else f'0{frame}:00h'
        case 'day': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%a')
        case 'week': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%b %d')
        case 'month': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%b')
        case 'year': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%b %d')



def get_network_usage():
    """
    Returns the network traffic in Mbps for the past second.
    """
    net_io_counters1 = psutil.net_io_counters()
    time.sleep(1)
    net_io_counters2 = psutil.net_io_counters()
    
    bytes_sent = net_io_counters2.bytes_sent - net_io_counters1.bytes_sent
    bytes_recv = net_io_counters2.bytes_recv - net_io_counters1.bytes_recv
    bits_sent = bytes_sent * 8
    bits_recv = bytes_recv * 8
    
    mbps_sent = bits_sent / 1000000
    mbps_recv = bits_recv / 1000000
    
    # Make sure that the values are a bit more than 0
    if mbps_sent < 0.01: mbps_sent = 0.01
    if mbps_recv < 0.01: mbps_recv = 0.01

    # Format the values to 2 decimal places
    mbps_sent = round(mbps_sent, 2)
    mbps_recv = round(mbps_recv, 2)

    return (mbps_sent, mbps_recv)



def get_cpu_usage():
    """
    Returns the CPU usage in percentage for the past second.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage



def get_memory_usage():
    """
    Returns the memory usage in percentage for the past second.
    """
    memory_usage = psutil.virtual_memory().percent
    return memory_usage



def log_stats():
    """
    Logs the statistics
    """
    # -- Get the stats
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    network_usage = get_network_usage()

    # -- Log the stats
    network_rx.append({
        'created': time.time(),
        'value': network_usage[1]
    })
    network_tx.append({
        'created': time.time(),
        'value': network_usage[0]
    })
    cpu_usage.append({
        'created': time.time(),
        'value': cpu_usage
    })
    memory_usage.append({
        'created': time.time(),
        'value': memory_usage
    })

    # Crimp the data to 1000 points
    network_rx = network_rx[-1000:]
    network_tx = network_tx[-1000:]
    cpu_usage = cpu_usage[-1000:]
    memory_usage = memory_usage[-1000:]