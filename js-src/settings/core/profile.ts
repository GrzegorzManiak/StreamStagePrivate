import { configuration } from '..';
import { attach, construct_modal, create_toast } from '../../common';
import { update_profile } from '../apis';
import { Pod } from '../index.d';
import Cropper from 'cropperjs';


/**
 * @param pod: Pod - The pod that this panel is attached to
 * 
 * @returns void
 * 
 * @description This function manages the profile panel
 */
export function manage_profile_panel(pod: Pod) {
    // -- Get the panel
    const panel = pod.panel.element;

    // -- Get the inputs
    const username = panel.querySelector('#username') as HTMLInputElement,
        fname = panel.querySelector('#fname') as HTMLInputElement,
        lname = panel.querySelector('#lname') as HTMLInputElement,
        bio = panel.querySelector('#bio') as HTMLInputElement,
        pfp = panel.querySelector('.profile-picture') as HTMLInputElement,
        timezone = panel.querySelector('#timezone') as HTMLSelectElement,
        country = panel.querySelector('#country') as HTMLSelectElement;

    const save_button = panel.querySelector('#save-btn') as HTMLButtonElement;


    pfp.addEventListener('click', () => {
        // -- Template
        const template = `
            <div class="w-100 d-flex justify-content-center gap-2">
                <!-- Rotate +90 -->
                <button 
                    id="rotate-right"
                    class="button-slim w-100 btn btn-primary info loader-btn"
                    loader-state='default'>   
                    <p><i class="fa-solid fa-rotate-right"></i></p>
                </button>

                <!-- Input -->
                <input 
                    name="rotate-input"
                    id="rotate-input" 
                    placeholder="0" 
                    value="0"
                class="form-control inp text-center">

                <!-- Rotate -90 -->
                <button 
                    id="rotate-left"
                    class="button-slim w-100 btn btn-primary info loader-btn"
                    loader-state='default'>   
                    <p><i class="fa-solid fa-rotate-left"></i></p>
                </button>
            </div>

            <div class="w-100 d-flex justify-content-center gap-2 mb-2 mt-2">
                <img 
                    class="modal-body img-upload rounded"
                    src="${configuration.profile_picture}"
                    alt="Profile Picture"
                >
            </div>

            <!-- Other buttons -->
            <div class="w-100 d-flex justify-content-center gap-3 mb-3">

                <div class="w-100 d-flex justify-content-center button-group">
                    <!-- Drag mode Crop -->
                    <button 
                        id="drag-mode-crop"
                        class="button-slim w-100 btn btn-primary info loader-btn"
                        loader-state='default'>   
                        <p><i class="fa-solid fa-crop"></i></p>
                    </button>

                    <!-- Drag mode Move -->
                    <button
                        id="drag-mode-move"
                        class="button-slim w-100 btn btn-primary info loader-btn"
                        loader-state='default'>
                        <p><i class="fa-solid fa-up-down-left-right"></i></p>
                    </button>
                </div>


                <div class="w-50 d-flex justify-content-center button-group">
                    <!-- Reset -->
                    <button 
                        id="reset"
                        class="button-slim w-100 btn btn-warning warning loader-btn"
                        loader-state='default'>   
                        <p><i class="fa-solid fa-rotate"></i></p>
                    </button>

                    <!-- Clear -->
                    <button 
                        id="clear"
                        class="button-slim w-100 btn btn-warning warning loader-btn"
                        loader-state='default'>   
                        <p><i class="fa-solid fa-expand"></i></p>
                    </button>
                </div>


                <div class="w-100 d-flex justify-content-center button-group">
                    <!-- Flip Horizontal -->
                    <button 
                        id="flip-horizontal"
                        class="button-slim w-100 btn btn-primary info loader-btn"
                        loader-state='default'>   
                        <p><i class="fa-solid fa-arrows-left-right"></i></p>
                    </button>

                    <!-- Flip Vertical -->
                    <button
                        id="flip-vertical"
                        class="button-slim w-100 btn btn-primary info loader-btn"
                        loader-state='default'>
                        <p><i class="fa-solid fa-arrows-up-down"></i></p>
                    </button>
                </div>

            </div>


            <div class="w-100 d-flex justify-content-center button-group">
                <!-- Save -->
                <button 
                    id="save"
                    class="button-slim w-100 btn btn-success success loader-btn"
                    loader-state='default'>   
                    <p><i class="fa-solid fa-save"></i></p>
                </button>

                <!-- Upload -->
                <button
                    id="upload"
                    class="button-slim w-100 btn btn-primary info loader-btn"
                    loader-state='default'>
                    <p><i class="fa-solid fa-upload"></i></p>
                </button>

                <!-- Cancel -->
                <button
                    id="cancel"
                    class="button-slim w-100 btn btn-danger error loader-btn"
                    loader-state='default'>
                    <p><i class="fa-solid fa-times"></i></p>
                </button>
            </div>
        `;

        // -- Create Modal
        const modal = construct_modal(
            'Profile Picture',
            'Update or Upload a new profile picture',
            false,
            'success',
            template
        );

        const modal_elm = document.createElement('div');
        modal_elm.innerHTML = modal;
        document.body.appendChild(modal_elm);

        // -- Get the modal
        const modal_body = modal_elm.querySelector('.img-upload') as HTMLImageElement,
            upload_button = modal_elm.querySelector('#upload') as HTMLButtonElement,
            save_button = modal_elm.querySelector('#save') as HTMLButtonElement,
            cancel_button = modal_elm.querySelector('#cancel') as HTMLButtonElement,
            reset_button = modal_elm.querySelector('#reset') as HTMLButtonElement,
            clear_button = modal_elm.querySelector('#clear') as HTMLButtonElement,
            drag_mode_crop_button = modal_elm.querySelector('#drag-mode-crop') as HTMLButtonElement,
            drag_mode_move_button = modal_elm.querySelector('#drag-mode-move') as HTMLButtonElement,
            flip_horizontal_button = modal_elm.querySelector('#flip-horizontal') as HTMLButtonElement,
            flip_vertical_button = modal_elm.querySelector('#flip-vertical') as HTMLButtonElement,
            rotate_right_button = modal_elm.querySelector('#rotate-right') as HTMLButtonElement,
            rotate_left_button = modal_elm.querySelector('#rotate-left') as HTMLButtonElement,
            rotate_input = modal_elm.querySelector('#rotate-input') as HTMLInputElement;
        
        // -- Create the cropper
        const cropper = new Cropper(modal_body, {
            aspectRatio: 1 / 1,
            viewMode: 1,
            responsive: true,
            restore: true,
            guides: true,
            center: true,
            highlight: true,
            background: true,
            movable: true,
            rotatable: true,
            scalable: true,
            zoomable: true,
            zoomOnWheel: true,
            zoomOnTouch: true,
            wheelZoomRatio: 0.1,
            cropBoxMovable: true,
            cropBoxResizable: true,
            toggleDragModeOnDblclick: true,
        });


        // -- Add the event listeners
        reset_button.addEventListener('click', () => cropper.reset());
        clear_button.addEventListener('click', () => cropper.clear());
        drag_mode_crop_button.addEventListener('click', () => cropper.setDragMode('crop'));
        drag_mode_move_button.addEventListener('click', () => cropper.setDragMode('move'));
        flip_horizontal_button.addEventListener('click', () => cropper.scaleX(cropper.getData().scaleX * -1));
        flip_vertical_button.addEventListener('click', () => cropper.scaleY(cropper.getData().scaleY * -1));


        rotate_right_button.addEventListener('click', () => {
            cropper.rotate(90);
            rotate_input.value = cropper.getData().rotate.toString();
        });
        rotate_left_button.addEventListener('click', () => {
            cropper.rotate(-90);
            rotate_input.value = cropper.getData().rotate.toString();
        });
        rotate_input.addEventListener('change', () => {
            const value = parseInt(rotate_input.value, 10) || 0;
            cropper.rotateTo(value);
        });


        // -- Add the event listener to the upload button
        upload_button.addEventListener('click', async() => {
            const stop_spinner = attach(upload_button),
                input = document.createElement('input');

            input.type = 'file';
            input.accept = 'image/*';
            input.click();

            input.addEventListener('change', async() => {
                const file = input.files[0];

                // -- Check if the file is an image
                if (!file.type.startsWith('image/')) {
                    create_toast('error', 'Oops!', 'The file you selected is not an image');
                    return stop_spinner();
                }

                // -- Check if the file is too large
                console.log(file.size);
                // if (file.size > 1000000) {
                //     create_toast('error', 'Oops!', 'The file you selected is too large');
                //     return stop_spinner();
                // }

                // -- Set the image
                stop_spinner();
                const url = URL.createObjectURL(file);
                cropper.replace(url);
            });

            stop_spinner();
        });
    });


    // -- Add the event listener to the save button
    save_button.addEventListener('click', async() => {
        const stop_spinner = attach(save_button);

        // -- Get the values
        const data = {
            username: username.value.trim(),
            description: bio.value.trim(),
            first_name: fname.value.trim(),
            last_name: lname.value.trim(),
            time_zone: timezone.value.trim(),
            country: country.value.trim(),
        }

        // -- Send the request
        const res = await update_profile(data);

        // -- Check if the request was successful
        if (res.code !== 200) create_toast('error', 'Oops!', res.message);
        else create_toast('success', 'Success!', res.message);
        return stop_spinner();
    });
}
