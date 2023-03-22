import { get_or_error } from '../api/config';
import { login_handler } from './src/core';

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
    login: document.querySelector('[data-panel-type="login"]') as HTMLDivElement,
    totp: document.querySelector('[data-panel-type="totp"]') as HTMLDivElement,
    mfa: document.querySelector('[data-panel-type="mfa"]') as HTMLDivElement,
}


let current_panel = 'login';
export function show_panel(panel: string) {
    // -- Get the current panel
    const current = panel_elms[current_panel];
    current.classList.add('login-area-panel-out');
    current.classList.remove('login-area-panel-in');

    // -- Get the new panel
    const new_panel = panel_elms[panel];
    new_panel.classList.add('login-area-panel-in');
    new_panel.classList.remove('login-area-panel-out');
    current_panel = panel;
}


// -- Get the main login form
login_handler();