import { Type, build_configuration } from "../api/config";
import { manage_broadcaster_list } from "./panel";
import { Config } from "./index.d"
import { single } from "../common/single";
import { attach_event_listeners } from "./core/panels";

single("broadcaster_edit");

export const configuration = build_configuration<Config>({
    csrf_token: new Type('data-csrf-token', 'string'),

    update_broadcaster_details: new Type('data-update-broadcaster-details', 'string'),
    get_broadcaster_details: new Type('data-get-broadcaster-details', 'string'),
    broadcaster_ids: new Type('data-broadcasters', 'string'),

    fetch_invites: new Type('data-fetch-invites', 'string'),
    send_invite: new Type('data-send-invite', 'string'),
    respond_invite: new Type('data-respond-invite', 'string')
});

var broadcaster_list = document.querySelector("#broadcaster-list") as HTMLElement;
if (broadcaster_list)
    manage_broadcaster_list(broadcaster_list);

attach_event_listeners();