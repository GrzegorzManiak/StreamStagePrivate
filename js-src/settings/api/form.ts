import { configuration } from "../";
import { VerifyAccessResponse } from "../index.d";
 
function format_data(dict: any): string {
    let data = '';
    for (const key in dict) {
        data += `${key}=${dict[key]}&`;
    }
    return data;
}

export const send_form_data = async (
    form_data: {
        [key: string]: string | number | boolean | null | undefined
    },
    endpoint: string,
): Promise<VerifyAccessResponse> => {   

    const response = await fetch(
        endpoint,
        {
            method: "POST",
            headers: {
                // FOrm data
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": configuration.csrf_token,
            },
            body: format_data(form_data),
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
