
// -- Get the navbar element
const navbar = document.getElementById('nav'),
    toggle_at = 50;

export const scrolled = () => {
    const scroll = window.scrollY;
    if (scroll > toggle_at) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
}

// -- Listen to scroll on the window
window.addEventListener('scroll', () => scrolled());
scrolled();

// -- Manage the dropdown menu
manage_dropdown(
    '#nav .nav-dropdown-menu', 
    '#nav .nav-dropdown-toggle'
);



/**
 * @name manage_dropdown
 * @description Manages the dropdown menu
 * @param {string} selector - The selector for the dropdown menu
 * @param {string} toggle - The selector for the toggle button
 * @param {number} [lag=500] - The lag time in milliseconds, aka how long the menu will stay open after the mouse leaves
 */
export async function manage_dropdown(
    selector: string, 
    toggle: string,
    lag: number = 500
) {
    // -- Get the dropdown menu and the toggle button
    const menu = document.querySelector(selector),
        button = document.querySelector(toggle);

    // -- If the menu or the button is null, return
    if (!menu || !button) return;

    // -- Last time the menu button was hovered
    let hovered = -1; 

    // -- If the menu is hovered, set the hovered time to now
    const show_menu = async() => {
        let hovering = true;
        menu.classList.add('show');
        button.classList.add('show');
        while (hovering) {
            await new Promise(r => setTimeout(r, 100));
            hovering = menu.matches(':hover') || button.matches(':hover');
            hovered = Date.now();
        }
    };

    // -- Listen to mouse movments
    menu.addEventListener('mousemove', () => show_menu());
    button.addEventListener('mousemove', () => show_menu());

    // -- If the menu is not hovered, and the hovered time is less than 1 second ago, hide the menu
    //    the idea is that if the menu is hovered, it will not hide instantly
    setInterval(() => {
        if (hovered > Date.now() - lag) return;
        menu.classList.remove('show');
        button.classList.remove('show');
    });
    
}


/**
 * @name update_profile_picture
 * @description Updates the profile picture
 * @param {string} url - The url of the profile picture
 * @returns {void}
 */
export function update_profile_picture(url: string) {
    // .user-icon, user-icon-drop-down
    const main = document.querySelector('.user-icon img') as HTMLImageElement,
        dropdown = document.querySelector('.user-icon-drop-down img') as HTMLImageElement;

    if (main) main.src = url;
    if (dropdown) dropdown.src = url;
}




// -- This manages all the buttons on the navbar
const logo = document.querySelector('#nav .logo-text'),
    buttons = document.querySelectorAll('[data-nav-area]'),
    nav_items = document.querySelector('#nav .nav-items'),
    home_locations = ['home', 'live', 'upcoming', 'past'];

// -- If the logo is clicked, go to the home page
const get_current_location = () => {
    const location = window.location.pathname.split('/')[1];
    return location;
}

const current = get_current_location(),
    is_home = home_locations.includes(current);

// -- Set location function (no reload)
const set_location = (location: string) => {
    if (!is_home) window.location 
    window.history.pushState(null, '', `/${location}`);
    window.dispatchEvent(new Event('locationchange'));
}

// -- If the logo is clicked, go to the home page
logo?.addEventListener('click', () => set_location('home'));
buttons.forEach(button => {
    const location = button.getAttribute('data-nav-area');
    if (!location) return;
    button.addEventListener('click', () => {
        set_location(location);
        nav_items.setAttribute('data-nav-active', location);
    });
});


// -- Get the initial location
const initial_location = get_current_location();
nav_items.setAttribute('data-nav-active', initial_location);
