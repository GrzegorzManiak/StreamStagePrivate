import { FilterOrder } from '../../common/index.d';
import { attach, confirmation_modal, construct_modal, create_toast } from '../../common';
import { delete_user, filter_users, get_user, update_email, update_streamer_status } from '../api';
import { FilterPosition, FilterSort, FilterdUser, FilterdUsersSuccess, Pod, UserSuccess } from '../index.d';

export async function manage_users_panel(pod: Pod) {
    // -- Gather all the inputs
    const panel = pod.panel.element;

    const position = panel.querySelector('#position'),
        filter = panel.querySelector('#filter'),
        order = panel.querySelector('#order'),
        search = panel.querySelector('#search'),
        prev = panel.querySelector('#prev'),
        next = panel.querySelector('#next'),
        page = panel.querySelector('#page'),
        out_of = panel.querySelector('.out-of'),
        content = panel.querySelector('.content-loader');


    // -- Create the functions to get the values
    //    of the inputs
    const get_position = () => (position as HTMLInputElement).value as FilterPosition,
        get_filter = () => (filter as HTMLInputElement).value as FilterSort,
        get_order = () => (order as HTMLInputElement).value as FilterOrder,
        get_search = () => (search as HTMLInputElement).value,
        get_page = () => parseInt((page as HTMLInputElement).value, 10) - 1;
        
    let page_num = 1;
    prev.addEventListener('click', () => {
        page_num = page_num - 1;
        (page as HTMLInputElement).value = page_num.toString();
    })

    next.addEventListener('click', () => {
        page_num = page_num + 1;
        (page as HTMLInputElement).value = page_num.toString();
    });

    
    // -- Gather the elements that will display the results
    const results = panel.querySelector('.users') as HTMLElement;

    // -- Add the event listeners to the inputs
    const update = async () => {
        content.setAttribute('dimmed', 'true');
        const res = await filter_users(
            get_page(),
            get_filter(),
            get_order(),
            get_position(),
            get_search()
        ) as FilterdUsersSuccess;
        
        // -- Make sure the results are valid
        if (res.code !== 200) {
            content.setAttribute('dimmed', 'false');
            return create_toast('error', 'Oops! My bad', res.message);
        }

        // -- Clear the results
        results.innerHTML = '';
        res.data.users.forEach(user => create_user(results, user));

        // -- Ensure that the buttons are enabled/disabled correctly
        if (res.data.page === 0) prev.setAttribute('disabled', 'true');
        else prev.removeAttribute('disabled');

        if (res.data.page === res.data.pages) next.setAttribute('disabled', 'true');
        else next.removeAttribute('disabled');

        // -- Update the max page
        out_of.innerHTML = 'out of ' + (res.data.pages + 1);
        content.setAttribute('dimmed', 'false');
    };


    position.addEventListener('change', update);
    filter.addEventListener('change', update);
    order.addEventListener('change', update);
    page.addEventListener('change', update);
    prev.addEventListener('click', update);
    next.addEventListener('click', update);

    manage_search(search as HTMLInputElement, () => update());
    update();
}



/**
 * @name manage_search
 * @description Get the search string from the search input
 * Delayed by x every time the user types a character
 * @param {HTMLInputElement} search The search input
 * @param {(search: string) => void} callback The callback to call when the search is ready
 * @param {number} delay The delay in milliseconds (default: 500)
 */
export function manage_search(
    search: HTMLInputElement, 
    callback: (search: string) => void,
    delay: number = 500
) {
    let timeout: NodeJS.Timeout;
    search.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            callback(search.value);
        }, delay);
    });
}



/**
 * @name create_user
 * @description Create a new user with the given data
 * @param {HTMLElement} element the element to add this user to
 * @param {FilterdUser} user the user to add
 */
