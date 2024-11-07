from typing import Annotated, Literal, TypedDict
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages, MessagesState
from llm import llm,tool_node

class State(TypedDict):
    messages: Annotated[list, add_messages]


def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_model(state: MessagesState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}



graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", call_model)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges('chatbot', should_continue)
graph_builder.add_edge("tools", 'chatbot')

graph = graph_builder.compile()



def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


user_input = input("User: ")
stream_graph_updates(user_input)
