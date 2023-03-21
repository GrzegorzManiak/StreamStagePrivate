"""
    Shortest Route Resolver

    This module provides a wrapper for the shortest route resolver.
    Written in rust, it is compiled to a shared library and imported
    here, than wrapped in a python class to provide a more pythonic
    interface.
"""

from .srr import ShortestRouteResolverWrapper
import json

class NodeType:
    INGRESS = 0
    RELAY = 1
    EDGE = 2

    def __init__(self):
        pass

    def unk(node_type: str | int):
        if isinstance(node_type, NodeType):
            return node_type

        if not str(node_type).isnumeric():
            match str(node_type).lower():
                case "ingress": return NodeType.INGRESS
                case "relay": return NodeType.RELAY
                case "edge": return NodeType.EDGE
        
        match node_type:
            case 0: return NodeType.INGRESS
            case 1: return NodeType.RELAY
            case 2: return NodeType.EDGE

        return None
    
    def to_str(node_type: int):
        match node_type:
            case 0: return "Ingress"
            case 1: return "Relay"
            case 2: return "Edge"
        
        return None
    
    def translate_cc(node_type: str):
        match node_type.upper():
            case 'I': return NodeType.INGRESS
            case 'RR': return NodeType.RELAY
            case 'R': return NodeType.EDGE
        
        return None

# class SerializedTree:
#     __init__(self, raw_json: str):
#         self.raw_json = raw_json
#         self.tree = json.loads(raw_json)
    
#     def _process(self, node):
        
    


class Node():
    def __init__(
        self,
        set_node_usage,
        name,
        id,
        node_type,
        node_usage,
    ):
        # -- Public --
        self.name = name
        self.id = id
        self.type = node_type
        self.usage = node_usage

        # -- Private --
        self.__set_node_usage = set_node_usage

    def __str__(self):
        return f"{NodeType.to_str(self.type)}-{self.name}-{self.id}"

    
    def set_usage(self, node_usage):
        """
            Sets the usage of the node.
        """
        self.node_usage = node_usage
        self.__set_node_usage(self.id, node_usage)
    
    

        
class ShortestRouteResolver:
    def __init__(self):
        self.resolver = ShortestRouteResolverWrapper()


    """
        Gets a node from the resolver.

        Original:
        get_node(&self, node_id: usize) -> Option<&Node> 
    """
    def get_node(self, node_id: int) -> Node:
        node = self.resolver.get_node(node_id)
        if node is None: return None
            
        return Node(
            self.set_node_usage,
            node[0],
            node[1],
            NodeType.unk(node[2]),
            node[3],
        )
    


    """
        Gets an ID from a Node, or just returns the ID if it's already an ID.
    """
    def get_node_id(self, node_id: int | Node) -> int:
        id = node_id if isinstance(node_id, int) else node_id.id
        if id is None: raise Exception("Invalid node id.")
        return id



    """
        Adds a node to the resolver.

        Original:
        add_node(&mut self, node_type: NodeType, node_usage: usize) -> usize
    """
    def add_node(self, name: str, type: NodeType, latency: int = 0, usage: int = 0, auto_connect = True) -> Node:
        node_id = self.resolver.add_node(name, type, latency, usage)

        if auto_connect:
            data = json.loads(self.to_json())
            for node in data["nodes"]:
                if node["node_id"] != node_id: 
                    # -- We have to make sure that we dont connect a
                    #    Node to itself, A edge node to an edge node,
                    #    an ingress node to an ingress node, or a
                    #    ingress node to an edge node.
                    if (
                        (node["node_type"] == 'Ingress' and type == 'Ingress') or
                        (node["node_type"] == 'Edge' and type == 'Edge') or
                        (node["node_type"] == 'Ingress' and type == 'Edge') or
                        (node["node_type"] == 'Edge' and type == 'Ingress')
                    ): continue
                    self.add_connection(node_id, node["node_id"])

        return self.get_node(node_id)



    """
        Adds a link/connection between two nodes.

        Original:
        add_connection(&mut self, node_a_id: usize, node_b_id: usize) -> usize
    """
    def add_connection(
            self, 
            node_a_id: int | Node,
            node_b_id: int | Node
        ) -> int:
        return self.resolver.add_connection(
            self.get_node_id(node_a_id),
            self.get_node_id(node_b_id),
        )
    


    """
        Set the usage of a node.

        Original:
        set_node_usage(&mut self, node_id: usize, node_usage: usize)
    """
    def set_node_usage(self, node, node_usage):
        return self.resolver.set_node_usage(
            self.get_node_id(node),
            node_usage
        )
    


    """
        Shortest path between two nodes.

        Original:
        shortest_route(&self, node_a_id: usize, node_b_id: usize, max_hops: usize) -> Option<Vec<usize>>
    """
    def shortest_route(self, node_a, node_b, max_hops = 100):
        return self.resolver.shortest_route(
            self.get_node_id(node_a),
            self.get_node_id(node_b),
            max_hops
        )
    


    """
        Serializes the resolver to JSON.

        Original:
        to_json(&self) -> String
    """
    def to_json(self):
        return self.resolver.to_json()
    


    """
        Suggests a node type for a node, given
        the current state of the resolver.
    """
    def suggest_node_type(self, as_cc: bool = True):
        mode = self.resolver.suggest_node_type()
        if not as_cc: return mode

        match mode.lower():
            case "ingress": return "I"
            case "relay": return "RR"
            case "edge": return "R"