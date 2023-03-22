import { AddCardResponse, Card, GetCardsResponse } from './index.d';
import { base_request } from '../api';
import { configuration } from '.';
import { DefaultResponse } from '../api/index.d';

/**
 * @name add_card
 * @param card - Card: Token, number, exp_month, exp_year, cvc
 * @returns Promise<DefaultResponse>
 */
export const add_card = async (
    card: Card
): Promise<AddCardResponse> => base_request(
    'POST',
    configuration.add_payment,
    card
);


/**
 * @name get_cards
 * @returns Promise<DefaultResponse>
 * @description Get the cards of the user
 */
export const get_cards = async (): Promise<GetCardsResponse> => base_request(
    'GET',
    configuration.get_payments,
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
    configuration.remove_payment,
    { id }
);
