'''
langgraph 最小实例
'''

import os
os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "fakenews"


from langchain_openai import ChatOpenAI

OPENAI_API_BASE='https://api.moonshot.cn/v1'
OPEN_API_KEY='sk-AbEqfrS5M7avPzwcfK1FdnAuI0ztiG5rbg29o8K85WSe8ETz'
llm = ChatOpenAI(model_name="moonshot-v1-8k", base_url=OPENAI_API_BASE,api_key=OPEN_API_KEY)


from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


graph = graph_builder.compile()

from io import BytesIO
from PIL import Image
try:
    byte_stream = BytesIO(graph.get_graph().draw_mermaid_png())
    roiimg = Image.open(byte_stream)
    roiimg.show()
except Exception: # 这需要一些额外的依赖项，是可选的
    pass

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break