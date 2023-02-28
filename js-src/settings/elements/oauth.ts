import { ServiceProvider } from '../index.d';
import { attach, confirmation_modal } from '../../click_handler';
import { create_toast } from '../../toasts';
import { remove_oauth } from '../apis';

export default (
    data: ServiceProvider,
    token: string,
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
        <div class="w-100 p-2 mb-2 rounded linked-account-continer" style="background-color: var(--theme-color);">
            <div class="w-100 container d-flex justify-content-between align-items-center mb-1">
                <!-- Provider name -->
                <h5 class="fw-bold col-3 m-0">${oauth_name}</h5>
                
                <!-- Provider Oauth ID -->
                <p class="col-6 m-0 oauth-id-top">${data.id}</p>

                <!-- Remove button -->
                <button
                    type="submit"
                    id="remove-tfa"
                    class="btn btn-danger btn-sm loader-btn col-3"
                    loader-state="default"
                > Remove </button>

            </div>

            <div class="oauth-id-bottom w-100 container d-flex justify-content-between align-items-center">
                <p class="text-muted m-0">${data.id}</p>
            </div>

            <div class="w-100 container d-flex justify-content-between align-items-center oauth-times">
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

        // -- Confirm the action
        confirmation_modal(
            async () => {
                // -- Remove the oauth
                const res = await remove_oauth(token, data.id);
                if (res.code !== 200) create_toast('error', "Failed to remove OAuth", res.message)

                else {
                    create_toast(
                        'success',
                        "OAuth removed",
                        "Successfully removed OAuth",
                    );
        
                    // -- Remove the element
                    div.remove();
                }
        
                // -- Stop the spinner
                stop();
            },
            () => stop(),
            'Are you sure you want to remove "' + oauth_name + '" from your linked accounts? This action cannot be undone.',
        )
    });

    // -- Return the element
    return div;
};

export async function attach_lister(la_elm: HTMLDivElement) {
    const oauth_providers = la_elm.querySelector('#oauth-providers') as HTMLSelectElement,
        add_tfa = la_elm.querySelector('#add-tfa') as HTMLButtonElement;

    add_tfa.addEventListener('click', async () => {
        // -- Get the selected provider
        const provider = oauth_providers.value,
            selected_elm = oauth_providers.querySelector(`option[value="${provider}"]`) as HTMLOptionElement;
        
        if (provider === 'Provider')
            return create_toast('warning', 'Oops', 'Please select a provider');

        // -- Open the oauth window
        const oauth_window = window.open(
            selected_elm.getAttribute('redirect-url'), '_blank', 
            'directories=no,titlebar=no,toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=no,width=600,height=700'
        );
        if (!oauth_window) return create_toast('error', 'Oops', 'There was an error opening the oauth window');
    });
}