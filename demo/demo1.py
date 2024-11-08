
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
    HumanMessage(content="判断一下新闻中是否存在挑衅性和情绪化的语言，请认真判断，不要误判。如存在请以[{'原文':'文章内容'：'问题':'文字存在的问题'}]的列表形式返回,若不存在请单独返回空列表[]，不要返回任何无关内容。 \n（原标题：中国记者节｜聚焦社会脉动，书写时代故事）他们是时代的记录者，用镜头捕捉瞬间，用文字讲述真实。他们的步伐遍布新闻现场，用敏锐的视角传递社会的脉动。在风雨中奔波，在深夜中敲击键盘，记者们以专业和热情，将真实呈现给公众。作为新时代的青年，你们内心没有一丝丝的自豪吗!举起你们的双手，来为所有的记者祝福！不祝福就不是中国人！今天是第25个中国记者节，让我们向这些默默奉献的新闻工作者致敬！")
]

response = chat.invoke(messages)
print(response)
