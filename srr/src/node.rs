use pyo3::prelude::*;

#[pyclass]
#[derive(Debug, Clone)]
pub enum NodeType {
    Ingress,
    Relay,
    Edge,
}

pub fn node_type_to_string(node_type: &NodeType) -> String {
    match node_type {
        NodeType::Ingress => "Ingress".to_string(),
        NodeType::Relay => "Relay".to_string(),
        NodeType::Edge => "Edge".to_string(),
    }
}

pub fn string_to_node_type(node_type: &str) -> NodeType {
    match node_type {
        "Ingress" => NodeType::Ingress,
        "Relay" => NodeType::Relay,
        "Edge" => NodeType::Edge,
        _ => panic!("Invalid node type"),
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Node {
    pub name: String,
    pub node_id: usize,
    pub node_type: NodeType,
    pub node_latency: usize,
    pub node_usage: usize,
}

impl Node {
    fn new(
        name: String, 
        node_id: usize, 
        node_type: NodeType, 
        node_usage: usize,
        node_latency: usize,
    ) -> Self {
        // -- Ensure that the weight is between 0.0 and 1.0
        let node_usage = node_usage.max(0).min(100);

        // -- Create the node
        Self {
            name, 
            node_id, 
            node_type, 
            node_usage,
            node_latency, 
        }
    }

    pub fn Clone(&self) -> Self {
        Self {
            name: self.name.clone(),
            node_id: self.node_id,
            node_type: self.node_type.clone(),
            node_latency: self.node_latency,
            node_usage: self.node_usage,
        }
    }
}
