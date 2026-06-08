#src/prompts/templates.py

class PromptTemplates:
    """
    LLM prompt templates for different analysis tasks.
    """
    
    FINANCIAL_ANALYSIS = """You are a financial analyst. Analyze the following financial metrics for {company_name} ({ticker}):

{metrics}

Provide a comprehensive analysis covering:
1. Revenue and profitability trends
2. Financial health (leverage, liquidity)
3. Efficiency metrics (ROE, profit margins)
4. Comparative analysis vs industry averages
5. Key strengths and weaknesses

Be specific, quantitative, and professional. output to be produced strictly in JSON format"""

    SENTIMENT_ANALYSIS = """You are a market analyst. Analyze the sentiment from recent news about {company_name} ({ticker}):

{news_summary}

Return ONLY a JSON object with these exact keys (no markdown, no code blocks):
{{
  "overall_sentiment": "positive | neutral | negative",
  "key_themes": ["theme1", "theme2"],
  "potential_impact": "description of potential stock impact",
  "risks_opportunities": "notable risks or opportunities",
  "SENTIMENT_SCORE": <float 0.0 to 1.0, where 0=very negative, 0.5=neutral, 1.0=very positive>
}}"""

    EXECUTIVE_SUMMARY = """You are an investment analyst. Create an executive summary for {company_name} ({ticker}) based on:

Financial Analysis:
{financial_analysis}

Sentiment Analysis:
{sentiment_analysis}

Market Data:
{market_data}

Provide a concise 3-4 paragraph executive summary that:
1. Opens with the investment thesis
2. Highlights key financial strengths/weaknesses
3. Incorporates market sentiment
4. Concludes with overall outlook

Be clear, professional, and actionable.Format your response as a structured analysis. output to be produced strictly in JSON format"""

    DETAILED_REPORT = """You are a senior investment analyst. Generate a comprehensive research report for {company_name} ({ticker}).

Executive Summary:
{executive_summary}

Financial Metrics:
{financial_metrics}

Financial Analysis:
{financial_analysis}

Sentiment Score: {sentiment_score}
Sentiment Analysis:
{sentiment_analysis}

Return ONLY a JSON object with these exact keys (no markdown, no code blocks):
{{
  "company_overview": "...",
  "financial_performance": "...",
  "market_position_and_sentiment": "...",
  "valuation_assessment": "...",
  "risk_factors": "...",
  "investment_recommendation": "...",
  "RECOMMENDATION": "BUY | SELL | HOLD",
  "CONFIDENCE": <float 0.0 to 1.0, based on strength and consistency of evidence>
}}

RECOMMENDATION must be one of: BUY, SELL, or HOLD — choose based on the actual data, do NOT default to HOLD unless the evidence is truly mixed.
CONFIDENCE must reflect how strongly the data supports the recommendation (e.g. 0.8+ for strong conviction, 0.5-0.7 for moderate, below 0.5 for weak).
Be thorough, professional, and data-driven."""