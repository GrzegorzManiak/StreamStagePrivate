use pyo3::prelude::*;

pub mod node;
pub mod connection;
mod resolver;

use node::{node_type_to_string, string_to_node_type};
use resolver::ShortestRouteResolver;


// -- name, node_id, node_type, node_latency, node_usage
type GetNodeResult = (String, usize, String, usize, usize);

#[pyclass]
struct ShortestRouteResolverWrapper {
    resolver: ShortestRouteResolver,
}

#[pymethods]
impl ShortestRouteResolverWrapper {
    #[new]
    fn new() -> Self {
        ShortestRouteResolverWrapper {
            resolver: ShortestRouteResolver::new(),
        }
    }

    fn get_node(&self, node_id: usize) -> PyResult<GetNodeResult> {
        let node = self.resolver.get_node(node_id).unwrap();
        Ok((node.name.clone(), node.node_id, node_type_to_string(&node.node_type), node.node_latency, node.node_usage))
    }

    fn add_node(&mut self, name: &str, node_type: &str, node_latency: usize, node_usage: usize)  -> PyResult<usize> {
        let node_type = string_to_node_type(&node_type);
        Ok(self.resolver.add_node(name.to_string(), node_type, node_latency, node_usage))
    }

    fn add_connection(&mut self, node_a_id: usize, node_b_id: usize) -> PyResult<usize> {
        Ok(self.resolver.add_connection(node_a_id, node_b_id))
    }

    fn set_node_weight(&mut self, node_id: usize, node_latency: usize, node_usage: usize) -> PyResult<()> {
        self.resolver.set_node_weight(node_id, node_latency, node_usage);
        Ok(())
    }

    fn shortest_route(&self, node_a_id: usize, node_b_id: usize, max_hops: usize) -> PyResult<Option<Vec<usize>>> {
        match self.resolver.shortest_route(node_a_id, node_b_id, max_hops) {
            Some(route) => Ok(Some(route.clone())),
            None => Ok(None),
        }
    }

    fn suggest_node_type(&self) -> PyResult<String> {
        Ok(node_type_to_string(&self.resolver.suggest_node_type()))
    }

    fn to_json(&self) -> PyResult<String> {
        Ok(self.resolver.to_json())
    }
}


#[pymodule]
fn srr(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<ShortestRouteResolverWrapper>()?;

    Ok(())
}