from typing import Annotated, Literal, TypedDict
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages, MessagesState
from llm import llm,tool_node

class State(TypedDict):
    messages: Annotated[list, add_messages]



'''
付费API,将于2025/2/1日取消API授权
'''


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
    mes = ("user", '请按照如下的工作流程判断此URL下的新闻是否为假新闻 URL={}'.format(user_input) +
           '运作流程表：'+
           '1. 如果新闻来自一个不知名 / 有怀疑的URl，则新闻有可能是假的'+
           '2. 如果新闻标题中存在包含煽情，挑衅性，情绪化的语言，以此来吸引读者的注意力，或暗示谣言，那么可能是假的'+
           '3. 如果新闻存在拼写错误的单词，语法错误，滥用引用或者全大写的单词，那可能是假的'+
           '4. 如果新闻不合理或者与常识相矛盾，或者新闻更像一片八卦而不是事实报道，则可能是假的'+
           '5. 如果新闻偏向于特定的政治观点，旨在影响公众舆论，而不是提供客观信息，那么他可能是假的'+
           '6. 如果其他的网络来源，包括不一样，冲突或者矛盾的内容，那么新闻可能是假的'+
           '请综合判断以上六条，运用工具，最终告诉我结果以及分析的原因'
           )
    for j,event in enumerate(graph.stream({"messages": [mes]})):
        for i,value in enumerate(event.values()):
            print(j,i,value)


user_input = input("请输入需要判断的新闻URL:(测试demo网址：https://news.sina.com.cn/s/2024-11-08/doc-incvisys0685097.shtml) ")
stream_graph_updates(user_input)
