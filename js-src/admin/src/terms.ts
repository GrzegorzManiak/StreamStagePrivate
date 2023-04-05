import { configuration } from '..';
import { confirmation_modal, create_toast } from '../../common';
import { manage_search_panel } from '../../common/search';
import { create_privacy, create_terms, filter_terms } from '../api';
import { FilterdTermsSuccess, Pod, Privacy, Terms, TermsPrivacySorts } from '../index.d';

export async function manage_terms_panel(pod: Pod) {
    const panel = pod.panel.element,
        md = panel.querySelector('#terms-md') as HTMLTextAreaElement,
        name = panel.querySelector('#terms-name') as HTMLInputElement,
        create = panel.querySelector('#terms-create') as HTMLButtonElement;

    const update = manage_search_panel<TermsPrivacySorts, Terms>(
        panel, (data, parent, refresh) => create_terms_privacy_elm(refresh, parent, data),
        async(page, sorts, order, search) => {
            const res = await filter_terms(page, sorts, order, search
            ) as FilterdTermsSuccess;

            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return;
            }

            return {
                data: res.data.terms,
                message: res.message,
                code: res.code,
                page: res.data.page,
                pages: res.data.pages,
            }
        },
    );

    create.addEventListener('click', async() => {
        await create_terms_privacy(update, name, md);
    });
}



/**
 * @name create_terms_privacy_elm
 * @param {() => void} refresh
 * @param {HTMLElement} parent
 * @param {Privacy | Terms} data,
 * @param {'terms' | 'privacy'} mode
 */
export function create_terms_privacy_elm(
    refresh_categories: () => void,
    parent: HTMLElement, 
    data: Privacy | Terms,
    mode: 'terms' | 'privacy' = 'terms'
) {
    const template = `        
    <div class='profile-info cat-info p-2'>
        <p class='m-0 text-muted'><span class='bold'> Name:</span> ${data.name}</p>
    </div>

    <div class='profile-info cat-info p-2'>
        <p class='m-0 text-muted'><span class='bold'> Created:</span> ${data.created}</p>
    </div>

    <div class='profile-actions p-2'>
        <button class="w-100 h-100 btn btn-primary info loader-btn edit" loader-state="default">   
            <span> <div class="spinner-border" role="status"> 
            <span class="visually-hidden">Loading...</span> </div> </span>
            <p>View</p>
        </button>
    </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = template;
    div.classList.add('d-flex', 'justify-content-between', 'align-items-center', 'gap-2', 'category', 'cat-container');
    parent.appendChild(div);

    const edit = div.querySelector('.edit') as HTMLButtonElement;
    edit.addEventListener('click', async() => {
        switch (mode) {
            case 'terms': 
                // -- Open a new tab with the terms
                window.open(configuration.render_terms + '?id=' + data.id, '_blank');
                break;

            case 'privacy':
                // -- Open a new tab with the privacy
                window.open(configuration.render_privacy + '?id=' + data.id, '_blank');
                break;
        }
    });
}



/**
 * @name create_terms_privacy
 * @param {() => void} refresh
 * @param {Element} parent
 * @param {HTMLInputElement} name
 * @param {HTMLTextAreaElement} md
 * @param {HTMLButtonElement} create
 */
export async function create_terms_privacy(
    refresh: Function,
    name: HTMLInputElement,
    md: HTMLTextAreaElement,
    mode: 'terms' | 'privacy' = 'terms'
) {
    // -- Make sure the name and md are not empty
    if (!name.value) return create_toast('error', 'Error', 'Please enter a name for the ' + mode + '.');
    if (!md.value) return create_toast('error', 'Error', 'Please enter some ' + mode + ' content.');

    confirmation_modal(
        async() => {
            let res;
            switch (mode) {        
                case 'terms': res = await create_terms(
                    name.value,
                    md.value
                ); break;
        
                case 'privacy': res = await create_privacy(
                    name.value,
                    md.value
                ); break;
            }
        
            if (!res || res.code !== 200) 
                return create_toast('error', 'Oops! My bad', res.message);
        
            create_toast('success', 'Success', res.message);
            refresh();
        },
        () => {},
        'Are you sure you want to create this ' + mode + '?, It set this ' + mode + ' as the active ' + mode + ' for the site.',
        'Create ' + mode,
    );
}