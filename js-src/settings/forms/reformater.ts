// -- Text input
//<div class="mb-4">
// <label class="form-label" for="username">Username</label>
// <input name="username" autocomplete='off' id="username" placeholder="CoolDude1" class="
//     form-control 
//     form-control-lg
//     inp
// ">
//</div>
export function text_input(elm: HTMLParagraphElement): [HTMLDivElement, string, () => any] {
    // -- Get all the data from this form
    const label = elm.getElementsByTagName('label')[0] as HTMLLabelElement,
        input = elm.getElementsByTagName('input')[0] as HTMLInputElement;

    // -- Create the container
    const container = document.createElement('div');
    container.classList.add('mb-4');

    // -- Create the label
    const label_elm = document.createElement('label');
    label_elm.classList.add('form-label');
    label_elm.setAttribute('for', input.getAttribute('name'));
    label_elm.innerText = label.innerText;

    // -- Create the input
    const input_elm = document.createElement('input');
    input_elm.setAttribute('name', input.getAttribute('name'));
    input_elm.setAttribute('autocomplete', input.getAttribute('autocomplete'));
    input_elm.setAttribute('id', input.getAttribute('id'));
    input_elm.setAttribute('placeholder', input.getAttribute('placeholder') || '');
    input_elm.classList.add('form-control', 'form-control-lg', 'inp');
    input_elm.value = input.getAttribute('value') || '';

    // -- Append the label and input to the container
    container.appendChild(label_elm);
    container.appendChild(input_elm);

    // -- Set the container id
    container.setAttribute('id', input_elm.getAttribute('name') + '-container');
    container.setAttribute('data-id', input_elm.getAttribute('id'));

    // -- Return the container
    return [container, input_elm.getAttribute('name'), () => input_elm.value];
}


// <!-- Description -->
// <div class="mb-4">
//     <label class="form-label" for="bio">Bio</label>
//     <textarea 
//         name="bio" 
//         id="bio" 
//         cols="40" rows="5"
//         placeholder="I like to eat cheese"
//         value="{{ user.description }}"
//         class="
//             form-control 
//             form-control-lg
//             inp
//         "> 
//     </textarea>
// </div>
export function text_area(elm: HTMLParagraphElement): [HTMLDivElement, string, () => any] {
    // -- Get all the data from this form
    const label = elm.getElementsByTagName('label')[0] as HTMLLabelElement,
        textarea = elm.getElementsByTagName('textarea')[0] as HTMLTextAreaElement;

    // -- Create the container
    const container = document.createElement('div');
    container.classList.add('mb-4');
    
    // -- Create the label
    const label_elm = document.createElement('label');
    label_elm.classList.add('form-label');
    label_elm.setAttribute('for', textarea.getAttribute('name'));
    label_elm.innerText = label.innerText;
    
    // -- Create the textarea
    const textarea_elm = document.createElement('textarea');
    textarea_elm.setAttribute('name', textarea.getAttribute('name'));
    textarea_elm.setAttribute('id', textarea.getAttribute('id'));
    textarea_elm.setAttribute('cols', textarea.getAttribute('cols'));
    textarea_elm.setAttribute('rows', textarea.getAttribute('rows'));
    textarea_elm.setAttribute('placeholder', textarea.getAttribute('placeholder') || '');
    textarea_elm.classList.add('form-control', 'form-control-lg', 'inp');
    textarea_elm.value = textarea.getAttribute('value') || '';

    // -- Append the label and textarea to the container
    container.appendChild(label_elm);
    container.appendChild(textarea_elm);

    // -- Set the contianre id
    container.setAttribute('id', textarea.getAttribute('name') + '-container');
    container.setAttribute('data-id', textarea.getAttribute('id'));
    
    // -- Return the container
    return [container, textarea_elm.getAttribute('name'), () => textarea_elm.value];
}


