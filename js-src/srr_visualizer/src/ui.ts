import { NodeDataLink } from '../index.d';

const tooltip = document.getElementById('node-tooltip'),
    first_child = tooltip.firstElementChild as HTMLDivElement;
let width = 0;
let height = 0;

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
    width = first_child.clientWidth;
    height = first_child.clientHeight;
    tooltip.style.display = org_display;
    tooltip.style.display = 'fixed';


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
}



/**
 * @name update_position
 * @param node The node to get the position from
 * @description Calculates the offset for the nodes
 * based on the relative mouse position
 */
export function update_position(node: NodeDataLink): void {
    // -- Get the elemetns postion
    //    and out mouse position relative to the element
    const abs = node.conva_circle.absolutePosition(),
        rel = node.conva_circle.getRelativePointerPosition();

    // -- Depending on if we are close to the edge of the screen
    //    we will move the tooltip to the left or right
    const window_width = window.innerWidth,
        window_height = window.innerHeight;

    const x = abs.x, y = abs.y;
    const x_offset = x + width, y_offset = y + height;

    // -- Offset the tooltip by the ammount of it that is off screen + some
    if (x_offset > window_width) abs.x -= width + (node.conva_circle.radius() * 2) + 5;
    else abs.x += node.conva_circle.radius();

    if (y_offset > window_height) abs.y -= height - node.conva_circle.radius() * 2;
    else abs.y += node.conva_circle.radius() * 3;
    
    // -- Set the tooltip position
    tooltip.style.left = `${abs.x + rel.x}px`;
    tooltip.style.top = `${abs.y + rel.y}px`;
}