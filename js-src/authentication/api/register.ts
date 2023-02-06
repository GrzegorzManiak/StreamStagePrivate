import { register_url } from "..";
import { csrf_token } from "../";

export async function register_with_oauth(
    oauth_token: string,
    password: string,
    username: string,
    email: string,
) {
    const response = await fetch(
        register_url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `${oauth_token}`,
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                password,
                username,
                email,
            }),
        },
    );
    
    try {
        console.log(response);
        const data = await response.json();
        return data;
    }
    catch (error) {
        return {
            message: 'An unknown error has occured, ' + error.message,
            status: 'error',
        };
    }
}


export const register = async (
    password: string,
    username: string,
    email: string,
) => {
    const response = await fetch(
        register_url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                password,
                username,
                email,
            }),
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