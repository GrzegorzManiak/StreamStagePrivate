import { create_toast } from '../../common';
import { filter_broadcasters } from '../api';
import { Broadcaster, BroadcasterSorts, FilterOrder, FilterdBroadcastersSuccess, Pod } from '../index.d';
import { manage_search } from './users';

export async function manage_broadcaster_panel(pod: Pod) {
    // -- Gather all the inputs
    const panel = pod.panel.element;

    const filter = panel.querySelector('#filter'),
        order = panel.querySelector('#order'),
        search = panel.querySelector('#search'),
        prev = panel.querySelector('#prev'),
        next = panel.querySelector('#next'),
        page = panel.querySelector('#page'),
        out_of = panel.querySelector('.out-of'),
        content = panel.querySelector('.content-loader'),
        create = panel.querySelector('#create');

    // -- Create the functions to get the values
    //    of the inputs
    const get_filter = () => (filter as HTMLInputElement).value as BroadcasterSorts,
        get_order = () => (order as HTMLInputElement).value as FilterOrder,
        get_search = () => (search as HTMLInputElement).value,
        get_page = () => parseInt((page as HTMLInputElement).value, 10) - 1;


    let page_num = 1;
    prev.addEventListener('click', () => { page_num = page_num - 1;
        (page as HTMLInputElement).value = page_num.toString();
    })

    next.addEventListener('click', () => { page_num = page_num + 1;
        (page as HTMLInputElement).value = page_num.toString();
    });

    // -- Gather the elements that will display the results
    const results = panel.querySelector('.users') as HTMLElement;


    // -- Add the event listeners to the inputs
    const update = async () => {
        content.setAttribute('dimmed', 'true');
        const res = await filter_broadcasters(
            get_page(),
            get_filter(),
            get_order(),
            get_search()
        ) as FilterdBroadcastersSuccess;
        
        // -- Make sure the results are valid
        if (res.code !== 200) {
            content.setAttribute('dimmed', 'false');
            return create_toast('error', 'Oops! My bad', res.message);
        }

        // -- Clear the results
        results.innerHTML = '';
        res.data.broadcasters.forEach(user => create_broadcaster(
            update, 
            results, 
            user
        ));

        // -- Ensure that the buttons are enabled/disabled correctly
        if (res.data.page === 0) prev.setAttribute('disabled', 'true');
        else prev.removeAttribute('disabled');

        if (res.data.page === res.data.pages) next.setAttribute('disabled', 'true');
        else next.removeAttribute('disabled');

        // -- Update the max page
        out_of.innerHTML = 'out of ' + (res.data.pages + 1);
        content.setAttribute('dimmed', 'false');
    };

    filter.addEventListener('change', update);
    order.addEventListener('change', update);
    page.addEventListener('change', update);
    prev.addEventListener('click', update);
    next.addEventListener('click', update);

    manage_search(search as HTMLInputElement, () => update());
    update();
}




/**
 * @name create_broadcaster
 * @description Create a new broadcaster with the given data
 * @param {Function} update the function to call to update the results
 * @param {HTMLElement} element the element to add this user to
 * @param {Broadcaster} broadcaster the user to add
 */
function create_broadcaster(
    update: Function,
    element: HTMLElement, 
    broadcaster: Broadcaster
) {

    // -- Date or null
    const date = (date: string) => {
        if (date === null) return 'Never';
        return new Date(date).toLocaleDateString()
    }

    const template = `        
        <div class='profile-images'>
            <img src='${broadcaster.profile_picture}' />
        </div>

        <div class='profile-info'>
            <h3 class='m-0'>${broadcaster.name}</h3>
            <p class='m-0 text-muted'>@${broadcaster.handle.toLowerCase()}</p>
            <p class='m-0 text-muted'>${broadcaster.streamer}</p>
        </div>
        
        <div class='profile-info flex-wrap'>
            <p class='m-0 text-muted'><span class='bold'>Joined</span> ${date(broadcaster.created)}</p>
            <p class='m-0 text-muted'><span class='bold'>Last seen</span> ${date(broadcaster.updated)}</p>
        </div>

        <div class='profile-info flex-wrap'>
            <p class='m-0 text-muted'>Approved: ${broadcaster.approved ? '<span class="text-success">Yes</span>' : '<span class="text-danger">No</span>'}</p>
            <p class='m-0 text-muted'>Over 18's: ${broadcaster.over_18 ? '<span class="text-success">Yes</span>' : '<span class="text-danger">No</span>'}</p>
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