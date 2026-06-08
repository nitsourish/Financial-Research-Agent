#src/node.py

from datetime import datetime  
from langchain_openai import ChatOpenAI
from src.tools.market_data import MarketResearch
from src.tools.news_client import NewsClient
from src.tools.sec_edger import SECClient
from src.state import ResearchState
from src.utils.cache import CacheManager
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from src.prompts.templates import PromptTemplates
from langchain_core.output_parsers import JsonOutputParser

class ResearchAgentNode:
    def __init__(self, config):
        self.config = config
        self.cache = CacheManager(ttl=self.config.CACHE_TTL_FINANCIALS)
        self.market_research_manager = MarketResearch()
        self.news_client_manager = NewsClient(api_key=self.config.NEWS_API_KEY, url = "https://newsapi.org/v2")
        self.company_facts_manager = SECClient()
        self.primary_model = ChatOpenAI(model=self.config.PRIMARY_MODEL, temperature=0.0)
        self.secondary_model = ChatOpenAI(model=self.config.SECONDARY_MODEL, temperature=0.0)
        
    def initialize_state(self, state: ResearchState) -> ResearchState:   
        
        print(f"Initializing research for {state['ticker']}")
        state['current_stage'] = 'initialization'
        state['iteration_count'] = 0
        state['max_iter'] = 3
        state['data_sufficient'] = False
        state['errors'] = []
        state['needs_retry'] = []
        
        ticker = state['ticker'].upper()
        if not ticker or len(ticker) > 5:
            state['errors'].append('no valid ticker')
        state['ticker'] = ticker
        state['timestamp'] = datetime.now().strftime('%d_%m_%H_%M')
        return state
    
    def fetch_financial(self, state: ResearchState) -> dict:
        key = f"financials:{state['ticker']}"
        cached_data = self.cache.get(key) if self.config.CACHE_ENABLED else None
        if cached_data:
            print('cache hit')
            return {'financial_data': cached_data}
        financial_data = self.market_research_manager.get_market_data(state['ticker'])
        if financial_data:
            self.cache.set(key, financial_data)
            return {'financial_data': financial_data}

        print(f"Error in fetching financial data for {state['ticker']}")
        return {'errors': [f"Error in fetching financial data for {state['ticker']}"], 'needs_retry': ['financial_data']}


    def fetch_news_data(self, state: ResearchState) -> dict:
        key = f"market news:{state['ticker']}"
        cached_data = self.cache.get(key) if self.config.CACHE_ENABLED else None
        if cached_data:
            print('cache hit')
            return {'news_articles': cached_data}
        news_articles = self.news_client_manager.get_news_data(state['ticker'])
        if news_articles:
            self.cache.set(key, news_articles)
            return {'news_articles': news_articles}

        print(f"Error in fetching news_data for {state['ticker']}")
        return {'errors': [f"Error in fetching news_data for {state['ticker']}"], 'needs_retry': ['news_data']}
    
    
    def fetch_company_facts(self, state: ResearchState) -> dict:
        market_data = self.company_facts_manager.get_company_facts(state['ticker']) 
        if market_data:
            return {'market_data': market_data}
        
        print(f"Error in fetching company_facts for {state['ticker']}")
        return {'errors':[f"Error in fetching company_facts for {state['ticker']}"], 'needs_retry':['company_facts']}   

    
    def analyze_financial_data(self, state):
        system_prompt = PromptTemplates.FINANCIAL_ANALYSIS
        prompt = ChatPromptTemplate.from_messages([
                (SystemMessage(content=system_prompt)),
                ('human', "Analyze company financials for {company_name}, {ticker} and {metrics}")
            ]
        )
        company_fiancials = {
        'company_name':state['market_data'].get('company_name', ''),
        'ticker':state['ticker'],
        'metrics': state['market_data']
    }
        agent = prompt | self.primary_model | JsonOutputParser()
        response = agent.invoke(input = company_fiancials)
        state['financial_analysis'] = str(response)
        state['financial_metrics'] = company_fiancials.get('metrics', {})
        state['current_stage'] = 'analyze_financial_data'
        return state
    
    def analyze_sentiment(self, state):    
        system_prompt = PromptTemplates.SENTIMENT_ANALYSIS
        prompt = ChatPromptTemplate.from_messages([
                (SystemMessage(content=system_prompt)),
                ('human', "Analyze company financials for {company_name}, {ticker} and {metrics}")
            ]
        )
        news_data = {
        'company_name':state['market_data'].get('company_name', ''),
        'ticker':state['ticker'],
        'news_summary': state['news_articles']
    }
        prompt = ChatPromptTemplate.from_messages([
            (SystemMessage(content=system_prompt)),
            ('human', 'Analyse senitiment based on {company_name}, {ticker} and \n\n {news_summary}')
        ])
        agent = prompt | self.primary_model | JsonOutputParser()
        response=agent.invoke(input=news_data)
        state['sentiment_analysis'] = str(response)
        score = response.get('SENTIMENT_SCORE') or response.get('sentiment_score')
        state['sentiment_score'] = float(score) if score is not None else 0.5
        state['current_stage'] = 'analyze_sentiment'
        return state
    
    def generate_summary(self, state: ResearchState):
        summary_input = {
        'company_name':state['market_data'].get('company_name', ''),
        'ticker':state['ticker'],
        'financial_analysis': state['financial_analysis'],
        'sentiment_analysis':state['sentiment_analysis'],
        'market_data':state['market_data']
        }
        system_prompt = PromptTemplates.EXECUTIVE_SUMMARY

        prompt = ChatPromptTemplate.from_messages([
                (SystemMessage(content=system_prompt)),
                ('human', 'create executive summary based {company_name}, {ticker} and \n\n {financial_analysis} \n\n {sentiment_analysis} and \n\n {market_data}')
            ])

        agent = prompt | self.primary_model | JsonOutputParser()
        response = agent.invoke(input=summary_input)
        state['executive_summary'] = str(response)
        state['current_stage'] = 'generate_summary'
        return state
    
    def create_detailed_report(self, state: ResearchState) -> ResearchState:
        report_input = {
        'company_name':state['market_data'].get('company_name', ''),
        'ticker':state['ticker'],
        'executive_summary': state['executive_summary'],
        'financial_analysis': state['financial_analysis'],
        'financial_metric': state['financial_metrics'],
        'sentiment_analysis':state['sentiment_analysis'],
        'sentiment_score':state['sentiment_score'],
    }
        system_prompt = PromptTemplates.DETAILED_REPORT

        prompt = ChatPromptTemplate.from_messages([
        (SystemMessage(content=system_prompt)),
        ('human', 'create executive summary based {company_name}, {ticker}, \n\n{executive_summary} ,\n\n{financial_analysis} with {financial_metric} and \n\n{sentiment_analysis} with {sentiment_score}')
    ])

        agent = prompt | self.primary_model | JsonOutputParser()
        response = agent.invoke(input=report_input)

        rec = response.get('RECOMMENDATION') or response.get('recommendation', 'HOLD')
        state['recommendation'] = str(rec).upper() if rec else 'HOLD'
        conf = response.get('CONFIDENCE') or response.get('confidence')
        state['confidence_score'] = float(conf) if conf is not None else 0.5
        
       
        state['detailed_report'] = str(response)
        state['current_stage'] = 'detailed_report'
        return state
    
    def should_continue(self, state: ResearchState) -> ResearchState:
        
        system_prompt = """You are a validation agent to validate whether {state['detailed_report']} conforms 80% of the objectives mentioned in {PromptTemplates.DETAILED_REPORT} or not
        don't produce any text. Answer just with bool 'TRUE' or 'FALSE'
        """
        prompt = ChatPromptTemplate.from_messages([
            (SystemMessage(system_prompt)),
            ('human', 'generated detailed report \n{detailed_report}')
        ])
        agent = prompt | self.secondary_model
        detailed_report = state['detailed_report']
        response = agent.invoke(input={'detailed_report':detailed_report}).content
        state['data_sufficient'] = bool(response) 
        state['iteration_count'] +=1
        state['current_stage'] = 'validating'
        return state

    def conditional_logic(self, state):
        print('into the conditional logic')
        if state['data_sufficient']:
            
            return "Analysis Research and Analysis complete"
        else:
            return "needs_improvement"
        
    def complete_workflow(self, state):
        state['current_stage'] = 'completed'
        # Merge live price fields from yfinance (financial_data) into market_data
        financial = state.get('financial_data') or {}
        if financial and state.get('market_data'):
            for key in ['current_price', 'market_cap', 'pe_ratio', 'beta',
                        '52_week_high', '52_week_low', 'dividend_yield', 'sector', 'industry']:
                if financial.get(key) is not None:
                    state['market_data'][key] = financial[key]
        return state
