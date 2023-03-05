use std::{collections::{HashMap, BinaryHeap}, cmp::Reverse};
use serde_json::json;

use crate::{
    node::{node_type_to_string, Node, NodeType}, 
    connection::NodeConnection
};


pub struct ShortestRouteResolver {
    // -- The connections between nodes
    connections: Vec<NodeConnection>,

    // -- The nodes
    nodes: Vec<Node>,
}

impl ShortestRouteResolver {
    pub fn new() -> Self {
        Self {
            connections: Vec::new(),
            nodes: Vec::new(),
        }
    }



    // -- Gets a node by its ID
    pub fn get_node(&self, node_id: usize) -> Option<&Node> {
        self.nodes.iter().find(|n| n.node_id == node_id)
    }



    // -- Adds a new node to the graph
    pub fn add_node(&mut self, name: String, node_type: NodeType, node_latency: usize, node_usage: usize) -> usize {
        // -- Generate a unique ID for the node
        let node_id = rand::random::<u32>() as usize;

        // -- Check for ID collision
        assert!(!self.get_node(node_id).is_some(), "Node ID already exists");

        // Add the new node to the graph
        let node = Node { name, node_id, node_type, node_latency, node_usage};
        self.nodes.push(node);
        node_id
    }



    // -- Adds a new connection to the graph
    pub fn add_connection(&mut self, node_a_id: usize, node_b_id: usize) -> usize {
        // Generate a unique ID for the connection
        let connection_id = self
            .connections
            .iter()
            .map(|c| c.connection_id)
            .max()
            .unwrap_or(0)
            + 1;

        // Check for ID collision
        assert!(
            !self
                .connections
                .iter()
                .any(|c| c.connection_id == connection_id),
            "Connection ID already exists"
        );

        // Check if the connection is valid according to the node types
        let node_a = self.nodes.iter().find(|n| n.node_id == node_a_id).unwrap();
        let node_b = self.nodes.iter().find(|n| n.node_id == node_b_id).unwrap();

        match (node_a.node_type.clone(), node_b.node_type.clone()) {
            (NodeType::Ingress, NodeType::Relay) | 
            (NodeType::Relay, NodeType::Ingress) |
            (NodeType::Relay, NodeType::Edge) |
            (NodeType::Edge, NodeType::Relay) |
            (NodeType::Relay, NodeType::Relay) => {
                let connection = NodeConnection {
                    node_a_id,
                    node_b_id,
                    usage_count: 0,
                    connection_id,
                };
                self.connections.push(connection);
                connection_id
            }
            
            // -- Invalid connection
            _ => panic!("Invalid connection"),
        }
    }




    // -- Sets a Nodes weight
    pub fn set_node_weight(
        &mut self, 
        node_id: usize, 
        node_latency: usize, 
        node_usage: usize
    ) {
        // -- Ensure that the weight is between 0 and 100
        let node_usage = node_usage.max(0).min(100);

        // -- Find the node
        let node = self.nodes.iter_mut().find(|n| n.node_id == node_id).unwrap();

        // -- Set the weights
        node.node_latency = node_latency;
        node.node_usage = node_usage;
    }

    
    
    // -- Calculates the weight of a connection
    pub fn calculate_weight(
        &self, 
        connection_id: usize
    ) -> usize {
        // -- Find the connection
        let connection = self.connections.iter().find(|c| c.connection_id == connection_id).unwrap();

        // -- Find the nodes
        let node_a = self.nodes.iter().find(|n| n.node_id == connection.node_a_id).unwrap();
        let node_b = self.nodes.iter().find(|n| n.node_id == connection.node_b_id).unwrap();

        // -- Calculate the weight
        //    If usage is above x than set the weight 100 + (lat_a + lat_b) / 2
        //    If usage is below x than set the weight ((lat_a + lat_b) / 2) * 0.3 - ((usage_a + usage_b) / 2) * 0.7
        let weight = if node_a.node_usage > 50 || node_b.node_usage > 50 
        {
            100 + (node_a.node_latency + node_b.node_latency) / 2
        } else {
            (((node_a.node_latency + node_b.node_latency) / 2) as f64 * 0.3 -
            ((node_a.node_usage + node_b.node_usage) / 2) as f64 * 0.7) as usize
        };
        weight
    }



