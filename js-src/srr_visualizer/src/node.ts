import Konva from 'konva';
import { ProcessedNode, Node, NodeDataLink } from '../index.d';
import { add_node_listner } from './listeners';
import { colors, stage } from '..';

function degreesToRadians(degrees: number): number {
    return degrees * (Math.PI / 180);
}

// -- General
const X_SPACING = 200;
const Y_SPACING = 200;
const X_STAG = 25;


/**
 * @name calculate_offset
 * @description Calculates the offset for all nodes
 * so that they are centered on the screen
 * @param relay_count The number of relay nodes
 * @param edge_count The number of edge nodes
 * @param ingress_count The number of ingress nodes
 * @returns {
 *     x: number;  // The x offset  
 *     y: number;  // The y offset   
 * }
 */
export function calculate_offset(
    relay_count: number,
    edge_count: number,
    ingress_count: number
): {
    x: number;
    y: number;
} {
    // -- Get the largest number of nodes
    const max = Math.max(relay_count, edge_count, ingress_count);

    // -- Calculate the offset the center the at the center of the screen
    const height = max * Y_SPACING;
    const width = (X_SPACING * 3) + X_STAG;

    const x = stage.width() / 2 - width / 2;
    const y = stage.height() / 2 - height / 5;
    return { x, y };
}



let formated_nodes: NodeDataLink[] = [];
export const get_formated_nodes = () => formated_nodes;

/**
 * @name format_node
 * @description Formats a node to be used in the visualizer
 *            This is where the node's position is calculated
 * @param node The node to format
 * @param edge_count The number of edge nodes
 * @param relay_count The number of relay nodes
 * @returns {
 *      z: number;      // The node's z index
 *      x: number;      // The node's x position
 *      y: number;      // The node's y position
 *      color: string;  // The node's color
 * }
 */
export function format_node(
    node: ProcessedNode | Node,
    edge_count: number,
    relay_count: number,
    x_offset: number,
    y_offset: number
): {
    z: number;
    x: number;
    y: number;
    color: string;
} {

    // -- Ark
    const ELIPSE_HEIGHT = 50 * edge_count;
    const ELIPSE_WIDTH = 25 * edge_count;
    const ARK_ANGLE = 180;
    const ARK_ROTATION = -90;

    switch (node.node_type) {
        case 'Ingress': return {
                z: node.z,
                x: 0 + x_offset,
                y: y_offset + node.z * Y_SPACING,
                color: colors.ingress
            }


        case 'Relay': return {
                z: node.z,
                x: X_SPACING + x_offset + (node.z % 2) * X_STAG,
                y: y_offset + ((node.z / 2) * Y_SPACING * 1.5) - Y_SPACING / relay_count,
                color: colors.relay
            }


        case 'Edge':            
            const angle = degreesToRadians((ARK_ANGLE / (edge_count - 1)) * node.z);

            let x = Math.cos(angle + degreesToRadians(ARK_ROTATION)) * ELIPSE_WIDTH;
            let y = Math.sin(angle + degreesToRadians(ARK_ROTATION)) * ELIPSE_HEIGHT;

            return {
                z: node.z,
                x: x + x_offset + (X_SPACING * 2) + X_STAG,
                y: y + y_offset + Y_SPACING / 2,
                color: colors.edge
            } 
    }
}


/**
 * @name center_text
 * @description Centers a text element around a circle
 * @param text: Konva.Text - The text to center
 * @param circle: Konva.Circle - The circle to center the text around
 */
export function center_text(
    text: Konva.Text,
    circle: Konva.Circle
) {
    const cx = circle.x();
    const cy = circle.y();

    const x = cx - (text.width() / 2);
    const y = cy - (text.height() / 2);

    text.x(x);
    text.y(y);
}



/**
 * @name add_node
 * @description Adds a node to the visualizer
 * @param node: ProcessedNode | Node - The node to add
 * @param edge_count: number - The number of edge nodes
 * @param relay_count: number - The number of relay nodes
 * @param text_layer: Konva.Layer - The text layer to add the node's text to
 * @param node_layer: Konva.Layer - The node layer to add the node's circle to
 * @returns NodeDataLink
 */
export function add_node(
    node: ProcessedNode | Node,
    edge_count: number,
    relay_count: number,
    text_layer: Konva.Layer,
    node_layer: Konva.Layer,
    x_offset: number = 150,
    y_offset: number = 200
): NodeDataLink {
    const circle = new Konva.Circle({
        radius: 20,
        fill: 'transparent',
        stroke: 'black',
        strokeWidth: 3,
        draggable: true
    });

    // -- Add the text
    const text = new Konva.Text({
        text: node.node_id.toString(),
        fontSize: 20,
        fontFamily: 'Calibri',
        fill: 'white'
    });

    // -- Add the elements to the layers
    node_layer.add(circle);
    text_layer.add(text);

    // -- Format the node
    const formatted_node = format_node(
        node, 
        edge_count,
        relay_count,
        x_offset,
        y_offset
    );

    circle.x(formatted_node.x);
    circle.y(formatted_node.y);
    circle.stroke(formatted_node.color);

    center_text(text, circle);

    const new_node: ProcessedNode = {
        ...node,
        ...formatted_node,
    }

    const node_data_link: NodeDataLink = {
        node: new_node,
        conva_circle: circle,
        conva_text: text
    }

    add_node_listner(node_data_link)
    formated_nodes.push(node_data_link);
    return node_data_link;
}