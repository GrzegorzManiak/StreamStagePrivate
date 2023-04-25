import { construct_modal, create_toast } from "../common";
import { add_evt_showing, del_evt_showing, get_evt_showings } from "./apis";
import { GetShowingsResponse, AddShowingResponse, Showing, GetShowingsSuccess, AddShowingSuccess } from "./index.d"
import { configuration } from "./index"
import { transpileModule } from "typescript";

import { manage_add_live_ticket_btn } from "./edit_tickets";

let showings_panel;

export function handle_showings_panel(panel: HTMLElement) {
    showings_panel = panel;

    const add_showing_btn = document.querySelector('#add-showing-btn') as HTMLElement;
    if (add_showing_btn) manage_add_showing_btn(add_showing_btn);
        
    query_showings();
}

function manage_add_showing_btn(
    btn: HTMLElement
) {
    btn.addEventListener("click", () => {
        const modal_wrap = construct_modal(
            "Add Showing", 
            "Enter event showing details", 
            true, 
            'success', 
            add_showing_form
        );

        // -- Get the buttons
        const yes_btn = modal_wrap.querySelector('.yes') as HTMLButtonElement,
            no_btn = modal_wrap.querySelector('.no') as HTMLButtonElement;

        var time_field = modal_wrap.querySelector(".form-control[name='time']") as HTMLInputElement;
        var venue_field = modal_wrap.querySelector(".form-control[name='venue']") as HTMLInputElement;
        var country_field = modal_wrap.querySelector(".form-select[name='country']") as HTMLInputElement;
        var city_field = modal_wrap.querySelector(".form-control[name='city']") as HTMLInputElement;
    
        // -- Add the event listeners
        yes_btn.addEventListener('click', async(evt) => {
            if (validate_showing_details(country_field.value, city_field.value, venue_field.value, time_field.valueAsDate)) {
                add_showing(country_field.value, city_field.value, venue_field.value, time_field.value);
                modal_wrap.remove();
            }
        });

        no_btn.addEventListener('click', async() => {
            modal_wrap.remove();
        });

        // -- Append the modal to the body
        document.body.appendChild(modal_wrap);
    });

}

// Functions managing physical list of ticket listings.

function set_showings(listings: Showing[]) {
    showings_panel.innerHTML = "";

    for (var listing of listings) {
        append_showing(listing);
    }
}

function remove_showing(sid: string) {
    showings_panel.querySelector(".listing-row[data-sid=\"" + sid + "\"]").remove();
}

function append_showing(showing: Showing) {
    showings_panel.appendChild(showing_html(showing));

    const btn = showings_panel.querySelector(`.remove-showing-btn[data-sid="${showing.showing_id}"]`);
    btn.addEventListener("click", () => {
        del_showing(showing.showing_id);
    });
        
    var add_ticket_btn = showings_panel.querySelector(`.add-live-ticket`);
    
    manage_add_live_ticket_btn(add_ticket_btn, showing.showing_id);
}

// API calls

export async function query_showings() {
    const response = await get_evt_showings(configuration.event_id);

    // -- Check if the request was successful
    if (response.code !== 200) return create_toast(
        'error', 'Oops!',
        'There was an error while trying to get event showings, please try again later.'
    )

    const data = (response as GetShowingsSuccess).data
    set_showings(data.showings);
}

async function add_showing(
    country: string,
    city: string,
    venue: string,
    time: string
) {
    const request = await add_evt_showing(configuration.event_id, country, city, venue, time);

    // -- Check if the request was successful
    if (request.code !== 200) return create_toast(
        'error', 'Oops!',
        'There was an error while trying to add event showing, please try again later.'
    )

    const data = (request as AddShowingSuccess).data
    append_showing(data.showing);
    create_toast('success', 'Event', 'Added new event showing successfully.')
}

async function del_showing(sid: string) {
    const request = await del_evt_showing(configuration.event_id, sid);

    // -- Check if the request was successful
    if (request.code !== 200)
        return create_toast(
            'error', 'Oops!',
            'There was an error while trying to remove event showing, please try again later.'
        )

    remove_showing(sid);

    create_toast(
        'success', 'Event',
        'Removed event showing.'
    )
}


