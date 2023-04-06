import { configuration } from '.';
import { DefaultResponse } from '../api/index.d';
import { base_request } from '../api';
import { BroadcasterResponse, BroadcasterSorts, CategoryResponse, CategorySorts, EventSorts, FaqSorts, FilterPosition, FilterSort, FilterdBroadcastersResponse, FilterdCategoriesResponse, FilterdEventsResponse, FilterdFaqsResponse, FilterdPrivacyResponse, FilterdTermsResponse, FilterdUsersResponse, Frame, PrivacyResponse, StatisticsResponse, TermsPrivacySorts, TermsResponse, UserResponse } from './index.d';
import { FilterOrder } from '../common/index.d';

/**
 * @name get_statistics
 * @param {string} group - The statistical group to get
 * @param {string} statistic - The statistic to get
 * @param {int} from - The start time (MS since epoch)
 * @param {int} to - The end time (MS since epoch)
 * @param {Frame} frame - The frame to get the statistics from
 * @returns {Promise<StatisticsResponse>}
 */
export const get_statistics = async (
    group: string,
    statistic: string,
    from: number,
    to: number,
    frame: Frame,
): Promise<StatisticsResponse> => base_request(
    'GET',
    configuration.statistics,
    { group, statistic, from, to, frame },
);



/**
 * @name filter_users
 * @param {number} page - The page to get
 * @param {FilterSort} sort - The sort to use (name, email, etc)
 * @param {FilterOrder} order - The order to use (asc, desc)
 * @param {FilterPosition} position - The position of the user (admin, user, etc)
 * @param {string} search - The search query
 * @returns {Promise<FilterdUsersResponse>}
 */
export const filter_users = async (
    page: number,
    sort: FilterSort,
    order: FilterOrder,
    position: FilterPosition,
    search: string,
): Promise<FilterdUsersResponse> => base_request(
    'GET',
    configuration.users,
    { page, sort, order, position, search }
)



/**
 * @name get_user
 * @param {string} id - The id of the user to get
 * @returns {Promise<FilterdUser>}
 */
export const get_user = async (
    id: string
): Promise<UserResponse> => base_request(
    'GET',
    configuration.get_user,
    { id },
);



/**
 * @name delete_user
 * @param {string} id - The id of the user to delete
 * @returns {Promise<DefaultResponse>}
 */
export const delete_user = async (
    id: string
): Promise<DefaultResponse> => base_request(
    'DELETE',
    configuration.delete_user,
    { id },
);



/**
 * @name update_email
 * @param {string} id - The id of the user to update
 * @param {string} email - The new email
 * @returns {Promise<DefaultResponse>}
 */
export const update_email = async (
    id: string,
    email: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.update_email,
    { id, email },
);



/**
 * @name update_streamer_status
 * @param {string} id - The id of the user to update
 * @param {boolean} streamer - The new streamer status
 * @returns {Promise<DefaultResponse>}
 */
export const update_streamer_status = async (
    id: string,
    streamer: boolean
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.update_streamer_status,
    { id, streamer },
);



/**
 * @name filter_categories
 * @param {number} page - The page to get
 * @param {CategorySorts} sort - The sort to use (name, email, etc)
 * @param {FilterOrder} order - The order to use (asc, desc)
 * @param {string} search - The search query
 * @returns {Promise<FilterdCategoriesResponse>}
 */
export const filter_categories = async (
    page: number,
    sort: CategorySorts,
    order: FilterOrder,
    search: string,
): Promise<FilterdCategoriesResponse> => base_request(
    'GET',
    configuration.category,
    { page, sort, order, search }
);



/**
 * @name create_category
 * @param {string} name - The name of the category
 * @param {string} description - The description of the category
 * @param {string} color - The color of the category
 * @param {string} image - The image of the category
 * @returns {Promise<DefaultResponse>}
 * @description Creates a new category
 */
