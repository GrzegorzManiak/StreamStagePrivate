export type List = Array<{
    id: string,
    old: Element,
    new: Element,
    getter: () => any,
    input_id: string
}>

function replace(list: List): void {
    list.forEach(elm => {
        elm.old.replaceWith(elm.new);
    });
}

function delete_old(list: List): void {
    list.forEach(elm => {
        elm.old.remove();
    });
}

function add_new(list: List): void {
    list.forEach(elm => {
        elm.old.parentElement.appendChild(elm.new);
    });
}

export function intercept(list: List, form_name: string) {
    switch (form_name) {
        case 'profile': return profile_intercept(list);
        default: return replace(list);
    }
}


// 
// Profile intercepter
// 
function profile_intercept(list: List) {
    // 
    // We only need to slighly modify the profile form
    // 1: Create a div and add 'frist_name-container' and 'last_name-container' to it
    // 2: Create a div and add 'id_country-container' and 'id_time_zone-container' to it
    //
    let new_list: List = [];

    // -- Create the first div
    const name_div = document.createElement('div'),
        country_div = document.createElement('div');

    // -- Add the classes 'd-flex gap-4'
    name_div.className = 'd-flex gap-4';
    name_div.id = 'name_div';

    country_div.className = 'd-flex gap-4';
    country_div.id = 'country_div';

    // -- Loop through the list
    list.forEach(elm => {
        switch (elm.id) {
            case 'first_name-container':
            case 'last_name-container':
                name_div.appendChild(elm.new);
                break;
            case 'id_country-container':
            case 'id_time_zone-container':
                country_div.appendChild(elm.new);
                break;
            default:
                new_list.push(elm);
        }
    });

    // -- Add the name_div as the 2nd element
    new_list.splice(1, 0, {
        id: 'name_div',
        old: list[1].old,
        new: name_div,
        getter: () => {},
        input_id: ''
    });

    // -- Add the country_div as the 4th element
    new_list.splice(3, 0, {
        id: 'country_div',
        old: list[3].old,
        new: country_div,
        getter: () => {},
        input_id: ''
    });

    // -- Replace the elements
    add_new(new_list);

    delete_old(list);
}