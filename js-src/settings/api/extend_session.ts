import { DefaultResponse } from "../index.d";
import { configuration } from "../";
import base_request from "./base_request";

export default async (token: string): Promise<DefaultResponse> => {
    return base_request(
        'POST',
        configuration.extend_session,
        { token }
    );
}