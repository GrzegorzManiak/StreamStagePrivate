import { connection_layer, node_layer, text_layer } from '..';
import { Data } from '../index.d';
import { add_connection } from './connection';
import { add_node, calculate_offset, get_formated_nodes } from './node';

// -- This is temporary code to get the visualizer working
const raw_data = '{"connections":[{"connection_id":1,"node_a_id":1,"node_b_id":3,"usage_count":0,"weight":25},{"connection_id":2,"node_a_id":1,"node_b_id":4,"usage_count":0,"weight":10},{"connection_id":3,"node_a_id":1,"node_b_id":5,"usage_count":0,"weight":5},{"connection_id":4,"node_a_id":2,"node_b_id":3,"usage_count":0,"weight":25},{"connection_id":5,"node_a_id":2,"node_b_id":4,"usage_count":0,"weight":10},{"connection_id":6,"node_a_id":2,"node_b_id":5,"usage_count":0,"weight":5},{"connection_id":7,"node_a_id":6,"node_b_id":3,"usage_count":0,"weight":40},{"connection_id":8,"node_a_id":7,"node_b_id":3,"usage_count":0,"weight":45},{"connection_id":9,"node_a_id":8,"node_b_id":3,"usage_count":0,"weight":70},{"connection_id":10,"node_a_id":9,"node_b_id":3,"usage_count":0,"weight":35},{"connection_id":11,"node_a_id":10,"node_b_id":3,"usage_count":0,"weight":30},{"connection_id":12,"node_a_id":6,"node_b_id":4,"usage_count":0,"weight":25},{"connection_id":13,"node_a_id":7,"node_b_id":4,"usage_count":0,"weight":30},{"connection_id":14,"node_a_id":8,"node_b_id":4,"usage_count":0,"weight":55},{"connection_id":15,"node_a_id":9,"node_b_id":4,"usage_count":0,"weight":20},{"connection_id":16,"node_a_id":10,"node_b_id":4,"usage_count":0,"weight":15},{"connection_id":17,"node_a_id":6,"node_b_id":5,"usage_count":0,"weight":20},{"connection_id":18,"node_a_id":7,"node_b_id":5,"usage_count":0,"weight":25},{"connection_id":19,"node_a_id":8,"node_b_id":5,"usage_count":0,"weight":50},{"connection_id":20,"node_a_id":9,"node_b_id":5,"usage_count":0,"weight":15},{"connection_id":21,"node_a_id":10,"node_b_id":5,"usage_count":0,"weight":10}],"nodes":[{"node_id":1,"node_latency":0,"node_type":"Ingress","node_usage":0},{"node_id":2,"node_latency":0,"node_type":"Ingress","node_usage":0},{"node_id":3,"node_latency":50,"node_type":"Relay","node_usage":0},{"node_id":4,"node_latency":20,"node_type":"Relay","node_usage":0},{"node_id":5,"node_latency":10,"node_type":"Relay","node_usage":0},{"node_id":6,"node_latency":30,"node_type":"Edge","node_usage":0},{"node_id":7,"node_latency":40,"node_type":"Edge","node_usage":0},{"node_id":8,"node_latency":90,"node_type":"Edge","node_usage":0},{"node_id":9,"node_latency":20,"node_type":"Edge","node_usage":0},{"node_id":10,"node_latency":10,"node_type":"Edge","node_usage":0}]}'
const data_obj = JSON.parse(raw_data) as Data;


// -- To evenly space the nodes, we need to know how many of each type there are
let ingress_count = 0, relay_count = 0, edge_count = 0;
data_obj.nodes.forEach(node => {
    switch (node.node_type) {
        case 'Ingress': return node.z = ingress_count++;
        case 'Relay': return node.z = relay_count++;
        case 'Edge': return node.z = edge_count++;
    }
});



/**
 * @name deserialize
 * @description Deserializes the data object into the visualizer
 * @param {Data} data The data object to deserialize
 * @returns {void}
 */
export function deserialize(
    data: Data = data_obj
) {

    const {x, y} = calculate_offset(
        ingress_count,
        relay_count,
        edge_count
    );


    //
    // Nodes
    //
    data.nodes.forEach(node => add_node(
        node,
        edge_count,
        relay_count,
        text_layer,
        node_layer,
        x, y
    ));


    //
    // -- Get the formatted nodes
    //
    const processed_nodes = get_formated_nodes();
    

    //
    // Connections
    // 
    data.connections.forEach(connection => add_connection(
        connection,
        processed_nodes.find(node => node.node.node_id === connection.node_a_id),
        processed_nodes.find(node => node.node.node_id === connection.node_b_id),
        connection_layer,
        text_layer
    ));
}