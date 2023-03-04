import Konva from 'konva';
import { NodeDataLink } from '../index.d';
import { calculate_color, get_connections } from './connection';
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
        
        // -- Update the connections
        connections.forEach((connection) => {
            // -- If the node is the first node in the connection
            if (connection.connection.node_a.node_id === node.node.node_id) {
                connection.conva_line.points([e.target.x(), e.target.y(), connection.connection.node_b.x, connection.connection.node_b.y]);
                calculate_color(connection);
                connection.conva_text.text(connection.connection.weight.toString());

                // -- Update the text
                connection.conva_text.x((e.target.x() + connection.connection.node_b.x) / 2);
                connection.conva_text.y((e.target.y() + connection.connection.node_b.y) / 2);

                // -- Prioritize the connection
                connection.conva_line.moveToTop();
                connection.conva_text.moveToTop();
            } 

            // -- If the node is the second node in the connection
            else if (connection.connection.node_b.node_id === node.node.node_id) {
                connection.conva_line.points([connection.connection.node_a.x, connection.connection.node_a.y, e.target.x(), e.target.y()]);
                calculate_color(connection);
                connection.conva_text.text(connection.connection.weight.toString());

                // -- Update the text
                connection.conva_text.x((connection.connection.node_a.x + e.target.x()) / 2);
                connection.conva_text.y((connection.connection.node_a.y + e.target.y()) / 2);

                // -- Prioritize the connection
                connection.conva_line.moveToTop();
                connection.conva_text.moveToTop();
            }

            // -- Else the node is not in the connection
            else {
                connection.conva_line.stroke('black');
                connection.conva_text.text('');
            }
        });
    });


    // -- On click, color the connections red
    node.conva_circle.on('click', (e) => {

        // -- Get the connections
        const connections = get_connections();

        connections.forEach((connection) => {
            // -- If the node is the first node in the connection
            if (
                connection.connection.node_a.node_id === node.node.node_id ||
                connection.connection.node_b.node_id === node.node.node_id
            ) {
                calculate_color(connection);
                connection.conva_text.text(connection.connection.weight.toString());

                // -- Prioritize the connection
                connection.conva_line.moveToTop();
                connection.conva_text.moveToTop();
            }
            
            // -- Else the node is not in the connection
            else {
                connection.conva_line.stroke('black');   
                connection.conva_text.text('');
            }
        });
    });
}



export function add_stage_listners(stage: Konva.Stage) {

    // -- Event listener for the stage so tat we can update the connections
    //    when the stage is resized, or clicked
    stage.on('resize', (e) => {
        // -- Get the formated connections
        const connections = get_connections();
        
        connections.forEach((connection) => {
            connection.conva_line.points([connection.connection.node_a.x, connection.connection.node_a.y, connection.connection.node_b.x, connection.connection.node_b.y]);
        });
    });

    stage.on('click', (e) => {
        // -- The stage is the first thing added, so its id is one
        //    therefore we can use this to check if the click was on the stage
        //    or on a node
        if (e.target._id !== 1) return;

        // -- Get the formated connections
        get_connections().forEach((connection) => {
            calculate_color(connection);
            connection.conva_text.text(connection.connection.weight.toString());
        });
    });
}