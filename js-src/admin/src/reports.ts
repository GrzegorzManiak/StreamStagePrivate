import { GetFilteredReportsSuccess, Pod, Report, ReportSorts } from '../index.d';
import { manage_search_panel } from '../../common/search';
import { filter_reports, solve_report } from '../api';
import { construct_modal, create_toast } from '../../common';

export async function manage_reports_panel(pod: Pod) {
    const panel = pod.panel.element,
        md = panel.querySelector('#privacy-md') as HTMLTextAreaElement,
        name = panel.querySelector('#privacy-name') as HTMLInputElement,
        create = panel.querySelector('#privacy-create') as HTMLButtonElement;

    const update = manage_search_panel<ReportSorts, Report>(
        panel, (data, parent, refresh) => create_terms_report_elm(refresh, parent, data),
        async(page, sorts, order, search) => {
            const res = await filter_reports(page, sorts, order, search
            ) as GetFilteredReportsSuccess;

            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return;
            }

            return {
                data: res.data.reports,
                message: res.message,
                code: res.code,
                page: res.data.page,
                pages: res.data.pages,
            }
        },
    );
}


function create_terms_report_elm(refresh: () => void, parent: HTMLElement, data: Report) {
    const template = `
    <div class='profile-info cat-info p-2'>
        <p class='m-0 text-muted'><span class='bold'> Solved:</span> ${data.solved}</p>
        <p class='m-0 text-muted'><span class='bold'> R:</span> ${data.reporter.username}</p>
        <p class='m-0 text-muted'><span class='bold'> T:</span> ${data.reported.user.username}</p>
    </div>

    <div class='profile-info cat-info p-2'>
        <p class='m-0 text-muted'><span class='bold'> Created:</span> ${data.created.split('T')[0]}</p>
        <p class='m-0 text-muted'><span class='bold'> Updated:</span> ${data.updated.split('T')[0]}</p>
    </div>

    <div class='profile-actions p-2'>
        <button class="w-100 h-100 btn btn-primary info loader-btn edit" loader-state="default">   
            <span> <div class="spinner-border" role="status"> 
            <span class="visually-hidden">Loading...</span> </div> </span>
            <p>View</p>
        </button>
    </div>
    `;

    const elm = document.createElement('div');
    elm.classList.add('d-flex', 'justify-content-between', 'align-items-center', 'gap-2', 'category', 'cat-container');
    elm.innerHTML = template;
    parent.appendChild(elm);

    const view = elm.querySelector('.edit') as HTMLButtonElement;
    view.addEventListener('click', async() => {

        const modal_template = `
        <div class="w-100 d-flex justify-content-center flex-column align-items-center">
            <a href="${data.reported.user.url}" class="w-100 text-muted">View reportee</a>
            <a href="${data.reporter.url}" class="w-100 text-muted">View reporter</a>

            <div class="mb-2">
                <label class="form-label" for="report">Report reason</label>
                <textarea 
                    name="report" 
                    id="report" 
                    cols="40" rows="5"
                    placeholder="You dont."
                    disabled
                    class="form-control inp fc-dark">${data.reason}</textarea>
            </div>
        </div>


        <div class='w-100 d-flex btn-group'>
            <!--Create Button-->
            <button type="submit" id="solved"
                class="btn btn-lg btn-success success w-100 loader-btn" loader-state='default'>
                <span> <div class='spinner-border' role='status'> 
                <span class='visually-hidden'>Loading...</span> </div> </span>
                <p>Solved</p>
            </button>

            <!--Cancel Button-->
            <button type="submit" id="close"
                class="btn btn-lg btn-warn warning w-100 loader-btn" loader-state='default'>
                <p>Close</p>
            </button>
        </div>
        `;

        // -- Create the element
        const div = construct_modal(
            'Manage report',
            'Manage the report, and mark it as solved or unsolved.',
            false, 'success',
            modal_template
        );
        document.body.appendChild(div);

        const solved = div.querySelector('#solved') as HTMLButtonElement,
            close = div.querySelector('#close') as HTMLButtonElement;

        // -- If the report is solved
        if (data.solved) solved.disabled = true;

        // -- Cancel button
        close.addEventListener('click', () => div.remove());

        // -- Solved button
        solved.addEventListener('click', async() => {
            const res = await solve_report(data.id);
            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return;
            }

            create_toast('success', 'Success', res.message);
            div.remove();
            refresh();
        });
    });
}


