import { Pod, FaqSorts, Faq, FilterdFaqsSuccess } from '../index.d';
import { manage_search_panel } from '../../common/search';
import { create_faq, delete_faq, filter_faq, update_faq } from '../api';
import { construct_modal, create_toast } from '../../common';

export async function manage_faq_panel(pod: Pod) {
    const panel = pod.panel.element,
        create = panel.querySelector('#faq-create') as HTMLButtonElement;

    const update = manage_search_panel<FaqSorts, Faq>(
        panel, (data, parent, refresh) => create_faq_elm(refresh, parent, data),
        async(page, sorts, order, search) => {
            const res = await filter_faq(page, sorts, order, search
            ) as FilterdFaqsSuccess;

            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return;
            }

            return {
                data: res.data.faq,
                message: res.message,
                code: res.code,
                page: res.data.page,
                pages: res.data.pages,
            }
        },
    );

    create.addEventListener('click', async() => {
        await manage_faq_modal(update);
    });
}



async function create_faq_elm(refresh: () => void, parent: HTMLElement, data: Faq) {
    const template = `
    <div class='profile-info cat-info p-2'>
        <p class='m-0 text-muted'><span class='bold'> Q:</span> ${data.question}</p>
        <p class='m-0 text-muted'><span class='bold'> S:</span> ${data.section}</p>
        <p class='m-0 text-muted'><span class='bold'> A:</span> ${data.answer}</p>
    </div>

    <div class='profile-info cat-info p-2'>
        <p class='m-0 text-muted'><span class='bold'> Created:</span> ${data.created.split('T')[0]}</p>
        <p class='m-0 text-muted'><span class='bold'> Updated:</span> ${data.updated.split('T')[0]}</p>
    </div>

    <div class='profile-actions p-2'>
        <button class="w-100 h-100 btn btn-primary info loader-btn edit" loader-state="default">   
            <span> <div class="spinner-border" role="status"> 
            <span class="visually-hidden">Loading...</span> </div> </span>
            <p>Edit</p>
        </button>
    </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = template;
    div.classList.add('d-flex', 'justify-content-between', 'align-items-center', 'gap-2', 'category', 'cat-container');
    parent.appendChild(div);

    const edit = div.querySelector('.edit') as HTMLButtonElement;
    edit.addEventListener('click', async() => {
        await manage_faq_modal(refresh, data);
    });
}




async function manage_faq_modal(
    refresh: Function,
    faq: Faq | null = null,
) {
    let answer_text = faq?.answer || '',
        question_text = faq?.question || '',
        section_text = faq?.section || '';

    const template = `
        <!-- Name and description -->
        <div class="w-100 d-flex justify-content-center flex-column align-items-center">
            <div class="mb-2 w-100">
                <label class="form-label" for="question">Question</label>
                <input 
                    name="question" 
                    id="question" 
                    placeholder="How do i?"
                    type="text"
                    value="${question_text}"
                    class="form-control inp w-100 fc-dark">
            </div>

            <div class="mb-2 w-100">
                <label class="form-label" for="section">Section</label>
                <input 
                    name="section" 
                    id="section" 
                    placeholder="General"
                    type="text"
                    value="${section_text}"
                    class="form-control inp w-100 fc-dark">
            </div>

            <div class="mb-2">
                <label class="form-label" for="answer">Answer</label>
                <textarea 
                    name="answer" 
                    id="answer" 
                    cols="40" rows="5"
                    placeholder="You dont."
                    class="form-control inp fc-dark">${answer_text}</textarea>
            </div>
        </div>

        <div class='w-100 d-flex btn-group'>
            <!--Create Button-->
            <button type="submit" id="create"
                class="btn btn-lg btn-success success w-100 loader-btn" loader-state='default'>
                <span> <div class='spinner-border' role='status'> 
                <span class='visually-hidden'>Loading...</span> </div> </span>
                <p>${faq === null ? 'Create' : 'Update'}</p>
            </button>

            ${faq === null ? '' : `
                <!--Delete Button-->
                <button type="submit" id="delete"
                    class="btn btn-lg btn-danger error w-100 loader-btn" loader-state='default'>
                    <span> <div class='spinner-border' role='status'>
                    <span class='visually-hidden'>Loading...</span> </div> </span>
                    <p>Delete</p>
                </button>
            `}

            <!--Cancel Button-->
            <button type="submit" id="cancel"
                class="btn btn-lg btn-warn warning w-100 loader-btn" loader-state='default'>
                <p>Cancel</p>
            </button>
        </div>

    `;

    // -- Create the element
    const div = document.createElement('div');
    document.body.appendChild(div);
    div.innerHTML = construct_modal(
        faq === null ? 'Create a new FAQ' : 'Update this FAQ',
        faq === null ? 'Create' : 'Update',
        false, 'success',
        template
    );

    // -- Get the elements
    const question = div.querySelector('#question') as HTMLInputElement,
        section = div.querySelector('#section') as HTMLInputElement,
        answer = div.querySelector('#answer') as HTMLTextAreaElement,
        create = div.querySelector('#create') as HTMLButtonElement,
        cancel = div.querySelector('#cancel') as HTMLButtonElement,
        delete_btn = div.querySelector('#delete') as HTMLButtonElement;


    // -- Cancel button
    cancel.addEventListener('click', () => div.remove());

    // -- Create button
    create.addEventListener('click', async() => {
        // -- Make sure the inputs are valid
        if (question.value.length < 1) {
            create_toast('error', 'Oops!', 'Please enter a question');
            return;
        }

        if (section.value.length < 1) {
            create_toast('error', 'Oops!', 'Please enter a section');
            return;
        }

        if (answer.value.length < 1) {
            create_toast('error', 'Oops!', 'Please enter an answer');
            return;
        }

        // -- Create / Update the faq
        let res;
        switch (faq === null) {
            case true: res = await create_faq(
                question.value,
                answer.value,
                section.value,
            ); break;

            case false: res = await update_faq(
                faq.id,
                question.value,
                answer.value,
                section.value,
            ); break;
        }


        // -- Check if the request was successful
        if (res.code !== 200) {
            create_toast('error', 'Oops!', res.message);
            return;
        }

        // -- Refresh the faqs
        refresh();
        create_toast('success', 'Success!', res.message);
        div.remove();
    });


    // -- Delete button
    if (faq !== null) {
        delete_btn.addEventListener('click', async() => {
            const res = await delete_faq(faq.id);

            // -- Check if the request was successful
            if (res.code !== 200) {
                create_toast('error', 'Oops!', res.message);
                return;
            }

            // -- Refresh the faqs
            refresh();
            create_toast('success', 'Success!', res.message);
            div.remove();
        });
    }
}   