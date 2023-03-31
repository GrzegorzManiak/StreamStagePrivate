import { configuration } from '.';
import { DefaultResponse } from '../api/index.d';
import { base_request } from '../api';
import { CategoryResponse, CategorySorts, FilterOrder, FilterPosition, FilterSort, FilterdCategoriesResponse, FilterdUsersResponse, Frame, StatisticsResponse, UserResponse } from './index.d';

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