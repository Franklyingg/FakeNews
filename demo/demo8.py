'''
增加了工具功能的langgraph对话机器人 最小实例
'''
from typing import Annotated, Literal, TypedDict
import os
os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "fakenews"


from langchain_openai import ChatOpenAI

OPENAI_API_BASE='https://api.moonshot.cn/v1'
OPEN_API_KEY='sk-AbEqfrS5M7avPzwcfK1FdnAuI0ztiG5rbg29o8K85WSe8ETz'



from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages, MessagesState


class State(TypedDict):
    messages: Annotated[list, add_messages]

from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

@tool
def search(query: str):
    """获取天气信息,请输入完整语句"""
    from langchain_community.tools import SearchAPIResults
    os.environ["SEARCHAPI_API_KEY"] = 'wpcriK7bESpT4LRVfpjpMz6u'

    search = SearchAPIResults()
    res = search.invoke(query)
    while 'Error' in res:
        res = search.invoke(query)
    return res[:5000]

tools = [search]

tool_node = ToolNode(tools)
llm = ChatOpenAI(model_name="moonshot-v1-32k", base_url=OPENAI_API_BASE,api_key=OPEN_API_KEY).bind_tools(tools)

# Define the function that determines whether to continue or not
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END


# Define the function that calls the model
def call_model(state: MessagesState):
    messages = state['messages']
    response = llm.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}



graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", call_model)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges('chatbot', should_continue)
graph_builder.add_edge("tools", 'chatbot')

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