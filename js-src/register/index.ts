import { get_or_error } from '../api/config';
import { register_handler } from './src/core';

const sso_config = document.getElementById('config');
export const configuration = {
    verify_token_url: get_or_error<string>(sso_config, 'data-token-url'),
    get_token_url: get_or_error<string>(sso_config, 'data-get-token-url'),
    register_url: get_or_error<string>(sso_config, 'data-register-url'),
    login_url: get_or_error<string>(sso_config, 'data-login-url'),
    csrf_token: get_or_error<string>(sso_config, 'data-csrf-token'),
    email_verify: get_or_error<string>(sso_config, 'data-email-verify'),
};


export const panel_elms = {
    register: document.querySelector('[data-panel-type="register"]') as HTMLDivElement,
    email_wait: document.querySelector('[data-panel-type="email-wait"]') as HTMLDivElement,
}


let current_panel = 'register';
export function show_panel(panel: string) {
    // -- Get the current panel
    const current = panel_elms[current_panel];
    current.classList.add('login-area-panel-out');
    current.classList.remove('login-area-panel-in');

    // -- Get the new panel
    const new_panel = panel_elms[panel];
    new_panel.style.opacity = '1';
    new_panel.classList.add('login-area-panel-in');
}


// -- Get the main register form
register_handler();