    // -- Returns the shortest route between two nodes
    pub fn shortest_route(&self, node_a_id: usize, node_b_id: usize, max_hops: usize) -> Option<Vec<usize>> {
        // -- Find the start and end nodes
        let node_a = self.nodes.iter().find(|n| n.node_id == node_a_id)?;
        let node_b = self.nodes.iter().find(|n| n.node_id == node_b_id)?;


        // -- Check if the start and end nodes are valid according to the node types
        match (node_a.node_type.clone(), node_b.node_type.clone()) {
            (NodeType::Ingress, NodeType::Edge) |
            (NodeType::Edge, NodeType::Ingress) |
            (NodeType::Ingress, NodeType::Relay) | 
            (NodeType::Relay, NodeType::Ingress) | 
            (NodeType::Relay, NodeType::Relay) => (),
            _ => panic!("Invalid connection between node types."),
        }


        // -- Create a map of nodes to their shortest distance from the start node
        let mut distances = HashMap::new();
        distances.insert(node_a_id, 0);

        // -- Create a map of nodes to their previous node in the shortest path
        let mut previous = HashMap::new();

        // -- Create a priority queue of nodes to visit, starting with the start node
        let mut queue = BinaryHeap::new();
        queue.push(Reverse((0, node_a_id)));

        while let Some(Reverse((distance, node_id))) = queue.pop() {



            //
            // We've found the end node, so we can stop searching
            //
            if node_id == node_b_id {
                let mut path = vec![node_id];
                let mut current_node_id = node_id;

                while let Some(prev_node_id) = previous.get(&current_node_id) {
                    path.push(*prev_node_id);
                    current_node_id = *prev_node_id;
                }

                path.reverse();
                return Some(path);
            }



            // 
            // Max hops reached, so we can stop searching
            // This is mainly to prevent infinite loops
            //
            if let Some(path_distance) = distances.get(&node_id) {
                if path_distance >= &max_hops { continue; }
            }


            // 
            // Find all connections that contain the current node
            //
            let connections = self
                .connections
                .iter()
                .filter(|c| 
                    c.node_a_id == node_id || 
                    c.node_b_id == node_id
                );
            

            //
            // Loop through all connections that contain the current node
            //
            for connection in connections {

                let neighbor_id = 
                if connection.node_a_id == node_id { connection.node_b_id } 
                else { connection.node_a_id };

                // -- Calculate the distance to the neighbor node
                let neighbor_distance = distance + self.calculate_weight(connection.connection_id);

                // -- Update the neighbor's distance and previous node if it's a new shortest path
                let is_shorter = match distances.get(&neighbor_id) {
                    None => true,
                    Some(&current_distance) => neighbor_distance < current_distance,
                };

                // -- Add the neighbor to the queue if it's a new shortest path
                if is_shorter {
                    distances.insert(neighbor_id, neighbor_distance);
                    previous.insert(neighbor_id, node_id);
                    queue.push(Reverse((neighbor_distance, neighbor_id)));
                }
            }
        }

        None
    }


    // -- Returns the node type that should be added to the network
    //    depending on the current node types and usage
    pub fn suggest_node_type(&self) -> NodeType {
        // -- Get all the nodes
        let ingress_nodes = self.nodes.iter().filter(|n| n.node_type == NodeType::Ingress).collect::<Vec<&Node>>();
        let relay_nodes = self.nodes.iter().filter(|n| n.node_type == NodeType::Relay).collect::<Vec<&Node>>();
        let edge_nodes = self.nodes.iter().filter(|n| n.node_type == NodeType::Edge).collect::<Vec<&Node>>();


        // -- Calculate average usage across all nodes
        let ingress_usage = ingress_nodes.iter().map(|n| n.node_usage).sum::<usize>() / ingress_nodes.len();
        let relay_usage = relay_nodes.iter().map(|n| n.node_usage).sum::<usize>() / relay_nodes.len();
        let edge_usage = edge_nodes.iter().map(|n| n.node_usage).sum::<usize>() / edge_nodes.len();

        // -- Calculate average latency across all nodes
        let ingress_latency = ingress_nodes.iter().map(|n| n.node_latency).sum::<usize>() / ingress_nodes.len();
        let relay_latency = relay_nodes.iter().map(|n| n.node_latency).sum::<usize>() / relay_nodes.len();
        let edge_latency = edge_nodes.iter().map(|n| n.node_latency).sum::<usize>() / edge_nodes.len();


        // -- Calculate average weight across all connections
        let ingress_weight = ingress_latency as f64 * ingress_usage as f64;
        let relay_weight = relay_latency as f64 * relay_usage as f64;
        let edge_weight = edge_latency as f64 * edge_usage as f64;

        // -- Return the node type with the lowest weight
        if ingress_weight < relay_weight && ingress_weight < edge_weight { NodeType::Ingress } 
        else if relay_weight < ingress_weight && relay_weight < edge_weight { NodeType::Relay } 
        else { NodeType::Edge }
    }


    // -- Serializes the network to a JSON string
    pub fn to_json(&self) -> String {
        let connections = self
            .connections
            .iter()
            .map(|c| {
                json!({
                    "node_a_id": c.node_a_id,
                    "node_b_id": c.node_b_id,
                    "usage_count": c.usage_count,
                    "connection_id": c.connection_id,
                    "weight": self.calculate_weight(c.connection_id)
                })
            })
            .collect::<Vec<_>>();

        let nodes = self
            .nodes
            .iter()
            .map(|n| {
                json!({
                    "node_id": n.node_id,
                    "node_type": node_type_to_string(&n.node_type),
                    "node_latency": n.node_latency,
                    "node_usage": n.node_usage,
                    "node_name": n.name.clone()
                })
            })
            .collect::<Vec<_>>();

        json!({
            "connections": connections,
            "nodes": nodes
        }).to_string()
    }
}