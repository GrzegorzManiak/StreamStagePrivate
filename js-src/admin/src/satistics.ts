import { Frame, Pod, StatisticsSuccess } from '../index.d';
import { get_statistics } from '../api';

// line chart from chart.js
import { Chart, LineElement, LineController, LinearScale, CategoryScale, PointElement } from 'chart.js';
import { attach, create_toast } from '../../common';
import { add_callback } from './panels';
Chart.register(LineElement, LineController, LinearScale, CategoryScale, PointElement);

export async function manage_statistical_panels(
    accounts: Pod,
    server: Pod,
    cash_flow: Pod,
    tickets: Pod,
    reviews: Pod,
    subscriptions: Pod,
    viewers: Pod
) {
    // -- The settle down period for the window resize event
    const RESIZE_TIMEOUT = 1000;

    // -- group the pods
    const pods = [
        accounts, server,
        cash_flow, tickets,
        subscriptions,
        // viewers, reviews
    ];

    pods.forEach(async (pod: Pod) => {
        let built = false;

        // -- Attach the event listeners
        add_callback(async(panel_type) => {
            let resize = () => {}
            if (panel_type == pod.panel.type && !built) {
                console.log('building graphs', pod.panel.type);
                resize = await build_graphs(pod);
                built = true;
            }

            // -- Attach a windows resize listener
            //    And wait till the window is done resizing 
            //    before rebuilding the graphs
            let last_resize = 0;
            window.addEventListener('resize', async () => {
                last_resize = Date.now();
                setTimeout(async () => {
                    // -- If the last resize was more than 1 second ago
                    //    Then rebuild the graphs
                    if (Date.now() - last_resize < RESIZE_TIMEOUT) return;
                    console.log('rebuilding graphs', pod.panel.type);
                    resize();
                }, RESIZE_TIMEOUT);
            });
        });
    });
}


