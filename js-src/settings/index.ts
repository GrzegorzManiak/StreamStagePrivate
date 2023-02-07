import { get_panel } from '../authentication/core/panel_manager';
import { create_toast } from '../toasts';
import { attach_event_listeners, get_pod } from './core/panels';
import { manage_security_panel } from './core/security';
import { PanelType } from './index.d';

export function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export function get_or_error<e>(element: HTMLElement, attribute: string): e {
    const value = element.getAttribute(attribute);
    if (!value) {
        create_toast('error', 'Configuration Error', `No ${attribute} found, please reload the page`);
        // -- Wait 3 seconds and reload the page
        setTimeout(() => {
            window.location.reload();
        }, 3000);
    }
    return value as unknown as e;
}


const config = document.getElementById('config');
console.log(config);
export const configuration = {
    admin: get_or_error<string>(config, 'data-admin') === 'True',
    username: get_or_error<string>(config, 'data-username'),
    userid: get_or_error<number>(config, 'data-userid'),
    useremail: get_or_error<string>(config, 'data-useremail'),
    userfirst: get_or_error<string>(config, 'data-userfirst'),
    userlast: get_or_error<string>(config, 'data-userlast'),
    access_level: get_or_error<number>(config, 'data-access-level'),
    profile_picture: get_or_error<string>(config, 'data-profile-picture'),
    change_details: get_or_error<string>(config, 'data-change-details'),
    csrf_token: get_or_error<string>(config, 'data-csrf-token'),

    send_verification: get_or_error<string>(config, 'data-send-verification'),
    resend_verification: get_or_error<string>(config, 'data-resend-verification'),
    remove_verification: get_or_error<string>(config, 'data-remove-verification'),
    recent_verification: get_or_error<string>(config, 'data-recent-verification'),
}


// -- Attach the event listeners
attach_event_listeners();


// -- Attach to all panels
let security_panel = get_pod('security');
if (security_panel) manage_security_panel(security_panel);