// -- Select
// <div class="mb-4">
//     <label class="form-label" for="country">Country</label>
//     <select name="country" id="country" class="
//         form-select 
//         form-select-lg
//         inp
//     ">
//         <option value="US">United States</option>
//         <option value="UK">United Kingdom</option>
//         <option value="CA">Canada</option>
//     </select>
// </div>
export function select(elm: HTMLParagraphElement): [HTMLDivElement, string, () => any] {
    // -- Get all the data from this form
    const label = elm.getElementsByTagName('label')[0] as HTMLLabelElement,
        select = elm.getElementsByTagName('select')[0] as HTMLSelectElement;

    // -- Create the container
    const container = document.createElement('div');
    container.classList.add('mb-4');

    // -- Create the label
    const label_elm = document.createElement('label');
    label_elm.classList.add('form-label');
    label_elm.setAttribute('for', select.getAttribute('name'));
    label_elm.innerText = label.innerText;

    // -- Create the select
    const select_elm = document.createElement('select');

    // -- Create the options
    const options = select.getElementsByTagName('option');

    for (let i = 0; i < options.length; i++) {
        const option = options[i] as HTMLOptionElement;
        const option_elm = document.createElement('option');
        option_elm.value = option.value;
        option_elm.innerText = option.innerText;
        select_elm.appendChild(option_elm);
    }

    select_elm.setAttribute('name', select.getAttribute('name'));
    select_elm.setAttribute('id', select.getAttribute('id'));
    select_elm.classList.add('form-select', 'form-select-lg', 'inp');
    select_elm.value = select.value;

    console.log(select.value);


    // -- Append the label and select to the container
    container.appendChild(label_elm);
    container.appendChild(select_elm);

    // -- Set the contianer id 
    container.setAttribute('id', select.getAttribute('id') + '-container');
    container.setAttribute('data-id', select.getAttribute('id'));

    // -- Return the container
    return [container, select_elm.getAttribute('name'), () => select_elm.value];
}


export function figure(
    elm: HTMLParagraphElement
): [HTMLDivElement, string, () => any] | undefined {

    let in_element = elm.getElementsByTagName('input')[0] as HTMLInputElement | undefined;
    if (in_element) switch (in_element.getAttribute('type')) {
        case 'text': return text_input(elm);
    }

    let ta_element = elm.getElementsByTagName('textarea')[0] as HTMLTextAreaElement | undefined;
    if (ta_element) return text_area(elm);


    let sel_element = elm.getElementsByTagName('select')[0] as HTMLSelectElement | undefined;
    if (sel_element) return select(elm);


    return undefined;
}


// <!-- Buttons -->
// <div class="
//     d-flex 
//     justify-content-lg-start
//     justify-content-center
//     flex-column
//     mb-5
// ">

//     <button 
//         type="submit" 
//         id="login-btn" 
//         class="
//             btn 
//             btn-primary
//             mb-3
//             btn-lg
//             loader-btn
//         "
//         loader-state='default'
//     >   
//         <span>
//             <div class='spinner-border' role='status'>
//                 <span class='visually-hidden'>Loading...</span>
//             </div>
//         </span>
//         <p>Create</p>
//     </button>
// </div>
export function create_button(id: string, text: string): HTMLDivElement {
    // -- Create the container
    const container = document.createElement('div');
    container.classList.add('d-flex', 'justify-content-lg-start', 'justify-content-center', 'flex-column', 'mb-5');

    // -- Create the button
    const button = document.createElement('button');
    button.setAttribute('type', 'submit');
    button.setAttribute('id', id);
    button.classList.add('btn', 'btn-primary', 'mb-3', 'btn-lg', 'loader-btn');
    button.setAttribute('loader-state', 'default');

    // -- Create the span
    const span = document.createElement('span');

    // -- Create the spinner
    const spinner = document.createElement('div');
    spinner.classList.add('spinner-border');
    spinner.setAttribute('role', 'status');

    // -- Create the span
    const spinner_span = document.createElement('span');
    spinner_span.classList.add('visually-hidden');
    spinner_span.innerText = 'Loading...';

    // -- Create the p
    const p = document.createElement('p');
    p.innerText = text;

    // -- Append the spinner and spinner span to the spinner
    spinner.appendChild(spinner_span);

    // -- Append the spinner and p to the span
    span.appendChild(spinner);

    // -- Append the span to the button
    button.appendChild(span);
    button.appendChild(p);

    // -- Append the button to the container
    container.appendChild(button);

    // -- Return the container
    return container;
}