document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('submitBtn');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('onPress', function(event) {
        event.preventDefault();
        const income = document.getElementById('salary').value;
        console.log(income)
        resultsDiv.innerHTML = '';
        fetch('/run-script', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ salary: income })
        })
        .then(response => response.json())
        .then(data => {
             // Clear previous results

            if (data.top_5_stocks && data.top_5_stocks.length > 0) {
                // Print details for the first 4 stocks
                data.top_5_stocks.slice(0, 4).forEach(stock => {
                    const stockDiv = document.createElement('div');
                    stockDiv.className = 'stock-details';
                    stockDiv.innerHTML = `
                        <h2>${stock.symbol}</h2>
                        <p>Combined Score: ${stock.combined_score}</p>
                        <p>Mean Close Price: ${stock.mean_close_price}</p>
                        <p>Mean Volume: ${stock.mean_volume}</p>
                        <canvas id="chart-${stock.symbol}" class="stock-chart"></canvas>
                    `;
                    resultsDiv.appendChild(stockDiv);

                    // Create chart for stock
                    const forecastedPrices = stock.forecasted_prices;
                    if (forecastedPrices) {
                        const ctx = document.getElementById(`chart-${stock.symbol}`).getContext('2d');
                        new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: Array.from({ length: forecastedPrices.length }, (_, i) => `Day ${i + 1}`),
                                datasets: [{
                                    label: 'Forecasted Prices',
                                    data: forecastedPrices,
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 2,
                                    fill: false
                                }]
                            },
                            options: {
                                scales: {
                                    x: {
                                        beginAtZero: true
                                    },
                                    y: {
                                        beginAtZero: false
                                    }
                                }
                            }
                        });
                    } else {
                        console.warn(`No forecasted data available for stock symbol: ${stock.symbol}`);
                    }
                });

                // Print details for the fifth stock
                const fifthStock = data.top_5_stocks[4];
                if (fifthStock) {
                    const fifthStockDiv = document.createElement('div');
                    fifthStockDiv.className = 'stock-details';
                    fifthStockDiv.innerHTML = `
                        <h2>${fifthStock.symbol}</h2>
                        <p>Combined Score: ${fifthStock.combined_score}</p>
                        <p>Mean Close Price: ${fifthStock.mean_close_price}</p>
                        <p>Mean Volume: ${fifthStock.mean_volume}</p>
                        <canvas id="chart-${fifthStock.symbol}" class="stock-chart"></canvas>
                    `;
                    resultsDiv.appendChild(fifthStockDiv);

                    // Create chart for fifth stock
                    const forecastedPrices = fifthStock.forecasted_prices;
                    if (forecastedPrices) {
                        const ctx = document.getElementById(`chart-${fifthStock.symbol}`).getContext('2d');
                        new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: Array.from({ length: forecastedPrices.length }, (_, i) => `Day ${i + 1}`),
                                datasets: [{
                                    label: 'Forecasted Prices',
                                    data: forecastedPrices,
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 2,
                                    fill: false
                                }]
                            },
                            options: {
                                scales: {
                                    x: {
                                        beginAtZero: true
                                    },
                                    y: {
                                        beginAtZero: false
                                    }
                                }
                            }
                        });
                    } else {
                        console.warn(`No forecasted data available for stock symbol: ${fifthStock.symbol}`);
                    }
                }
            } else {
                resultsDiv.innerHTML = '<p>No stock data available.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultsDiv.innerHTML = '<p>Error fetching data.</p>';
        });
    });
});
