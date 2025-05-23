import os
import requests
import pandas as pd
from lets_plot import ggplot, aes, geom_bar, coord_flip, ggsize, labs, ggsave, LetsPlot

# Configure LetsPlot to open plots in external browser
LetsPlot.setup_show_ext()

# Configuration
API_KEY = '8c059fea-116f-4b61-b132-1eb6cd647c52'
BASE_URL = 'https://pro-api.coinmarketcap.com/v1'
HEADERS = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}

# Helper Functions
def get_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter an integer.")

def select_platform(df):
    platforms = sorted(df['platform'].dropna().unique())
    platform_dict = {str(i+1): p for i, p in enumerate(platforms)}
    print("\nAvailable Platforms:")
    for i, name in platform_dict.items():
        print(f"{i}. {name}")
    choice = input("Select a platform by number (or press Enter to skip): ").strip()
    return platform_dict.get(choice, None)

def save_option(obj, obj_type='table'):
    choice = input("Would you like to save this? (y/n): ").strip().lower()
    if choice == 'y':
        name = input("Enter file name (without extension): ").strip()
        if obj_type == 'table':
            obj.to_csv(f"{name}.csv", index=False)
            print(f"Table saved as {name}.csv")
        elif obj_type == 'plot':
            ggsave(obj, f"{name}.png")
            print(f"Chart saved as {name}.png")

# Data Fetching
def fetch_listings(days=30, convert='USD'):
    url = f"{BASE_URL}/cryptocurrency/listings/latest"
    params = {'start': 1, 'limit': 100, 'convert': convert}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json().get('data', [])
    records = []
    for item in data:
        quote = item.get('quote', {}).get(convert, {})
        platform = item.get('platform')
        platform_name = platform.get('name') if isinstance(platform, dict) else 'Native'
        records.append({
            'symbol': item.get('symbol'),
            'name': item.get('name'),
            'platform': platform_name,
            'price_usd': quote.get('price'),
            'market_cap_usd': quote.get('market_cap'),
            f'change_{days}d': quote.get(f'percent_change_{days}d')
        })
    df = pd.DataFrame(records)
    df = df.sort_values(by='market_cap_usd', ascending=False).reset_index(drop=True)
    df.insert(0, 'Rank', df.index + 1)
    return df

# Analysis Functions
def top_n(df, column, n=10):
    return df.nlargest(n, column)

# Filter DataFrame by platform
def filter_by_platform(df, platform_filter):
    if not platform_filter:
        return df
    # filter tokens on the given platform
    df_filtered = df[df['platform'].str.lower() == platform_filter.lower()]
    # include native coin whose symbol matches platform name or its first three letters
    sym_lower = platform_filter.lower()
    prefix = sym_lower[:3]
    native_coin = df[(df['symbol'].str.lower() == sym_lower) | (df['symbol'].str.lower() == prefix)]
    # if native coin is not in the filtered DataFrame, add it
    result = pd.concat([df_filtered, native_coin])
    return result.drop_duplicates().reset_index(drop=True)

def show_marketcap_table(df, timeframe, top_k, platform_filter=None):
    df = filter_by_platform(df, platform_filter)
    cap_df = df.head(top_k).copy()
    print(f"\nTop {top_k} Coins by Market Cap" + (f" on {platform_filter}" if platform_filter else '') + ":")
    print(cap_df[['Rank', 'symbol', 'name', 'market_cap_usd', 'price_usd', f'change_{timeframe}d']].to_string(index=False))
    save_option(cap_df, obj_type='table')

def show_change_table(df, timeframe, top_k, platform_filter=None):
    df = filter_by_platform(df, platform_filter)
    change_df = df.sort_values(by=f'change_{timeframe}d', ascending=False).head(top_k).copy()
    print(f"\nTop {top_k} Coins by {timeframe}-Day % Change" + (f" on {platform_filter}" if platform_filter else '') + ":")
    print(change_df[['Rank', 'symbol', 'name', 'market_cap_usd', 'price_usd', f'change_{timeframe}d']].to_string(index=False))
    save_option(change_df, obj_type='table')

def plot_change(df, timeframe, top_k, platform_filter=None):
    df = filter_by_platform(df, platform_filter)
    top_by_change = df.sort_values(by=f'change_{timeframe}d', ascending=False).head(top_k).sort_values(by=f'change_{timeframe}d')
    p = (
        ggplot(top_by_change, aes(x='name', y=f'change_{timeframe}d'))
        + geom_bar(stat='identity')
        + coord_flip()
        + labs(
            title=f"Top {top_k} Coins by {timeframe}-Day % Change" + (f" on {platform_filter}" if platform_filter else ''),
            x='Coin', y='Percent Change'
        )
    )
    ggsize(800, 400)
    p.show()
    save_option(p, obj_type='plot')

def plot_platform_distribution(df):
    dist = df['platform'].value_counts().reset_index(name='count').sort_values(by='count')
    dist.columns = ['platform', 'count']
    q = (
        ggplot(dist, aes(x='platform', y='count'))
        + geom_bar(stat='identity')
        + coord_flip()
        + labs(
            title="Distribution of Top 100 Coins by Blockchain Platform",
            x='Platform', y='Number of Coins'
        )
    )
    ggsize(800, 400)
    q.show()
    save_option(q, obj_type='plot')

def show_platform_avg_change(df, timeframe):
    col = f'change_{timeframe}d'
    # Calculate the weighted average % change for each platform
    weighted_avg = df.groupby('platform', group_keys=False).apply(
        lambda g: (g[col] * g['market_cap_usd']).sum() / g['market_cap_usd'].sum()
    ).reset_index(name=f'Weighted Avg % Change ({timeframe}d)')

    weighted_avg = weighted_avg.sort_values(by=f'Weighted Avg % Change ({timeframe}d)', ascending=False)

    p = (
        ggplot(weighted_avg, aes(x='platform', y=f'Weighted Avg % Change ({timeframe}d)'))
        + geom_bar(stat='identity')
        + coord_flip()
        + labs(
            title=f"Weighted Avg {timeframe}-Day % Change by Platform",
            x='Platform', y='Weighted Avg % Change'
        )
    )
    ggsize(800, 400)
    p.show()
    save_option(p, obj_type='plot')

# Main Program 
if __name__ == '__main__':
    timeframe = get_int("Enter timeframe in days to analyze (e.g., 7 or 30): ")
    df = fetch_listings(days=timeframe)

    while True:
        print("\nSelect a chart or table to display (based on top 100 coins by market cap):")
        print("1. Show Top-K Market Cap Table")
        print("2. Show Top-K % Change Table")
        print("3. Show Top-K % Change Chart")
        print("4. Show Platform Distribution Chart")
        print("5. Show Weighted Avg % Change by Platform")
        print("6. Exit")
        choice = input("Enter choice (1-6): ").strip()

        if choice == '6':
            print("Goodbye!")
            break
        elif choice in ['1', '2', '3']:
            top_k = get_int("Enter how many top coins to show (e.g., 10): ")
            platform_filter = select_platform(df)

            if choice == '1':
                show_marketcap_table(df, timeframe, top_k, platform_filter)
            elif choice == '2':
                show_change_table(df, timeframe, top_k, platform_filter)
            else:
                plot_change(df, timeframe, top_k, platform_filter)
        elif choice == '4':
            plot_platform_distribution(df)
        elif choice == '5':
            show_platform_avg_change(df, timeframe)
        else:
            print("Invalid choice. Please select 1-6.")
