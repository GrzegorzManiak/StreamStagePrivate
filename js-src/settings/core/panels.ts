import { PanelType, Panel, Pod } from '../index.d';
import { sleep, create_toast } from '../../common';

const navbar = document.getElementById('nav'),
    toggle_at = 50;

export const scrolled = () => {
    const scroll = window.scrollY;
    if (scroll > toggle_at) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
}

let panels: Array<Panel> = [];
export let pods: Array<Pod> = [];


/**
 * @name locate_panels
 * @returns void
 * 
 * @description This function locates all the panels
 *              on the page and adds them to the panels
 *              array.
 */
export function locate_panels() {
    // -- Get all elements with the data-panel-type attribute
    const panel_elements = document.querySelectorAll('[data-panel-type]');
    
    // -- Loop through the panel elements
    panel_elements.forEach(element => panels.push({
        element,
        type: element.getAttribute('data-panel-type') as PanelType
    }));
}



/**
 * @name get_panel
 * @param panel_type: PanelType - The panel type
 * @returns Panel | undefined
 * 
 * @description This function returns the panel
 *              object that matches the panel type
 *              that was passed in.
 */
export function get_panel(panel_type: PanelType): Panel | undefined {
    for (const panel of panels) { if (panel.type === panel_type) return panel; }
}



/**
 * @name get_pod
 * @param panel_type: PanelType - The panel type
 * @returns Pod | undefined
 * 
 * @description This function returns the pod
 *              object that matches the panel type
 *              that was passed in.
 */
export function get_pod(panel_type: PanelType): Pod | undefined {
    for (const pod of pods) {
        if (pod.type === panel_type) return pod;
    }
}



/**
 * @name get_active_pod
 * @returns Pod | undefined
 * 
 * @description This function returns the active
 *              pod object.
 */
export function get_active_pod(): Pod | undefined {
    for (const pod of pods) { if (pod.element.getAttribute('data-pod-status') === 'active') return pod; }
}



/**
 * @name set_sidebar_state
 * @param state: 'open' | 'closed' - The state of the sidebar
 * @returns void
 */
export let set_sidebar_state = (state: 'open' | 'closed') => { 
    Error('set_sidebar_state has not been initialized');
};



/**
  * @name attach_to_sidepanel
 * @returns void
 * 
 * @description This function attaches the sidepanel
 *              to the sidepanel button.
 *              
 *              It handles the opening and closing
 *              of the sidepanel.
 */
export function attach_to_sidepanel() {
    // -- Get the sidepanel button #navbar-carrot and the sidepanel
    const sidepanel_button = document.getElementById('navbar-carrot') as HTMLInputElement,
        main_container = document.getElementById('main-container'),
        nav_bar = document.getElementById('nav'),
        sidepanel_btn_group = document.querySelector('.sidepanel-button') as HTMLElement,
        sidepanel = document.getElementById('side-panel');

    // -- Make sure the sidepanel button is visible
    sidepanel_btn_group.removeAttribute('elem-status');

    const allow_overflow = (status: boolean) => {
        if (status) {
            document.body.style.overflow = 'hidden';
            main_container.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
            main_container.style.overflow = 'auto';
        }
    }

    // -- Check if they both exist
    if (!sidepanel_button || !sidepanel || !main_container) 
        return create_toast('error', 'Error', 'There was an error loading the sidepanel, site functionality might be impaired.');

    const anim_lenght = 500;

    const manage_panel = (
        action: 'open' | 'close' | 'toggle' = 'toggle'
    ) => {
        // -- Check if the action is toggle
        let checked = sidepanel_button.checked;
        
        if (action === 'open' && checked) return;
        if (action === 'close' && !checked) return;
        
        // -- Set the status of the checkbox
        sidepanel_button.checked = checked;

        // -- Check the status of the checkbox
        switch(checked) {
            case true: 
                sidepanel.setAttribute('side-panel', 'in'); 
                nav_bar.classList.add('scrolled');
                allow_overflow(true);
                break;

            case false: 
                sidepanel.setAttribute('side-panel', 'out');
                scrolled();
                allow_overflow(false);
                break;
        }

        // -- Wait for the transition to finish
        sleep(anim_lenght).then(() => {
            // -- Check the status of the checkbox
            switch(sidepanel_button.checked) {
                case true: sidepanel.setAttribute('side-panel', 'visible'); break;
                case false: sidepanel.setAttribute('side-panel', 'hidden'); break;
            }
        });
    }

    // -- Attach the event listener
    sidepanel_button.addEventListener('change', async() => manage_panel());
    sidepanel_button.addEventListener('close', async() => manage_panel('close'));

    // -- Set the function to the global variable
    set_sidebar_state = (state: 'open' | 'closed') => {
        if (state === 'open') {
            sidepanel_button.checked = true;
            manage_panel();
        }
        else {
            sidepanel_button.checked = false;
            manage_panel('close');
        }
    }
}




