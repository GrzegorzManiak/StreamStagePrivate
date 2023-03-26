import { Type, build_configuration } from "../api/config";
import { report } from "../common/report";
import { manage_reviews_panel } from "./src/reviews";

export const configuration = build_configuration<{
    authenticated: boolean,
    username: string,
    is_you: boolean,
}>({
    username: new Type('data-username', 'string'),
    is_you: new Type('data-is-you', 'boolean'),
    authenticated: new Type('data-is-authenticated', 'boolean'),
}); 

// -- Load the review panel
manage_reviews_panel();


// -- Get the tab selector
const tab_selector = Array.from(document.querySelectorAll('.tab-selector')),
    more_desc = document.querySelector('.more-desc'),
    tabs = document.querySelector('#tabs');

// -- Get the tab from the URL
const url = new URL(window.location.href);
const tab = url.searchParams.get('t');
if (tab) {
    const tab_button = tab_selector.find(tab_button => tab_button.getAttribute('data-url') === tab);
    if (tab_button) tabs.setAttribute('data-tab', tab_button.getAttribute('data-tab'));
}


// -- Attach the event listeners
more_desc.addEventListener('click', () => tabs.setAttribute('data-tab', 'about-tab'));
tab_selector.forEach(tab => tab.addEventListener('click', () => {
    tabs.setAttribute('data-tab', tab.getAttribute('data-tab'));
    window.history.pushState({}, '', '?t=' + tab.getAttribute('data-url'));
}));


// -- Attach to the report button
const report_button = document.querySelector('.report');
report_button.addEventListener('click', () => {
    report('user', configuration.username);
});