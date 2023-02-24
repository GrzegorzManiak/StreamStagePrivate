import { configuration } from "../";
import { SecurityInfoResponse } from "../index.d";

export const get_security_info = async (
    token: string,
): Promise<SecurityInfoResponse> => {
    const response = await fetch(
        configuration.security_info,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration.csrf_token,
            },
            body: JSON.stringify({
                token,
            }),
        },
    );

    try {
        const data = await response.json();
        
        // -- Check for code 200
        if (response.status !== 200) {
            return {
                code: response.status,
                message: data.message as string,
            }
        }

        return {
            data: data,
            code: response.status,
            message: data.message as string,
        }
    }
    catch (error) {
        return {
            code: response.status,
            message: 'An unknown error has occured, ' + error.message,
        };
    }
}