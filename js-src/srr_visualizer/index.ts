import { Data, ProcessedNode, ProcessedConnection, NodeDataLink, ConectionDataLink, Node } from './index.d';
import Konva from 'konva';

// -- This is temporary code to get the visualizer working
const data = '{"connections":[{"connection_id":1,"node_a_id":1,"node_b_id":3,"usage_count":0,"weight":25},{"connection_id":2,"node_a_id":1,"node_b_id":4,"usage_count":0,"weight":10},{"connection_id":3,"node_a_id":1,"node_b_id":5,"usage_count":0,"weight":5},{"connection_id":4,"node_a_id":2,"node_b_id":3,"usage_count":0,"weight":25},{"connection_id":5,"node_a_id":2,"node_b_id":4,"usage_count":0,"weight":10},{"connection_id":6,"node_a_id":2,"node_b_id":5,"usage_count":0,"weight":5},{"connection_id":7,"node_a_id":6,"node_b_id":3,"usage_count":0,"weight":40},{"connection_id":8,"node_a_id":7,"node_b_id":3,"usage_count":0,"weight":45},{"connection_id":9,"node_a_id":8,"node_b_id":3,"usage_count":0,"weight":70},{"connection_id":10,"node_a_id":9,"node_b_id":3,"usage_count":0,"weight":35},{"connection_id":11,"node_a_id":10,"node_b_id":3,"usage_count":0,"weight":30},{"connection_id":12,"node_a_id":6,"node_b_id":4,"usage_count":0,"weight":25},{"connection_id":13,"node_a_id":7,"node_b_id":4,"usage_count":0,"weight":30},{"connection_id":14,"node_a_id":8,"node_b_id":4,"usage_count":0,"weight":55},{"connection_id":15,"node_a_id":9,"node_b_id":4,"usage_count":0,"weight":20},{"connection_id":16,"node_a_id":10,"node_b_id":4,"usage_count":0,"weight":15},{"connection_id":17,"node_a_id":6,"node_b_id":5,"usage_count":0,"weight":20},{"connection_id":18,"node_a_id":7,"node_b_id":5,"usage_count":0,"weight":25},{"connection_id":19,"node_a_id":8,"node_b_id":5,"usage_count":0,"weight":50},{"connection_id":20,"node_a_id":9,"node_b_id":5,"usage_count":0,"weight":15},{"connection_id":21,"node_a_id":10,"node_b_id":5,"usage_count":0,"weight":10}],"nodes":[{"node_id":1,"node_latency":0,"node_type":"Ingress","node_usage":0},{"node_id":2,"node_latency":0,"node_type":"Ingress","node_usage":0},{"node_id":3,"node_latency":50,"node_type":"Relay","node_usage":0},{"node_id":4,"node_latency":20,"node_type":"Relay","node_usage":0},{"node_id":5,"node_latency":10,"node_type":"Relay","node_usage":0},{"node_id":6,"node_latency":30,"node_type":"Edge","node_usage":0},{"node_id":7,"node_latency":40,"node_type":"Edge","node_usage":0},{"node_id":8,"node_latency":90,"node_type":"Edge","node_usage":0},{"node_id":9,"node_latency":20,"node_type":"Edge","node_usage":0},{"node_id":10,"node_latency":10,"node_type":"Edge","node_usage":0}]}'
const data_obj = JSON.parse(data) as Data;



// -- Create the stage
const stage = new Konva.Stage({
    container: 'app',
    width: window.innerWidth,
    height: window.innerHeight
});

// -- Create and add the layer
const node_layer = new Konva.Layer(),
    connection_layer = new Konva.Layer(),
    text_layer = new Konva.Layer();

stage.add(node_layer);
stage.add(connection_layer);
stage.add(text_layer);

node_layer.zIndex(1);
connection_layer.zIndex(0);
text_layer.zIndex(2);

// -- Disable callbacks for the connection layer
//    as we don't want to be able to interact with it
connection_layer.listening(false);
text_layer.listening(false);


// -- Node counts
let ingress_count = 0, relay_count = 0, edge_count = 0;

// -- Count all the nodes
data_obj.nodes.forEach(node => {
    switch (node.node_type) {
        case 'Ingress': return node.z = ingress_count++;
        case 'Relay': return node.z = relay_count++;
        case 'Edge': return node.z = edge_count++;
    }
});

function degreesToRadians(degrees: number): number {
    return degrees * (Math.PI / 180);
}


// -- Create the nodes
function format_node(
    node: Node,
): ProcessedNode {
    // -- General
    const X_OFFSET = 150;
    const Y_OFFSET = 200;
    const X_SPACING = 200;
    const Y_SPACING = 200;
    const X_STAG = 25;

    // -- Ark
    const ELIPSE_HEIGHT = 50 * edge_count;
    const ELIPSE_WIDTH = 25 * edge_count;
    const ARK_ANGLE = 180;
    const ARK_ROTATION = -90;

    let x = 0, y = 0, color = 'red';

    switch (node.node_type) {
        case 'Ingress':
            color = 'green';
            x = 0 + X_OFFSET;
            y = Y_OFFSET + node.z * Y_SPACING; 
            break;

        case 'Relay':
            color = 'blue';
            x = X_SPACING + X_OFFSET + (node.z % 2) * X_STAG;
            y = Y_OFFSET + ((node.z / 2) * Y_SPACING * 1.5) - Y_SPACING / relay_count;
            break;

        case 'Edge':
            color = 'red';
            
            const angle = degreesToRadians((ARK_ANGLE / (edge_count - 1)) * node.z);

            x = Math.cos(angle + degreesToRadians(ARK_ROTATION)) * ELIPSE_WIDTH;
            y = Math.sin(angle + degreesToRadians(ARK_ROTATION)) * ELIPSE_HEIGHT;

            x += X_OFFSET + (X_SPACING * 2) + X_STAG;
            y += Y_OFFSET + Y_SPACING / 2;
            
            break;
    }

    return {
        ...node,
        x,
        y,
        color
    };
}


