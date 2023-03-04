import Konva from 'konva';
import { ConectionDataLink, Connection, ProcessedConnection, ProcessedNode } from '../index.d'

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
 * @name add_connection
 * @description Adds a connection to the canvas
 * @param connection: Connection - The connection to add
 * @param node_a: ProcessedNode - The first node in the connection
 * @param node_b: ProcessedNode - The second node in the connection
 * @param connection_layer: Konva.Layer - The layer to add the connection to
 * @param text_layer: Konva.Layer - The layer to add the connection's text to
 * @returns ConectionDataLink
 */
export function add_connection(
    connection: Connection,
    to_node: ProcessedNode,
    from_node: ProcessedNode,
    connection_layer: Konva.Layer,
    text_layer: Konva.Layer,
): ConectionDataLink {
    
    const line = new Konva.Line({
        points: [to_node.x, to_node.y, from_node.x, from_node.y],
        stroke: 'black',
        strokeWidth: 2,
        lineCap: 'round',
        lineJoin: 'round',
    });

    // -- Add the weight text
    const text = new Konva.Text({
        x: (to_node.x + from_node.x) / 2,
        y: (to_node.y + from_node.y) / 2,
        text: connection.weight.toString(),
        fontSize: 20,
        fontFamily: 'Calibri',
        fill: 'white'
    });

    text_layer.add(text);
    connection_layer.add(line);

    const processed_connection: ProcessedConnection = {
        ...connection,
        node_a: to_node,
        node_b: from_node,
    }

    const connection_data_link: ConectionDataLink = {
        connection: processed_connection,
        conva_line: line,
        conva_text: text,
    }

    calculate_color(connection_data_link);
    connections.push(connection_data_link);
    return connection_data_link;
}