import { NodeDataLink } from '../index.d';

const tooltip = document.getElementById('node-tooltip'),
    tt_first_child = tooltip.firstElementChild as HTMLDivElement;
let tt_width = 0, tt_height = 0;

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
