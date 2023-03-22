import { SecurityPreferences } from '../index.d';

/*
    @name: create_preference_toggle
    @description: This function creates a preference toggle
    @param: name: string - The name of the preference
    @param: description: string - The description of the preference
    @param: value: boolean - The value of the preference
    @param: key: string - The key of the preference
    @param: callback: (value: boolean) => void - The callback function
*/
export function create_preference_toggle(
    name: string,
    description: string,
    value: boolean,
    key: string,
    callback: (value: boolean) => void,
): HTMLDivElement {
    const template = `
        <div class="d-flex justify-content-center align-items-center flex-column col-2">
            <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" id="${key}" ${value ? 'checked' : ''}>
                <label class="form-check-label" for="${key}"></label>
            </div>
        </div>

        <div class='col-10'>
            <h5 class="fw-bold">${name}</h5>
            <p class="text-muted">${description}</p>
        </div>
    `;
    const elm = document.createElement('div');
    elm.classList.add('d-flex', 'justify-content-start', 'align-items-center', 'flex-wrap', 'mb-2', 'w-50');
    elm.setAttribute('data-key', key);
    elm.innerHTML = template;

    // -- Get the checkbox and add the event listener
    const checkbox = elm.querySelector('input') as HTMLInputElement;
    checkbox.addEventListener('change', (e) => {
        callback((e.target as HTMLInputElement).checked);
    });
    
    // -- Return the element
    return elm;
}



/*
    @name: create_preference_toggles
    @description: This function creates a preference toggles
        for an array of preferences
    @param: preferences: SecurityPreferences
    @param: callback: (key: string, value: boolean) => void
*/
export function create_preference_toggles(
    preferences: SecurityPreferences,
    callback: (key: string, value: boolean) => void,
): Array<HTMLDivElement> {
    const toggles: Array<HTMLDivElement> = [];
    for (const key in preferences) {
        const preference = preferences[key];
        const toggle = create_preference_toggle(
            preference.name,
            preference.help_text,
            preference.value,
            key,
            (value) => callback(key, value),
        );
        toggles.push(toggle);
    }
    return toggles;
}
