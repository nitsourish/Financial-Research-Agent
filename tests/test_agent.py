#tests/test_agent.py

import datetime
# from src.node import ResearchAgentNode
from src.state import ResearchState
from src.agent import create_agent
import pytest

@pytest.fixture
def research_agent():
     return create_agent()
 
@pytest.fixture
def initial_state():
     return ResearchState( ticker = 'AAPL',
        company_name = 'None',
    
        # Research stage tracking
        current_stage = 'initialization',
        iteration_count=0,
        max_iter = 3,
        
        # Data collection results
        financial_data = {},
        market_data = {},
        news_articles =[{}],
        
        # Analysis results
        financial_metrics = {},
        financial_analysis = None,
        sentiment_score  = 0.0,
        sentiment_analysis = None,
        competitive_analysis = None,
        
        # Report components
        executive_summary = None,
        detailed_report = None,
        recommendation = None,
        target_price = None,
        confidence_score = None,
        
        # Metadata and control
        errors = [],
        data_sufficient = False,
        needs_retry =[],
        timestamp = datetime.datetime.now().strftime('%d_%m_%H_%M')
        )
     
def test_run_end_end(research_agent, initial_state):
    result = research_agent.invoke(initial_state)
    assert result['ticker'] == 'AAPL'
    assert result['current_stage'] == 'completed'
    
def test_agent_generates_recommendation(research_agent, initial_state):
    result = research_agent.invoke(initial_state)
    assert result.get('recommendation') in ['BUY', 'SELL', 'HOLD']
    assert 0 <= result.get('confidence_score', 0) <= 1 


