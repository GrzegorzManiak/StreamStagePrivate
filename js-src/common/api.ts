import { AddCardResponse, Card, CheckPaymentIntentResponse, GetCardsResponse, GetReviewsResponse, NewPaymentIntentResponse, report_type } from './index.d';
import { base_request } from '../api';
import { load_cfg } from '.';
import { DefaultResponse } from '../api/index.d';
import { Type, build_configuration } from '../api/config';

/**
 * @name add_card
 * @param card - Card: Token, number, exp_month, exp_year, cvc
 * @returns Promise<DefaultResponse>
 */
export const add_card = async (
    card: Card
): Promise<AddCardResponse> => base_request(
    'POST',
    load_cfg().add_payment,
    card
);


/**
 * @name get_cards
 * @returns Promise<DefaultResponse>
 * @description Get the cards of the user
 */
export const get_cards = async (): Promise<GetCardsResponse> => base_request(
    'GET',
    load_cfg().get_payments,
    {}
);


/**
 * @name remove_card
 * @param id - Card id
 * @returns Promise<DefaultResponse>
 * @description Remove a card from the user
 */
export const remove_card = async (
    id: string
): Promise<DefaultResponse> => base_request(
    'POST',
    load_cfg().remove_payment,
    { id }
);



/**
 * @name get_reviews
 * @param filter - Filter
 * @param sort - Sort
 * @param page - Page
 * @param username - Username
 */
export const get_reviews = async (
    sort: 'created' | 'rating' | 'likes',
    order: 'asc' | 'desc',
    page: number,
    username: string
): Promise<GetReviewsResponse> => base_request(
    'POST',
    build_configuration<{get_reviews: string}>({
        get_reviews: new Type('data-get-reviews', 'string'),
    }).get_reviews,
    { sort, order, page, username }
);
    


/**
 * @name submit_report
 * @param {report_type} type - Type of report
 * @param r_id - Id of the object that is being reported
 * @param reason - Reason for the report
 */
export const submit_report = async (
    type: report_type,
    r_id: string,
    reason: string
): Promise<DefaultResponse> => base_request(
    'POST',
    build_configuration<{submit_report: string}>({
        submit_report: new Type('data-submit-report', 'string'),
    }).submit_report,
    { type, r_id, reason }
);



/**
 * @name create_intent
 * @param {string | Card & { save: boolean }} method - Payment method
 * @param {string} buyable_id - The ID of the thing being bought
 * @returns {Promise<NewPaymentIntentResponse>}
 */
export const create_intent = async (
    buyable_id: string,
    payment_method: string | Card & { save: boolean },
): Promise<NewPaymentIntentResponse> => base_request(
    'POST',
    build_configuration<{create_intent: string}>({
        create_intent: new Type('data-create-payment-intent', 'string'),
    }).create_intent,
    { payment_method, buyable_id }
);



/**
 * @name check_intent
 * @param {string} intent_id - The ID of the payment intent
 * @returns {Promise<CheckPaymentIntentResponse>}
 * @description Check the status of a payment intent
 */
export const check_intent = async (
    intent_id: string
): Promise<CheckPaymentIntentResponse> => base_request(
    'POST',
    build_configuration<{check_intent: string}>({
        check_intent: new Type('data-check-payment-intent', 'string'),
    }).check_intent,
    { intent_id }
);