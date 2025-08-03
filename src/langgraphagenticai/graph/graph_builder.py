from src.langgraphagenticai.state.state_graph import State
from langgraph.graph import StateGraph , START , END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatBotNode
from src.langgraphagenticai.tools.search_tool import get_Tools , create_tool_node
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotToolNode
from src.langgraphagenticai.nodes.AI_news import AINewsNode
class GraphBuilder:
    def __init__(self , model):
        self.llm = model
        self.graph_builder = StateGraph(State)
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """
        self.graph_builder = StateGraph(State)
        self.basic_chatbot_node = BasicChatBotNode(self.llm)
        self.graph_builder.add_node('chatbot' , self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START , 'chatbot')
        self.graph_builder.add_edge('chatbot' , END)
    

    def chatbot_with_tool_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot with tool 
        capabilities, and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """
        self.graph_builder = StateGraph(State)
        ### Defining the tools and tool Node
        tools = get_Tools()
        tool_node = create_tool_node(tools)

        ### Defining ChatBot Node
        obj_chatbot_tool = ChatbotToolNode(self.llm)
        chatbot_node = obj_chatbot_tool.create_chatbot(tools)

        ### Define the LLM 
        llm = self.llm
        self.graph_builder.add_node("chatbot" , chatbot_node)
        self.graph_builder.add_node("tools" , tool_node)
        self.graph_builder.add_edge(START , "chatbot")
        self.graph_builder.add_conditional_edges("chatbot" , tools_condition)
        self.graph_builder.add_edge("tools" , "chatbot")

    def ai_news_builder_graph(self):
        self.graph_builder = StateGraph(State)
         # the structure of graph is like : 1 -> fetch News 2 -> summarizer 3 -> format the Result(Save Results)
        llm = self.llm
        ai_news_node = AINewsNode(llm)


        self.graph_builder.add_node("fetch_news" , ai_news_node.fetch_news)
        self.graph_builder.add_node("summarizer" , ai_news_node.summarizing_result)
        self.graph_builder.add_node("formatter_save" , ai_news_node.save_results)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news" , 'summarizer')
        self.graph_builder.add_edge('summarizer' , "formatter_save")
        self.graph_builder.add_edge('formatter_save' , END)





    def setup_graph(self , usecase : str):
        """
        Sets up the graph for the selected usecase
        """
        if usecase == "Basic ChatBot":
            self.basic_chatbot_build_graph()
        if usecase == "ChatBot with Web":
            self.chatbot_with_tool_build_graph()

        if usecase =="AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()