export async function build_graphs(
    pod: Pod,
): Promise<() => void> {

    // -- Get the graphs element
    const graphs = pod.panel.element.querySelector('.graphs'),
        stat_group = graphs.getAttribute('data-stat-group'),
        stats = graphs.querySelectorAll('.data-chart');

    let built_graphs: Array<Chart<"line", any[], any>> = [];

    // -- Get the statistics
    Array.from(stats).forEach(async (stat: HTMLDivElement) => {

        const type = stat.getAttribute('data-stat-id'),
            pretty_name = stat.getAttribute('data-pretty'),
            description = stat.getAttribute('data-description'),
            def_scale = stat.getAttribute('def-scale'),
            def_frame = stat.getAttribute('def-frame');

        // -- load in the template
        const template = `
            <div class="data-chart-info">
                <h3>${pretty_name}</h3>
                <p>${description}</p>
            </div>

            <!-- FIlters -->
            <div class='
                mb-1
                d-flex
                graph-filters
                gap-2
                w-100
            '>  
                <div class='w-50'>
                    <label class="form-label" for="frame">Frame</label>
                    <select 
                        name="frame" 
                        id="frame" 
                        class="form-select w-100 inp"
                    >   
                        <option value="seconds">Seconds</option>
                        <option value="minute">Minutes</option>
                        <option value="hour">Hours</option>
                        <option value="day" selected>Days</option>
                        <option value="week">Weeks</option>
                        <option value="month">Months</option>
                        <option value="year">Years</option>
                    </select>
                </div>

                <div class='w-25'>
                    <label class="form-label" for="from">From</label>
                    <input
                        type="text"
                        inputmode="numeric"
                        pattern="[0-9]*"
                        name="from"
                        id="from"
                        class="form-control w-100 inp"
                        value="0"
                    />
                </div>

                <div class='w-25'>
                    <label class="form-label" for="to">To</label>
                    <input
                        type="text"
                        inputmode="numeric"
                        pattern="[0-9]*"
                        name="to"
                        id="to"
                        class="form-control w-100 inp"
                        value="7"
                    />
                </div>
            </div>


            <div class="data-chart-container"> </div>

            <div class='w-100 btn-group'>
                <button type="submit" id="export-btn" class="btn btn-primary mb-3 btn-slim w-100 info loader-btn mt-2" loader-state="default">   
                    <span>
                        <div class="spinner-border" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </span>
                    <p>Export</p>
                </button>

                <button type="submit" id="save-btn" class="btn btn-success mb-3 btn-slim w-100 success loader-btn mt-2" loader-state="default">   
                    <span>
                        <div class="spinner-border" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </span>
                    <p>Save Graph</p>
                </button>
            </div>
        `;

        stat.innerHTML = template;
        const container = stat.querySelector('.data-chart-container'),
            export_btn = stat.querySelector('#export-btn'),
            save_btn = stat.querySelector('#save-btn');
            
        // -- Create the chart
        const ctx = document.createElement('canvas');
        container.appendChild(ctx);

        // -- Get the statistics
        const statistics = get_statistics(
            stat_group, type, Number(def_scale), 0, def_frame as Frame
        ) as Promise<StatisticsSuccess>;
        
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                // -- Empty data
                labels: [],
                datasets: [{
                    label: pretty_name,
                    data: [],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                resizeDelay: 100,
                aspectRatio: 1,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        built_graphs.push(chart);

        // -- Make sure that the request came back good
        if ((await statistics).code === 200) {
            const data = (await statistics).data;
            chart.data.labels = data.labels;
            chart.data.datasets[0].data = data.data;
            chart.update();
        }

        else create_toast('error', 'Error',
            'There was an error getting the statistics')


        // -- Add the event listeners
        const from = stat.querySelector('#from') as HTMLInputElement,
            to = stat.querySelector('#to') as HTMLInputElement,
            frame = stat.querySelector('#frame') as HTMLSelectElement;

        // -- Set the default values
        to.value = def_scale;
        frame.value = def_frame;

        from.addEventListener('change', () => update_graph(
            chart, stat_group, type, Number(to.value), Number(from.value), frame.value as Frame));

        to.addEventListener('change', () => update_graph(
            chart, stat_group, type, Number(to.value), Number(from.value), frame.value as Frame));
        
        frame.addEventListener('change', () => update_graph(
            chart, stat_group, type, Number(to.value), Number(from.value), frame.value as Frame));
        

        // -- Export the data
        export_btn.addEventListener('click', () => {
            const stop = attach(export_btn as HTMLButtonElement);
            export_chart(chart, pretty_name);
            stop();
        });

        save_btn.addEventListener('click', () => {
            const stop = attach(save_btn as HTMLButtonElement);
            save_chart(chart, pretty_name);
            stop();
        });


        // -- Update the graph every x time
        setInterval(() => update_graph(
            chart, stat_group, type, Number(to.value), Number(from.value), frame.value as Frame), 
            get_sleep_interval(frame.value as Frame)
        );
    });


    // -- This function when called just resizes the chart to fit the container
    return () => {
        built_graphs.forEach(chart => chart.resize());
    }
}



/**
 * @name update_graph
 * @description Updates the graph
 * @param {Chart} chart
 * @param {string} stat_group
 * @param {string} type
 * @param {number} scale
 * @param {number} offset
 * @param {Frame} frame
 * @returns {Promise<void>}
 */
export async function update_graph(
    chart: Chart,
    stat_group: string,
    type: string,
    scale: number,
    offset: number,
    frame: Frame,
) {
    const statistics = get_statistics(
        stat_group, type, scale, offset, frame
    ) as Promise<StatisticsSuccess>;

    if ((await statistics).code === 200) {
        const data = (await statistics).data;
        chart.data.labels = data.labels;
        chart.data.datasets[0].data = data.data;
        chart.update();
    }

    else create_toast('error', 'Error',
        'There was an error getting the statistics')
}



/**
 * @name export_chart
 * @description Exports the chart and saves it as a csv
 * @param {Chart} chart
 * @param {string} name
 * @returns {Promise<void>}
 */
export async function export_chart(chart: Chart, name: string) {
    let csv = 'data:text/csv;charset=utf-8,';
    csv += chart.data.labels.join(',') + '\n';
    csv += chart.data.datasets[0].data.join(',');

    const encodedUri = encodeURI(csv),
        link = document.createElement('a');
    
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `${name}-${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}



/**
 * @name get_sleep_interval
 * @description Gets the sleep interval based 
 * on the frame type
 * @param {Frame} frame
 * @returns {number} ms
 */
export function get_sleep_interval(frame: Frame): number {
    switch(frame) {
        case 'seconds': return 1000 * 10; // -- 15 seconds
        case 'minute': return 1000 * 50; // -- 50 seconds
        case 'hour': return 1000 * 60 * 5; // -- 5 minutes
        case 'day': return 1000 * 60 * 15 // -- 15 minutes
        case 'week': return 1000 * 60 * 60 // -- 1 hour
        case 'month': return 1000 * 60 * 60 * 2 // -- 2 hours
        case 'year': return 1000 * 60 * 60 * 6 // -- 6 hours
    }
}



/**
 * @name save_chart
 * @description Exports the chart and saves it as a csv
 * @param {Chart} chart
 * @param {string} name
 * @returns {Promise<void>}
 */
export async function save_chart(chart: Chart, name: string) {
    const link = document.createElement('a');    
    link.setAttribute('href', chart.toBase64Image());
    link.setAttribute('download', `${name}-${Date.now()}.png`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
