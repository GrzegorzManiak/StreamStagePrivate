import { attach, create_toast } from '../../common';
import { update_profile } from '../apis';
import { Pod } from '../index.d';

/**
 * @param pod: Pod - The pod that this panel is attached to
 * 
 * @returns void
 * 
 * @description This function manages the profile panel
 */
export function manage_profile_panel(pod: Pod) {
    // -- Get the panel
    const panel = pod.panel.element;

    // -- Get the inputs
    const username = panel.querySelector('#username') as HTMLInputElement,
        fname = panel.querySelector('#fname') as HTMLInputElement,
        lname = panel.querySelector('#lname') as HTMLInputElement,
        bio = panel.querySelector('#bio') as HTMLInputElement,
        timezone = panel.querySelector('#timezone') as HTMLSelectElement,
        country = panel.querySelector('#country') as HTMLSelectElement;

    const save_button = panel.querySelector('#save-btn') as HTMLButtonElement;

    // -- Add the event listener to the save button
    save_button.addEventListener('click', async() => {
        const stop_spinner = attach(save_button);

        // -- Get the values
        const data = {
            username: username.value.trim(),
            description: bio.value.trim(),
            first_name: fname.value.trim(),
            last_name: lname.value.trim(),
            time_zone: timezone.value.trim(),
            country: country.value.trim(),
        }

        // -- Send the request
        const res = await update_profile(data);

        // -- Check if the request was successful
        if (res.code !== 200) create_toast('error', 'Oops!', res.message);
        else create_toast('success', 'Success!', res.message);
        return stop_spinner();
    });
}