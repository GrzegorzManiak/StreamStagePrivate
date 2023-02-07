import { configuration } from '../';
import { PanelType, Panel, Pod } from '../index.d';

let panels: Array<Panel> = [];
export let pods: Array<Pod> = [];


function locate_panels() {
    // -- Get all elements with the data-panel-type attribute
    const panel_elements = document.querySelectorAll('[data-panel-type]');
    
    // -- Loop through the panel elements
    panel_elements.forEach(element => {
        // -- Get the panel type
        const panel_type = element.getAttribute('data-panel-type') as PanelType;

        // -- Create the panel object
        const panel: Panel = {
            element,
            type: panel_type
        }

        // -- Add the panel to the panels array
        panels.push(panel);
    });
}

function get_panel(panel_type: PanelType): Panel | undefined {
    // -- Loop through the panels
    for (const panel of panels) {
        // -- Check if the panel type matches the one
        //    that was passed in
        if (panel.type === panel_type) {
            return panel;
        }
    }
}

export function get_pod(panel_type: PanelType): Pod | undefined {
    // -- Loop through the pods
    for (const pod of pods) {
        // -- Check if the panel type matches the one
        //    that was passed in
        if (pod.type === panel_type) return pod;
    }
}

export function get_active_pod(): Pod | undefined {
    // -- Loop through the pods
    for (const pod of pods) {
        // -- Check if the panel type matches the one
        //    that was passed in
        if (pod.element.getAttribute('data-pod-status') === 'active') return pod;
    }
}



export function attach_event_listeners() {
    // -- Get all the elements with the 
    //    data-pod attribute
    const pod_elms = document.querySelectorAll('[data-pod]');
    locate_panels();
    
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
        pod.addEventListener('click', () => {
            // -- Get the current active pod button
            const active_pod = get_active_pod();
            console.log(active_pod);
            if (!active_pod) return;

            // -- Make sure the active panel is not the same
            //    as the one that was clicked
            if (active_pod.type === panel_type) return;

            // -- Set the active panel to inactive
            active_pod.panel.element.setAttribute('data-panel-status', 'hidden');
            panel.element.setAttribute('data-panel-status', 'active');

            // -- If the active pod is not the same as the
            //    one that was clicked, then set the active
            //    pod to inactive and set the clicked pod to
            //    active
            active_pod.element.setAttribute('data-pod-status', '');
            pod.setAttribute('data-pod-status', 'active');
        });

        // -- Check if the pod is an admin only pod
        if (pod.classList.contains('admin-pod') && configuration.admin === true) 
            pod.setAttribute('data-pod-status', '');
    });


    // -- Get all admin panel headers
    const headers = Array.from(document.getElementsByClassName('admin-header'));

    // -- Loop through the headers, and disable the 
    //    'data-pod-status' attribute, if the user
    //    is an admin
    if (configuration.admin === true) 
    for (const element of headers) {
        element.setAttribute('data-pod-status', '');
    }
}