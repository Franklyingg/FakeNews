'''
langsmith使用实例
'''

import os
os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "fakenews"

import os
from langchain_community.llms.moonshot import Moonshot
from langchain_core.messages import SystemMessage, HumanMessage

os.environ["MOONSHOT_API_KEY"] = 'sk-AbEqfrS5M7avPzwcfK1FdnAuI0ztiG5rbg29o8K85WSe8ETz'

chat = Moonshot(
    model="moonshot-v1-8k",
    temperature=0.8,
    max_tokens=20, )

messages = [
    SystemMessage(content="你是一个很棒的智能助手"),
    HumanMessage(content="请给我的花店起个名,多输出几个结果，直接输出名字，不要输出多余的语句")
]

response = chat.invoke(messages)
print(response)