import { AttributeType, JStype, LiteralJS } from './index.d';
import { create_toast } from '../common';

export function get_or_error<e>(element: HTMLElement | Element, attribute: string): e {
    const value = element.getAttribute(attribute);
    if (!value) {
        create_toast('error', 'Configuration Error', `No ${attribute} found, please reload the page`);
        // -- Wait 3 seconds and reload the page
        setTimeout(() => {
            window.location.reload();
        }, 3000);
    }
    return value as unknown as e;
}


export class Type {
    public attribute: string;
    public type: AttributeType;
    public cast: JStype;
    
    constructor(
        attribute: string,
        type: AttributeType,
        cast?: JStype
    ) { 
        this.type = type;
        this.cast = cast || type;
        this.attribute = attribute;
    }

    public cast_value(value: string): any {
        switch (this.cast) {
            case 'string': return value;
            case 'number': return Number(value);
            case 'boolean': return Boolean(value.toLowerCase() === 'true');
            case 'object': return JSON.parse(value);
            case 'function': return value;
            case 'undefined': return undefined;
            case 'bigint': return BigInt(value);
            case 'symbol': return Symbol(value);
            case 'null': return null;
        }
    }
}


function build_inverse_map(
    configuration: { [key: string]: Type }
) {
    const inverse_map: { [key: string]: {
        type: Type,
        name: string
    } } = {};
    
    Object.keys(configuration).forEach(key => {
        const type = configuration[key];
        inverse_map[type.attribute] = {
            type,
            name: key
        };
    });

    return inverse_map;
}


export function build_configuration<e>(configuration: {
    [key: string]: Type
}) {
    // -- Get all the elements with the class 'config'
    const config_elements = document.querySelectorAll('.config'),
        inverse_map = build_inverse_map(configuration),
        ignored = ['class', 'id'],
        config: { [key: string]: LiteralJS } = {};

    // -- Loop through the config elements
    config_elements.forEach(element => {
        Array.from(element.attributes).forEach(attribute => {

            // -- Check if the attribute should be ignored
            if (ignored.includes(attribute.name)) return;

            // -- Check if the attribute name is in the configuration
            if (inverse_map.hasOwnProperty(attribute.name)) 
                config[inverse_map[attribute.name].name] = 
                inverse_map[attribute.name].type
                .cast_value(
                    get_or_error<string>(
                        element, 
                        attribute.name
                    )
                );
        });
    });

    // -- Check if all the configuration values are set
    Object.keys(configuration).forEach(key => {
        if (!config.hasOwnProperty(key)) 
            create_toast('error', 'Configuration Error', `No ${key} found, please reload the page`);
    });

    return config as e;
}

export function configuration() {
    return build_configuration<{
        csrf_token: string,
        recent_verification: string,
        resend_verification: string
    }>({
        csrf_token: new Type('data-csrf-token', 'string'),
        recent_verification: new Type('data-recent-verification', 'string'),
        resend_verification: new Type('data-resend-verification', 'string'),
    });
}