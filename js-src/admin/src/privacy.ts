import { FilterdPrivacySuccess, Pod, Privacy, TermsPrivacySorts } from '../index.d';
import { manage_search_panel } from '../../common/search';
import { create_terms_privacy, create_terms_privacy_elm } from './terms';
import { filter_privacy } from '../api';
import { create_toast } from '../../common';

export async function manage_privacy_panel(pod: Pod) {
    const panel = pod.panel.element,
        md = panel.querySelector('#privacy-md') as HTMLTextAreaElement,
        name = panel.querySelector('#privacy-name') as HTMLInputElement,
        create = panel.querySelector('#privacy-create') as HTMLButtonElement;

    const update = manage_search_panel<TermsPrivacySorts, Privacy>(
        panel, (data, parent, refresh) => create_terms_privacy_elm(refresh, parent, data, 'privacy'),
        async(page, sorts, order, search) => {
            const res = await filter_privacy(page, sorts, order, search
            ) as FilterdPrivacySuccess;

            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return;
            }

            return {
                data: res.data.privacy,
                message: res.message,
                code: res.code,
                page: res.data.page,
                pages: res.data.pages,
            }
        },
    );

    create.addEventListener('click', async() => {
        await create_terms_privacy(update, name, md, 'privacy');
    });
}
