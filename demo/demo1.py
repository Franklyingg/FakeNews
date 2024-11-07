
'''
连接kimi api的最简单实例
'''

import os
from langchain_community.llms.moonshot import Moonshot
from langchain_core.messages import SystemMessage, HumanMessage

os.environ["MOONSHOT_API_KEY"] = 'sk-AbEqfrS5M7avPzwcfK1FdnAuI0ztiG5rbg29o8K85WSe8ETz'

chat = Moonshot(
    model="moonshot-v1-8k",
    temperature=0.8,
    api_key=os.environ['MOONSHOT_API_KEY'],)

messages = [
    SystemMessage(content="你是一个很棒的智能助手"),
    HumanMessage(content="请给我的花店起个名,多输出几个结果，直接输出名字，不要输出多余的语句")
]

response = chat.invoke('你好')
print(response)
