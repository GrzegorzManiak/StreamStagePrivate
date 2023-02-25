import { ServiceProvider } from '../index.d';
import { attach } from '../../click_handler';

export default (
    data: ServiceProvider,
    remove_callback: (success: boolean, message: string) => void
): HTMLDivElement => {
    // GOOGLE = 0, DISCORD = 1, GITHUB = 2
    let oauth_name = 'Unknown';
    switch (data.oauth_type.toString()) {
        case '0': oauth_name = 'Google'; break;
        case '1': oauth_name = 'Discord'; break;
        case '2': oauth_name = 'Github'; break;
    }

    const added = data.added.split('T'),
        added_date = added[0],
        added_time = added[1].split('.')[0];

    const last_used = data.last_used.split('T'),
        last_used_date = last_used[0],
        last_used_time = last_used[1].split('.')[0];


    const elm = `
        <div class="w-100 p-2 mb-2 rounded" style="background-color: var(--theme-color);">
            <div class="w-100 container d-flex justify-content-between align-items-center mb-1">
                <!-- Provider name -->
                <h5 class="fw-bold col-3 m-0">${oauth_name}</h5>
                
                <!-- Provider Oauth ID -->
                <p class="col-6 m-0">${data.id}</p>

                <!-- Remove button -->
                <button
                    type="submit"
                    id="remove-tfa"
                    class="btn btn-danger btn-sm loader-btn col-3"
                    loader-state="default"
                > Remove </button>

            </div>

            <div class="w-100 container d-flex justify-content-between align-items-center">
                <!-- Date added -->
                <p class="text-muted col-6 m-0">Added: ${added_date} at ${added_time}</p>

                <!-- Last used -->
                <p class="text-muted col-6 m-0">Last used: ${last_used_date} at ${last_used_time}</p>
            </div>

        </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = elm;

    // -- Get the remove button
    const btn = div.querySelector('button') as HTMLButtonElement;

    // -- Add the event listener
    btn.addEventListener('click', async () => {
        // -- Attach the spinner
        const stop = attach(btn);

        // TODO: RIGHt now just wait for 2 seconds
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // -- Remove this element
        div.remove();

        // -- Stop the spinner
        stop();
    });

    // -- Return the element
    return div;
};