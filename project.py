import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime
from tabulate import tabulate

import warnings

warnings.filterwarnings("ignore")

def main():
    print('We are going to make an automatic exploratory analysis.')

    stock = input('Stock code: ') + '.SA'
    while not is_valid_stock_code(stock):
        print('Invalid stock code. Please, try again.')
        stock = input('Stock code: ') + '.SA'

    money = int(input('How much money for investment? $'))
    while not is_valid_money(money):
        print('Invalid amount. Please, try again.')
        money = int(input('How much money for investment? $'))

    time = input("Period (YYYY-MM-DD to YYYY-MM-DD): ")
    while not is_valid_date(time):
        print('Please, try again.')
        time = input("Period (YYYY-MM-DD to YYYY-MM-DD): ")

    start, end = time.split(' to ')

    # Downloading stock data
    dados = yf.download(stock, start=start, end=end)['Close']

    # Verifying the data
    if dados.empty:
        print("No data found for the given period. Please try another range.")
    else:
        # Calculating the portfolio value through the time
        value_portfolio = dados * (money / dados.iloc[0])

        # Calculate the SMA (50-period by default)
        sma_period = 50
        sma = value_portfolio.rolling(window=sma_period).mean()

        # Calculating daily returns
        daily_returns = dados.pct_change().dropna()

        # Calculate risk metrics
        volatility, var_95, drawdowns = calculate_risk_metrics(value_portfolio, daily_returns)

        final_data = {
            'Metric': ['Initial Investment', 'Final Value', 'Return', 'Annualized Volatility',
                    'Value at Risk (95% confidence)', 'Maximum Drawdown'],
            'Value': [
                f'${money:,.2f}',
                f'${float(value_portfolio.iloc[-1]):,.2f}',
                f'{((float(value_portfolio.iloc[-1]) - money) / money * 100):.2f}%',
                f'{volatility.iloc[0]:.2%}',
                f'{var_95:.2%}',
                f'{drawdowns.iloc[0]:.2%}']}


        # Generating the graph
        plt.figure(figsize=(15, 8))

        # Plotting the original portfolio value
        plt.plot(value_portfolio, linewidth=2, color='#2E86C1', label='Portfolio Value')

        # Plotting the SMA
        plt.plot(sma, linewidth=2, color='#F39C12', label=f'SMA ({sma_period} periods)')

        # Title and labels
        plt.title(f'Evolution through time starting with ${money}', fontsize=14, pad=20)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Value ($)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Formating the values on the y-axis
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R${int(x):,}'))

        # Rotating the dates on the x-axis
        plt.xticks(rotation=45)

        # Adding a legend to differentiate between the portfolio value and SMA
        plt.legend(loc='best')

        # Layout adjustment
        plt.tight_layout()

        # Showing the graph
        plt.show()

        # DataFrame Creation
        df = pd.DataFrame(final_data)

        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))



        # Descriptive Statistics to understand the data
        print("\nDescriptive Statistics:")
        print(dados.describe())

def is_valid_stock_code(stock_code):
    try:
        # Tenta buscar com o código original
        ticker = yf.Ticker(stock_code)
        data = ticker.history(period="1d")
        if not data.empty:
            return True
        else:
          return False
    except Exception as e:
        return False

# Function to validate date
def is_valid_date(period):
    # Match the pattern for the date range
    matches = re.fullmatch(r'(\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})', period)

    if matches:
        date_start, date_end = matches.groups()

        try:
            # Parse the dates
            start_date = datetime.strptime(date_start, "%Y-%m-%d")
            end_date = datetime.strptime(date_end, "%Y-%m-%d")
            today = datetime.now()

            # Check if the start date is earlier than the end date
            if start_date > end_date:
                print("The start date must be earlier than the end date.")
                return False

            # Check if the dates are not in the future
            if start_date > today or end_date > today:
                print(f"Dates cannot be in the future. The maximum allowed date is {today.strftime('%Y-%m-%d')}.")
                return False

            return True

        except ValueError as e:
            print(f"Invalid date: {e}")
            return False
    else:
        print("Invalid date format. Use 'YYYY-MM-DD to YYYY-MM-DD'.")
        return False

def is_valid_money(money):
    try:
        money = int(money)
        if money <= 0:
            return False
        else:
            return True
    except ValueError:
        return False

def calculate_risk_metrics(value_portfolio, daily_returns):
    # Volatility (standard deviation)
    volatility = daily_returns.std() * np.sqrt(252)  # Annualized

    # Value at Risk (VaR) - 95% confidence
    var_95 = np.percentile(daily_returns, 5)

    # Calculate drawdowns
    rolling_max = value_portfolio.cummax()
    drawdowns = (value_portfolio / rolling_max - 1).min()

    return volatility, var_95, drawdowns


if __name__ == "__main__":
    main()
