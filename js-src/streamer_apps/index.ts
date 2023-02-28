import { get_panel } from '../authentication/core/panel_manager';
import { create_toast } from '../toasts';

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