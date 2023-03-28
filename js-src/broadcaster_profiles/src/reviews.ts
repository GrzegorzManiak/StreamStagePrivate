import { GetReviewsSuccess, Review } from "../../common/index.d";
import { create_toast } from "../../common";
import { get_reviews } from "../../common/api";
import { create_review } from "../../common/review";
import { configuration } from "..";

function create_reviews(
    reviews: Array<Review>
): Array<HTMLDivElement> {
    const review_elements: Array<HTMLDivElement> = [];
    reviews.forEach((review) => review_elements.push(create_review(
        review, 
        false, 
        configuration.is_you
    )));
    return review_elements;
}


export function manage_reviews_panel(
    username: string,
    you: boolean
) {
    // -- Get the panel
    const panel = document.querySelector('#reviews-tab') as HTMLDivElement;

    // -- Get the review container
    const review_container = panel.querySelector('.reviews') as HTMLDivElement,
        filter = panel.querySelector('#filter') as HTMLSelectElement,
        order = panel.querySelector('#order') as HTMLSelectElement;

    // -- Get the pagenation controlls
    const prev = panel.querySelector('.prev') as HTMLButtonElement,
        next = panel.querySelector('.next') as HTMLButtonElement,
        page_number = panel.querySelector('#review-page') as HTMLInputElement,
        out_of = panel.querySelector('.out-of') as HTMLSpanElement;


    let page = 0, toatl_pages = 0;
    async function reload_reviews() {
        // -- Get the reviews
        const reviews = await get_reviews(
            filter.value as 'created' | 'rating' | 'likes',
            order.value as 'asc' | 'desc', page,
            configuration.username
        );

        // -- Check if the request was successful
        if (reviews.code !== 200) return create_toast(
            'error', 'Oops!', 'There was an error while trying to get the reviews, please try again later.')

        const data = (reviews as GetReviewsSuccess).data,
            renderd_reviews = create_reviews(data.reviews);
        
        // -- Clear the review container
        review_container.innerHTML = '';
        renderd_reviews.forEach(review => review_container.appendChild(review));
        out_of.innerText = 'out of ' + Number(data.pages);
        page_number.value = page + 1 + '';
        toatl_pages = data.pages;


        // -- Update the pagenation controlls
        if (page === 0) prev.disabled = true;
        else prev.disabled = false;

        if (page === toatl_pages -1) next.disabled = true;
        else next.disabled = false;

        // -- Check if there are no reviews
        if (data.reviews.length === 0) review_container.innerHTML = `
            <div class="no-reviews w-100 h-100 d-flex justify-content-center align-items-center">
                <h3 class="text-center text-muted">${ you ? 'You' : '@' + username } has no reviews yet.</h3>
            </div>
        `;
    }


    // -- Add the event listeners
    prev.disabled = true;
    prev.addEventListener('click', () => {
        if (page === 0) return prev.disabled = true;
        page--;
        reload_reviews();
    });

    next.addEventListener('click', () => {
        if (page === toatl_pages) return
        prev.disabled = false;
        page++;
        reload_reviews();
    });

    page_number.addEventListener('change', () => {
        const number = parseInt(page_number.value);
        if (number < 1 || number > toatl_pages) return;
        page = number - 1;
        reload_reviews();
    });

    filter.addEventListener('change', reload_reviews);
    order.addEventListener('change', reload_reviews);

    reload_reviews();
    console.log('Reviews panel loaded');
}
