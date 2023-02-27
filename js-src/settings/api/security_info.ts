import { configuration } from "../";
import { SecurityInfoResponse } from "../index.d";
import base_request from "./base_request";

export const get_security_info = async (
    token: string,
): Promise<SecurityInfoResponse> => {
    return base_request(
        'POST',
        configuration.security_info,
        { token }
    ) as Promise<SecurityInfoResponse>;
}