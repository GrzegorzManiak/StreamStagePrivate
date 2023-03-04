import Konva from 'konva';
import { deserialize } from './src/deserialize';
import { add_stage_listners } from './src/listeners';
import { add_pan_control, add_zoom_control } from './src/controls';

// -- Create the stage
export const stage = new Konva.Stage({
    container: 'app',
    width: window.innerWidth,
    height: window.innerHeight
});

//
// Configuration
// 
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
// -- Deserialize the data
//
deserialize();


// 
// -- Add stage listeners
//
add_stage_listners(stage);