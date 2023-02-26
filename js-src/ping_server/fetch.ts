import { csrf_token, servers_url } from './';

interface Server {
    id: string,
    name: string,
    mode: string,
    slug: string,
    region: string,
    country: string,
    rtmp_url: string,
    http_url: string,
    live: boolean,
    url: string,
    flag: string,
}

export const get_servers = async (): Promise<{data?: Array<Server>, code: number}> => {
    const response = await fetch(
        servers_url,
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            }
        },
    );

    try {
        return {
            data: await response.json(),
            code: response.status,
        }
    }
    catch (error) {
        return {
            code: response.status,
        };
    }
}