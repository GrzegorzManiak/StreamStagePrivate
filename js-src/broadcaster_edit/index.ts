import { Type, build_configuration } from "../api/config";
import { manage_broadcaster_list } from "./panel";
import { Config } from "./index.d"
import { single } from "../common/single";
import { attach_event_listeners } from "./core/panels";
import { manage_contrib_panel } from "./contrib";

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

var contrib_panel = document.querySelector("#contribution-panel") as HTMLElement
if (contrib_panel)
    manage_contrib_panel(contrib_panel);

attach_event_listeners();