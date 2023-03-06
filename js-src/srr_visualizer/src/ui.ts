import { attach, confirmation_modal } from '../../click_handler';
import { NodeDataLink } from '../index.d';

const tooltip = document.getElementById('node-tooltip'),
    tt_first_child = tooltip.firstElementChild as HTMLDivElement;
let tt_width = 0, tt_height = 0;

const right_click_menu = document.getElementById('node-rightclick'),
    rc_first_child = right_click_menu.firstElementChild as HTMLDivElement;
let rc_width = 0, rc_height = 0;

// -- Add the event listener
// open, shutdown, graceful-shutdown, reboot, graceful-reboot
const open = document.getElementById('open'),
    shutdown = document.getElementById('shutdown'),
    graceful_shutdown = document.getElementById('graceful-shutdown'),
    reboot = document.getElementById('reboot'),
    graceful_reboot = document.getElementById('graceful-reboot');


// --shutdown
shutdown.addEventListener('click', () => {
    confirmation_modal(
        () => { },
        () => { },
        'Are you sure you want to shutdown this server? This will cause all users to be disconnected.',
    )
});

// --graceful-shutdown
graceful_shutdown.addEventListener('click', () => {
    confirmation_modal(
        () => { },
        () => { },
        'Are you sure you want to shutdown this server? This will cause the server to stop accepting new connections, but will allow current connections to finish.',
    )
});

// --reboot
reboot.addEventListener('click', () => {
    confirmation_modal(
        () => { },
        () => { },
        'Are you sure you want to reboot this server? This will cause all users to be disconnected.',
    )
});

// --graceful-reboot
graceful_reboot.addEventListener('click', () => {
    confirmation_modal(
        () => { },
        () => { },
        'Are you sure you want to reboot this server? This will cause the server to stop accepting new connections, but will allow current connections to finish.',
    )
});


/**
 * @name tooltip_mouseover
 * @description Mouseover event for nodes
 * @param event The mouseover event
 * @param node The node that was moused over
 * @param server_id The server id (if applicable)
 * @returns void
 */
export function tooltip_mouseover(
    node: NodeDataLink,
    server_id: number | null = null
): void {
    // NOTE: This is a very hacky way to do this, but so is this language
    const org_display = tooltip.style.display;
    tooltip.style.display = 'block';
    tt_width = tt_first_child.clientWidth;
    tt_height = tt_first_child.clientHeight;
    tooltip.style.display = org_display;
    tooltip.style.display = 'fixed';
    tt_first_child.classList.add('fade-in');

    // -- Show the tooltip
    tooltip.style.display = 'block';
}



/**
 * @name tooltip_mouseout
 * @description Mouseout event for nodes
 * @returns void
 */
export function tooltip_mouseout(): void {
    // -- Get the tooltip
    const tooltip = document.getElementById('node-tooltip');
    tooltip.style.display = 'none';
    tt_first_child.classList.remove('fade-in');
}



/**
 * @name update_position
 * @param node The node to get the position from
 * @description Calculates the offset for the nodes
 * based on the relative mouse position
 */
export function update_tooltip_position(node: NodeDataLink): void {
    // -- Get the elemetns postion
    //    and out mouse position relative to the element
    const abs = node.conva_circle.absolutePosition(),
        rel = node.conva_circle.getRelativePointerPosition();

    // -- Depending on if we are close to the edge of the screen
    //    we will move the tooltip to the left or right
    const window_width = window.innerWidth,
        window_height = window.innerHeight;

    const x = abs.x, y = abs.y;
    const x_offset = x + tt_width, y_offset = y + tt_height;

    // -- Offset the tooltip by the ammount of it that is off screen + some
    if (x_offset > window_width) abs.x -= tt_width + (node.conva_circle.radius() * 2) + 5;
    else abs.x += node.conva_circle.radius();

    if (y_offset > window_height) abs.y -= tt_height - node.conva_circle.radius() * 2;
    else abs.y += node.conva_circle.radius() * 3;
    
    // -- Set the tooltip position
    tooltip.style.left = `${abs.x + rel.x}px`;
    tooltip.style.top = `${abs.y + rel.y}px`;
}



/**
 * @name right_click
 * @description Right click event for nodes
 * @param event The right click event
 * @param node The node that was right clicked
 * @param server_id The server id (if applicable)
 * @returns void
 */
export function right_click(
    node: NodeDataLink,
    server_id: number | null = null
): void {
    // NOTE: This is a very hacky way to do this, but so is this language
    const org_display = right_click_menu.style.display;
    right_click_menu.style.display = 'block';
    rc_width = rc_first_child.clientWidth;
    rc_height = rc_first_child.clientHeight;
    right_click_menu.style.display = org_display;
    right_click_menu.style.display = 'fixed';
    rc_first_child.classList.add('fade-in');

    // -- Show the tooltip
    right_click_menu.style.display = 'block';
    update_rc_position(node);

}


/**
 * @name update_rc_position
 * @param node The node to get the position from
 * @description Calculates the offset for the nodes
 * based on the relative mouse position
 */
export function update_rc_position(node: NodeDataLink): void {
    // -- Get the elemetns postion
    //    and out mouse position relative to the element
    const abs = node.conva_circle.absolutePosition(),
        rel = node.conva_circle.getRelativePointerPosition();
    
    // -- Depending on if we are close to the edge of the screen
    //    we will move the tooltip to the left or right
    const window_width = window.innerWidth,
        window_height = window.innerHeight;

    const x = abs.x, y = abs.y;
    const x_offset = x + rc_width, y_offset = y + rc_height;

    // -- Offset the tooltip by the ammount of it that is off screen + some
    if (x_offset > window_width) abs.x -= rc_width + (node.conva_circle.radius() * 2) + 5;
    else abs.x += node.conva_circle.radius();

    if (y_offset > window_height) abs.y -= rc_height - node.conva_circle.radius() * 2;
    else abs.y += node.conva_circle.radius() * 3;

    // -- Set the tooltip position
    right_click_menu.style.left = `${abs.x + rel.x}px`;
    right_click_menu.style.top = `${abs.y + rel.y}px`;
}


/**
 * @name hide_right_click
 * @description Hides the right click menu
 * @returns void
 */
export function hide_right_click(): void {
    right_click_menu.style.display = 'none';
    rc_first_child.classList.remove('fade-in');
}