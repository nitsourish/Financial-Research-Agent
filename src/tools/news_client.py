#src/tools/news_client.py
import requests
import time
from datetime import timedelta, datetime

class NewsClient:
  def __init__(self, api_key, url):
    self.url = url
    self.api_key = api_key

  def get_news_data(self, ticker, days:int = 7):
    params = {'q': ticker,
              'sortBy': 'relevancy',
              'language': 'en',
              'apiKey': self.api_key,
              'pageSize': 20}
    
    try:
      response = requests.get(url = f"{self.url}/everything", params=params, timeout=10)
      response.raise_for_status()
      data = response.json()
      all_data = []
      articles = data.get('articles', [])
      for article in articles:
        all_data.append({
          'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'content': article.get('content', '')
        })
    except requests.RequestException as e:
        print(f'HTTP Error:{e}')
        return []
    return all_data