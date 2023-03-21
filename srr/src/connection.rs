use pyo3::prelude::*;

#[pyclass]
pub struct NodeConnection {
    pub node_a_id: usize,
    pub node_b_id: usize,

    // -- The number of times this connection has been used
    pub usage_count: usize,
    
    // -- The id of this connection
    pub connection_id: usize,
}

impl NodeConnection {
    fn new(
        node_a_id: usize, 
        node_b_id: usize,
        connection_id: usize,
    ) -> Self {

        // -- Create the connection
        Self {
            node_a_id, node_b_id,
            usage_count: 0,
            connection_id,
        }
    }
}