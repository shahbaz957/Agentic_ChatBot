from typing_extensions import TypedDict
from typing import List , Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class State(TypedDict):
    """
    Represent the structure of State of Graph
    """
    messages : Annotated[List[BaseMessage] , add_messages]