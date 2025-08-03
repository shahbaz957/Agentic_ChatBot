from src.langgraphagenticai.state.state_graph import State
from langchain_core.messages import AIMessage
import streamlit as st
from langchain_core.messages import HumanMessage ,AIMessage
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
         # Get the latest user input
        user_input = state['messages'][-1].content

        # Append latest user message to session history
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        # Send entire history to the LLM
        response = self.llm.invoke(st.session_state.chat_history)

        # Append AI response
        ai_message = response if isinstance(response, AIMessage) else AIMessage(content=str(response.content))
        st.session_state.chat_history.append(ai_message)

        # Return the full updated message history
        return {"messages": st.session_state.chat_history}
