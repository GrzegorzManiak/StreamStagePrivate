import { BroadcasterDetails, GetInvitationsResponse, GetInvitationsSuccess, Invite } from "./index.d";
import { construct_modal, create_toast } from "../common";
import { fetch_invites, respond_invite, send_invite } from "./api";

let invite_list:HTMLElement;

export function manage_contrib_panel(invite_panel: HTMLElement) {
    invite_list = invite_panel.querySelector("#invite_list");

    var no_invite_notice = invite_panel.querySelector("#no-invites-notice") as HTMLElement;
    var text_your_invites = invite_panel.parentElement.querySelector("#text-your-invites") as HTMLElement;

    get_invites(no_invite_notice, text_your_invites);

}


export function show_contrib(broadcaster: BroadcasterDetails) {
    const modal_wrap = construct_modal(
        "Broadcaster Contributors",
        "Manage contributors to your broadcaster.", 
        false,
        'success',
        contrib_modal(broadcaster)
    );

    // -- Get the buttons
    const invite_btn = modal_wrap.querySelector('#invite-member-btn') as HTMLButtonElement;
    // -- Get the buttons
    const close_btn = modal_wrap.querySelector('#close-modal') as HTMLButtonElement;

    close_btn.addEventListener('click', async() => {
        // -- Call the no function
        //no();

        // -- Remove the modal
        modal_wrap.remove();
    });
    invite_btn.addEventListener('click', async() => {
       show_invite_modal(broadcaster.id);
    });

    // -- Append the modal to the body
    document.body.appendChild(modal_wrap);
    (modal_wrap.querySelector('.modal-content') as HTMLElement).setAttribute("style",  "width:45rem!important");
}

function show_invite_modal(broadcaster_id: string) {
    const modal_wrap = construct_modal(
        "Invite", 
        "Invite a user to contribute on your broadcaster.", 
        false,
        'success', 
        invite_template()
    );

    // -- Get the buttons
    const invite_btn = modal_wrap.querySelector('#invite-member-btn') as HTMLButtonElement;
    // -- Get the buttons
    const close_btn = modal_wrap.querySelector('#close-modal') as HTMLButtonElement;

    const username_field = modal_wrap.querySelector('#id_name') as HTMLInputElement;
    const message_field = modal_wrap.querySelector('#id_message') as HTMLInputElement;

    close_btn.addEventListener('click', async() => {
        // -- Call the no function
        //no();

        // -- Remove the modal
        modal_wrap.remove();
    });
    invite_btn.addEventListener('click', async() => {
        // send

        var response = await send_invite(broadcaster_id, username_field.value, message_field.value);

        // -- Check if the request was successful
        if (response.code !== 200)
            return create_toast(
                'error', 'Oops!',
                response.message
        )

        create_toast('success', 'Contribution', 'Sent invitation to contribute.')
    });


    // -- Append the modal to the body
    document.body.appendChild(modal_wrap);
    (modal_wrap.querySelector('.modal-content') as HTMLElement).setAttribute("style",  "width:30rem!important");
}

function invite_template() {
    return `
    <form>
        <div class="mb-3">
            <h1>Username:</h1>
        </div>
        <div>
            <div class="mb-3">
                <label for="id_name" class="form-label requiredField">Username<span class="asteriskField">*</span> </label>
                <input type="text" name="name" maxlength="32" class="textinput textInput form-control" required="" id="id_name">
            </div>
            <div class="mb-3">
                <label for="id_message" class="form-label requiredField">Message (optional)<span class="asteriskField">*</span> </label>
                <textarea name="message" cols="40" rows="10" maxlength="512" class="textarea form-control" required="" id="id_message"></textarea>
            </div>
    </div>
        <span id="invite-member-btn" class="btn success">Send Inv ite</span>
        <span id="close-modal" class="btn info">Cancel</span>
    </form>`;
}

function contrib_modal(broadcaster: BroadcasterDetails) {
    var contributors  = ``;

    console.log(broadcaster);
    for (var contributor of broadcaster.contributors) {
        contributors += `
        <div class="row">
            <div class='col-3'>
                <img src='${contributor.profile}' />
            </div>
            <div class='col-6'>
                <a class='h3 m-0' href="${contributor.url}">${contributor.username}</a>
            </div>
            <div class='col-2'>
                <button data-user="${contributor.username}" class="btn error remove-contributor">
                    <p>Remove</p>
                </button>
            </div>
            </div>
        `;
    }

    return `
        <form>
            <div class="mb-3">
                <h1>Contributors:</h1>
            </div>
            <div id="bc-contributors">
            ${contributors}
            </div>
            <span id="invite-member-btn" class="btn success">Invite Member</span>
            <span id="close-modal" class="btn info">Close</span>
        </form>
    `;
}


async function get_invites(no_invite_notice: HTMLElement, text_your_invites:HTMLElement) {
    const response = await fetch_invites();

    // -- Check if the request was successful
    if (response.code !== 200)
        return create_toast('error', 'Oops!', response.message)

    var invites = (response as GetInvitationsSuccess).data.invites

    populate_invite_list(invites);

    console.log(text_your_invites);
    if (invites.length == 0) {
        no_invite_notice.setAttribute("style", "display:inherit;");
        text_your_invites.setAttribute("style", "display:none;");
    }
}

function populate_invite_list(invites: Invite[]) {
    invite_list.innerHTML = "";

    for (var invite of invites) {
        append(invite);
    }
}

function append(invite: Invite) {
    var elem = invite_html(invite);

    invite_list.appendChild(elem);
    
    elem.querySelector(".accept-invite").addEventListener('click', async function() {
        if (await respond(invite, "y")){
            create_toast('success', 'Invite', "Accepted invitation!")
            elem.remove();
        }
    });
    elem.querySelector(".decline-invite").addEventListener('click', async function() {
        if (await respond(invite, "n")){
            create_toast('success', 'Invite', "Declined invitation.")
            elem.remove();
        }
    });
}

async function respond(invite: Invite, state:"y"|"n") : Promise<boolean> {
    const response = await respond_invite(invite.id, state);

    // -- Check if the request was successful
    if (response.code !== 200){
        create_toast('error', 'Oops!', response.message)
        return false;
    }

    return true;
}

function invite_html(invite: Invite) : HTMLElement {
    var row = document.createElement('div');
    row.className = "contrib-invite row";
    row.setAttribute("data-invite-id", invite.id);

    // row.setAttribute("style", "background-image: url('" + details.banner + "'); background-");
    
    // row.style.backgroundImage = details.banner;

    // var approval_html = "";

    // if (!details.approved) {
    //     approval_html = `<div class="float-end text-danger">Awaiting Approval</div>`
    // }

    row.innerHTML = `
        <div class="col-5">
            <div class='profile-info'>
                <img alt="Profile Picture" class="profile-picture-edit" src="${invite.bc_profile}">
                <a href="${invite.bc_url}" class='h3'>@${invite.broadcaster}</a>
            </div>
        </div>
        <div class="col-7 d-flex flex-column">
            <div>    
                <p>Invited by ${invite.inviter}.</p>

                <b>Message:</b>
                <p class='text-muted' style="max-width: 50%;">
                    ${invite.message}
                </p>
            </div>

            <div class="align-self-end mt-auto">
                <div class="decline-invite btn error">
                    Decline
                </div>
                <div class="accept-invite btn success">
                    Accept
                </div>
            </div>
        </div>
    `

    return row;
}