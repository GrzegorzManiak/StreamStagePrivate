import { configuration } from "../";
import { DefaultResponse } from "../index.d";
import base_request from "./base_request";

export default async (
    token: string,
): Promise<DefaultResponse> => {
    return base_request(
        'POST',
        configuration.disable_mfa,
        { token },
    );
}