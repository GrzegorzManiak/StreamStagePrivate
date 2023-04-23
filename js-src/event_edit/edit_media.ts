import { construct_modal, create_toast } from "../common";
import { get_evt_media, add_evt_media, del_evt_media } from "./apis";
import { GetMediaSuccess, AddMediaSuccess, Media } from "./index.d"
import { configuration } from "./index"
import { picture_upload_modal } from "../common/picture";

let media_panel;

export function handle_media_panel(panel: HTMLElement) {
    media_panel = panel;

    var add_media_btn = document.querySelector('#add-media-btn') as HTMLElement;

    if (add_media_btn)
        manage_add_media_btn(add_media_btn);
        
    query_media();
}

function manage_add_media_btn(
    btn: HTMLElement
) {
    btn.addEventListener('click', () => picture_upload_modal(
        null, 1,
        'Event Image',
        'Upload an image for your event',
        async (image: string) => {
            var description = (document.querySelector("#id_media_description") as HTMLInputElement).value

            const res = await add_evt_media(configuration.event_id, image, description);

            if (res.code !== 200) {
                create_toast('error', 'Oops!', res.message);
                return false;
            } else {
                create_toast('success', 'Success!', res.message);
                
                var data = (res as AddMediaSuccess).data

                append_media(data.media)

                return true;
            }
        },
        media_description_input
    ));
}

// // Functions managing physical list of media

function set_media(evt_media: Media[]) {
    media_panel.innerHTML = "";
    
    for (var media of evt_media) {
        append_media(media);
    }
}

function remove_media(mid: string) {
    media_panel.querySelector(".media-elem[data-mid=\"" + mid + "\"]").remove();
}

function append_media(media: Media) {
    media_panel.appendChild(media_html(media));

    media_panel.querySelector(`.remove-media-btn[data-mid="${media.media_id}"]`)
            .addEventListener("click", () => del_media(media.media_id));
}

// // API calls

async function query_media() {
    const listings = await get_evt_media(configuration.event_id);

    // -- Check if the request was successful
    if (listings.code !== 200)
        return create_toast(
            'error', 'Oops!',
            'There was an error while trying to get event media, please try again later.'
        )

    const data = (listings as GetMediaSuccess).data

    console.log(data);
        
    set_media(data.media);
}

async function del_media(mid: string) {
    const request = await del_evt_media(configuration.event_id, mid);

    // -- Check if the request was successful
    if (request.code !== 200)
        return create_toast(
            'error', 'Oops!',
            'There was an error while trying to remove event media, please try again later.'
        )

    remove_media(mid);

    create_toast(
        'success', 'Event',
        'Removed event media.'
    )
}


// // HTML generation

function media_html(
    media: Media
) : HTMLElement {
    var sq = document.createElement('div');
    sq.className = "m-2 media-elem";
    sq.setAttribute("data-mid", media.media_id);

    sq.innerHTML = `
        <div class="col-6">
            <img class="event-cover " src="${media.picture}"></div>
            <span>${media.description}</span>
        </div>
        <div class="remove-media-btn btn btn-danger" data-mid="${media.media_id}">
            Remove Media
        </div>
    `

    return sq;
}

const media_description_input = `
    <div class="mb-3">
        <label for="id_media_description" class="form-label requiredField">Description</label>
        <input name="description" maxlength="300" class="textarea form-control" required="" id="id_media_description" placeholder="Cool photograph!"></input>
    </div>
`;