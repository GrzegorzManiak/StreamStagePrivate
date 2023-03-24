import { attach, construct_modal, create_toast } from ".";
import Cropper from 'cropperjs';


/**
 * @name picture_upload_modal
 * @param {string} initial_image - The initial image to display
 * @param {number | undefined} aspect_ratio - The aspect ratio of the image, undefined if not required
 * @param {string} title - The title of the modal
 * @param {string} description - The description of the modal
 * @param {(image: string) => void} on_upload - The function to call when the image is uploaded (base64)
 * 
 * @returns void
 */
export function picture_upload_modal(
    initial_image: string,
    aspect_ratio: number | undefined = undefined,
    title: string = 'Upload Picture',
    description: string = 'Upload a new picture',
    on_upload: (image: string) => void,
) {
    const modal = construct_modal(
        title, description, false,
        'success', upload_template(initial_image)
    );

    // -- Add the modal to the body
    const modal_elm = document.createElement('div');
    modal_elm.innerHTML = modal;
    document.body.appendChild(modal_elm);

    
    // -- Get the modal elements
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
        aspectRatio: aspect_ratio,
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


    // -- Manage new image uploads 
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

            // -- Set the image
            stop_spinner();
            const url = URL.createObjectURL(file);
            cropper.replace(url);
        });

        stop_spinner();
    });



    // -- Close and save the modal
    save_button.addEventListener('click', () => {
        const stop_spinner = attach(save_button);
        on_upload(cropper.getCroppedCanvas().toDataURL());
        stop_spinner();
        modal_elm.remove();
    });
    cancel_button.addEventListener('click', () => modal_elm.remove());
}


// -- Template
const upload_template = (picture: string) => `
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
        src="${picture}"
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