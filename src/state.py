#src/state.py
from datetime import datetime
from typing import TypedDict, Annotated, Optional, Dict, List
import operator

class ResearchState(TypedDict):
    """
    Complete state for financial research agent.
    Each field represents data accumulated during the research process.
    """
    
    # Input
    ticker: str
    company_name: Optional[str]
    
    # Research stage tracking
    current_stage: str
    iteration_count: int
    max_iter: int
    
    # Data collection results
    financial_data: Optional[Dict]
    market_data: Optional[Dict]
    news_articles: Optional[List[Dict]]
    
    # Analysis results
    financial_metrics: Optional[Dict]
    financial_analysis: Optional[str]
    sentiment_score: Optional[float]
    sentiment_analysis: Optional[str]
    competitive_analysis: Optional[str]
    
    # Report components
    executive_summary: Optional[str]
    detailed_report: Optional[str]
    recommendation: Optional[str]
    target_price: Optional[float]
    confidence_score: Optional[float]
    
    # Metadata and control
    errors: Annotated[List[str], operator.add]
    data_sufficient: bool
    needs_retry: Annotated[List[str], operator.add]
    timestamp: str
    