import { token_url } from "..";
import { csrf_token } from "../core/headers";

export async function login(
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
        return data;
    }
    catch (error) {
        return {
            message: 'An unknown error has occured, ' + error.message,
            status: 'error',
        };
    }
}