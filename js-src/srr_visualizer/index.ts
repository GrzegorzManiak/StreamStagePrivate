import Konva from 'konva';
import { add_stage_listners } from './src/listeners';
import { add_pan_control, add_zoom_control, resize_canvas } from './src/controls';
import { update_interval } from './api';
import { create_toast } from '../common';
import { single } from '../common/single';



//
// CONFIGURATION
//
single('srr');

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
    proxy_request_url: get_or_error<string>(config, 'data-proxy-request'),
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
resize_canvas(stage, 'app');

// -- Disable callbacks for the connection layer
//    as we don't want to be able to interact with it
connection_layer.listening(false);
text_layer.listening(false);


// 
// -- Add stage listeners
//
add_stage_listners(stage);