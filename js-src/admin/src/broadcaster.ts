import { attach, confirmation_modal, construct_modal, create_toast } from '../../common';
import { delete_broadcaster, filter_broadcasters, get_broadcaster, update_broadcaster } from '../api';
import { Broadcaster, BroadcasterSorts, BroadcasterSuccess, FilterdBroadcastersSuccess, Pod } from '../index.d';
import { manage_search_panel } from '../../common/search';

export async function manage_broadcaster_panel(pod: Pod) {
    // -- Gather all the inputs
    const panel = pod.panel.element;

    manage_search_panel<BroadcasterSorts, Broadcaster>(
        panel, (data, parent, refresh) => create_broadcaster(refresh, parent, data),
        async(page, sorts, order, search) => {
            const res = await filter_broadcasters(page, sorts, order, search
            ) as FilterdBroadcastersSuccess;

            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return;
            }

            return {
                data: res.data.broadcasters,
                message: res.message,
                code: res.code,
                page: res.data.page,
                pages: res.data.pages,
            }
        },
    );
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
    edit.addEventListener('click', () => manage_modal(update, edit, div, broadcaster));
}





/**
 * @name manage_modal
 * @description Creates and pops up a modal
 * @param {Function} update The function to call to update the results
 * @param {HTMLButtonElement} button The button to open the modal
 * @param {HTMLElement} entry The entry in the list to update
 * @param {broadcaster} broadcaster The id of the broadcaster to manage
 */
async function manage_modal(update: Function, button: HTMLButtonElement, entry: HTMLElement, broadcaster: Broadcaster) {
    // -- Attach the spinner and get the user 
    const stop = attach(button);

    // -- Get the user
    const res = await get_broadcaster(broadcaster.id) as BroadcasterSuccess;
    if (res.code !== 200) {
        create_toast('error', 'Oops! My bad', res.message);
        return stop();
    }

    // -- Create the modal
    const modal_div = construct_modal(
        'Manage Broadcaster',
        'Delete, Manage, and more!',
        false, 'success',
        modal_template(res.data),
    );

    // -- Add the modal to the page
    document.body.appendChild(modal_div);

    // -- Get the buttons and inputs
    const handle_input = modal_div.querySelector('#handle') as HTMLInputElement,
        handle_save = modal_div.querySelector('#handle-save-btn') as HTMLButtonElement,
        name_input = modal_div.querySelector('#name') as HTMLInputElement,
        name_save = modal_div.querySelector('#name-save-btn') as HTMLButtonElement,
        approved = modal_div.querySelector('#approved-status') as HTMLInputElement,
        over_18 = modal_div.querySelector('#over-18-status') as HTMLInputElement,
        more_btn = modal_div.querySelector('#more-btn') as HTMLButtonElement,
        owner_input = modal_div.querySelector('#streamer') as HTMLInputElement,
        owner_save = modal_div.querySelector('#streamer-save-btn') as HTMLButtonElement,
        delete_btn = modal_div.querySelector('#delete-btn') as HTMLButtonElement,
        exit = modal_div.querySelector('#exit') as HTMLButtonElement;

    const get_name = () => name_input.value,
        get_handle = () => handle_input.value,
        get_approved = () => approved.checked,
        get_over_18 = () => over_18.checked,
        get_owner = () => owner_input.value;
    
    // -- On leave destroy the modal
    exit.addEventListener('click', () => {
        update();
        modal_div.remove(); stop();
    });

    // -- Handle the handle change
    const update_server = async (
        btn: HTMLButtonElement = undefined,
    ) => {
        let stop = () => {};
        if (btn !== undefined) stop = attach(btn);
        const res = await update_broadcaster(
            broadcaster.id,
            get_name(),
            get_handle(),
            get_over_18(),
            get_approved(),
            broadcaster.biography,
            get_owner(),
        );

        if (res.code !== 200) {
            create_toast('error', 'Oops! My bad', res.message);
            return stop();
        }

        create_toast('success', 'Success!', 'Broadcaster updated!');
        stop();
    }

    more_btn.addEventListener('click', () => {
        const url = `https://me.streamstage.co/broadcaster/?bid=${broadcaster.id}`;
        const stop = attach(more_btn);
        
        // -- Open a popup
        window.open(
            url, 'popUpWindow',
            '_blank, width=900, height=700, left=10, top=10, resizable=yes, scrollbars=yes, toolbar=yes, menubar=no, location=no, directories=no, status=yes'
        );
        
        stop();
    });

    handle_save.addEventListener('click', async () => update_server(handle_save));
    name_save.addEventListener('click', async () => update_server(name_save));
    over_18.addEventListener('change', async () => update_server());
    approved.addEventListener('change', async () => update_server());
    owner_save.addEventListener('click', async () => update_server(owner_save));

    // -- Handle the delete
    delete_btn.addEventListener('click', async () => confirmation_modal(
        async () => {
            const res = await delete_broadcaster(broadcaster.id);
            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return stop();
            }
    
            create_toast('success', 'Success!', 'Broadcaster deleted!');
            entry.remove();
            modal_div.remove();
            update();
            stop();
        },
        () => {},
        'Are you sure you want to delete this broadcaster?',
        'This action cannot be undone',
    ));
}




