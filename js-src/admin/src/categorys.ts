import { attach, construct_modal, create_toast } from '../../common';
import { picture_upload_modal } from '../../common/picture';
import { create_category, delete_category, filter_categories, get_category, set_category_image, update_category } from '../api';
import { Category, CategorySorts, CategorySuccess, FilterdCategoriesSuccess, Pod } from '../index.d';
import { manage_search_panel } from '../../common/search';

export async function manage_category_panel(pod: Pod) {
    // -- Gather all the inputs
    const panel = pod.panel.element,
        create = panel.querySelector('#create');

    const update = manage_search_panel<CategorySorts, Category>(
        panel, (data, parent, refresh) => create_category_modal(refresh, parent, data),
        async(page, sorts, order, search) => {
            const res = await filter_categories(page, sorts, order, search
            ) as FilterdCategoriesSuccess;

            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return;
            }

            return {
                data: res.data.categorys,
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
 * @name create_category
 * @param {() => void} refresh_categories
 * @param {HTMLElement} parent
 * @param {Category} category
 */
export function create_category_modal(
    refresh_categories: () => void,
    parent: HTMLElement, 
    category: Category
) {
    const template = `        
    <div class='profile-info cat-info p-2'>
        <h3 class='m-0'>${category.name}</h3>
        <p class='m-0 text-muted' style='color: ${category.color}!important'>${category.color}</p>
        <p class='m-0 text-muted cat-desc' style='overflow: none'>${category.description}</p>
    </div>

    <div class='profile-actions p-2'>
        <button class="w-100 h-100 btn btn-primary info loader-btn edit" loader-state="default">   
            <span> <div class="spinner-border" role="status"> 
            <span class="visually-hidden">Loading...</span> </div> </span>
            <p>Manage</p>
        </button>
    </div>
    `;

    // -- Create the element
    const div = document.createElement('div');
    div.innerHTML = template;
    div.classList.add('d-flex', 'justify-content-between', 'align-items-center', 'gap-2', 'category', 'cat-container');
    parent.appendChild(div);

    // -- Add the event listeners
    const edit = div.querySelector('.edit') as HTMLButtonElement;
    edit.addEventListener('click', async() => {
        const stop = attach(edit);
        await create_category_panel(
            refresh_categories,
            category.image,
            category.id,
        )
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