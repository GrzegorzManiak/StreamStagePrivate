from . import ServerMode
from server_manager.models.publisher import Publisher
from server_manager.models.server import Server

import uuid
from .router import router

"""
    :name: get_servers_by_mode

    :description: Returns a list of servers that are currently
                  Being used for a specific mode in the system

    :param mode: The mode to check for
    :return: A list of servers
"""
def get_servers_by_mode(mode: ServerMode) -> list[Server]:
    server_list = []

    for pub in Publisher.objects.all():
        if pub.ingest_server.mode == mode.to_string():
            server_list.append(pub.ingest_server)

    return server_list



"""
    :name: get_publisher_by_server

    :description: Returns publishers that are currently
                  Using the specified server

    :param server: The server to check for
    :return: A list of publishers
"""
def get_publisher_by_server(server: Server) -> list[Publisher]:
    publisher_list = []

    for pub in Publisher.objects.all():
        if pub.ingest_server.id == server.id:
            publisher_list.append(pub)
            continue

        for s in pub.server_list.all():
            if s.id == server.id:
                publisher_list.append(pub)

    return publisher_list



"""
    :name: get_all_servers
    :param active: If the server should be active or not
    :return: A list of servers
"""
def get_all_servers(active: bool = True) -> list[Server]:
    servers = []
    if active: servers = Server.objects.filter(live=True)
    else: servers = Server.objects.all()

    return [server.serialize() for server in servers]



"""
    :name: add_server
    :description: This function is used to add a server to the database.
    :param rtmp_ip: The IP address of the RTMP server
    :param rtmp_port: The port of the RTMP server
    :param http_ip: The IP address of the HTTP server
    :param http_port: The port of the HTTP server
    :return: The server object or None

    :note: This function will return None if the server already exists
           And usally the rtmp_ip and http_ip will be the same, just 
           the ports will be different.
"""
def add_server(
    server_uuid: uuid.UUID,
    rtmp_ip: str,
    rtmp_port: int,
    http_ip: str,
    http_port: int,
) -> Server or None:
    """
        This function is used to add a server to the database.
    """

    # -- Check if the server already exists
    try:
        server = Server.objects.get(server_uuid=server_uuid)

        if server is not None:
            # -- Update the server
            server.rtmp_port = rtmp_port
            server.http_port = http_port
            server.save()
            
            server.regenerate_secret()
            if server.update_cloudflare() == False:
                return None 
            
            # -- Update the router configuration
            router.add_node(
                name=str(server.id),
                type='Relay',
                latency=0,
                usage=0,
            )

            return server
    except Exception as e:
        print(e)
        
    # -- Create the server
    server = Server(
        server_uuid=server_uuid,
        rtmp_ip=rtmp_ip,
        rtmp_port=rtmp_port,
        http_ip=http_ip,
        http_port=http_port,
    )
    server.save()
    if server.update_cloudflare() == False:
        return None
    
    # -- Update the router configuration
    router.add_node(
        name=str(server.id),
        type='Relay',
        latency=0,
        usage=0,
    )
    
    return server