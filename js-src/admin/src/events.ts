import { attach, construct_modal, create_toast } from '../../common';
import { picture_upload_modal } from '../../common/picture';
import { manage_search_panel } from '../../common/search';
import { create_category, delete_category, filter_events, get_category, set_category_image, update_category } from '../api';
import { Event, CategorySuccess, FilterdEventsSuccess, Pod, CategorySorts, EventSorts } from '../index.d';
import { manage_search } from './users';

export async function manage_event_panel(pod: Pod) {
    // -- Gather all the inputs
    const panel = pod.panel.element,
        create = panel.querySelector('#create');

    const update = manage_search_panel<EventSorts, Event>(
        panel, (data, parent, refresh) => create_event_modal(refresh, parent, data),
        async(page, sorts, order, search) => {
            const res = await filter_events(page, sorts, order, search
            ) as FilterdEventsSuccess;

            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return;
            }

            return {
                data: res.data.events,
                message: res.message,
                code: res.code,
                page: res.data.page,
                pages: res.data.pages,
            }
        },
    );
        
        
    // -- Add the event listener to the create button
    create.addEventListener('click', () => create_category_panel(
        () => update(),
    ));
}



/**
 * @name create_event_modal
 * @param {() => void} refresh_categories
 * @param {HTMLElement} parent
 * @param {Event} event
 */
export function create_event_modal(
    refresh_events: () => void,
    parent: HTMLElement, 
    event: Event
) {
    // -- Date or null
    const date = (date: string) => {
        if (date === null) return 'Never';
        return new Date(date).toLocaleDateString()
    }


    const template = ` 
    <div>
        <div class='w-100 d-flex justify-content-between align-items-center events-scale p-2'>
            <div class='profile-info flex-wrap'>
                <p class='m-0 text-muted'><span class='bold'> Created:</span> ${date(event.created)}</p>
                <p class='m-0 text-muted'><span class='bold'> Updated:</span> ${date(event.updated)}</p>
            </div>

            <div class='profile-info flex-wrap'>
                <p class='m-0 text-muted'>Over 18's: ${event.over_18 ? '<span class="text-success">Yes</span>' : '<span class="text-danger">No</span>'}</p>
                <p class='m-0 text-muted'>Approved: ${event.approved ? '<span class="text-success">Yes</span>' : '<span class="text-danger">No</span>'}</p>
            </div>

            <div class='profile-info flex-wrap'>
                <p class='m-0 text-muted'><span class='bold'> Showings:</span> ${event.showings.length}</p>
                <p class='m-0 text-muted'><span class='bold'> Contributors:</span> ${event.contributors.length}</p>
            </div>

            <div class='profile-actions p-2'>
                <button class="w-100 h-100 btn btn-primary info loader-btn edit" loader-state="default">   
                    <span> 
                        <div class="spinner-border" role="status"> 
                            <span class="visually-hidden">Loading...</span>  
                        </div>
                    </span>

                    <p>Manage</p>
                </button>
            </div>
        </div>

        <div class='w-100 d-flex justify-content-between align-items-center p-2'>
            <div class='profile-info cat-info'>

                <div class='m-0 text-muted d-flex justify-content-between w-100 event-details-flex'>
                    <h3 class='m-0 w-25'>Broadcaster</h3>
                    <span class='w-25'>${event.broadcaster.handle}</span>
                    <span class='w-50'>ID: ${event.broadcaster.id}</span>
                </div>

                <div class='m-0 text-muted d-flex justify-content-between w-100 event-details-flex'>
                    <h3 class='m-0 w-25'>Title</h3>
                    <span class='w-25'>${event.title}</span>
                    <span class='w-50'>ID: ${event.id}</span>
                </div>

                <h3 class='m-0'>Description: <span class='m-0 text-muted'>${event.description}</span></h3>
            </div>
        </div>
    <div>
    `;

    // -- Create the element
    const div = document.createElement('div');
    div.innerHTML = template;
    div.classList.add('category', 'cat-container');
    parent.appendChild(div);

    // -- Add the event listeners
    const edit = div.querySelector('.edit') as HTMLButtonElement;
    edit.addEventListener('click', async() => {
        const url = event.url + 'update';
        const stop = attach(edit);
        const popup = window.open(
            url, 'popUpWindow',
            '_blank, width=900, height=700, left=10, top=10, resizable=yes, scrollbars=yes, toolbar=yes, menubar=no, location=no, directories=no, status=yes'
        );
        if (popup) popup.focus();
        stop();
    });
}



/**
 * @name create_category_panel
 * @param {() => void} refresh_categories
 * @param {string} image - The image url
 * @param {string} id - The id of the category
 * @returns {Promise<void>}
 */
