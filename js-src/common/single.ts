/**
 * @name single
 * @description This function just esures that the script is only ran once per 
 * page, as webpack has a tendancy of creating multiple entrys.
 * @param {string} name - The name of the script
 */
export function single(name: string) {
    // -- If the script has already been ran, CRASH!
    if (window[name]) {
        throw new Error(`Script ${name} has already been ran!`);
    }   

    // -- Set the script as ran
    window[name] = true;
}