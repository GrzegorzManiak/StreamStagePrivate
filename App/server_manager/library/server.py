from . import ServerMode
from server_manager.models.publisher import Publisher
from server_manager.models.server import Server

"""
    @name: get_servers_by_mode

    @description: Returns a list of servers that are currently
                  Being used for a specific mode in the system

    @param mode: The mode to check for
    @return: A list of servers
"""
def get_servers_by_mode(mode: ServerMode) -> list[Server]:
    server_list = []

    for pub in Publisher.objects.all():
        if pub.ingest_server.mode == mode.to_string():
            server_list.append(pub.ingest_server)

    return server_list



"""
    @name: get_publisher_by_server

    @description: Returns publishers that are currently
                  Using the specified server

    @param server: The server to check for
    @return: A list of publishers
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
