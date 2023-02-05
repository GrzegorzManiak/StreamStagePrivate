import { token_url, get_token_url } from "..";
import { csrf_token } from "../core/headers";

export const login = async (
    emailorusername: string,
    password: string,
) => {
    const response = await fetch(
        get_token_url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                emailorusername,
                password,
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

export async function login_with_token(
    token: string,
) {
    const response = await fetch(
        token_url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `${token}`,
                "X-CSRFToken": csrf_token,
            }
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
