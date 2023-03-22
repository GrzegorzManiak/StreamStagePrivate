import { attach, confirmation_modal, construct_modal, create_toast} from '../../common';
import { delete_review, update_review } from '../apis';
import { Review } from '../index.d';

export function create_review(
    review: Review
): HTMLDivElement {
    const template = `
    <div class='w-100'>
        <div class='event d-flex justify-content-between align-items-center w-100'>
            <p class='event-title'>${review.event_name}</p>
            <p class='event-rating'>${review.rating} / 10</p>
            <p class='event-likes'>${review.likes} ${review.likes === 1 ? 'like' : 'likes'}</p>
            <p class='event-date'>${new Date(review.created).toLocaleDateString()}</p>
        </div>
        <hr>
        <div class='d-flex justify-content-between align-items-start w-100 flex-column'>
            <p class='review-title'><span class='title'>${review.title}</span> <span class='text-muted you'>- You</span></p>
            <p class='review-body'>${review.body}</p>
        </div>
    </div>

    <div class='btn-container d-flex justify-content-end align-items-center flex-column gap-2 h-100 flex-grow-0'>
        <button 
            data-review-id='${review.id}'
            class="w-100 h-100 btn btn-primary btn-lg info loader-btn edit-review-btn review-btn"
            loader-state='default'> <span> <div class='spinner-border' role='status'> 
            <span class='visually-hidden'>Loading...</span> </div> </span>
            <p>Edit</p>
        </button>

        <button 
            data-review-id='${review.id}'
            class="w-100 h-100 btn btn-danger btn-lg error loader-btn remove-review-btn review-btn"
            loader-state='default'> <span> <div class='spinner-border' role='status'> 
            <span class='visually-hidden'>Loading...</span> </div> </span>
            <p>Delete</p>
        </button>
    </div>
    `

    const div = document.createElement('div');
    div.classList.add('review', 'd-flex', 'justify-content-between', 'align-items-center', 'w-100', 'gap-2');
    div.innerHTML = template;

    return div;
}

export function create_reviews(
    reviews: Array<Review>
): Array<HTMLDivElement> {
    const review_elements: Array<HTMLDivElement> = [];
    reviews.forEach((review) => {
        const elm = create_review(review),
            edit_btn = elm.querySelector('.review-btn') as HTMLButtonElement,
            remove_btn = elm.querySelector('.remove-review-btn') as HTMLButtonElement;
            
        review_elements.push(elm);
        edit_btn.addEventListener('click', async() => {
            const stop = attach(edit_btn);
            create_review_edit(review, elm);
            stop();
        });

        remove_btn.addEventListener('click', async() => {
            const stop = attach(remove_btn);
            confirmation_modal(
                async() => {
                    // -- Remove review
                    const res = await delete_review(review.id);
                    if (res.code !== 200) {
                        stop();
                        return create_toast('error', 'Failed to delete review', res.message);
                    }
                    
                    // -- Remove review element
                    create_toast('success', 'Review deleted', 'Review deleted successfully');
                    elm.remove();
                    stop();
                },
                () => stop(),
                'Are you sure you want to delete this review?',
                'Delete Review',
            )
        });
    });

    return review_elements;
}

export async function create_review_edit(
    review: Review,
    elm: HTMLDivElement
) {
    const modal_template = `
    <div class='mb-3'>
        <!-- Rating | Title -->
        <div class='d-flex justify-content-between align-items-center w-100'>
            <!-- Input -->
            <div class="h-100 w-25">
                <label for="review-rating" class="form-label">Rating</label>
                <input 
                    name="review-rating" 
                    id="review-rating" 
                    placeholder="0" 
                    value="${review.rating}"
                    type="number"
                    min="0"
                    max="10"
                class="form-control form-control-lg inp-dark text-center">
            </div>

            <!-- Input -->
            <div class="h-100 w-100">
                <label for="review-title" class="form-label">Title</label>
                <input 
                    name="review-title" 
                    id="review-title" 
                    placeholder="0" 
                    value="${review.title}"
                class="form-control form-control-lg inp-dark">
            </div>
        </div>

        <!-- Body -->
        <div class='d-flex justify-content-between align-items-center w-100 mt-2'>
            <div class="h-100 w-100">
                <label for="review-body" class="form-label">Body</label>
                <textarea
                    name="review-body"
                    id="review-body"
                    placeholder="0"
                    value="${review.body}"
                class="form-control form-control-lg inp-dark">${review.body}</textarea>
            </div>
        </div>
    </div>
    `;

    // -- Create Modal
    const modal = construct_modal(
        'Edit Review',
        'Edit review',
        true,
        'success',
        modal_template
    );

    const modal_elm = document.createElement('div');
    modal_elm.innerHTML = modal;
    document.body.appendChild(modal_elm);

    // -- yes / no buttons
    const yes = modal_elm.querySelector('.yes') as HTMLButtonElement,
        no = modal_elm.querySelector('.no') as HTMLButtonElement;

    // -- Input fields
    const rating = modal_elm.querySelector('#review-rating') as HTMLInputElement,
        title = modal_elm.querySelector('#review-title') as HTMLInputElement,
        body = modal_elm.querySelector('#review-body') as HTMLTextAreaElement;


    // -- Event Listeners 
    rating.style['-moz-appearance'] = 'textfield';
    rating.addEventListener('input', () => {
        // -- Ensure rating is a number
        if (isNaN(parseInt(rating.value)))
            rating.value = '0';
        
        // -- Ensure rating is between 0 and 10
        if (parseInt(rating.value) > 10)
            rating.value = '10';

        else if (parseInt(rating.value) < 0)
            rating.value = '0';
    });

    yes.addEventListener('click', async() => {
        const stop = attach(yes),
            res = await update_review(
                review.id,
                parseInt(rating.value),
                title.value,
                body.value
        );
            
        if (res.code !== 200) create_toast('error', 'Oops!', res.message);
        else {
            create_toast('success', 'Success!', res.message);
            modal_elm.remove();
            elm.getElementsByClassName('event-rating')[0].innerHTML = `${rating.value} / 10`;
            elm.getElementsByClassName('title')[0].innerHTML = title.value;
            elm.getElementsByClassName('review-body')[0].innerHTML = body.value;
        }

        stop();
    });

    no.addEventListener('click', () => {
        modal_elm.remove();
    });
}