import { Chart } from 'frappe-charts';
import { NodeDataLink, Server, StatisticsRequestData } from '../index.d'
import { get_node_statistics } from "../api";
import { create_toast } from '../../common';

const side_panel = document.querySelector('#node-panel') as HTMLDivElement;
if (!side_panel) {
    create_toast('error', 'Fatal Error', 'Could not find the side panel');
    throw new Error('Could not find the side panel');
}

// 
// CLOSE BUTTON
// 
const close = side_panel.querySelector('#close');
close.addEventListener('click', () => {
    clear_server();
});

// 
// STATISTICS
//
const name = side_panel.querySelector('#node-name'),
    type = side_panel.querySelector('#node-type'),
    id = side_panel.querySelector('#node-id'),
    router_id = side_panel.querySelector('#node-router-id'),
    rtmp = side_panel.querySelector('#node-rtmp'),
    http = side_panel.querySelector('#node-http');

//
// QUICK ACTIONS
//
// const open = side_panel.querySelector('#open'),
//     shutdown = side_panel.querySelector('#shutdown'),
//     graceful_shutdown = side_panel.querySelector('#graceful-shutdown'),
//     reboot = side_panel.querySelector('#reboot'),
//     graceful_reboot = side_panel.querySelector('#graceful-reboot');



//
// TABS
//
const tabs = side_panel.querySelector('#node-graphs-tabs'),
    content = side_panel.querySelector('#node-graphs-tabs-content');

const io = side_panel.querySelector('#node-io') as HTMLCanvasElement,
    logs = side_panel.querySelector('#node-logs');

let cur_server: Server = null;
let init = true;
let chart: Chart = null;

/**
 * @name clear_server
 * @description Clears the current server
 * @returns void
 */
export function clear_server(): void {
    cur_server = null;
    name.innerHTML = '';
    type.innerHTML = '';
    id.innerHTML = '';
    router_id.innerHTML = '';
    rtmp.innerHTML = '';
    http.innerHTML = '';

    side_panel.classList.remove('visable');
    side_panel.classList.add('hidden');
}



/**
 * @name set_server
 * @description Sets the current server
 * @param server The server to set
 * @param node The node to set
 * @returns void
 */
export function set_server(
    server: Server,
    node: NodeDataLink
): void {
    cur_server = server;

    // -- Set the server name
    name.innerHTML = server.slug;
    type.innerHTML = node.node.node_type;
    id.innerHTML = server.id;
    router_id.innerHTML = node.node.node_id.toString();
    rtmp.innerHTML = server.rtmp_url;
    http.innerHTML = server.http_url;

    // -- Show the panel
    side_panel.classList.remove('hidden');
    side_panel.classList.add('visable');

    if (init) {
        init = false;
        chart = new Chart(io, {
            title: 'Node Server Metrics',
            type: 'axis-mixed',
            colors: ['#E3C567', '#FF6666', '#6FD08C', '#39A9DB'],
            data: {
                datasets: [
                    { name: 'CPU%', type: 'line', values: [] },
                    { name: 'RAM%', type: 'line', values: [] },
                    { name: 'NET RX (Mbps)', type: 'line', values: [] },
                    { name: 'NET TX (Mbps)', type: 'line', values: [] },
                ]
            }
        })
        update();
    }
}



/**
 * @name update
 * @description Updates the node panel
 * @returns void
 */
export async function update(): Promise<void> {
    // -- Create the interval
    setInterval(async () => {
        
        // -- Make sure that we have a server
        if (!cur_server) return;

        // -- Get the statistics
        const response = await get_node_statistics(cur_server);

        // -- Process the response
        if (response.code !== 200) return create_toast(
            'error', 'Oops! There appears to be an issue',
            response.message,
            5000
        );

        // -- Cast the response, since we got a 200
        const resp = response as StatisticsRequestData;

        // -- Update the chart
        chart.update(resp.data);
    }, 2000);
}