import { LoginHistory } from '../index.d';

export default (
    data: LoginHistory,
): HTMLDivElement => {
    const elm = `
        <div class="w-100 p-2 mb-2 rounded" style="background-color: var(--theme-color);">
            <div class="w-100 container d-flex justify-content-between align-items-center mb-1">
                <!-- Date added -->
                <p class="text-muted col-12 m-0">
                    On ${data.date} at ${data.time.split('.')[0]}
                </p>
            </div>

            <div class="w-100 container d-flex justify-content-between align-items-center">
                <!-- Provider IP -->
                <p class="col-6 text-muted m-0">
                    IP: ${data.ip}
                </p>

                <!-- Method -->
                <p class="text-muted col-6 m-0">
                    Method: ${data.method}
                </p>
            </div>

        </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = elm;

    // -- Return the element
    return div;
};