import { configuration } from "../";
import { RecentVerificationResponse, VerifyAccessResponse } from "../index.d";

export const send_verification = async (
    mode: 'email' | 'tfa',
    mfa_code?: string,
): Promise<VerifyAccessResponse> => {

    const response = await fetch(
        configuration.send_verification,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration.csrf_token,
            },
            body: JSON.stringify({
                mode,
                mfa: mfa_code,
            }),
        },
    );

    try {
        const data = await response.json();
        
        // -- Check for code 200
        if (response.status !== 200) {
            return {
                data: data,
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


export const recent = async (
    token: string,
): Promise<RecentVerificationResponse> => {
    const response = await fetch(
        configuration.recent_verification,
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
        const data = await response.json() as {
            status: string,
            message: string,
        };

        return {
            data: data,
            code: response.status,
            message: data.message,
        }
    }
    catch (error) {
        return {
            message: 'An unknown error has occured, ' + error.message,
            code: response.status,
        };
    }
}


export const remove = async (
    token: string,
): Promise<RecentVerificationResponse> => {
    const response = await fetch(
        configuration.remove_verification,
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
        const data = await response.json() as {
            status: string,
            message: string,
        };

        return {
            code: response.status,
            message: data.message,
        }
    }
    catch (error) {
        return {
            message: 'An unknown error has occured, ' + error.message,
            code: response.status,
        };
    }
}