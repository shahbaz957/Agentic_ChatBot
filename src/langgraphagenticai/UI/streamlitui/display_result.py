import streamlit as st
from langchain_core.messages import HumanMessage
import json


class DisplayResultsStreamlit:
    def __init__(self , usecase , graph , user_message):
        self.usecase = usecase 
        self.graph = graph
        self.user_message = user_message     
    
    def display_result_on_ui(self):
        usecase = self.usecase
        user_message = self.user_message
        graph = self.graph
        if usecase == "Basic ChatBot":
            try:
                # Use HumanMessage instead of tuple
                result = graph.invoke({'messages': [HumanMessage(content=user_message)]})
                with st.chat_message("user"):
                    st.write(user_message)
                with st.chat_message("assistant"):
                    # Extract the last message's content
                    if isinstance(result['messages'], list):
                        st.write(result['messages'][-1].content)
                    else:
                        st.write(result['messages'].content)
            except Exception as e:
                st.error(f"Error displaying result: {e}")