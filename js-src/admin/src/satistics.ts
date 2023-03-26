import { Pod, StatisticsSuccess } from '../index.d';
import { get_statistics } from '../api';

// line chart from chart.js
import { Chart, LineElement, LineController, LinearScale, CategoryScale, PointElement } from 'chart.js';
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
    console.log('Managing statistical panels');
    const login_stats = await get_statistics(
        'accounts',
        'login',
        2, 
        0,
        'day'
    ) as StatisticsSuccess;

    console.log(login_stats);

    // -- Create the chart
    const ctx = document.createElement('canvas');
    ctx.width = 250;
    ctx.height = 250;
    accounts.panel.element.appendChild(ctx);

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Logins',
                data: login_stats.data,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        }
    });

}