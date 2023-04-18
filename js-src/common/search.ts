import { FilterOrder } from './index.d';
import { create_toast } from '.';

export function manage_search_panel<
    sorts extends string, 
    data
>(
    parent_element: Element,
    get_element: (
        data: data,
        parent: HTMLElement,
        reload: () => void
    ) => void,
    get_data: (
        page_num: number,
        sorts: sorts,
        order: FilterOrder,
        search: string
    ) => Promise<{
        data: Array<data>,
        message: string,
        code: number,
        page: number,
        pages: number,
    }> | Promise<void>,
    page_num = 1
): Function {
    const filter = parent_element.querySelector('#filter') as HTMLSelectElement,
        order = parent_element.querySelector('#order') as HTMLSelectElement,
        search = parent_element.querySelector('#search'),
        prev = parent_element.querySelector('#prev'),
        next = parent_element.querySelector('#next'),
        page = parent_element.querySelector('#page'),
        out_of = parent_element.querySelector('.out-of'),
        content = parent_element.querySelector('.content-loader');  


    const get_filter = () => (filter).value as sorts,
        get_order = () => (order).value as FilterOrder,
        get_search = () => (search as HTMLInputElement).value,
        get_page = () => parseInt((page as HTMLInputElement).value, 10) - 1;


    prev.addEventListener('click', () => { page_num = page_num - 1;
        (page as HTMLInputElement).value = page_num.toString(); })

    next.addEventListener('click', () => { page_num = page_num + 1;
        (page as HTMLInputElement).value = page_num.toString();});

    // -- Gather the elements that will display the results
    const results = parent_element.querySelector('.content') as HTMLElement;

        
    const update = async () => {
        content.setAttribute('dimmed', 'true');
        const res = await get_data(
            get_page(), get_filter(), get_order(), get_search()
        );

        if (res === undefined) return;
        const data = res as { 
            data: Array<data>, message: string, 
            code: number, page: number, pages: number 
        };

        // -- Clear the results
        results.innerHTML = '';
        data.data.forEach(res_data => get_element(
            res_data, results, update
        ));

        // -- Ensure that the buttons are enabled/disabled correctly
        if (Number(data.page) === 0) prev.setAttribute('disabled', 'true');
        else prev.removeAttribute('disabled');

        if (Number(data.page) === Number(data.pages)) next.setAttribute('disabled', 'true');
        else next.removeAttribute('disabled');

        // -- Update the max page
        out_of.innerHTML = 'out of ' + (Number(data.pages) + 1);
        content.setAttribute('dimmed', 'false');
    }

    filter.addEventListener('change', update);
    order.addEventListener('change', update);
    page.addEventListener('change', update);
    prev.addEventListener('click', update);
    next.addEventListener('click', update);

    manage_search(search as HTMLInputElement, () => update());
    update();

    return update;
}



/**
 * @name manage_search
 * @description Get the search string from the search input
 * Delayed by x every time the user types a character
 * @param {HTMLInputElement} search The search input
 * @param {(search: string) => void} callback The callback to call when the search is ready
 * @param {number} delay The delay in milliseconds (default: 500)
 */
export function manage_search(
    search: HTMLInputElement, 
    callback: (search: string) => void,
    delay: number = 500
) {
    let timeout: NodeJS.Timeout;
    search.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            callback(search.value);
        }, delay);
    });
}