export const create_category = async (
    name: string,
    description: string,
    color: string,
    image: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.create_category,
    { name, description, color, image },
);



/**
 * @name update_category
 * @param {string} id - The id of the category to update
 * @param {string} name - The name of the category
 * @param {string} description - The description of the category
 * @param {string} color - The color of the category
 * @returns {Promise<DefaultResponse>}
 * @description Updates a category
 */
export const update_category = async (
    id: string,
    name: string,
    description: string,
    color: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.update_category,
    { id, name, description, color },
);



/**
 * @name delete_category
 * @param {string} id - The id of the category to delete
 * @returns {Promise<DefaultResponse>}
 * @description Deletes a category
 */
export const delete_category = async (
    id: string,
): Promise<DefaultResponse> => base_request(
    'DELETE',
    configuration.delete_category,
    { id },
);



/**
 * @name get_category
 * @param {string} id - The id of the category to get
 * @returns {Promise<CategoryResponse>}
 * @description Gets a category
 */
export const get_category = async (
    id: string,
): Promise<CategoryResponse> => base_request(
    'GET',
    configuration.get_category,
    { id },
);



/**
 * @name set_category_image
 * @param {string} id - The id of the category to update
 * @param {string} image - The image to set (base64)
 * @returns {Promise<DefaultResponse>}
 * @description Sets the image of a category
 */
export const set_category_image = async (
    id: string,
    image: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.set_category_image,
    { id, image },
);



/**
 * @name filter_broadcasters
 * @param {number} page - The page to get
 * @param {BroadcasterSorts} sort - The sort to use (name, email, etc)
 * @param {FilterOrder} order - The order to use (asc, desc)
 * @param {string} search - The search query
 * @returns {Promise<FilterdBroadcastersResponse>}
 */
export const filter_broadcasters = async (
    page: number,
    sort: BroadcasterSorts,
    order: FilterOrder,
    search: string,
): Promise<FilterdBroadcastersResponse> => base_request(
    'GET',
    configuration.broadcaster,
    { page, sort, order, search }
);



/**
 * @name get_broadcaster
 * @param {string} id - The id of the broadcaster to get
 * @returns {Promise<BroadcasterResponse>}
 * @description Gets a broadcaster
 */
export const get_broadcaster = async (
    id: string,
): Promise<BroadcasterResponse> => base_request(
    'GET',
    configuration.get_broadcaster,
    { id },
);



/**
 * @name update_broadcaster
 * @param {string} id - The id of the broadcaster to update
 * @param {string} name - The name of the broadcaster
 * @param {string} handle - Broadcasters handle
 * @param {boolean} over_18 - If the broadcaster is over 18 only
 * @param {boolean} approved - If the broadcaster is approved
 * @param {string} biography - The biography of the broadcaster
 * @param {string} streamer - Bastically the owner of the broadcaster
 */
export const update_broadcaster = async (
    id: string,
    name: string,
    handle: string,
    over_18: boolean,
    approved: boolean,
    biography: string,
    owner: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.update_broadcaster,
    { id, name, over_18, approved, biography, handle, owner },
);



/**
 * @name delete_broadcaster
 * @param {string} id - The id of the broadcaster to delete
 * @returns {Promise<DefaultResponse>}
 * @description Deletes a broadcaster
 */
export const delete_broadcaster = async (
    id: string,
): Promise<DefaultResponse> => base_request(
    'DELETE',
    configuration.delete_broadcaster,
    { id },
);



/**
 * @name filter_events
 * @param {number} page - The page to get
 * @param {EventSorts} sort - The sort to use (name, email, etc)
 * @param {FilterOrder} order - The order to use (asc, desc)
 * @param {string} search - The search query
 * @returns {Promise<FilterdEventsResponse>}
 */
export const filter_events = async (
    page: number,
    sort: EventSorts,
    order: FilterOrder,
    search: string,
): Promise<FilterdEventsResponse> => base_request(
    'GET',
    configuration.event,
    { page, sort, order, search }
);



