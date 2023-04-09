import { BroadcasterDetails, GetBroadcasterDetailsSuccess, UpdateBroadcasterDetailsSuccess } from "./index.d";
import { create_toast } from "../common";
import { get_broadcaster_details, update_broadcaster_details } from "./api";
import { configuration } from "./index";
import { construct_modal } from "../common/index";
import { picture_upload_modal } from "../common/picture";

let form_template:HTMLFormElement;
let pfp, banner_img : HTMLElement;
let bc_list;

let editing_broadcaster : BroadcasterDetails;

export function manage_broadcaster_list(panel: HTMLElement) {
    bc_list = panel;

    form_template = document.querySelector("#bc-update-form") as HTMLFormElement;

    load_broadcasters();
}

function load_broadcasters() {
    bc_list.innerHTML = "";

    var ids = configuration.broadcaster_ids.split(",");

    for (var id of ids) {
        query_and_append(id);
    }
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
        
        create_toast('success', "Broadcaster", `Successfully updated broadcaster details for @${editing_broadcaster.handle}`);
        modal.remove();
        load_broadcasters();
    });

    var cancel_btn = update_form.querySelector(".cancel-update");

    cancel_btn.addEventListener('click', async() => {
        modal.remove();
    });

    pfp.addEventListener('click', () => show_picture_modal("pfp"));
    banner_img.addEventListener('click', () => show_picture_modal("banner"));
}

function show_picture_modal(type: string) {
    if (type === "pfp") {
        picture_upload_modal(
            editing_broadcaster.profile, 1,
            'Profile Picture',
            'Upload a profile picture',

            (image: string) => {
                pfp.src = image;

                editing_broadcaster.profile = image;
                editing_broadcaster.profile_updated = true;

                return true;
            }
        );
    } else if (type === "banner") {
        picture_upload_modal(
            editing_broadcaster.banner, 21 / 7,
            'Profile Banner',
            'Upload a profile banner',
            (image: string) => {
                banner_img.style.backgroundImage = `url(${image})`;
                
                editing_broadcaster.banner = image;
                editing_broadcaster.banner_updated = true;

                return true;
            }
        )
    }
}

async function query_and_append(id: string) {
    const response = await get_broadcaster_details(id);

    // -- Check if the request was successful
    if (response.code !== 200)
        return create_toast('error', 'Oops!', response.message)

    const data = (response as GetBroadcasterDetailsSuccess).data

    console.log(data);

    append(data.details);
}

function append(broadcaster: BroadcasterDetails) {
    var bc_elem = bc_html(broadcaster);

    bc_list.appendChild(bc_elem);
    
    bc_elem.querySelector(".broadcaster-edit-btn").addEventListener('click', function() {
        edit(broadcaster);
    });
}

function edit(broadcaster: BroadcasterDetails) {
    editing_broadcaster = broadcaster;

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

function bc_html(details: BroadcasterDetails) : HTMLElement {
    var row = document.createElement('div');
    row.className = "broadcaster-entry flex-column";
    row.setAttribute("data-broadcaster-id", details.id);

    row.innerHTML = `
        <div>
            <a href="#" class="h4">@${details.handle}</a>
            <p>${details.biography}</p>
        </div>
        <div class="">
            <div class="broadcaster-edit-btn btn btn-success" data-broadcaster-id="${details.id}">Edit</div>        
        </div>
    `

    return row;
}