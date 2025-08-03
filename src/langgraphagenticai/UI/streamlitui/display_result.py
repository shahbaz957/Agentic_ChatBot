import streamlit as st
from langchain_core.messages import HumanMessage , ToolMessage , AIMessage
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
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []

                st.session_state.chat_history.append(HumanMessage(content=user_message))
                result = graph.invoke({'messages' : st.session_state.chat_history})
                if isinstance(result['messages'], list):
                    response_message = result['messages'][-1]
                else:
                    response_message = result['messages']
                st.session_state.chat_history.append(response_message)

        # Display user message
                with st.chat_message("user"):
                    st.write(user_message)

        # Display AI response
                with st.chat_message("assistant"):
                    st.write(response_message.content)
            except Exception as e:
                st.error(f"Error displaying result: {e}")
        elif usecase == "ChatBot with Web":
                # Prepare state and invoke the graph
                initial_state = {"messages": [HumanMessage(content=user_message)]}
                result = graph.invoke(initial_state)
                
                for message in result["messages"]:
                    # if isinstance(message, HumanMessage):
                    #     with st.chat_message("user"):
                    #         st.write(message.content)
                    if isinstance(message, ToolMessage):
                        with st.chat_message("ai"):
                            st.write("**Tool Call Start**")
                            st.write(message.content)
                            st.write("**Tool Call End**")
                    # elif isinstance(message, AIMessage) and message.content:
                    #     with st.chat_message("assistant"):
                    #         st.write(message.content)
                    st.write(message.content)

        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing News ..."):
                result = graph.invoke({"messages": [HumanMessage(content=frequency)]})

                try:
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH , 'r') as f:
                        markdown_content = f.read()
                    st.markdown(markdown_content , unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                with open(AI_NEWS_PATH, 'r') as f:
                    st.download_button(
                        "💾 Download Summary",
                        f.read(),
                        file_name=AI_NEWS_PATH,
                        mime="text/markdown"
                    )
                st.success(f"✅ Summary saved to {AI_NEWS_PATH}")