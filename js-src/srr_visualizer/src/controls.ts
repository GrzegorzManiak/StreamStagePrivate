import Konva from 'konva';

export function add_zoom_control(
    stage: Konva.Stage,
) {
    const INCRAMENT = 0.1,
        MAX_SCALE = 2,
        MIN_SCALE = 0.2;

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
    });



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
            return;
        }

        // -- Max
        if (new_scale > MAX_SCALE) {
            stage.scale({ x: MAX_SCALE, y: MAX_SCALE });
            stage.batchDraw();
            zoom_level.value = `${Math.trunc(MAX_SCALE * 100)}%`;
            return;
        }

        zoom_level.value = `${Math.trunc(new_scale * 100)}%`;
        stage.scale({ x: new_scale, y: new_scale });

        const new_x = -(mouse_point_to.x - stage.getPointerPosition().x / new_scale) * new_scale;
        const new_y = -(mouse_point_to.y - stage.getPointerPosition().y / new_scale) * new_scale;
        stage.position({ x: new_x, y: new_y });
        stage.batchDraw();
    });
}


export function add_pan_control(
    stage: Konva.Stage,
) {
    let is_panning = false;

    stage.on('mousedown', (e) => {
        if (e.target._id !== 1) return;
        is_panning = true;
        document.body.style.cursor = 'grabbing';
    });

    stage.on('mouseup', (e) => {
        is_panning = false;
        document.body.style.cursor = 'default';
    });
    
    stage.on('mousemove', (e) => {
        if (!is_panning) return;

        stage.position({
            x: stage.x() + e.evt.movementX,
            y: stage.y() + e.evt.movementY
        });
        stage.batchDraw();
    });
}