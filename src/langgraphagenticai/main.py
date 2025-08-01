## Using this file all the components of langgraphagenticai is called
import streamlit as st
from src.langgraphagenticai.UI.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.UI.streamlitui.display_result import DisplayResultsStreamlit
def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    
    """
    ## Load UI

    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui() ## this is returning user_controls to the user_input variable
    if not user_input:
        st.error("Error : Failed to Load the User input from UI Template file")
        return
    user_message = st.chat_input("Enter your Messages : ")
    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input = user_input)
            model = obj_llm_config.get_llm_model()
            if not model :
                st.error("Error : LLM model could not be Initialized")
                return 
            usecase = user_input.get("selected_usecase")
            if not usecase :
                st.error("Error : No use case is selected")
                return 
            graph_builder = GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase) # here we implement the specific workflow related to ChatBot Architechture
                DisplayResultsStreamlit(usecase  , graph , user_message).display_result_on_ui()

            except Exception as e:
                st.error(f'Error : Graph Setup Failed --> {e}')
                return 
        except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