export async function create_category_panel(
    refresh_categories: () => void,
    image: string = 'https://placehold.co/1050x350',
    id: string = null,
) {
    let name_text = '',
        description_text = '',
        color_text = '#000000'; 

    // -- Get the data
    if (id !== null) {
        const res = await get_category(id) as CategorySuccess;
        if (res.code !== 200) return create_toast('error', 'Oops! My bad', res.message);

        name_text = res.data.name;
        description_text = res.data.description;
        color_text = res.data.color;
        image = res.data.image;
    }


    const template = `
        <!-- Banner -->
        <div style="background-image: url('${image}')" 
            class="modal-banner mb-2" 
            alt="Banner">
        </div>


        <!-- Name and description -->
        <div class="w-100 d-flex justify-content-center flex-column align-items-center">
            <div class="mb-2 w-100">
                <label class="form-label" for="name">Name</label>
                <input 
                    name="name" 
                    id="name" 
                    placeholder="Mega Comedy"" 
                    type="text"
                    value="${name_text}"
                    class="form-control inp w-100 fc-dark">
            </div>

            <div class="mb-2">
                <label class="form-label" for="description">Description</label>
                <textarea 
                    name="description" 
                    id="description" 
                    cols="40" rows="5"
                    placeholder="I like to eat cheese"
                    class="form-control inp fc-dark">${description_text}</textarea>
            </div>

            <div class="mb-4 w-100">
                <!-- Color -->
                <label class="form-label" for="color">Color</label>
                <div class='color-parent'>
                    <input
                        name="color"
                        id="color"
                        value="${color_text}"
                        type="color"
                        class="form-control inp fc-dark w-100 p-0">
                </div>
            </div>
        </div>
        
        <div class='w-100 d-flex btn-group'>
            <!--Create Button-->
            <button type="submit" id="create"
                class="btn btn-lg btn-success success w-100 loader-btn" loader-state='default'>
                <span> <div class='spinner-border' role='status'> 
                <span class='visually-hidden'>Loading...</span> </div> </span>
                <p>${id === null ? 'Create' : 'Update'}</p>
            </button>

            ${id === null ? '' : `
                <!--Delete Button-->
                <button type="submit" id="delete"
                    class="btn btn-lg btn-danger error w-100 loader-btn" loader-state='default'>
                    <span> <div class='spinner-border' role='status'>
                    <span class='visually-hidden'>Loading...</span> </div> </span>
                    <p>Delete</p>
                </button>
            `}

            <!--Cancel Button-->
            <button type="submit" id="cancel"
                class="btn btn-lg btn-warn warning w-100 loader-btn" loader-state='default'>
                <p>Cancel</p>
            </button>
        </div>
    `;

    // -- Create the element
    const div = construct_modal(
        id === null ? 'Create Category' : 'Update Category',
        id === null ? 'Create a new category' : 'Update the category',
        false, 'success',
        template
    );
    document.body.appendChild(div);


    // -- Get the elements
    const create = div.querySelector('#create') as HTMLButtonElement,
        cancel = div.querySelector('#cancel') as HTMLButtonElement,
        name = div.querySelector('#name') as HTMLInputElement,
        description = div.querySelector('#description') as HTMLTextAreaElement,
        color = div.querySelector('#color') as HTMLInputElement,
        banner = div.querySelector('.modal-banner') as HTMLImageElement,
        delete_btn = div.querySelector('#delete') as HTMLButtonElement;


    let b64_image: string | null = null;
    banner.addEventListener('click', () => picture_upload_modal(
        image, 21 / 7,
        'Banner Picture',
        'Upload a banenr picture',
        async (image: string) => {
            b64_image = image;
            banner.style.backgroundImage = `url('${image}')`;
            return true;
        }
    ));


    // -- Add the event listeners
    if (id === null) create.disabled = true;
    create.addEventListener('click', async () => {
        const stop = attach(create);

        // -- Check if the ID is present (Update)
        if (id !== null) {
            const res = await update_category(
                id,
                name.value,
                description.value,
                color.value
            );

            // -- Check if the category was updated
            if (res.code !== 200) {
                create_toast('error', 'Oops!', res.message);
                return stop();
            }

            // -- Check if B64 image is present
            if (b64_image !== null) {
                const res = await set_category_image(id, b64_image);
                if (res.code !== 200) {
                    create_toast('error', 'Oops!', res.message);
                    return stop();
                }
            }

            // -- Create the toast
            create_toast('success', 'Success!', 'Category updated successfully');
            refresh_categories();
            div.remove();
        }

        else {
            // -- Create the category
            const res = await create_category(
                name.value,
                description.value,
                color.value,
                b64_image ?? ''
            );

            // -- Check if the category was created
            if (res.code !== 200) {
                create_toast('error', 'Oops!', res.message);
                return stop();
            }

            // -- Create the toast
            create_toast('success', 'Success!', 'Category created successfully');
            refresh_categories();
            div.remove();
        }
    });


    cancel.addEventListener('click', () => div.remove());

    // -- Make sure all the inputs are filled
    let inputs = [name, description, color];
    inputs.forEach(inp => inp.addEventListener('input', () => {
        create.disabled = inputs.some(inp => inp.value === '');
    }));

    // -- Delete the category
    if (id === null) return;
    delete_btn.addEventListener('click', async () => {
        const stop = attach(delete_btn);

        // -- Delete the category
        const res = await delete_category(id);
        if (res.code !== 200) {
            create_toast('error', 'Oops!', res.message);
            return stop();
        }

        // -- Create the toast
        create_toast('success', 'Success!', 'Category deleted successfully');
        refresh_categories();
        div.remove();
    });
}