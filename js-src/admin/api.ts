import { configuration } from '.';
import { DefaultResponse } from '../api/index.d';
import { base_request } from '../api';
import { FilterOrder, FilterPosition, FilterSort, FilterdUsersResponse, Frame, StatisticsResponse, UserResponse } from './index.d';

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