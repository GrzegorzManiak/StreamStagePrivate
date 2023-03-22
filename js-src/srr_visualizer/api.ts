import { configuration } from '.';
import { base_request } from '../api';
import { create_toast } from '../common';
import { SRRUpdateResponse, Server, StatisticsResponse, UpdateSRRRequestData } from './index.d';
import { deserialize } from './src/deserialize';


//
// REQUESTS
//
export const get_updated_tree = async (): Promise<SRRUpdateResponse> => 
    base_request('GET', configuration.srr_tree_url, configuration.csrf_token, {});

export const get_node_statistics = async (server: Server): Promise<StatisticsResponse> =>
    base_request('GET', configuration.proxy_request_url, {}, { 
        'p-headers': '{ "NodeSecret": "' + server.secret + '" }',
        'p-url': server.http_url + '/statistics/server'
    });

//
// AUXILIARY FUNCTIONS
//


/**
 * @name update_interval
 * @description Ran on script start, updates the tree every x seconds
 * @param interval: number - How often should the tree be updated
 */
export const update_interval = async (interval: number): Promise<void> => {
    const req = async() => {
        // -- Get the updated tree
        const response = await get_updated_tree();

        // -- Process the response
        if (response.code !== 200) return create_toast(
            'error', 
            'Oops! There appears to be an issue',
            response.message,
            5000
        );

        // -- Cast the response, since we got a 200
        const resp = response as UpdateSRRRequestData;

        // -- Update the tree
        deserialize(resp.data.tree, resp.data.servers);
        console.log('Updated tree');
    }

    await req();

    setInterval(async () => {
        await req();
    }, interval);
}