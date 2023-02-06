import { csrf_token } from "../";
import { email_recent, email_resend } from "..";

export const resend = async (
    resend_key: string,
    email?: string,
) => {
    let body: {
        token: string,
        email?: string,
    } = { token: resend_key };
    if (email) body['email'] = email;

    const response = await fetch(
        email_resend,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify(body),
        },
    );

    try {
        const data = await response.json();
        return {
            data: data,
            status: data.status as string,
            code: response.status,
            message: data.message as string,
        }
    }
    catch (error) {
        return {
            message: 'An unknown error has occured, ' + error.message,
            code: response.status,
            status: 'error',
        };
    }
}

export const recent = async (
    token: string,
) => {
    const response = await fetch(
        email_recent,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                token,
            }),
        },
    );

    try {
        const data = await response.json();
        return {
            data: data,
            status: 'success',
            code: response.status,
        }
    }
    catch (error) {
        return {
            message: 'An unknown error has occured, ' + error.message,
            code: response.status,
            status: 'error',
        };
    }
}