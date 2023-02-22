import { get_servers } from "./fetch";

const config = document.getElementById('config');
export let servers_url = config?.getAttribute('data-servers-api'),
    csrf_token = config?.getAttribute('data-csrf-token');

// -- Make sure both items are defined
if (servers_url === null || csrf_token === null) 
    throw new Error('Missing required config data');

// -- Get the servers
(async () => {
    let servers = await get_servers();
    if (servers.code !== 200) 
        return console.error('Failed to get servers');

    const server_list = servers.data;
    
    // -- Get the server list element
    const server_list_element = document.getElementById('server-list');
    if (server_list_element === null)
        return console.error('Failed to find server list element');

    // -- Create a list item for each server
    for (let server of server_list) {
        const server_item = document.createElement('li');
        server_item.innerHTML = `
            <a href="${server.url}">
                <img src="${server.flag}" alt="${server.country}" />
                <span>${server.name}</span>
            </a>

        `;
        server_list_element.appendChild(server_item);
    }
})();