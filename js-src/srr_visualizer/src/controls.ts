import Konva from 'konva';
import { hide_right_click } from '../ui/context';

const INCRAMENT = 0.1,
    MAX_SCALE = 2,
    MIN_SCALE = 0.2;

interface TouchPosition { x: number; y: number;}
  
export function add_zoom_control(
    stage: Konva.Stage,
) {

    // -- Get all the adjustment elements
    const zoom_in = document.getElementById('zoom-in') as HTMLButtonElement,
        zoom_out = document.getElementById('zoom-out') as HTMLButtonElement,
        zoom_level = document.getElementById('zoom-level') as HTMLInputElement;



    //
    // Zoom in (centered on stage, dont get pointer position)
    //
    zoom_in.addEventListener('click', () => {
        if (stage.scaleX() >= MAX_SCALE) return;
        const old_scale = stage.scaleX();
        const new_scale = old_scale + INCRAMENT;
        stage.scale({ x: new_scale, y: new_scale });
        zoom_level.value = `${Math.trunc(new_scale * 100)}%`;
        hide_right_click();
    });



    //
    // Zoom out
    //
    zoom_out.addEventListener('click', () => {
        if (stage.scaleX() <= MIN_SCALE) return;
        const old_scale = stage.scaleX();
        const new_scale = old_scale - INCRAMENT;
        stage.scale({ x: new_scale, y: new_scale });
        zoom_level.value = `${Math.trunc(new_scale * 100)}%`;
        hide_right_click();
    });



    //
    // Zoom Input
    //
    let zoom = 100;
    zoom_level.addEventListener('input', () => {
        zoom = parseInt(zoom_level.value) || MIN_SCALE * 100;
        if (zoom > MAX_SCALE * 100) zoom = MAX_SCALE * 100;
        if (zoom < MIN_SCALE * 100) zoom = MIN_SCALE * 100;

        const new_scale = zoom / 100;
        stage.scale({ x: new_scale, y: new_scale });
    });

    zoom_level.addEventListener('blur', () => {
        zoom_level.value = `${zoom}%`;
        hide_right_click();
    });


    //
    // Mouse Wheel
    //
    stage.on('wheel', (e) => {
        e.evt.preventDefault();

        const old_scale = stage.scaleX();

        const mouse_point_to = {
            x: stage.getPointerPosition().x / old_scale - stage.x() / old_scale,
            y: stage.getPointerPosition().y / old_scale - stage.y() / old_scale,
        };

        const new_scale = e.evt.deltaY > 0 ? old_scale * 0.9 : old_scale / 0.9;

        // -- Min
        if (new_scale < MIN_SCALE) {
            stage.scale({ x: MIN_SCALE, y: MIN_SCALE });
            stage.batchDraw();
            zoom_level.value = `${Math.trunc(MIN_SCALE * 100)}%`;
            hide_right_click();
            return;
        }

        // -- Max
        if (new_scale > MAX_SCALE) {
            stage.scale({ x: MAX_SCALE, y: MAX_SCALE });
            stage.batchDraw();
            zoom_level.value = `${Math.trunc(MAX_SCALE * 100)}%`;
            hide_right_click();
            return;
        }

        zoom_level.value = `${Math.trunc(new_scale * 100)}%`;
        stage.scale({ x: new_scale, y: new_scale });

        const new_x = -(mouse_point_to.x - stage.getPointerPosition().x / new_scale) * new_scale;
        const new_y = -(mouse_point_to.y - stage.getPointerPosition().y / new_scale) * new_scale;
        stage.position({ x: new_x, y: new_y });
        stage.batchDraw();
        hide_right_click();
    });
}


