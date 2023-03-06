import Konva from 'konva';
import { deserialize } from './src/deserialize';
import { add_stage_listners } from './src/listeners';
import { add_pan_control, add_zoom_control } from './src/controls';
import { create_toast } from '../toasts';
import { update_interval } from './api';
import { construct_graph } from './ui/sidebar';



//
// CONFIGURATION
//

const config = document.getElementById('config');
export function get_or_error<e>(element: HTMLElement, attribute: string): e {
    const value = element.getAttribute(attribute);
    if (!value) { 
        create_toast('error', 'Configuration Error', `No '${attribute}' found, please reload the page`);
        setTimeout(() => window.location.reload(), 3000);
    } return value as unknown as e;
}

export const configuration = {
    csrf_token: get_or_error<string>(config, 'data-csrf-token'),
    srr_tree_url: get_or_error<string>(config, 'data-get-ssr-tree'),
};



// 
// API
//
update_interval(5000);



// 
// VISUALIZER
//
export const stage = new Konva.Stage({
    container: 'app',
    width: window.innerWidth,
    height: window.innerHeight
});

export const colors = {
    ingress: '#6FD08C',
    relay: '#39A9DB',
    edge: '#FF6666'
}

//
// Layer setup
//
export const node_layer = new Konva.Layer(),
    connection_layer = new Konva.Layer(),
    text_layer = new Konva.Layer();


stage.add(node_layer);
stage.add(connection_layer);
stage.add(text_layer);


connection_layer.zIndex(0);
node_layer.zIndex(1);
text_layer.zIndex(2);

// -- Stage controls
add_zoom_control(stage);
add_pan_control(stage);

// -- Disable callbacks for the connection layer
//    as we don't want to be able to interact with it
connection_layer.listening(false);
text_layer.listening(false);


// 
// -- Add stage listeners
//
add_stage_listners(stage);


//
// -- UI
//

// 
// STATISTICS
//
// -- Locate the element
export const side_panel = document.querySelector('#node-panel') as HTMLDivElement;

export const name = side_panel.querySelector('#node-name'),
    type = side_panel.querySelector('#node-type'),
    id = side_panel.querySelector('#node-id'),
    router_id = side_panel.querySelector('#node-router-id'),
    rtmp = side_panel.querySelector('#node-rtmp'),
    http = side_panel.querySelector('#node-http');

//
// QUICK ACTIONS
//
export const open = side_panel.querySelector('#open'),
    shutdown = side_panel.querySelector('#shutdown'),
    graceful_shutdown = side_panel.querySelector('#graceful-shutdown'),
    reboot = side_panel.querySelector('#reboot'),
    graceful_reboot = side_panel.querySelector('#graceful-reboot');

// 
// GRAPH / LOGS
//
export const tabs = side_panel.querySelector('#node-graphs-tabs'),
    content = side_panel.querySelector('#node-graphs-tabs-content');

export const io = side_panel.querySelector('#node-io') as HTMLCanvasElement,
    logs = side_panel.querySelector('#node-logs');

construct_graph(io);