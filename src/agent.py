from src.node import ResearchAgentNode
from src.state import ResearchState
from langgraph.graph import StateGraph, START, END
from config import Config

class Orchestrator:
    def __init__(self, node:ResearchAgentNode):
        self.node = node
    
    def build_graph(self):
      graph = StateGraph(ResearchState)
      graph.add_node('initialize_state', self.node.initialize_state)
      graph.add_node('fetch_news_data', self.node.fetch_news_data)
      graph.add_node('fetch_financial', self.node.fetch_financial)
      graph.add_node('fetch_company_facts', self.node.fetch_company_facts)
      graph.add_node('analyze_financial_data', self.node.analyze_financial_data)
      graph.add_node('analyze_sentiment', self.node.analyze_sentiment)
      graph.add_node('generate_summary', self.node.generate_summary)
      graph.add_node('create_detailed_report', self.node.create_detailed_report)
      graph.add_node('should_continue', self.node.should_continue)
      graph.add_node('complete_workflow', self.node.complete_workflow)

      graph.add_edge(START, 'initialize_state')
      # all fetch nodes start after initialize, run in parallel
      graph.add_edge('initialize_state', 'fetch_news_data')
      graph.add_edge('initialize_state', 'fetch_financial')
      graph.add_edge('initialize_state', 'fetch_company_facts')  # was wrongly from START
      # all three feed into analyze
      graph.add_edge('fetch_news_data', 'analyze_financial_data')
      graph.add_edge('fetch_financial', 'analyze_financial_data')
      graph.add_edge('fetch_company_facts', 'analyze_financial_data')
      graph.add_edge('analyze_financial_data', 'analyze_sentiment')
      graph.add_edge('analyze_sentiment', 'generate_summary')
      graph.add_edge('generate_summary', 'create_detailed_report')
      graph.add_edge('create_detailed_report', 'should_continue')
      graph.add_conditional_edges(
          'should_continue',
          self.node.conditional_logic,
          {'Analysis Research and Analysis complete': 'complete_workflow', 'needs_improvement': 'fetch_news_data'}
      )
      graph.add_edge('complete_workflow', END)
      workflow = graph.compile()
      return workflow

def create_agent():
    node = ResearchAgentNode(config=Config) 
    orchestrator = Orchestrator(node)
    return orchestrator.build_graph()
       