/**
 * @name latest_privacy
 * @returns {Promise<PrivacyResponse>}
 * @description Gets the latest privacy policy
 */
export const latest_privacy = async (): Promise<PrivacyResponse> => base_request(
    'GET',
    configuration.latest_privacy,
);



/**
 * @name latest_terms
 * @returns {Promise<TermsResponse>}
 * @description Gets the latest terms of service
 */
export const latest_terms = async (): Promise<TermsResponse> => base_request(
    'GET',
    configuration.latest_terms,
);



/**
 * @name filter_privacy
 * @param {number} page - The page to get
 * @param {TermsPrivacySorts} sort - The sort to use (name, email, etc)
 * @param {FilterOrder} order - The order to use (asc, desc)
 * @param {string} search - The search query
 */
export const filter_privacy = async (
    page: number,
    sort: TermsPrivacySorts,
    order: FilterOrder,
    search: string,
): Promise<FilterdPrivacyResponse> => base_request(
    'GET',
    configuration.filter_privacy,
    { page, sort, order, search }
);



/**
 * @name filter_terms
 * @param {number} page - The page to get
 * @param {TermsPrivacySorts} sort - The sort to use (name, email, etc)
 * @param {FilterOrder} order - The order to use (asc, desc)
 * @param {string} search - The search query
 * @returns {Promise<FilterdTermsResponse>}
*/
export const filter_terms = async (
    page: number,
    sort: TermsPrivacySorts,
    order: FilterOrder,
    search: string,
): Promise<FilterdTermsResponse> => base_request(
    'GET',
    configuration.filter_terms,
    { page, sort, order, search }
);



/**
 * @name create_terms
 * @param {string} title - The title of the terms
 * @param {string} content - The content of the terms
 * @returns {Promise<DefaultResponse>}
 * @description Creates a new terms of service
 */
export const create_terms = async (
    title: string,
    content: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.create_terms,
    { title, content },
);



/**
 * @name create_privacy
 * @param {string} title - The title of the privacy
 * @param {string} content - The content of the privacy
 * @returns {Promise<DefaultResponse>}
 * @description Creates a new privacy policy
 */
export const create_privacy = async (
    title: string,
    content: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.create_privacy,
    { title, content },
);



/**
 * @name filter_faq
 * @param {number} page - The page to get
 * @param {FaqSorts} sort - The sort to use (name, email, etc)
 * @param {FilterOrder} order - The order to use (asc, desc)
 * @param {string} search - The search query
 * @returns {Promise<FilterdFaqsResponse>}
 */
export const filter_faq = async (
    page: number,
    sort: FaqSorts,
    order: FilterOrder,
    search: string,
): Promise<FilterdFaqsResponse> => base_request(
    'GET',
    configuration.faq_filter,
    { page, sort, order, search }
);



/**
 * @name create_faq
 * @param {string} question - The question of the faq
 * @param {string} answer - The answer of the faq
 * @param {string} section - The section of the faq
 * @returns {Promise<DefaultResponse>}
 */
export const create_faq = async (
    question: string,
    answer: string,
    section: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.faq_create,
    { question, answer, section },
);



/**
 * @name update_faq
 * @param {string} id - The id of the faq to update
 * @param {string} question - The question of the faq
 * @param {string} answer - The answer of the faq
 * @param {string} section - The section of the faq
 * @returns {Promise<DefaultResponse>}
 */
export const update_faq = async (
    id: string,
    question: string,
    answer: string,
    section: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.faq_update,
    { id, question, answer, section },
);



/**
 * @name delete_faq
 * @param {string} id - The id of the faq to delete
 * @returns {Promise<DefaultResponse>}
 */
export const delete_faq = async (
    id: string,
): Promise<DefaultResponse> => base_request(
    'DELETE',
    configuration.faq_delete,
    { id },
);