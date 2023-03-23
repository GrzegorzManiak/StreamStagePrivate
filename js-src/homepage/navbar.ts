export function manage_navbar() {
    // -- Get the navbar element
    const navbar = document.getElementById('nav'),
        toggle_at = 50;

    const scrolled = () => {
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
}


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