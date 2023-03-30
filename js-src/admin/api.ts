import { configuration } from '.';
import { base_request } from '../api';
import { FilterOrder, FilterPosition, FilterSort, FilterdUser, FilterdUsersResponse, FilterdUsersSuccess, Frame, StatisticsResponse, UserResponse } from './index.d';

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