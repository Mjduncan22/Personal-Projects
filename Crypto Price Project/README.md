# Overview

As a software engineer passionate about data analysis, I built this Crypto Analyzer tool to deepen my understanding of API-based data ingestion, data transformation with Pandas, and data visualization with Lets-Plot. This project serves as a practical application of my skills in Python and data science, while also providing insights into the cryptocurrency market.

I analyze a dataset of the top 100 cryptocurrencies by market capitalization, retrieved in real-time from the CoinMarketCap API:  
`https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest`  
The tool computes rankings by market cap, percentage change over a user-defined timeframe, and weighted platform-level returns.

My purpose in developing this software is to create a reusable application that:  
- Provides a simple interface for users to analyze cryptocurrency data
- Offers insights into market trends and performance
- Serves as a foundation for future enhancements and features

[Software Demo Video](https://youtu.be/97XbopB5lj8)

# Data Analysis Results

Question 1: Which coins are outpacing Bitcoin over 90 days?
Answer: The tool compares each coin’s 90-day percentage change against Bitcoin’s. It lists those whose 90-day returns exceed BTC’s, highlighting alternative assets that have delivered stronger performance. As of 5/23/2025, there are 24 coins outperforming Bitcoin.

Question 2: Which blockchains are performing the best?
Answer: By computing the market-cap-weighted average 90-day return for each blockchain platform, the tool ranks ecosystems (e.g., Solana, Ethereum, Avalanche) according to their collective performance. As of 5/23/2025, the BNB Smart Chain leads.

Question 3: Which blockchains are the most successful for project integration?
Answer: Using the count of top-100 projects deployed on each platform as a proxy for integration success, the tool identifies platforms (e.g., Ethereum, BNB Chain) with the highest number of leading projects. As of 5/23/2025, Ethereum has the most projects (43) in the top 100.

# Development Environment

- **IDE/Editor:** VS Code  
- **Language:** Python 3.10  
- **Libraries:**  
  - `pandas` for data manipulation  
  - `requests` for HTTP API calls  
  - `lets-plot` for visualization  
  - `ggsave` for exporting charts  

# Useful Websites

- [CoinMarketCap API Documentation](https://coinmarketcap.com/api/)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)  
- [Lets-Plot Python Tutorial](https://github.com/JetBrains/lets-plot)

# Future Work

- Integrate sector/category data and allow filtering by sector  
- Add support for historical OHLCV data and line charts of price trends  
- Implement caching to reduce API calls and improve performance  
