import Konva from 'konva';
import { ConectionDataLink, Connection, NodeDataLink } from '../index.d'

let connections: ConectionDataLink[] = [];
export const get_connections = () => connections;

/**
 * @name calculate_color
 * @description Calculates the color of a connection
 * @param connection: ConectionDataLink - The connection to calculate the color of
 * @returns void
 */
export function calculate_color(connection: ConectionDataLink, max = 100): void {
    const steped_colors = [
        '#6fd08c',
        '#8bc76d',
        '#a5bc53',
        '#beae40',
        '#d49f39',
        '#e88d3f',
        '#f67a4f',
        '#ff6666',
    ];

    const step = max / steped_colors.length;
    const index = Math.floor(connection.connection.weight / step);
    connection.conva_line.stroke(steped_colors[index]);
}



/**
 * @name align_connection
 * @description Aligns a connection to the edge of the nodes it connects
 * @param connection: ConectionDataLink - The connection to align
 * @returns void
 */
export function align_connection(connection: ConectionDataLink): void {
    // -- All we need to do is just account for the radius of the nodes
    const r1 = connection.connection.node_a.conva_circle.radius();
    const r2 = connection.connection.node_b.conva_circle.radius();

    const x1 = connection.connection.node_a.conva_circle.x();
    const y1 = connection.connection.node_a.conva_circle.y();

    const x2 = connection.connection.node_b.conva_circle.x();
    const y2 = connection.connection.node_b.conva_circle.y();

    // -- Calculate the distance between the two points
    const d = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);

    // -- Calculate the new positions of the points
    const x1_new = x1 + (r1 / d) * (x2 - x1);
    const y1_new = y1 + (r1 / d) * (y2 - y1);
    const x2_new = x2 + (r2 / d) * (x1 - x2);
    const y2_new = y2 + (r2 / d) * (y1 - y2);

    // -- Return the new positions of the points
    const line = [x1_new, y1_new, x2_new, y2_new];
    connection.conva_line.points(line);

    // -- Align the text
    const text_x = (x1_new + x2_new) / 2;
    const text_y = (y1_new + y2_new) / 2;
    
    connection.conva_text.x(text_x);
    connection.conva_text.y(text_y);
}



/**
 * @name focous_connection
 * @description Focous a connection
 * @param connection: ConectionDataLink - The connection to focous
 * @returns void
 */
export function focous_connection(connection: ConectionDataLink): void {
    connection.conva_line.strokeWidth(3);
    connection.conva_line.moveToTop();
    connection.conva_text.moveToTop();

    connection.conva_text.text(connection.connection.weight.toString());

    align_connection(connection);
    calculate_color(connection);

    // -- Get the node and set its color to its border color
    connection.connection.node_a.conva_circle.fill(connection.connection.node_a.conva_circle.stroke());
    connection.connection.node_b.conva_circle.fill(connection.connection.node_b.conva_circle.stroke());
}



/**
 * @name unfocous_connection
 * @description Unfocous a connection
 * @param connection: ConectionDataLink - The connection to unfocous
 * @returns void
 */
export function unfocous_connection(connection: ConectionDataLink): void {
    connection.conva_line.strokeWidth(2);
    connection.conva_line.moveToBottom();
    connection.conva_text.moveToBottom();

    connection.conva_line.stroke('black');
    connection.conva_text.text('');

    align_connection(connection);

    // -- Get the node and set its color to transparent
    connection.connection.node_a.conva_circle.fill('transparent');
    connection.connection.node_b.conva_circle.fill('transparent');
}



/**
 * @name reset_connection
 * @description Resets a connection
 * @param connection: ConectionDataLink - The connection to reset
 * @returns void
 */
export function reset_connection(connection: ConectionDataLink): void {
    connection.conva_line.strokeWidth(2);
    connection.conva_line.moveToBottom();
    connection.conva_text.moveToBottom();

    connection.conva_text.text(connection.connection.weight.toString());

    align_connection(connection);
    calculate_color(connection);

    // -- Get the node and set its color to transparent
    connection.connection.node_a.conva_circle.fill('transparent');
    connection.connection.node_b.conva_circle.fill('transparent');
}



/**
 * @name add_connection
 * @description Adds a connection to the canvas
 * @param connection: Connection - The connection to add
 * @param node_a: NodeDataLink - The first node in the connection
 * @param node_b: NodeDataLink - The second node in the connection
 * @param connection_layer: Konva.Layer - The layer to add the connection to
 * @param text_layer: Konva.Layer - The layer to add the connection's text to
 * @returns ConectionDataLink
 */
export function add_connection(
    connection: Connection,
    to_node: NodeDataLink,
    from_node: NodeDataLink,
    connection_layer: Konva.Layer,
    text_layer: Konva.Layer,
): ConectionDataLink {
    
    const line = new Konva.Line({
        stroke: 'black',
        strokeWidth: 2,
        lineCap: 'round',
        lineJoin: 'round',
    });

    // -- Add the weight text
    const text = new Konva.Text({
        text: connection.weight.toString(),
        fontSize: 23,
        fontFamily: 'Calibri',
        fill: 'white'
    });

    text_layer.add(text);
    connection_layer.add(line);


    const connection_data_link: ConectionDataLink = {
        connection: {
            ...connection,
            node_a: to_node,
            node_b: from_node,
            weight: connection.weight,
        },
        conva_line: line,
        conva_text: text,
    }

    calculate_color(connection_data_link);
    align_connection(connection_data_link);
    connections.push(connection_data_link);
    return connection_data_link;
}