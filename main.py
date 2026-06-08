#main.py
from datetime import datetime
from src.node import ResearchAgentNode
from src.agent_with_observability import create_agent
from src.state import ResearchState
import json
from dotenv import load_dotenv
load_dotenv()

def main(ticker):
    print(F"running Agent for {ticker}")
    file_name = f"{datetime.now().strftime('%d_%m_%H_%M')}_{ticker}.json"
    workflow, tracer = create_agent()
    state = ResearchState(ticker=ticker)
    output = workflow.invoke(state,  config={"callbacks": [tracer]})
    with open(file_name, mode='w')as f:
        json.dump(output, fp=f, indent = 2)
    print(f"\nFull report saved to: {file_name}")
    return output
    
# if __name__ == "__main__":
#     ticker = input("Enter stock ticker: ").strip().upper()   
#     output = main(ticker)   