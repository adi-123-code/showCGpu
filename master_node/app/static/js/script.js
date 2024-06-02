document.addEventListener('DOMContentLoaded', function () {
    const maxDataPoints = 20; // 最大数据点数
    const cpuUsageChart = createChart('cpuUsageChart', 'CPU Usage (%)');
    const memoryUsageChart = createChart('memoryUsageChart', 'Memory Usage (%)');
    const gpuUsageChart = createChart('gpuUsageChart', 'GPU Usage (%)');
    const gpuMemoryUsageChart = createChart('gpuMemoryUsageChart', 'GPU Memory Usage (%)');

    const nodeColors = {};  // 用于存储每个节点的颜色

    function createChart(canvasId, label) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: []
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: 100
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 0  // 禁用动画
                }
            }
        });
    }

    function fetchData() {
        axios.get('/fetch_data').then(function (response) {
            const data = response.data;
            const timestamp = new Date().toLocaleTimeString();
            updateCharts(data, timestamp);
        });
    }

    function updateCharts(data, timestamp) {
        Object.keys(data).forEach((node, index) => {
            const nodeData = data[node];
            if (!nodeColors[node]) {  // 如果节点还没有颜色，分配一个颜色
                nodeColors[node] = getBorderColor(index);
            }
            // 更新图表，gpu_usage和gpu_memory_usage为一个数组，如何更新？

            // 检查gpu_usage和gpu_memory_usage是否是数组
            const gpuUsages = Array.isArray(nodeData.gpu_usage) ? nodeData.gpu_usage : [nodeData.gpu_usage];
            const gpuMemoryUsages = Array.isArray(nodeData.gpu_memory_usage) ? nodeData.gpu_memory_usage : [nodeData.gpu_memory_usage];

            // 为每个GPU添加数据
            gpuUsages.forEach((gpuUsage, gpuIndex) => {
                addDataToChart(gpuUsageChart, `${node} GPU ${gpuIndex}`, gpuUsage, timestamp, nodeColors[node]);
            });
            gpuMemoryUsages.forEach((gpuMemoryUsage, gpuIndex) => {
                addDataToChart(gpuMemoryUsageChart, `${node} GPU ${gpuIndex}`, gpuMemoryUsage, timestamp, nodeColors[node]);
            });

            addDataToChart(cpuUsageChart, node, nodeData.cpu_usage, timestamp, nodeColors[node]);
            addDataToChart(memoryUsageChart, node, nodeData.memory_usage, timestamp, nodeColors[node]);

        });
    }

    function addDataToChart(chart, nodeLabel, newData, newLabel, borderColor) {
        let dataset = chart.data.datasets.find(ds => ds.label === nodeLabel);
        if (!dataset) {
            dataset = {
                label: nodeLabel,
                data: [],
                borderColor: borderColor,
                fill: false,
                tension: 0.1
            };
            chart.data.datasets.push(dataset);
        }
        if (dataset.data.length >= maxDataPoints) {
            dataset.data.shift(); // 删除最早的数据点
        }
        dataset.data.push(newData);
        if (chart.data.labels.length >= maxDataPoints) {
            chart.data.labels.shift(); // 删除最早的标签
        }
        chart.data.labels.push(newLabel); // 添加新标签
        chart.update();
    }

    function getBorderColor(index) {
        const colors = ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 206, 86)', 'rgb(75, 192, 192)', 'rgb(153, 102, 255)'];
        return colors[index % colors.length];  // 循环使用颜色数组
    }

    fetchData();
    setInterval(fetchData, 1000);  // 每5秒更新一次数据
});
