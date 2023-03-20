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
        <button class="w-100 h-100 btn btn-primary btn-lg info loader-btn edit-review-btn review-btn"
            loader-state='default'> <span> <div class='spinner-border' role='status'> 
            <span class='visually-hidden'>Loading...</span> </div> </span>
            <p>Edit</p>
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
        review_elements.push(create_review(review));
    });

    return review_elements;
}