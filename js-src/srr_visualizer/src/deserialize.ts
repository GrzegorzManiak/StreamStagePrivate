import { connection_layer, node_layer, text_layer } from '..';
import { create_toast } from '../../toasts';
import { Data, Server } from '../index.d';
import { add_connection, delete_connections, focous_connection } from './connection';
import { add_node, calculate_offset, center_text, delete_node, focus_node, get_formated_nodes } from './node';

let init = true;

/**
 * @name deserialize
 * @description Deserializes the data object into the visualizer
 * @param {Data} data The data object to deserialize
 * @returns {void}
 */
export function deserialize(
    data: Data,
    servers: Array<Server>,
) {
    // -- Purge the old nodes
    get_formated_nodes().forEach(node => {
        if (!data.nodes.find(data_node => data_node.node_id === node.node.node_id
        )) {
            delete_node(node.node.node_id);  
            if (init === false) create_toast(
                'info', 'Node Removed', 
                `Node ${node.node.node_id} has been removed from the network`
            )
        }
    });


    //
    // Nodes
    //
    let ingress_count, relay_count, edge_count;
    let local_ingress_count, local_relay_count, local_edge_count;

    // -- Count the nodes first
    ingress_count = data.nodes.filter(node => node.node_type === 'Ingress').length;
    relay_count = data.nodes.filter(node => node.node_type === 'Relay').length;
    edge_count = data.nodes.filter(node => node.node_type === 'Edge').length;
    
    get_formated_nodes().forEach(node => {
        switch (node.node.node_type) {
            case 'Ingress': if (node.node?.z > ingress_count) return ingress_count = node.node.z; break;
            case 'Relay': if (node.node?.z > relay_count) return relay_count = node.node.z; break;
            case 'Edge': if (node.node?.z > edge_count) return edge_count = node.node.z; break;
        }
    });

    local_ingress_count = ingress_count;
    local_relay_count = relay_count;
    local_edge_count = edge_count;

    const {x, y} = calculate_offset(
        ingress_count,
        relay_count,
        edge_count
    );

    data.nodes.forEach(node => {
        switch (node.node_type) {
            case 'Ingress': node.z = --local_ingress_count; break;
            case 'Relay': node.z = --local_relay_count; break;
            case 'Edge': node.z = --local_edge_count; break;
        }

        const new_node = add_node(
            node,
            edge_count,
            relay_count,
            text_layer,
            node_layer,
            x, y,
            init
        )

        // -- Check if a server exists for this node
        for(const server of servers) {
            if (node.node_name !== server.id) continue;

            // -- TODO: Click handlers etc
            new_node.conva_text.text(`${server.slug}`);
            center_text(new_node.conva_text, new_node.conva_circle);
        }
    });


    //
    // -- Get the formatted nodes
    //    and delete any old ones and old connections
    //
    let processed_nodes = get_formated_nodes();
    delete_connections();


    //
    // Connections
    // 
    data.connections.forEach(connection => {
        // -- Find the nodes that the connection is connected to
        const node_a = processed_nodes.find(node => node.node.node_id === connection.node_a_id);
        const node_b = processed_nodes.find(node => node.node.node_id === connection.node_b_id);

        // -- If the nodes don't exist, we can't create the connection
        if (!node_a || !node_b) return;

        // -- Create the connection
        add_connection(
            connection,
            node_a,
            node_b,
            connection_layer,
            text_layer
        )
    });


    // -- Focus any connections
    processed_nodes.forEach(node => {
        if (!node.focused) return;
        focus_node(node);
    });


    init = false;
}