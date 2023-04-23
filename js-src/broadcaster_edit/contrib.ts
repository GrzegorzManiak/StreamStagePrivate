import { GetInvitationsResponse, GetInvitationsSuccess, Invite } from "./index.d";
import { create_toast } from "../common";
import { fetch_invites, respond_invite } from "./api";

let invite_list:HTMLElement;

export function manage_contrib_panel(invite_panel: HTMLElement) {
    invite_list = invite_panel.querySelector("#invite_list");

    var no_invite_notice = invite_panel.querySelector("#no-invites-notice") as HTMLElement;
    var text_your_invites = invite_panel.parentElement.querySelector("#text-your-invites") as HTMLElement;

    get_invites(no_invite_notice, text_your_invites);
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