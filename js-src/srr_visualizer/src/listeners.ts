import Konva from 'konva';
import { NodeDataLink } from '../index.d';
import { align_connection, get_connections, reset_connection } from './connection';
import { center_text, focus_node, get_formated_nodes, unfocus_node } from './node';

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

        // -- Focus the node
        get_formated_nodes().forEach((n_node) => 
            unfocus_node(n_node));

        focus_node(node);
    });


    // -- On click, color the connections red
    node.conva_circle.on('click', (e) => {
        // -- Focus the node
        get_formated_nodes().forEach((n_node) => 
            unfocus_node(n_node));

        focus_node(node);
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

        // -- Get the nodes
        get_formated_nodes().forEach((node) => {
            unfocus_node(node);
        });

    });
}