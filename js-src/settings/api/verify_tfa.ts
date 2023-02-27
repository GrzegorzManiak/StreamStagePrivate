import { configuration } from "../";
import { DefaultResponse } from "../index.d";
import base_request from "./base_request";

export default async (
    token: string,
    otp: string,
): Promise<DefaultResponse> => {
    return base_request(
        'POST',
        configuration.verify_mfa,
        { token, otp }
    );
}