export function add_pan_control(
    stage: Konva.Stage,
) {
    let is_panning = false;
    const UI_PANEL = document.getElementById('ui') as HTMLDivElement;


    // -- Get all the adjustment elements
    const zoom_level = document.getElementById('zoom-level') as HTMLInputElement;


    // -- Stage on mouse down / touch start
    const down = (
        e:  Konva.KonvaEventObject<MouseEvent> | 
            Konva.KonvaEventObject<TouchEvent>
    ) => {
        if (e.target._id !== 1) return;
        is_panning = true;
        document.body.style.cursor = 'grabbing';
        UI_PANEL.classList.add('no-pointer-events');
    }
    stage.on('mousedown', (e) => down(e));
    stage.on('touchstart', (e) => down(e));


    // -- Stage on mouse up / touch end
    const up = () => {
        is_panning = false;
        document.body.style.cursor = 'default';
        UI_PANEL.classList.remove('no-pointer-events');
    }
    stage.on('mouseup', up);
    stage.on('touchend', up);

    stage.on('mousemove', (e) => {
        if (!is_panning) return;
        stage.position({
            x: stage.x() + e.evt.movementX,
            y: stage.y() + e.evt.movementY,
        });
        stage.batchDraw();
    });


    let last_center: TouchPosition | null = null;
    let last_distance: number | null = null;

    const get_center = (p1: TouchPosition, p2: TouchPosition): TouchPosition =>{
        return { x: (p1.x + p2.x) / 2, y: (p1.y + p2.y) / 2 }}

    const get_distance = (p1: TouchPosition, p2: TouchPosition): number => {
        return Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2))}

    
    // 
    // Two finger touch, allows for zooming
    // and panning
    // 
    stage.on('touchmove', (e) => {
        e.evt.preventDefault();
        const touch1 = e.evt.touches[0];
        const touch2 = e.evt.touches[1];

        // -- Zoom / Pan (2 fingers)
        if (touch1 && touch2) {
            if (stage.isDragging()) stage.stopDrag();

            const p1: TouchPosition = { x: touch1.clientX, y: touch1.clientY };
            const p2: TouchPosition = { x: touch2.clientX, y: touch2.clientY };

            if (!last_center) { last_center = get_center(p1, p2); return; }
            const new_center = get_center(p1, p2);
            const dist = get_distance(p1, p2);
            if (!last_distance) { last_distance = dist; return; }

            const point_to = {
                x: (new_center.x - stage.x()) / stage.scaleX(),
                y: (new_center.y - stage.y()) / stage.scaleY(),
            };

            let scale = stage.scaleX() * (dist / last_distance);
            if (scale < MIN_SCALE) scale = MIN_SCALE;
            if (scale > MAX_SCALE) scale = MAX_SCALE;
            zoom_level.value = `${Math.trunc(scale * 100)}%`;
            stage.scale({ x: scale, y: scale });

            const new_x = new_center.x - last_center.x;
            const new_y = new_center.y - last_center.y;

            stage.position({ 
                x: new_center.x - point_to.x * scale + new_x,
                y: new_center.y - point_to.y * scale + new_y,
            });
            stage.batchDraw();

            last_center = new_center;
            last_distance = dist;
        }

        // -- Pan (1 finger)
        else if (touch1) {
            // -- We need to make sure that we are dragging
            //    on the stage, not any other element
            if (e.target._id !== 1) return;
            if (stage.isDragging()) return;
            stage.startDrag();

            const p1: TouchPosition = { x: touch1.clientX, y: touch1.clientY };
            if (!last_center) { last_center = p1; return; }
            const new_center = p1;

            const new_x = new_center.x - last_center.x;
            const new_y = new_center.y - last_center.y;

            stage.position({
                x: stage.x() + new_x,
                y: stage.y() + new_y,
            });

            stage.batchDraw();
            last_center = new_center;
        }
    });

    // -- On end
    stage.on('touchend', (e) => {
        last_center = null;
        last_distance = 0;
    });



    // -- Stage on cooridnation change
    const x_coord = document.getElementById('x-coord') as HTMLInputElement,
        y_coord = document.getElementById('y-coord') as HTMLInputElement;

    let x_focused = false, y_focused = false;

    // -- Focus and unfocus 
    x_coord.addEventListener('focus', () => { x_focused = true; });
    x_coord.addEventListener('blur', () => { 
        x_focused = false; 
        x_coord.value = `${stage.x().toFixed(2)}x`;
    });

    y_coord.addEventListener('focus', () => { y_focused = true; });
    y_coord.addEventListener('blur', () => { 
        y_focused = false; 
        y_coord.value = `${stage.y().toFixed(2)}y`;
    });


    // -- Input on stage change
    x_coord.addEventListener('input', () => {
        stage.x(parseInt(x_coord.value) || 0);
        stage.batchDraw();
    });

    y_coord.addEventListener('input', () => {
        stage.y(parseInt(y_coord.value) || 0);
        stage.batchDraw();
    });


    // -- Update on stage change
    stage.on('xChange', () => { 
        if (x_focused) return;
        x_coord.value = `${stage.x().toFixed(2)}x`; 
        hide_right_click();
    });
    stage.on('yChange', () => { 
        if (y_focused) return;
        y_coord.value = `${stage.y().toFixed(2)}y`; 
        hide_right_click();
    });
}


export function resize_canvas(
    stage: Konva.Stage,
    parent_elm: string,
) {
    const parent = document.getElementById(parent_elm) as HTMLDivElement;

    const resize = () => {
        stage.width(parent.clientWidth);
        stage.height(parent.clientHeight);
        stage.batchDraw();
    }

    window.addEventListener('resize', resize);
    resize();
}