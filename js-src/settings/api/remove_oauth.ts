import { configuration } from "../";
import { DefaultResponse } from "../index.d";
import base_request from "./base_request";

export default async (token: string, oauth_id: string): Promise<DefaultResponse> => {
    return base_request(
        'POST',
        configuration.remove_oauth,
        { token, oauth_id }
    );
}