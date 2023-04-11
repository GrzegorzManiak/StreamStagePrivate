import { BroadcasterDetails, GetBroadcasterDetailsSuccess, UpdateBroadcasterDetailsSuccess } from "./index.d";
import { create_toast } from "../common";
import { get_broadcaster_details, update_broadcaster_details } from "./api";
import { configuration } from "./index";
import { construct_modal } from "../common/index";
import { picture_upload_modal } from "../common/picture";

let form_template:HTMLFormElement;
let pfp, banner_img : HTMLElement;
let bc_list;

let broadcasters : BroadcasterDetails[] = [];

let page_init_bid;

let editing_broadcaster : BroadcasterDetails;

export function manage_broadcaster_list(panel: HTMLElement) {
    bc_list = panel;

    form_template = document.querySelector("#bc-update-form") as HTMLFormElement;

    // Check to see if user has been sent
    // from broadcaster profile page
    parse_get_params();

    load_broadcasters();
}

function parse_get_params() {
    // -- Read GET parameters 
    const url = new URL(window.location.href);
    
    const id = url.searchParams.get('bid');
    
    if (!id) return;

    page_init_bid = id;
    update_url(null);
}

function update_url(details : BroadcasterDetails) {
    const url = new URL(window.location.href);

    // Add id as GET parameter (or nothing if details = null)
    if (details == null) {
        url.searchParams.delete('bid');
    } else {
        url.searchParams.set('bid', details.id);
    }

    window.history.replaceState(null, null, url); // or pushState
}

function load_broadcasters() {
    bc_list.innerHTML = "";
    broadcasters = [];

    var ids = configuration.broadcaster_ids.split(",");

    for (var id of ids) {
        query_and_append(id);
    }
}

function on_successful_update(modal: HTMLDivElement) {
    create_toast('success', "Broadcaster", `Successfully updated broadcaster details for @${editing_broadcaster.handle}`);
    modal.remove();

    update_url(null);

    load_broadcasters();
}

function init_form(update_form: HTMLFormElement, modal: HTMLDivElement) {
    pfp = update_form.querySelector('.profile-picture') as HTMLElement;
    banner_img = update_form.querySelector('.profile-banner') as HTMLElement;
    var banner_img_img = update_form.querySelector('.profile-banner-img') as HTMLElement;

    var name_field = update_form.querySelector("#id_name") as HTMLInputElement;
    var bio_field = update_form.querySelector("#id_biography") as HTMLInputElement;

    // Populate fields with current values 
    name_field.value = editing_broadcaster.name;
    bio_field.value = editing_broadcaster.biography;

    banner_img_img.style.backgroundImage = `url('${editing_broadcaster.banner}')`
    pfp.src = `${editing_broadcaster.profile}`

    update_form.addEventListener('submit', async (event) => {
        event.preventDefault();

        var profile = editing_broadcaster.profile_updated ? editing_broadcaster.profile : "";
        var banner = editing_broadcaster.banner_updated ? editing_broadcaster.banner : ""; 

        const response = await update_broadcaster_details(editing_broadcaster.id, name_field.value, bio_field.value, profile, banner);

        if (response.code !== 200) {
            return create_toast('error', "Oops!", response.message);
        }

        const data = (response as UpdateBroadcasterDetailsSuccess).data;
        
        on_successful_update(modal);
    });

    var cancel_btn = update_form.querySelector(".cancel-update");

    cancel_btn.addEventListener('click', async() => {
        modal.remove();
        update_url(null);
    });

    pfp.addEventListener('click', () => picture_upload_modal(
        editing_broadcaster.profile, 1,
        'Profile Picture',
        'Upload a profile picture',

        (image: string) => {
            pfp.src = image;

            editing_broadcaster.profile = image;
            editing_broadcaster.profile_updated = true;

            return true;
        }
    ));

    banner_img.addEventListener('click', () => picture_upload_modal(
        editing_broadcaster.banner, 21 / 7,
        'Profile Banner',
        'Upload a profile banner',
        (image: string) => {
            banner_img.style.backgroundImage = `url(${image})`;
            
            editing_broadcaster.banner = image;
            editing_broadcaster.banner_updated = true;

            return true;
        }
    ));
}

function edit(broadcaster: BroadcasterDetails) {
    editing_broadcaster = broadcaster;
    
    update_url(editing_broadcaster);

    var modal_html = construct_modal(
        "Update Broadcaster Details",
        `Adjust settings for @${broadcaster.handle}`,
        false,
        "success",
        form_template.outerHTML
    );
    
    // -- Create a div element
    const modal_wrap = document.createElement('div');

    // -- Set the innerHTML of the div to the modal
    modal_wrap.innerHTML = modal_html;

    // -- Append the modal to the body
    document.body.appendChild(modal_wrap);

    var form = modal_wrap.querySelector("#bc-update-form") as HTMLFormElement;

    form.style.display = "block";

    init_form(form, modal_wrap)
}

async function query_and_append(id: string) {
    const response = await get_broadcaster_details(id);

    // -- Check if the request was successful
    if (response.code !== 200)
        return create_toast('error', 'Oops!', response.message)

    const data = (response as GetBroadcasterDetailsSuccess).data

    console.log(data);

    broadcasters.push(data.details);
    append(data.details);

    // Check if this is the broadcaster the user 
    // has been redirected to edit
    if (page_init_bid == data.details.id) {
        edit(data.details);

        page_init_bid = null;
    }
}

function append(broadcaster: BroadcasterDetails) {
    var bc_elem = bc_html(broadcaster);

    bc_list.appendChild(bc_elem);
    
    bc_elem.querySelector(".broadcaster-edit-btn").addEventListener('click', function() {
        edit(broadcaster);
    });
}

function bc_html(details: BroadcasterDetails) : HTMLElement {
    var row = document.createElement('div');
    row.className = "broadcaster-entry";
    row.setAttribute("data-broadcaster-id", details.id);

    row.setAttribute("style", "background-image: url('" + details.banner + "'); background-");
    
    row.style.backgroundImage = details.banner;

    var approval_html = "";

    if (!details.approved) {
        approval_html = `<div class="float-end text-danger">Awaiting Approval</div>`
    }

    row.innerHTML = `
        <img alt="Profile Picture" class="profile-picture-edit" src="${details.profile}">
        <div class='profile-info'>
            <h1>${details.name}</h1>
            <a href="${details.url}" class='h3 t/media/broadcaster/banners/e8d3acef-77fc-4dc4-9829-2216d110aa28.webpext-muted'>@${details.handle}</a>
        </div>
        <p class='text-muted' style="max-width: 50%;">
            ${details.biography}
        </p>
        <div class="float-end" style="width:100%;">
            ${approval_html}
            <div data-broadcaster-id="${details.id}" class="broadcaster-edit-btn edit-details float-end"> Edit Details <i class="fas fa-chevron-right"></i> </div>
        </div>
    `

    return row;
}