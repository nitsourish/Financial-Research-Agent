#src/tools/sec_edger.py
import requests
import time

class SECClient:
    def __init__(self):
        self.min_elapse_time = 0.1
        self.last_updated_time = 0
    
    def apply_rate_limiter(self):
        elapsed_time = time.time() - self.last_updated_time
        if elapsed_time < self.min_elapse_time:
            time.sleep(self.min_elapse_time - elapsed_time)
        self.last_updated_time = time.time()    
    
    def get_cik(self, ticker):
        url = "https://www.sec.gov/files/company_tickers.json"
        session = requests.Session()
        session.headers.update({
            "User-Agent": "MyApp/1.0 sourish.syntel@gmail.com",
            "Accept-Encoding": "gzip, deflate",
        })
        self.apply_rate_limiter()
        response = session.get(url = url, timeout=10)
        data = response.json()
        cik = next(v['cik_str'] for v in data.values() if v['ticker'] == ticker)
        title = next(v['title'] for v in data.values() if v['ticker'] == ticker)
        return cik, title

    def _get_annual_figures(self, gaap, concept):
        facts = gaap[concept]['units']['USD']
        annual = [f for f in facts if f.get('form') == '10-K' and 'end' in f]
        return max(annual, key=lambda x:x['end'])['val']

    def get_company_facts(self, ticker):
        cik, title = self.get_cik(ticker)
        cik_padded = str(cik).zfill(10)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
        self.apply_rate_limiter()
        session = requests.Session()
        session.headers.update({
            "User-Agent": "MyApp/1.0 sourish.syntel@gmail.com"})
        response=session.get(url=url, timeout=10)
        response.raise_for_status()
        data = response.json()
        gaap = data.get('facts', '')['us-gaap']

        return {
            'company_name': title,
            'cik': cik,
            'revenue':self._get_annual_figures(gaap, 'Revenues'),
            'net_income':self._get_annual_figures(gaap, 'NetIncomeLoss'),
            'total_assets':self._get_annual_figures(gaap, 'Assets'),
            'total_liabilities':self._get_annual_figures(gaap, 'Liabilities'),
            'shareholders_equity':self._get_annual_figures(gaap, 'StockholdersEquity'), 
            'data_source': 'SEC EDGAR',
            'last_updated': time.strftime('%Y-%m-%d') 
        }