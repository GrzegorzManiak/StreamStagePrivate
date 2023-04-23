import { Type, build_configuration } from "../api/config";
import { report } from "../common/report";
import { single } from "../common/single";
import { manage_events_panel } from "./src/events";

single('broad_profiles');

export const configuration = build_configuration<{
    csrf_token: string,
    handle: string,
    broadcaster_id: string,

    submit_report: string,
    get_events: string,
}>({
    csrf_token: new Type('data-csrf-token', 'string'),
    handle: new Type('data-handle', 'string'),
    broadcaster_id: new Type('data-broadcaster-id', 'string'),

    submit_report: new Type('data-submit-report', 'string'),
    get_events: new Type('data-get-bc-events', 'string'),
}); 

// -- Load the events panel
manage_events_panel();

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
    report('broadcaster', configuration.handle);
});