// HTML generation

function showing_html(
    showing: Showing
) : HTMLElement {
    const row = document.createElement('div');
    row.className = "row m-1 listing-row";
    row.setAttribute("data-sid", showing.showing_id);

    let formatted_location = '';
    if (showing.venue.length > 0) formatted_location = `${showing.venue} - ${showing.city}`;
    else formatted_location = `${showing.city}`;
    

    row.innerHTML = `
        <div class='showing-area'>
            <div class="showing-text">
                <p class="m-0">${showing.time}</p>
                <p class="m-0">${formatted_location}</p>
                <p>${showing.country}</p>
            </div>

            <div class="showing-tickets" data-sid="${showing.showing_id}"></div>

            <div class="btn-group showing-button">
                <div class="remove-showing-btn btn error" data-sid="${showing.showing_id}">
                    Delete Showing
                </div>

                <div class="add-live-ticket btn success" data-sid="${showing.showing_id}">
                    Add Ticket
                </div>
            </div>
        </div>
    `

    return row;
}

function validate_showing_details(country: string, city: string, venue: string, time: Date) : boolean {
    if (time == null) {
        create_toast(
            'error', 'Oops!',
            'Please enter a date and time for your showing.'
        );
        return false;
    }

    if (city.length == 0) {
        create_toast(
            'error', 'Oops!',
            'Please enter a city for your showing.'
        );
        return false;
    }

    if (country.length == 0) {
        create_toast(
            'error', 'Oops!',
            'Please select a country for your showing.'
        );
        return false;
    }

    return true;
}


