# from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langchain_community.tools import ArxivQueryRun , WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper , ArxivAPIWrapper

def get_Tools():
    """
    Return the List of Tools to be used in the ChatBot
    """
    arxiv_api = ArxivAPIWrapper(top_k_results=2 , doc_content_chars_max=5000)
    arxiv = ArxivQueryRun(api_wrapper=arxiv_api)
    wiki_api = WikipediaAPIWrapper(top_k_results=2 , doc_content_chars_max=500)
    wiki = WikipediaQueryRun(api_wrapper=wiki_api)
    tools = [arxiv , wiki]
    return tools

def create_tool_node(tools):
    """
    Creates and Return the Tool Node for graph
    """
    return ToolNode(tools=tools)