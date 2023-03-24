import { Type, build_configuration } from '../api/config';
import { login_handler } from './src/core';

export const configuration = build_configuration<{
    verify_token_url: string,
    get_token_url: string,
    register_url: string,
    login_url: string,
    csrf_token: string,
    email_verify: string,
}>({
    verify_token_url: new Type('data-token-url', 'string'),
    get_token_url: new Type('data-get-token-url', 'string'),
    register_url: new Type('data-register-url', 'string'),
    login_url: new Type('data-login-url', 'string'),
    csrf_token: new Type('data-csrf-token', 'string'),
    email_verify: new Type('data-email-verify', 'string'),
});


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