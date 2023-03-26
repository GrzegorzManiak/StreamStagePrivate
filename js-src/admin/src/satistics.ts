import { Frame, Pod, StatisticsSuccess } from '../index.d';
import { get_statistics } from '../api';

// line chart from chart.js
import { Chart, LineElement, LineController, LinearScale, CategoryScale, PointElement } from 'chart.js';
import { create_toast } from '../../common';
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

    // -- group the pods
    const pods = [
        accounts
        // , server,
        // cash_flow, tickets,
        // reviews, subscriptions,
        // viewers
    ];

    // -- Build the graphs
    pods.forEach(async (pod: Pod) => 
        build_graphs(pod));
}


export async function build_graphs(
    pod: Pod,
) {

    // -- Get the graphs element
    const graphs = pod.panel.element.querySelector('.graphs'),
        stat_group = graphs.getAttribute('data-stat-group'),
        stats = graphs.querySelectorAll('.data-chart');

    // -- Get the statistics
    Array.from(stats).forEach(async (stat: HTMLDivElement) => {

        const type = stat.getAttribute('data-stat-id'),
            pretty_name = stat.getAttribute('data-pretty'),
            description = stat.getAttribute('data-description');

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
                        <option value="minute">Minutes</option>
                        <option value="hour">Hours</option>
                        <option value="day" selected>Days</option>
                        <option value="week">Weeks</option>
                        <option value="month">Months</option>
                        <option value="year">Years</option>
                    </select>
                </div>

                <div class='w-50'>
                    <label class="form-label" for="scale">Scale</label>
                    <input
                        type="text"
                        inputmode="numeric"
                        pattern="[0-9]*"
                        name="scale"
                        id="scale"
                        class="form-control w-100 inp"
                        value="7"
                    />
                </div>
            </div>


            <div class="data-chart-container"> </div>
        `;

        stat.innerHTML = template;
        const container = stat.querySelector('.data-chart-container');
            
        // -- Create the chart
        const ctx = document.createElement('canvas');
        container.appendChild(ctx);

        // -- Get the statistics
        const statistics = get_statistics(
            stat_group, type, 7, 0, 'day'
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
        const scale = stat.querySelector('#scale') as HTMLInputElement,
            frame = stat.querySelector('#frame') as HTMLSelectElement;

        async function update_graph() {
            const statistics = get_statistics(
                stat_group, type, +scale.value, 0, frame.value as Frame
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

        scale.addEventListener('change', update_graph);
        frame.addEventListener('change', update_graph);

        // -- Update the graph every 5 minutes
        setInterval(update_graph, 1000 * 60 * 5);
    });
}