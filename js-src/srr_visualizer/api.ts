import { configuration } from '.';
import request from '../api'
import { create_toast } from '../toasts';
import { SRRUpdateResponse, UpdateSRRRequestData, UpdatedSRRTree } from './index.d';
import { deserialize } from './src/deserialize';


//
// REQUESTS
//
export const get_updated_tree = async (): Promise<SRRUpdateResponse> => 
    request('GET', configuration.srr_tree_url, configuration.csrf_token, {});



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
        deserialize(resp.data.tree)
        console.log('Updated tree');
    }

    await req();

    setInterval(async () => {
        await req();
    }, interval);
}