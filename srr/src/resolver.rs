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
    pub fn add_node(&mut self, name: String, node_type: NodeType, node_usage: usize) -> usize {
        // -- Generate a unique ID for the node
        let node_id = self.nodes.iter().map(|n| n.node_id).max().unwrap_or(0) + 1;

        // -- Check for ID collision
        assert!(!self.get_node(node_id).is_some(), "Node ID already exists");

        // Add the new node to the graph
        let node = Node { name, node_id, node_type, node_usage };
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


    // -- Sets a Nodes usage
    pub fn set_node_usage(&mut self, node_id: usize, node_usage: usize) {
        // -- Ensure that the usage is between 0.0 and 1.0
        let node_usage = node_usage.max(0).min(100);

        // -- Find the node
        let node = self.nodes.iter_mut().find(|n| n.node_id == node_id).unwrap();

        // -- Set the usage
        node.node_usage = node_usage;
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
            _ => { panic!("Invalid connection between node types."); }
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
            // If we've reached the end node, return the shortest path
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


            // -- Stop searching if we've exceeded the maximum number of hops
            if let Some(path_distance) = distances.get(&node_id) {
                if path_distance >= &max_hops { continue; }
            }


            // -- Add unvisited neighbors to the priority queue
            let connections = self
                .connections
                .iter()
                .filter(|c| c.node_a_id == node_id || c.node_b_id == node_id);

            for connection in connections {
                let neighbor_id = if connection.node_a_id == node_id {
                    connection.node_b_id } 
                
                else { connection.node_a_id };

                let neighbor = self.nodes.iter().find(|n| n.node_id == neighbor_id).unwrap();

                // -- Calculate the weight of the connection (usage of both nodes / 2)
                let connection_weight = (node_a.node_usage + neighbor.node_usage) / 2;

                // -- Calculate the distance to the neighbor node
                let neighbor_distance = distance + connection_weight;

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
                    "connection_id": c.connection_id
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
                    "node_usage": n.node_usage
                })
            })
            .collect::<Vec<_>>();

        json!({
            "connections": connections,
            "nodes": nodes
        }).to_string()
    }
}