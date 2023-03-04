import Konva from "konva";

export interface Node {
    z: number;
    node_id: number;
    node_latency: number;
    node_type: string;
    node_usage: number;
}

export type ProcessedNode = Node & {
    x: number;
    y: number;
    color: string;
}

export interface Connection {
    connection_id: number;
    node_a_id: number;
    node_b_id: number;
    usage_count: number;
    weight: number;
}

export type ProcessedConnection = Connection & {
    node_a: ProcessedNode;
    node_b: ProcessedNode;
}

export interface Data {
    connections: Array<Connection>;
    nodes: Array<Node>;
}

export type ConectionDataLink = {
    connection: ProcessedConnection;
    conva_line: Konva.Line;
    conva_text: Konva.Text;
}

export type NodeDataLink = {
    node: ProcessedNode;
    conva_circle: Konva.Circle;
    conva_text: Konva.Text;
}