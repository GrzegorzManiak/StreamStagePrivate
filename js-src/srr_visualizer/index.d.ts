//
// Visualizer typescript definitions
//

import Konva from "konva";
import { DefaultResponseData, DefaultResponse } from "../api/index.d";

export interface Node {
    z: number;
    node_id: number;
    node_latency: number;
    node_type: string;
    node_usage: number;
    node_name: string;
    name: string;
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

export type NodeDataLink = {
    node: ProcessedNode;
    conva_circle: Konva.Circle;
    conva_text: Konva.Text;
    focused: boolean;
}

export type ConectionDataLink = {
    connection: {
        node_a: NodeDataLink;
        node_b: NodeDataLink;
        weight: number;
    };
    conva_line: Konva.Line;
    conva_text: Konva.Text;
}



//
// API typescript definitions
//

export interface Server {
    http_ip: string;
    http_port: number;
    http_url: string;
    id: string;
    live: boolean;
    mode: string;
    name: string;
    region: string;
    rtmp_ip: string;
    rtmp_port: number;
    rtmp_url: string;
    secret: string;
    slug: string;
}

export interface UpdatedSRRTree {
    tree: Data;
    servers: Array<Server>;
}

export type UpdateSRRRequestData = DefaultResponseData & { data: UpdatedSRRTree } ;
export type SRRUpdateResponse = UpdateSRRRequestData | DefaultResponse;


export interface Statistics {
    lables: Array<string>;
    data: Array<{
        name: string;
        type: string;
        data: Array<number | string>;
    }>;
}

export type StatisticsRequestData = DefaultResponseData & { data: Statistics } ;
export type StatisticsResponse = StatisticsRequestData | DefaultResponse;