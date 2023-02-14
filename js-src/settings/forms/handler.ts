import { attach } from "../../click_handler";
import { recent, send_verification } from "../api/email_verification";
import { create_toast } from '../../toasts';
import { Form, Pod, VerifyAccessSuccess } from "../index.d";
import { create_button, figure } from "./reformater";
import { intercept, List } from "./intercept";
import { send_form_data } from "../api/form";

let data_forms: Array<Form> = [];

export function handle_forms() {
    // -- Get every element with the data-form-id attribute
    const forms = document.querySelectorAll('[data-form-id]');

    // -- Loop through the forms
    forms.forEach(form => {
        
        // -- Get the form id
        const form_type = form.getAttribute('data-form-id'),
            form_endpoint = form.getAttribute('data-form-endpoint');
        
        // -- Create the form object
        const form_object: Form = {
            element: form,
            type: form_type,
            endpoint: form_endpoint
        };

        // -- Add the form to the data_forms array
        data_forms.push(form_object);
    });


    // -- Loop through the data_forms
    data_forms.forEach(form => {
        set_up_form(form);
    });

}


function get_data(list: List): any {
    let data: any = {};

    // -- Loop through the list
    list.forEach(elm => {
        data[elm.input_id] = elm.getter();
    });

    return data;
}

function set_up_form(form: Form) {
    // -- All the elements will be stored in 'p' elements
    const form_elements = form.element.querySelectorAll('p');

    let list: List = [];

    // -- Loop through the form elements
    form_elements.forEach(element => {
        const new_elm = figure(element);

        // -- Check if the element is there
        if (!new_elm) return;

        // -- Replace the old element with the new one
        list.push({
            id: new_elm[0].id,
            old: element,
            new: new_elm[0],
            getter: new_elm[2],
            input_id: new_elm[1]
        });
    });

    intercept(list, form.type);

    // -- Attach the button
    const button = create_button(form.type + '-button', 'Submit'),
        button_elm = button.childNodes[0] as HTMLButtonElement;

    // -- Attach the click handler
    button_elm.addEventListener('click', async() => {
        // -- Attach the loading animation
        const stop_spinner = attach(button_elm);

        // -- Get the values
        const values = get_data(list)
        console.log(values);
        // -- Ship the values off
        const response = await send_form_data(
            values, form.endpoint);

        // -- Check if the response is valid
        if (response.code === 200) {
            // -- Create the toast
            create_toast('success', 'Details save', response.message);
            return await stop_spinner();
        }

        create_toast('error', 'Error', response.message);
        return await stop_spinner();
    });

    // -- Append the button to the form
    form.element.appendChild(button);
}