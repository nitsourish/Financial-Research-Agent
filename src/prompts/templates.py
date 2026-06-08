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

Provide:
1. Overall sentiment assessment (positive/neutral/negative)
2. Key themes from the news
3. Potential impact on stock performance
4. Notable risks or opportunities mentioned

At the end, include a line:
SENTIMENT_SCORE: [0.0 to 1.0 where 0=very negative, 0.5=neutral, 1.0=very positive]. output to be produced strictly in JSON format"""

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

Create a detailed report with these sections:
1. Company Overview
2. Financial Performance Analysis
3. Market Position and Sentiment
4. Valuation Assessment
5. Risk Factors
6. Investment Recommendation

At the end, include:
RECOMMENDATION: [BUY/SELL/HOLD]
CONFIDENCE: [0.0 to 1.0]

Be thorough, professional, and data-driven.output to be produced strictly in JSON format"""