function create_user(element: HTMLElement, user: FilterdUser) {

    // -- Date or null
    const date = (date: string) => {
        if (date === null) return 'Never';
        return new Date(date).toLocaleDateString()
    }

    const template = `        
        <div class='profile-images'>
            <img src='${user.profile_picture}' />
        </div>

        <div class='profile-info'>
            <h3 class='m-0'>${user.cased_username}</h3>
            <p class='m-0 text-muted'>${user.first_name ? user.first_name : 'N/A'}, ${user.last_name ? user.last_name : 'N/A'}</p>
            <p class='m-0 text-muted'>${user.email}</p>
        </div>
        
        <div class='profile-info flex-wrap'>
            <p class='m-0 text-muted'><span class='bold'> Joined</span> ${date(user.created)}</p>
            <p class='m-0 text-muted'><span class='bold'> Last seen</span> ${date(user.updated)}</p>
        </div>

        <div class='profile-info flex-wrap'>
            <p class='m-0 text-muted'>Admin: ${user.is_staff ? '<span class="text-success">Yes</span>' : '<span class="text-danger">No</span>'}</p>
            <p class='m-0 text-muted'>Streamer: ${user.streamer ? '<span class="text-success">Yes</span>' : '<span class="text-danger">No</span>'}</p>
            <p class='m-0 text-muted'>Over 18: ${user.over_18 ? '<span class="text-success">Yes</span>' : '<span class="text-danger">No</span>'}</p>
        </div>

        <div class='profile-actions'>
            <button class="w-100 h-100 btn btn-primary info loader-btn edit" loader-state="default">   
                <span> <div class="spinner-border" role="status"> 
                <span class="visually-hidden">Loading...</span> </div> </span>
                <p>Manage</p>
            </button>
        </div>
    `;

    // -- Create the element
    const div = document.createElement('div');
    div.classList.add('filterd-user');
    div.innerHTML = template;
    element.appendChild(div);


    // -- Get the buttons
    const edit = div.querySelector('.edit') as HTMLButtonElement;
    edit.addEventListener('click', () => manage_modal(edit, div, user.id));
}



/**
 * @name manage_modal
 * @description Creates and pops up a modal
 * @param {HTMLButtonElement} button The button to open the modal
 * @param {HTMLElement} entry The entry in the list to update
 * @param {string} id The id of the user this modal is for
 */
async function manage_modal(button: HTMLButtonElement, entry: HTMLElement, id: string) {
    // -- Attach the spinner and get the user 
    const stop = attach(button);

    // -- Get the user
    const res = await get_user(id) as UserSuccess;
    if (res.code !== 200) {
        create_toast('error', 'Oops! My bad', res.message);
        return stop();
    }

    // -- Create the modal
    const modal = construct_modal(
        'Manage User',
        'Delete, Impersonate, and more!',
        false, 'success',
        modal_template(res.data),
    );

    // -- Add the modal to the page
    const modal_div = document.createElement('div');
    modal_div.innerHTML = modal;
    document.body.appendChild(modal_div);

    // -- Get the buttons and inputs
    const email_save = modal_div.querySelector('#save-btn') as HTMLButtonElement,
        email = modal_div.querySelector('#email') as HTMLInputElement,
        reset_password = modal_div.querySelector('#reset-btn') as HTMLButtonElement,
        delete_btn = modal_div.querySelector('#delete-btn') as HTMLButtonElement,
        streamer = modal_div.querySelector('#streamer-status') as HTMLInputElement,
        impersonate = modal_div.querySelector('#impersonate-btn') as HTMLButtonElement,
        leave = modal_div.querySelector('#exit') as HTMLButtonElement;


    // -- On leave destroy the modal
    leave.addEventListener('click', () => {
        modal_div.remove(); stop();
    });



    // -- On impersonate
    impersonate.addEventListener('click', async () => {
        // -- Open a popup
        const stop_impersonate = attach(impersonate);
        const popup = window.open(
            '/?impersonate=' + id, 
            'popUpWindow',
            '_blank, width=900, height=700, left=10, top=10, resizable=yes, scrollbars=yes, toolbar=yes, menubar=no, location=no, directories=no, status=yes'
        );
        if (popup) popup.focus();
        popup?.addEventListener('load', () => stop_impersonate());
    });



    // -- Email change
    email_save.addEventListener('click', async () => confirmation_modal(
        async() => {
            const res = await update_email(id, email.value) as UserSuccess;
            if (res.code !== 200) create_toast('error', 'Oops! My bad', res.message);
            else create_toast('success', 'Success!', 'Email updated!');
            email.value = res.data.email;
        },
        () => {},
        'Are you sure you want to change the email?',
    ));
    


    // -- Delete user
    delete_btn.addEventListener('click', async () => confirmation_modal(
        async() => {
            const res = await delete_user(id) as UserSuccess;
            if (res.code !== 200) create_toast('error', 'Oops! My bad', res.message);
            else create_toast('success', 'Success!', 'User deleted!');
            modal_div.remove(); stop();
            entry.remove();
        },
        () => {},
        'Are you sure you want to delete this user?',
    ));



    // -- Streamer status
    streamer.addEventListener('change', async () => {
        const res = await update_streamer_status(id, streamer.checked) as UserSuccess;
        if (res.code !== 200) create_toast('error', 'Oops! My bad', res.message);
        else create_toast('success', 'Success!', 'Streamer status updated!');
    });
}



