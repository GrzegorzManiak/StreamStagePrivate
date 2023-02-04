import {
    Response,
} from './index.d';

// -- Handle instructions
const instruction_parser = (instructions: string): Response | null => {
    // -- Try decoding instructions
    try { return JSON.parse(atob(instructions)); }
    catch (error) { return null; }
};

export const instruction_handler = (instructions: string) => {
    // -- Parse instructions
    const response = instruction_parser(instructions);

    // -- If there is no response, return
    if (!response) return;

    // -- Handle response
    console.log(response);
}