/**
 * @name modal_template
 * @description The template for the modal
 * @param {Broadcaster} broadcaster The broadcaster to create the modal for
 * @returns {string} The template
 */
const modal_template = (broadcaster: Broadcaster) => `
    <div class="d-flex w-100 justify-content-between flex-column pb-2">
        <!-- Handle Change-->
        <label class="form-label" for="email">Handle</label>
        
        <div class='w-100 btn-group fc-dark'>
            <input 
                name="handle" 
                id="handle" 
                placeholder="Smelly socks" 
                value="${broadcaster.handle}"
            class="form-control form-control-lg inp fc-dark">
            
            <!-- Confirm handle Change -->
            <button type="submit" id="handle-save-btn" class="btn btn-primary info loader-btn" loader-state='default'>   
                <span><div class='spinner-border' role='status'><span class='visually-hidden'>Loading...</span></div>
                </span><p>Save</p>
            </button>
        </div>
    </div>


    <div class="d-flex w-100 justify-content-between flex-column">
        <!-- Name Change-->
        <label class="form-label" for="email">Name</label>
        
        <div class='w-100 btn-group fc-dark'>
            <input 
                name="name" 
                id="name" 
                placeholder="Cat Hater" 
                value="${broadcaster.name}"
            class="form-control form-control-lg inp fc-dark">
            
            <!-- Confirm handle Change -->
            <button type="submit" id="name-save-btn" class="btn btn-primary info loader-btn" loader-state='default'>   
                <span><div class='spinner-border' role='status'><span class='visually-hidden'>Loading...</span></div>
                </span><p>Save</p>
            </button>
        </div>
    </div>

    <hr>

    <div class="d-flex w-100 justify-content-between flex-column">
        <!-- Owner Change-->
        <label class="form-label" for="streamer">Streamer</label>
        
        <div class='w-100 btn-group fc-dark'>
            <input 
                name="streamer" 
                id="streamer" 
                placeholder="@Gregor" 
                value="${broadcaster.streamer}"
            class="form-control form-control-lg inp fc-dark">
            
            <!-- Confirm handle Change -->
            <button type="submit" id="streamer-save-btn" class="btn btn-primary info loader-btn" loader-state='default'>   
                <span><div class='spinner-border' role='status'><span class='visually-hidden'>Loading...</span></div>
                </span><p>Save</p>
            </button>
        </div>
    </div>

    <hr>

    <div class="d-flex w-100 justify-content-between gap-2">
        <div class="w-100 form-check">
            <!--Approved Status-->
            <input 
                class="form-check-input" 
                id="approved-status" 
                type="checkbox"
                value="${broadcaster.approved}">
            <label class="form-check-label" for="approved-status">Approved</label>
        </div>

        <div class="w-100 form-check">
            <!--Over 18 Status-->
            <input 
                class="form-check-input" 
                id="over-18-status" 
                type="checkbox"
                value="${broadcaster.over_18}">
            <label class="form-check-label" for="over-18-status">Over 18</label>
        </div>
    </div>

    <hr>

    <div class="d-flex w-100 btn-group">
        <!--More-->
        <button type="submit" id="more-btn" class="btn btn-slim btn-primary info loader-btn" loader-state='default'>
            <span><div class='spinner-border' role='status'><span class='visually-hidden'>Loading...</span></div>
            </span><p>More</p>
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
