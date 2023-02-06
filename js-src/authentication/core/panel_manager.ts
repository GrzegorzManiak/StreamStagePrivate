import { Panel, PanelType } from "../index.d";

// -- Get all the panels
const raw_panels = Array.from(document.getElementsByClassName('panel'));

export let panels: Array<Panel> = [];
raw_panels.forEach((panel) => {
    
    // -- Get the type from the aria lable
    const type = panel.getAttribute('data-panel-type') as PanelType;

    // -- Add to panels
    panels.push({
        type,
        element: panel as HTMLDivElement,
    });
});


export const get_panel = (type: PanelType) => {
    const panel = panels.find((panel) => panel.type === type);
    if (!panel) throw new Error(`No panel of type ${type} found`);
    return panel;
}

export const show_panel = (type: PanelType) => {
    const panel = get_panel(type);
    panel.element.style.display = 'block';
}

export const hide_panel = (type: PanelType) => {
    const panel = get_panel(type);
    panel.element.style.display = 'none';
}

export const hide_all_panels_except = (type: PanelType) => {
    panels.forEach((panel) => {
        if (panel.type !== type) {
            panel.element.style.display = 'none';
        }
    });

    show_panel(type);
}