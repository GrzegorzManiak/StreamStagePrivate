import Konva from 'konva';

export function add_zoom_control(
    stage: Konva.Stage,
) {
    stage.on('wheel', (e) => {
        e.evt.preventDefault();

        const old_scale = stage.scaleX();

        const mouse_point_to = {
            x: stage.getPointerPosition().x / old_scale - stage.x() / old_scale,
            y: stage.getPointerPosition().y / old_scale - stage.y() / old_scale,
        };

        const new_scale = e.evt.deltaY > 0 ? old_scale * 0.9 : old_scale / 0.9;
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