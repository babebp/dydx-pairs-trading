import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from constants import MAX_HALF_LIFE, WINDOW

"""
Calculate Half Life
https://www.pythonforfinance.net/2016/05/09/python-backtesting-mean-reversion-part-2/
"""
def calculate_half_life(spread):
    df_spread = pd.DataFrame(spread, columns=['spread'])
    spread_lag = df_spread['spread'].shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]
    spread_return = df_spread['spread'] - spread_lag
    spread_return.iloc[0] = spread_return.iloc[1]
    spread_lag2 = sm.add_constant(spread_lag)
    model = sm.OLS(spread_return, spread_lag2)
    res = model.fit()
    half_life = round(-np.log(2) / res.params[1], 0)
    return half_life

# Calculate Z-Score
def calculate_zscore(spread):
    spread_series = pd.Series(spread)
    mean = spread_series.rolling(center=False, window=WINDOW).mean()
    std = spread_series.rolling(center=False, window=WINDOW).std()
    x = spread_series.rolling(center=False, window=1).mean()
    zscore = (x - mean) / std
    return zscore

# Calculate cointegration
def calculate_cointegration(series1, series2):
    series1 = np.array(series1).astype(np.float64)
    series2 = np.array(series2).astype(np.float64)
    coint_flag = 0
    coint_res = coint(series1, series2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]
    model = sm.OLS(series1, series2).fit()
    hedge_ratio = model.params[0]
    spread = series1 - (hedge_ratio * series2)
    half_life = calculate_half_life(spread)
    t_check = coint_t < critical_value  # t < critical value
    coint_flag = 1 if p_value < 0.05 and t_check else 0
    return coint_flag, hedge_ratio, half_life

# Store cointegration results
def store_cointegration_results(df_market_prices):

    # Initialize
    markets = df_market_prices.columns.to_list()
    criteria_met_pairs = []

    # Find cointegrated pairs
    # Start with our base pairs
    for index, base_market in enumerate(markets[:-1]):
        series_1 = df_market_prices[base_market].values.astype(float).tolist()

        # Get quote pairs
        for quote_market in markets[index+1:]:
            series_2 = df_market_prices[quote_market].values.astype(float).tolist()

            # Check cointegration
            coint_flag, hedge_ratio, half_life = calculate_cointegration(series_1, series_2)

            # Log pairs
            if coint_flag == 1 and half_life <= MAX_HALF_LIFE and half_life > 0:
                criteria_met_pairs.append({
                    "base_market": base_market,
                    "quote_market": quote_market,
                    "hedge_ratio": hedge_ratio,
                    "half_life": half_life,
                })

    # Create and save DataFrame
    df_criteria_met = pd.DataFrame(criteria_met_pairs)
    df_criteria_met.to_csv('cointegrated_pairs.csv')
    del df_criteria_met

    print('Cointegrated pairs successfully saved')
    return "saved"