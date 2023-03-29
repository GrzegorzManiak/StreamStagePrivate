import { create_toast, sleep } from '../../common';
import { filter_users } from '../api';
import { FilterOrder, FilterPosition, FilterSort, FilterdUser, FilterdUsersSuccess, Pod } from '../index.d';

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
function manage_search(
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
}

