import { create_toast } from '../../common';
import { manage_search_panel } from '../../common/search';
import { filter_purchases } from '../apis';
import { GetPurchasesSuccess, Pod, Purchase, PurchaseSorts } from '../index.d';

export function manage_purchases_panel(pod: Pod) {
    // -- Get the panel
    const panel = pod.panel.element;

    const update = manage_search_panel<PurchaseSorts, Purchase>(
        panel, (data, parent, refresh) => create_purchase_elm(refresh, parent, data),
        async(page, sorts, order, search) => {
            const res = await filter_purchases(page, sorts, order, search
            ) as GetPurchasesSuccess;

            if (res.code !== 200) {
                create_toast('error', 'Oops! My bad', res.message);
                return;
            }

            return {
                data: res.data.purchases,
                message: res.message,
                code: res.code,
                page: res.data.page,
                pages: res.data.pages,
            }
        },
    );
}

async function create_purchase_elm(refresh: () => void, parent: HTMLElement, data: Purchase) {
    const template = `
    <div class='w-100 d-flex justify-content-between align-items-center'>
        <div class='profile-info cat-info p-2'>
            <p class='m-0 text-muted'><span class='bold text-white'> ID:</span> ${data.purchase_id}</p>
            <p class='m-0 text-muted'><span class='bold text-white'> Total:</span> ${data.total}</p>
            <p class='m-0 text-muted'><span class='bold text-white'> Multiplier:</span> ${data.total_multiplier}</p>
        </div>

        <div class='profile-info cat-info p-2'>
            <p class='m-0 text-muted'><span class='bold text-white'> Timestamp:</span> ${data.purchase_timestamp}</p>
            <p class='m-0 text-muted'><span class='bold text-white'> Stripe ID:</span> ${data.stripe_id}</p>
            <p class='m-0 text-muted'><span class='bold text-white'> Payment ID:</span> ${data.payment_id}</p>
        </div>
    </div>

    <div class='w-100'> 
        <!-- Items -->
        ${data.items.map(item => `
            <div class='w-100 purchase-item'>
                <div class='w-100 d-flex justify-content-between align-items-center'>
                    <p class='m-0 text-muted'><span class='bold text-white'> Item: </span> ${item.item_name}</p>
                    <p class='m-0 text-muted'><span class='bold text-white'> Price: </span> ${item.price}</p>
                </div>

                <div class='w-100 d-flex justify-content-between align-items-center'>
                    <p class='m-0 text-muted'>${item.other_data}</p>
                </div>
            </div>
        `).join('')}
    </div>
    `;

    const div = document.createElement('div');
    div.classList.add('d-flex', 'justify-content-between', 'align-items-center', 'gap-2', 'purchase', 'cat-container', 'flex-column');
    div.innerHTML = template;
    parent.appendChild(div);
}