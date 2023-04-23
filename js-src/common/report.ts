import { attach, construct_modal, create_toast } from '.';
import { submit_report } from './api';
import { report_type } from './index.d';

/**
 * @name report
 * @param {report_type} type - Type of report
 * @param {string} r_id - Id of the object that is being reported
 * @description Creates and submits a report to the server
 * @returns void
 */
export const report = (
    type: report_type,
    r_id: string,
) => {
    const template = `
        <div class="form-group mb-3">
            <textarea 
                class="form-control form-control-lg inp" 
                id="report-reason"
                rows="5"
                placeholder="This user is being rude... he said 'I hate you' :("
            ></textarea>
        </div>
    `;

    // -- Add the element to the body
    const div = construct_modal(
        'Report',
        'Why do you want to report this?',
        true, 'primary', template
    );
    document.body.appendChild(div);

    // -- Submit the report
    const yes = div.querySelector('.yes') as HTMLButtonElement,
        no = div.querySelector('.no') as HTMLButtonElement;

    yes.addEventListener('click', async () => {
        const stop = attach(yes);

        // -- Get the reason
        const reason = (div.querySelector('#report-reason') as HTMLTextAreaElement).value,
            res = await submit_report(type, r_id, reason);

        // -- Check if we got an error
        if (res.code !== 200) {
            create_toast('error', 'Oops, there appears to be an error', res.message);
            return stop();
        }

        // -- Alert the user
        create_toast('success', 'Success', 'Your report has been submitted');
        stop();
        div.remove();
    });

    // -- Cancel the report
    no.addEventListener('click', () => div.remove());
}