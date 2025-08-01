from src.langgraphagenticai.state.state_graph import State
from langchain_core.messages import AIMessage

class BasicChatBotNode:
    """
    Basic Chatbot Logic Implementation
    """
    def __init__(self , model):
        self.llm = model
    def process(self, state: State) -> dict:
        """
        Process the input and generate the Chatbot Response
        """
        # Invoke the model and ensure the response is an AIMessage
        response = self.llm.invoke(state['messages'])
        # Ensure response is an AIMessage (ChatGroq should return AIMessage)
        if isinstance(response, AIMessage):
            return {"messages": response}
        else:
            # Fallback: manually create AIMessage from response content
            return {"messages": AIMessage(content=str(response.content))}
