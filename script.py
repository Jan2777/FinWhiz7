import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from nselib import capital_market
from datetime import datetime, timedelta
from tensorflow import keras
import json
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
# Get salary from command line argument
salary = float(sys.argv[1])

# Function to fetch one month's worth of data
def fetch_one_month_data(end_date_str):
    end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
    start_date = end_date - timedelta(days=30)

    df_all = pd.DataFrame()
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%d-%m-%Y')
        try:
            df_daily = pd.DataFrame(capital_market.bhav_copy_equities(date_str))
            df_all = pd.concat([df_all, df_daily], ignore_index=True)
        except Exception as e:
            print(f"Error fetching data for {date_str}: {e}")
        current_date += timedelta(days=1)

    df_all.reset_index(drop=True, inplace=True)
    return df_all

# Fetch one month's data
df = fetch_one_month_data('23-07-2024')

# Calculate additional metrics
df['PriceChange'] = df['ClsPric'] - df['PrvsClsgPric']
df['PctPriceChange'] = df['PriceChange'] / df['PrvsClsgPric'] * 100
df['HighLowSpread'] = df['HghPric'] - df['LwPric']

# Group by stock symbol and calculate mean values
stock_summary = df.groupby('TckrSymb').agg({
    'ClsPric': 'mean',
    'OpnPric': 'mean',
    'HghPric': 'mean',
    'LwPric': 'mean',
    'PrvsClsgPric': 'mean',
    'TtlNbOfTxsExctd': 'mean',
    'PriceChange': 'mean',
    'PctPriceChange': 'mean',
    'HighLowSpread': 'mean'
}).reset_index()

# Calculate volatility (standard deviation of closing prices)
volatility = df.groupby('TckrSymb')['ClsPric'].std().reset_index()
volatility.columns = ['TckrSymb', 'Volatility']
stock_summary = stock_summary.merge(volatility, on='TckrSymb', how='left')

# Normalize the scores
features_to_normalize = ['PctPriceChange', 'HighLowSpread', 'Volatility', 'TtlNbOfTxsExctd']
for feature in features_to_normalize:
    stock_summary[feature + 'Norm'] = (stock_summary[feature] - stock_summary[feature].min()) / (stock_summary[feature].max() - stock_summary[feature].min())

# Combined score (simple average of normalized scores)
stock_summary['CombinedScore'] = (stock_summary['PctPriceChangeNorm'] + stock_summary['HighLowSpreadNorm'] + stock_summary['VolatilityNorm'] + stock_summary['TtlNbOfTxsExctdNorm']) / 4

# Filter stocks based on salary
stock_summary = stock_summary[stock_summary['ClsPric'] <= salary]

# Get top 5 stocks based on combined score
top_5_stocks = stock_summary.nlargest(5, 'CombinedScore')

# Forecasting function using LSTM
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

def forecast_stock_prices(stock_df, time_step=10, forecast_days=10):
    if len(stock_df) < time_step + 1:
        print(f"Not enough data for stock: {stock_df['TckrSymb'].iloc[0]}")
        return None

    close_prices = stock_df['ClsPric'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_close_prices = scaler.fit_transform(close_prices)

    X, y = create_dataset(scaled_close_prices, time_step)
    if X.shape[0] == 0 or X.shape[1] == 0:
        print(f"Insufficient data to create dataset for stock: {stock_df['TckrSymb'].iloc[0]}")
        return None

    X = X.reshape(X.shape[0], X.shape[1], 1)

    # Split data
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Build LSTM model
    model = keras.Sequential()
    model.add(keras.layers.LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
    model.add(keras.layers.LSTM(50, return_sequences=False))
    model.add(keras.layers.Dense(25))
    model.add(keras.layers.Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=1, batch_size=1)

    # Forecasting next 10 days
    x_input = scaled_close_prices[-time_step:].reshape(1, -1)
    temp_input = list(x_input[0])
    lst_output = []

    for i in range(forecast_days):
        x_input = np.array(temp_input[-time_step:]).reshape(1, time_step, 1)
        yhat = model.predict(x_input, verbose=0)
        temp_input.append(yhat[0][0])
        lst_output.append(yhat[0][0])

    # Inverse transform to get actual forecasted prices
    lst_output = scaler.inverse_transform(np.array(lst_output).reshape(-1, 1))

    return lst_output

# Forecast next 10 days for each top stock
forecast_results = {}
for symbol in top_5_stocks['TckrSymb']:
    stock_df = df[df['TckrSymb'] == symbol]
    forecasted_prices = forecast_stock_prices(stock_df)
    if forecasted_prices is not None:
        forecast_results[symbol] = forecasted_prices.flatten().tolist()

# Prepare results in JSON format
results = {
    "top_5_stocks": [
        {
            "symbol": row['TckrSymb'],
            "combined_score": round(row['CombinedScore'], 2),
            "mean_close_price": round(row['ClsPric'], 2),
            "mean_volume": round(row['TtlNbOfTxsExctd'], 2),
            "forecasted_prices": forecast_results.get(row['TckrSymb'], [])
        }
        for index, row in top_5_stocks.iterrows()
    ]
}

# Save results to a JSON file
with open('results.json', 'w') as file:
    json.dump(results, file, indent=4)
