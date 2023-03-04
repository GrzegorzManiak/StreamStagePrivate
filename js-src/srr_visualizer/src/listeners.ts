import Konva from 'konva';
import { ConectionDataLink, NodeDataLink } from '../index.d';
import { align_connection, focous_connection, get_connections, reset_connection, unfocous_connection } from './connection';
import { center_text } from './node';

/**
 * 
 */
export function add_node_listner(
    node: NodeDataLink
) {
    node.conva_circle.on('dragmove', (e) => {
        // -- Update the node
        node.node.x = e.target.x();
        node.node.y = e.target.y();

        // -- Update the text
        center_text(node.conva_text, node.conva_circle);

        // -- Get the connections
        const connections = get_connections();
        let to_focus: Array<ConectionDataLink> = [];
        
        // -- Update the connections
        connections.forEach((connection) => {
            if (connection.connection.node_a.node.node_id === node.node.node_id ||
                connection.connection.node_b.node.node_id === node.node.node_id
            ) to_focus.push(connection);
            else unfocous_connection(connection);
        });

        // -- Focus the connections
        to_focus.forEach((connection) => focous_connection(connection));
    });


    // -- On click, color the connections red
    node.conva_circle.on('click', (e) => {

        // -- Get the connections
        const connections = get_connections();
        let to_focus: Array<ConectionDataLink> = [];

        connections.forEach((connection) => {
            if (connection.connection.node_a.node.node_id === node.node.node_id ||
                connection.connection.node_b.node.node_id === node.node.node_id
            ) to_focus.push(connection);
            else unfocous_connection(connection);
        });

        // -- Focus the connections
        to_focus.forEach((connection) => focous_connection(connection));
    });
}



export function add_stage_listners(stage: Konva.Stage) {

    // -- Event listener for the stage so tat we can update the connections
    //    when the stage is resized, or clicked
    stage.on('resize', (e) => {
        // -- Get the formated connections
        const connections = get_connections();
        
        connections.forEach((connection) => align_connection(connection));
    });

    stage.on('click', (e) => {
        // -- The stage is the first thing added, so its id is one
        //    therefore we can use this to check if the click was on the stage
        //    or on a node
        if (e.target._id !== 1) return;

        // -- Get the formated connections
        get_connections().forEach((connection) => {
            reset_connection(connection);
        });
    });
}