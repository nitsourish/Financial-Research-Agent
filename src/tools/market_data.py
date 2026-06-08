#src/tools/market_data.py
import yfinance as yf

class MarketResearch:
    
    def get_market_data(self,ticker):
        try:
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            history = stock.history(period = '1y')
            
            market_data = {
                'ticker': ticker,
                'company_name': stock_info.get('longName', ticker),
                'current_price': stock_info.get('currentPrice', 0),
                'market_cap': stock_info.get('marketCap', 0),
                'pe_ratio': stock_info.get('trailingPE', 0),
                'dividend_yield': stock_info.get('dividendYield', 0),
                'beta': stock_info.get('beta', 0),
                '52_week_high': stock_info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': stock_info.get('fiftyTwoWeekLow', 0),
                'avg_volume': stock_info.get('averageVolume', 0),
                'sector': stock_info.get('sector', 'Unknown'),
                'industry': stock_info.get('industry', 'Unknown'),
                'year_high': history['High'].max(),
                'year_low': history['Low'].min(),
                'year_volatality': history['Close'].pct_change().std() * (252 ** 0.5),
                'annual_return': (history['Close'].iloc[-1] - history['Open'].iloc[0]) / history['Open'].iloc[0] * 100
            }
        except Exception as e:
            print(f"Market data error for {ticker}: {e}")
            return None
        return market_data