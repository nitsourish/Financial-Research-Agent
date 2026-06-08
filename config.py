#config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    #Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    # Model Configuration
    PRIMARY_MODEL = "gpt-4o-mini"
    SECONDARY_MODEL = "gpt-3.5-turbo"
    
    # Cache Configuration
    CACHE_ENABLED = True
    CACHE_TTL_FINANCIALS = 86400  # 24 hours
    CACHE_TTL_NEWS = 3600  # 1 hour
    
    # Agent Configuration
    MAX_ITERATIONS = 5
    CONFIDENCE_THRESHOLD = 0.7
    
    # Logging
    LOG_LEVEL = "INFO"
    
