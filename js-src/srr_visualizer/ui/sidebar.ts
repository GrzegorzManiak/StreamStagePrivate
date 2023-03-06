import { 
    Chart
} from "frappe-charts"

// -- CPU / RAM / DISK / NETWORK CHART
export function construct_graph(io_chart_elm: HTMLElement) {
    const data = {
        datasets: [
            {
                name: "CPU", type: "line",
                values: [25, 40, 30, 35, 8, 52, 17, 4]
            },
            {
                name: "RAM", type: "line",
                values: [25, 50, 10, 15, 18, 32, 27, 14]
            }
        ],
        labels: ["12am-3am", "3am-6am", "6am-9am", "9am-12pm"]
    }
    
    const chart = new Chart(io_chart_elm, {
        data: data,
        type: 'axis-mixed', // or 'bar', 'line', 'pie', 'percentage'
    })


    // -- Add data
    chart.update_values(0, [25, 40, 30, 35, 8, 52, 17, 4]);
}