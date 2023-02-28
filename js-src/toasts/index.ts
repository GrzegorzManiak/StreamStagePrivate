import { sleep } from "../click_handler";

export type ToastType = 'error' | 'success' | 'warning' | 'info';



/**
 * @name create_toast
 * 
 * @param type: ToastType - The type of toast to create EG, error, success, warning
 * @param title: string - The title of the toast
 * @param message: string - The message of the toast
 * @param close_after: number - The amount of time to wait before closing the toast
 * @param closed: () => void - The function to call when the toast is closed
 * 
 * @returns void
 * 
 * @description This function creates a toast and appends it to the DOM
 *              it also handles the removal of the toast after x seconds.
 *              This function is used to show the user that something
 *              has happened.
 */
export const create_toast = (
    type: ToastType, 
    title: string, 
    message: string,
    close_after: number = 5000,
    closed: () => void = () => {},
) => {
    // -- Lets get the root toasts element
    const toasts = document.getElementById('toasts');
    if (!toasts) throw new Error('No toasts element found');

    const toast = `
        <div 
            toast-type='${type}'
            class='
                toast
                d-flex
                align-items-center
                justify-content-start
            '
        >
            <!-- Icon, pinned to the top -->
            <div class='toast-icon col-1'>
                <i class="fa-regular fa-circle-check" icon='success'></i>
                <i class="fa-solid fa-triangle-exclamation" icon='warning'></i>
                <i class="fa-solid fa-exclamation" icon='error'></i>
                <i class="fa-solid fa-circle-info" icon='info'></i>
            </div>

            <!-- Content -->
            <div class='toast-content col-9'>
                <p class='toast-content-header m-0'>${title}</p>
                <p class='toast-content-text m-0'>${message}</p>
                <p class='toast-content-time m-0'>Now</p>
            </div>

            <!-- Close button -->
            <div class='toast-close col-2'>
                <i class="fa-solid fa-times"></i>
            </div>
        </div>
    `;

    // -- Add the toast to the toasts element
    const new_toast = document.createElement('div');
    new_toast.innerHTML = toast;

    // -- Get the close button and time
    const close_button = new_toast.querySelector('.toast-close'),
            time = new_toast.querySelector('.toast-content-time') as HTMLParagraphElement;


    const time_created = new Date();

    // -- For the life of the toast, update the time
    const time_interval = setInterval(() => {
        time.innerText = moment(time_created);
    }, 1000);


    // -- Add the close button event listener
    close_button.addEventListener('click', () => {
        unanimate_toast(new_toast, toasts);
        clearInterval(time_interval);
        closed();
    });

    // -- Close the toast after x seconds
    setTimeout(() => {
        unanimate_toast(new_toast, toasts);
        clearInterval(time_interval);
        closed();
    }, close_after);

    // -- Add the toast to the toasts element
    toasts.appendChild(new_toast);
}



/**
 * @name unanimate_toast
 * 
 * @param toast: HTMLDivElement - The toast to animate
 * 
 * @returns void
 * 
 * @description This function animates the toast out
 *              and then removes it from the DOM
 */
async function unanimate_toast(
    toast: HTMLDivElement,
    toasts: HTMLElement,
) {
    // -- We want to animate its opacity 
    const animation_length = 1000;

    // -- Add the animation class
    toast.classList.add('toast-out');
    const child = toast.children[0] as HTMLDivElement,
        computed_style = getComputedStyle(child),
        margin = computed_style.getPropertyValue('margin-bottom');

    const toast_height = toast.offsetHeight + parseInt(margin);

    // -- Animate the rest of the toasts
    const toasts_children = toasts.children;
    const toast_index = Array.from(toasts_children).indexOf(toast);

    // -- Check if the child is animating
    if (toast.style.animation) {
        toast.style.animation = '';

    // -- Animate the rest of the toasts
    for (let i = 0; i < toasts_children.length; i++) {
        const child = toasts_children[i] as HTMLDivElement;
        if (i <= toast_index) continue;
        if (child.classList.contains('toast-out')) continue;

        // --toast-adjust-height
        child.style.setProperty('--toast-adjust-height', `-${toast_height}px`);
        child.style.animation = `toast_adjust ${animation_length}ms ease-in-out`;
    }

    // -- Sleep for the animation length
    await sleep(animation_length);
    toast.classList.remove('toast-out');

    
    for (let i = 0; i < toasts_children.length; i++) {
        const child = toasts_children[i] as HTMLDivElement;
        if (i <= toast_index) continue;
        child.style.animation = '';
    }


    // -- Remove the toast from the DOM
    toast.remove();
}



/**
 * @name moment
 * 
 * @param date: Date - The date to format
 *
 * @returns string - The formatted date
 * 
 * @description This function formats a date to a
 *              more human-readable format
 *              
 *              For example, if the date is 5 minutes ago,
 *              it will return '5 minutes ago'    
 */ 
export function moment(date: Date): string {
    // -- Get the time difference in milliseconds
    const diff = (Date.now() - date.getTime()) / 1000;
  
    // -- Define the thresholds for different time intervals
    const thresholds = [
        { threshold: 0, label: 'Just now' }, // -- 1 second
        { threshold: 60 * 1000, label: 'A few seconds ago' }, // -- 1 minute
        { threshold: 60 * 60 * 1000, label: 'A few minutes ago' }, // -- 1 hour
        // -- Im not using the below two thresholds, but i added them anyway
        //    As i MIGHT use them for something else later
        { threshold: 24 * 60 * 60 * 1000, label: 'A few hours ago' }, // -- 1 day
        { threshold: 7 * 24 * 60 * 60 * 1000, label: 'A few days ago' }, // -- 1 week
        { threshold: Infinity, label: 'A while ago' }, // -- 1 week
    ];
  
    // -- Find the first threshold that the time difference is less than or equal to
    const { label } = thresholds.find(({ threshold }) => diff <= threshold) || thresholds[thresholds.length - 1];
    return label;
}