const nodes: ProcessedNode[] = data_obj.nodes.map(format_node);

// -- Create the connections
const connections: ProcessedConnection[] = data_obj.connections.map((connection) => {
    const node_a = nodes.find((node) => node.node_id === connection.node_a_id);
    const node_b = nodes.find((node) => node.node_id === connection.node_b_id);
    return {
        ...connection,
        node_a: node_a,
        node_b: node_b
    }
});


let conva_nodes: NodeDataLink[] = [],
    conva_connections: ConectionDataLink[] = [];


function center_text(
    text: Konva.Text,
    circle: Konva.Circle
) {
    const text_rect = text.getClientRect();
    const circle_rect = circle.getClientRect();

    const x = circle_rect.x + (circle_rect.width / 2) - (text_rect.width / 2);
    const y = circle_rect.y + (circle_rect.height / 2) - (text_rect.height / 2);

    text.x(x);
    text.y(y);
}


// -- Draw the nodes
nodes.forEach((node) => {
    const circle = new Konva.Circle({
        x: node.x,
        y: node.y,
        radius: 25,
        fill: node.color,
        stroke: 'black',
        strokeWidth: 1,
        draggable: true
    });

    // -- Add the text
    const text = new Konva.Text({
        x: node.x,
        y: node.y,
        text: node.node_id.toString(),
        fontSize: 20,
        fontFamily: 'Calibri',
        fill: 'white'
    });

    center_text(text, circle);

    node_layer.add(circle);
    text_layer.add(text);
    conva_nodes.push({
        node: node,
        conva_circle: circle,
        conva_text: text
    });
});


// -- Draw the connections
connections.forEach((connection) => {
    const line = new Konva.Line({
        points: [connection.node_a.x, connection.node_a.y, connection.node_b.x, connection.node_b.y],
        stroke: 'black',
        strokeWidth: 2,
        lineCap: 'round',
        lineJoin: 'round',
    });

    // -- Add the weight text
    const text = new Konva.Text({
        x: (connection.node_a.x + connection.node_b.x) / 2,
        y: (connection.node_a.y + connection.node_b.y) / 2,
        text: connection.weight.toString(),
        fontSize: 20,
        fontFamily: 'Calibri',
        fill: 'white'
    });

    text_layer.add(text);
    connection_layer.add(line);
    conva_connections.push({
        connection: connection,
        conva_line: line,
        conva_text: text
    });
});



// -- Add the event listeners for the nodes
//    so we can update the connections when they move
conva_nodes.forEach((node) => {

    node.conva_circle.on('dragmove', (e) => {
        // -- Update the node
        node.node.x = e.target.x();
        node.node.y = e.target.y();

        // -- Update the text
        center_text(node.conva_text, node.conva_circle);

        // -- Update the connections
        conva_connections.forEach((connection) => {
            // -- If the node is the first node in the connection
            if (connection.connection.node_a.node_id === node.node.node_id) {
                connection.conva_line.points([e.target.x(), e.target.y(), connection.connection.node_b.x, connection.connection.node_b.y]);
                connection.conva_line.stroke('red');

                // -- Update the text
                connection.conva_text.x((e.target.x() + connection.connection.node_b.x) / 2);
                connection.conva_text.y((e.target.y() + connection.connection.node_b.y) / 2);
            } 

            // -- If the node is the second node in the connection
            else if (connection.connection.node_b.node_id === node.node.node_id) {
                connection.conva_line.points([connection.connection.node_a.x, connection.connection.node_a.y, e.target.x(), e.target.y()]);
                connection.conva_line.stroke('red');

                // -- Update the text
                connection.conva_text.x((connection.connection.node_a.x + e.target.x()) / 2);
                connection.conva_text.y((connection.connection.node_a.y + e.target.y()) / 2);
            }

            // -- Else the node is not in the connection
            else {
                // -- Color the connection black
                connection.conva_line.stroke('black');
            }
        });
    });


    // -- On click, color the connections red
    node.conva_circle.on('click', (e) => {
        conva_connections.forEach((connection) => {
            // -- If the node is the first node in the connection
            if (
                connection.connection.node_a.node_id === node.node.node_id ||
                connection.connection.node_b.node_id === node.node.node_id
            ) connection.conva_line.stroke('red');
            
            // -- Else the node is not in the connection
            else connection.conva_line.stroke('black');   
        });
    });
})

// -- Event listener for the stage so tat we can update the connections
//    when the stage is resized, or clicked
stage.on('resize', (e) => {
    conva_connections.forEach((connection) => {
        connection.conva_line.points([connection.connection.node_a.x, connection.connection.node_a.y, connection.connection.node_b.x, connection.connection.node_b.y]);
    });
});

stage.on('click', (e) => {
    // -- The stage is the first thing added, so its id is one
    //    therefore we can use this to check if the click was on the stage
    //    or on a node
    if (e.target._id === 1) conva_connections.forEach((connection) => 
        connection.conva_line.stroke('black'));
});