const add_showing_form = `
    <form class="form-class form-layout" action="" method="POST" enctype="multipart/form-data">
        <div id="div_id_time" class="mb-3">
            <label for="id_time" class="form-label requiredField">Time<span class="asteriskField">*</span> </label>
            <input type="datetime-local" name="time" class="form-control datetimeinput" required="" id="id_time">
        </div>

        <div id="div_id_venue" class="mb-3">
            <label for="id_venue" class="form-label">Venue</label>
            <input type="text" name="venue" maxlength="50" class="textinput textInput form-control" id="id_venue">
        </div>

        <div id="div_id_city" class="mb-3">
            <label for="id_city" class="form-label">City</label>
            <input type="text" name="city" maxlength="25" class="textinput textInput form-control" id="id_city">
        </div>

        <div id="div_id_country" class="mb-3">
            <label for="id_country" class="form-label requiredField">Country<span class="asteriskField">*</span></label>
            <select name="country" class="lazyselect form-select" required="" id="id_country">
                <option value="" selected="">---------</option>
                <option value="AF">Afghanistan</option> <option value="AX">Åland Islands</option> <option value="AL">Albania</option> <option value="DZ">Algeria</option> <option value="AS">American Samoa</option> <option value="AD">Andorra</option> <option value="AO">Angola</option> <option value="AI">Anguilla</option> <option value="AQ">Antarctica</option> <option value="AG">Antigua and Barbuda</option> <option value="AR">Argentina</option> <option value="AM">Armenia</option> <option value="AW">Aruba</option> <option value="AU">Australia</option> <option value="AT">Austria</option> <option value="AZ">Azerbaijan</option> <option value="BS">Bahamas</option> <option value="BH">Bahrain</option> <option value="BD">Bangladesh</option> <option value="BB">Barbados</option> <option value="BY">Belarus</option> <option value="BE">Belgium</option> <option value="BZ">Belize</option> <option value="BJ">Benin</option> <option value="BM">Bermuda</option> <option value="BT">Bhutan</option> <option value="BO">Bolivia</option> <option value="BQ">Bonaire, Sint Eustatius and Saba</option> <option value="BA">Bosnia and Herzegovina</option> <option value="BW">Botswana</option> <option value="BV">Bouvet Island</option> <option value="BR">Brazil</option> <option value="IO">British Indian Ocean Territory</option> <option value="BN">Brunei</option> <option value="BG">Bulgaria</option> <option value="BF">Burkina Faso</option> <option value="BI">Burundi</option> <option value="CV">Cabo Verde</option> <option value="KH">Cambodia</option> <option value="CM">Cameroon</option> <option value="CA">Canada</option> <option value="KY">Cayman Islands</option> <option value="CF">Central African Republic</option> <option value="TD">Chad</option> <option value="CL">Chile</option> <option value="CN">China</option> <option value="CX">Christmas Island</option> <option value="CC">Cocos (Keeling) Islands</option> <option value="CO">Colombia</option> <option value="KM">Comoros</option> <option value="CG">Congo</option> <option value="CD">Congo (the Democratic Republic of the)</option> <option value="CK">Cook Islands</option> <option value="CR">Costa Rica</option> <option value="CI">Côte d'Ivoire</option> <option value="HR">Croatia</option> <option value="CU">Cuba</option> <option value="CW">Curaçao</option> <option value="CY">Cyprus</option> <option value="CZ">Czechia</option> <option value="DK">Denmark</option> <option value="DJ">Djibouti</option> <option value="DM">Dominica</option> <option value="DO">Dominican Republic</option> <option value="EC">Ecuador</option> <option value="EG">Egypt</option> <option value="SV">El Salvador</option> <option value="GQ">Equatorial Guinea</option> <option value="ER">Eritrea</option> <option value="EE">Estonia</option> <option value="SZ">Eswatini</option> <option value="ET">Ethiopia</option> <option value="FK">Falkland Islands (Malvinas)</option> <option value="FO">Faroe Islands</option> <option value="FJ">Fiji</option> <option value="FI">Finland</option> <option value="FR">France</option> <option value="GF">French Guiana</option> <option value="PF">French Polynesia</option> <option value="TF">French Southern Territories</option> <option value="GA">Gabon</option> <option value="GM">Gambia</option> <option value="GE">Georgia</option> <option value="DE">Germany</option> <option value="GH">Ghana</option> <option value="GI">Gibraltar</option> <option value="GR">Greece</option> <option value="GL">Greenland</option> <option value="GD">Grenada</option> <option value="GP">Guadeloupe</option> <option value="GU">Guam</option> <option value="GT">Guatemala</option> <option value="GG">Guernsey</option> <option value="GN">Guinea</option> <option value="GW">Guinea-Bissau</option> <option value="GY">Guyana</option> <option value="HT">Haiti</option> <option value="HM">Heard Island and McDonald Islands</option> <option value="VA">Holy See</option> <option value="HN">Honduras</option> <option value="HK">Hong Kong</option> <option value="HU">Hungary</option> <option value="IS">Iceland</option> <option value="IN">India</option> <option value="ID">Indonesia</option> <option value="IR">Iran</option> <option value="IQ">Iraq</option> <option value="IE">Ireland</option> <option value="IM">Isle of Man</option> <option value="IL">Israel</option> <option value="IT">Italy</option> <option value="JM">Jamaica</option> <option value="JP">Japan</option> <option value="JE">Jersey</option> <option value="JO">Jordan</option> <option value="KZ">Kazakhstan</option> <option value="KE">Kenya</option> <option value="KI">Kiribati</option> <option value="KW">Kuwait</option> <option value="KG">Kyrgyzstan</option> <option value="LA">Laos</option> <option value="LV">Latvia</option> <option value="LB">Lebanon</option> <option value="LS">Lesotho</option> <option value="LR">Liberia</option> <option value="LY">Libya</option> <option value="LI">Liechtenstein</option> <option value="LT">Lithuania</option> <option value="LU">Luxembourg</option> <option value="MO">Macao</option> <option value="MG">Madagascar</option> <option value="MW">Malawi</option> <option value="MY">Malaysia</option> <option value="MV">Maldives</option> <option value="ML">Mali</option> <option value="MT">Malta</option> <option value="MH">Marshall Islands</option> <option value="MQ">Martinique</option> <option value="MR">Mauritania</option> <option value="MU">Mauritius</option> <option value="YT">Mayotte</option> <option value="MX">Mexico</option> <option value="FM">Micronesia (Federated States of)</option> <option value="MD">Moldova</option> <option value="MC">Monaco</option> <option value="MN">Mongolia</option> <option value="ME">Montenegro</option> <option value="MS">Montserrat</option> <option value="MA">Morocco</option> <option value="MZ">Mozambique</option> <option value="MM">Myanmar</option> <option value="NA">Namibia</option> <option value="NR">Nauru</option> <option value="NP">Nepal</option> <option value="NL">Netherlands</option> <option value="NC">New Caledonia</option> <option value="NZ">New Zealand</option> <option value="NI">Nicaragua</option> <option value="NE">Niger</option> <option value="NG">Nigeria</option> <option value="NU">Niue</option> <option value="NF">Norfolk Island</option> <option value="KP">North Korea</option> <option value="MK">North Macedonia</option> <option value="MP">Northern Mariana Islands</option> <option value="NO">Norway</option> <option value="OM">Oman</option> <option value="PK">Pakistan</option> <option value="PW">Palau</option> <option value="PS">Palestine, State of</option> <option value="PA">Panama</option> <option value="PG">Papua New Guinea</option> <option value="PY">Paraguay</option> <option value="PE">Peru</option> <option value="PH">Philippines</option> <option value="PN">Pitcairn</option> <option value="PL">Poland</option> <option value="PT">Portugal</option> <option value="PR">Puerto Rico</option> <option value="QA">Qatar</option> <option value="RE">Réunion</option> <option value="RO">Romania</option> <option value="RU">Russia</option> <option value="RW">Rwanda</option> <option value="BL">Saint Barthélemy</option> <option value="SH">Saint Helena, Ascension and Tristan da Cunha</option> <option value="KN">Saint Kitts and Nevis</option> <option value="LC">Saint Lucia</option> <option value="MF">Saint Martin (French part)</option> <option value="PM">Saint Pierre and Miquelon</option> <option value="VC">Saint Vincent and the Grenadines</option> <option value="WS">Samoa</option> <option value="SM">San Marino</option> <option value="ST">Sao Tome and Principe</option> <option value="SA">Saudi Arabia</option> <option value="SN">Senegal</option> <option value="RS">Serbia</option> <option value="SC">Seychelles</option> <option value="SL">Sierra Leone</option> <option value="SG">Singapore</option> <option value="SX">Sint Maarten (Dutch part)</option> <option value="SK">Slovakia</option> <option value="SI">Slovenia</option> <option value="SB">Solomon Islands</option> <option value="SO">Somalia</option> <option value="ZA">South Africa</option> <option value="GS">South Georgia and the South Sandwich Islands</option> <option value="KR">South Korea</option> <option value="SS">South Sudan</option> <option value="ES">Spain</option> <option value="LK">Sri Lanka</option> <option value="SD">Sudan</option> <option value="SR">Suriname</option> <option value="SJ">Svalbard and Jan Mayen</option> <option value="SE">Sweden</option> <option value="CH">Switzerland</option> <option value="SY">Syria</option> <option value="TW">Taiwan</option> <option value="TJ">Tajikistan</option> <option value="TZ">Tanzania</option> <option value="TH">Thailand</option> <option value="TL">Timor-Leste</option> <option value="TG">Togo</option> <option value="TK">Tokelau</option> <option value="TO">Tonga</option> <option value="TT">Trinidad and Tobago</option> <option value="TN">Tunisia</option> <option value="TR">Türkiye</option> <option value="TM">Turkmenistan</option> <option value="TC">Turks and Caicos Islands</option> <option value="TV">Tuvalu</option> <option value="UG">Uganda</option> <option value="UA">Ukraine</option> <option value="AE">United Arab Emirates</option> <option value="GB">United Kingdom</option> <option value="UM">United States Minor Outlying Islands</option> <option value="US">United States of America</option> <option value="UY">Uruguay</option> <option value="UZ">Uzbekistan</option> <option value="VU">Vanuatu</option> <option value="VE">Venezuela</option> <option value="VN">Vietnam</option> <option value="VG">Virgin Islands (British)</option> <option value="VI">Virgin Islands (U.S.)</option> <option value="WF">Wallis and Futuna</option> <option value="EH">Western Sahara</option> <option value="YE">Yemen</option> <option value="ZM">Zambia</option> <option value="ZW">Zimbabwe</option>
            </select> 
        </div>
    </form>
`;