/**
 * @name modal_template
 * @description The template for the modal
 * @param {FilterdUser} user The user to display
 * @returns {string} The template
 */
const modal_template = (user: FilterdUser) => `
    <div class="d-flex w-100 justify-content-between flex-column">
        <!--Email Change-->
        <label class="form-label" for="email">New Email</label>
        
        <div 
            class='w-100 btn-group'
            style='background-color: var(--theme-backdrop-color)'
        >
            <input 
                name="email" 
                id="email" 
                placeholder="Sick@email.com" 
                value="${user.email}"
            class="form-control form-control-lg inp">
            
            <!-- Confirm Email Change -->
            <button type="submit" id="save-btn" class="btn btn-primary info loader-btn" loader-state='default'>   
                <span><div class='spinner-border' role='status'><span class='visually-hidden'>Loading...</span></div>
                </span><p>Save</p>
            </button>
        </div>

    </div>

    <hr>

    <div class="d-flex w-100 justify-content-between flex-column">
        <div class="w-100 form-check">
            <!--Streamer Status-->
            <input 
                class="form-check-input" 
                id="streamer-status" 
                type="checkbox"
                value="${user.streamer}">
            <label class="form-check-label" for="streamer-status">Streamer</label>
        </div>
    <hr>

    <div class="d-flex w-100 btn-group">
        <!--Send reset password email-->
        <button type="submit" id="reset-btn" class="btn btn-slim btn-warn warning loader-btn" loader-state='default'>
            <span><div class='spinner-border' role='status'><span class='visually-hidden'>Loading...</span></div>
            </span><p>Reset Password</p>
        </button>

        <!--Impersonate-->
        <button type="submit" id="impersonate-btn" class="btn btn-slim btn-primary info loader-btn" loader-state='default'>
            <span><div class='spinner-border' role='status'><span class='visually-hidden'>Loading...</span></div>
            </span><p>Impersonate</p>
        </button>

        <!--Delete-->
        <button type="submit" id="delete-btn" class="btn btn-slim btn-danger error loader-btn" loader-state='default'>
            <span><div class='spinner-border' role='status'><span class='visually-hidden'>Loading...</span></div>
            </span><p>Delete</p>
        </button>
    </div>

    <hr>

    <!--Exit Button-->
    <button type="submit" id="exit"
        class="btn btn-lg btn-success success w-100 loader-btn" loader-state='default'>
        <p>Leave</p>
    </button>
`;