/**
 * @name change_callbacks
 * @description This object contains all the callbacks
 *              That will be called when a panel is changed
 */
export let callbacks: Array<(
    panel_type: PanelType,
    panel: Panel,
    pod: Pod
) => void> = [];



/**
 * @name add_callback
 * @param callback: (panel_type: PanelType, panel: Panel, pod: Pod) => void - The callback
 * @returns void
 */
export function add_callback(callback: (panel_type: PanelType, panel: Panel, pod: Pod) => void) {
    callbacks.push(callback);
}


/**
 * @name attach_event_listeners
 * @returns void
 * 
 * @description This function attaches the click
 *              event listeners to the pods
 *              
 *              It handles the showing and hiding
 *              of panels.
 */
export function attach_event_listeners() {
    // -- Get all the elements with the 
    //    data-pod attribute
    const pod_elms = document.querySelectorAll('[data-pod]');
    locate_panels();
    attach_to_sidepanel();

    // -- Get all admin panel headers
    const admin_opts = document.querySelector('#admin-options');

    // -- Loop through the pods
    pod_elms.forEach(pod => {
        // -- Get the panel type
        const panel_type = pod.getAttribute('data-pod') as PanelType,
            panel = get_panel(panel_type);

        // -- Check if the panel exists
        if (!panel) return;

        // -- Create the pod object
        const pod_object: Pod = {
            element: pod,
            panel,
            type: panel_type
        }

        // -- Add the pod to the pods array
        pods.push(pod_object);

        // -- Check if the panel is being clicked
        pod.addEventListener('click', () => open_panel(panel_type));
    });
}



/**
 * @name open_panel
 * @param panel_type: PanelType - The panel type
 * @returns void
 * 
 * @description This function opens the panel
 *             that matches the panel type
 *             that was passed in.
 */
export function open_panel(panel_type: PanelType) {
    // -- Get the panel and pod
    const pod = get_pod(panel_type),
        active_pod = get_active_pod();
    
    // -- Check if the panel exists
    if (!pod) return;


    // -- Set the active panel to inactive
    if (active_pod) active_pod.panel.element.setAttribute('data-panel-status', 'hidden');
    pod.panel.element.setAttribute('data-panel-status', 'active');

    // -- If the active pod is not the same as the
    //    one that was clicked, then set the active
    //    pod to inactive and set the clicked pod to
    //    active
    if (active_pod) active_pod.element.setAttribute('data-pod-status', '');
    pod.element.setAttribute('data-pod-status', 'active');

    // -- Call all the callbacks
    callbacks.forEach(callback => callback(panel_type, pod.panel, pod));
}



/**
 * @name hide_pod
 * @param panel_type: PanelType - The panel type
 * @param redirect: PanelType - The panel type to redirect to
 * @returns void
 * 
 * @description This function hides the pod
 *              that matches the panel type  
 *              that was passed in.
 * 
 *              Also, it redirects to the
 *              panel type that was passed in.
 */
export function hide_pod(panel_type: PanelType, redirect: PanelType) {
    // -- Get the pod
    const pod = get_pod(panel_type);

    // -- Check if the pod exists
    if (!pod) return;

    // -- Open the panel that was passed in only if the 
    //    panel was active
    if (pod.element.getAttribute('data-pod-status') === 'active')
        open_panel(redirect);

    // -- Set the pod to hidden
    pod.element.setAttribute('data-pod-status', 'hidden');
}



/**
 * @name show_pod
 * @param panel_type: PanelType - The panel type
 * @returns void
 */
export function show_pod(panel_type: PanelType) {
    // -- Get the pod
    const pod = get_pod(panel_type);

    // -- Check if the pod exists
    if (!pod) return;

    // -- Set the pod to nothing
    pod.element.setAttribute('data-pod-status', '');
}