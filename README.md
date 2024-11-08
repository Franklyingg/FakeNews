# 虚假新闻检测Agent
***
本程序实现了AIAgent虚假新闻检测基础功能

## 使用的工具如下：

1. URL Paser
   - 输入新闻URL
   - 获取所有的html内容
   - 返回所有文本内容
2. Phrase Tool
   - 检测文章是否存在挑衅性和情绪化的语言
   - 它的运作假设是假新闻经常使用这些策略来吸引读者的注意力。
3. Language Tool
   - 旨在识别新闻报道中的语法错误、措辞错误、引号的误用或全部大写的单词
   - 它假设假新闻通常包含此类错误，以过分强调可信度或吸引读者
4. Commonsense Tool
   - 该工具利用 LLM 的内部知识来评估新闻报道的合理性，并与常识识别任何矛盾之处。
   - 它的运作假设是假新闻可能类似于八卦而不是事实报道，并且可能包含与常识相矛盾的元素。
5. Standing Tool
    - 该工具专为与政治相关的新闻而设计，旨在检测新闻是否宣传特定观点，而不是呈现客观事实。
    - 它的运作假设是假政治新闻通常会强化目标受众所持有的现有信念或偏见。此外，它可能通过以负面方式描绘政治对手或妖魔化某些群体来促进两极分化。
6. Search Tool
   - 该工具利用 SearchAPI 来搜索其他媒体资源报道的任何冲突信息。总结说，假新闻通常包含未经证实的信息，几乎没有证据来支持所提出的主张。
   - 利用 SearchAPI 还可以通过使用外部知识来交叉引用和验证新闻声明，从而缓解 LLM 的幻觉问题。
7. Url Tool
   - 该工具集成了 LLM 内部和外部知识，以评估新闻声明是否来自缺乏可信度的域 URL。它首先利用 LLM 内部知识来获得域 URL 的概述。然后通过外部知识库验证 URL 的真实和虚假新闻，以增强对域 URL 的理解。
   - 这个工具的基础假设是假新闻通常来自不可信的领域。每当新闻文章经过验证时，外部知识库都可以更新，确保其及时性和可靠性。
>demo文件 :  程序最小功能模块实现,实现内容顺序与上文工具描述无关

## 运作流程表：
1. 如果新闻来自一个不知名/有怀疑的URl，则新闻有可能是假的
2. 如果新闻标题中存在包含煽情，挑衅性，情绪化的语言，以此来吸引读者的注意力，或暗示谣言，那么可能是假的
3. 如果新闻存在拼写错误的单词，语法错误，滥用引用或者全大写的单词，那可能是假的
4. 如果新闻不合理或者与常识相矛盾，或者新闻更像一片八卦而不是事实报道，则可能是假的
5. 如果新闻偏向于特定的政治观点，旨在影响公众舆论，而不是提供客观信息，那么他可能是假的
6. 如果其他的网络来源，包括不一样，冲突或者矛盾的内容，那么新闻可能是假的


## 内容介绍
1. exts.py
   - 存放内容为MoonShotKimi API密钥 ，LangSmith 跟踪调试工具API
   - 若需要使用LangSmith 需前往Langsmith官网注册并创建项目
   - ![图片说明](rsc\langsmith.png)  
   - 复制tracing跟踪调试相关环境变量，并替换exts内相关
2. FakeNews.py
   - 程序主程序
   - class State（TypedDict）为一个字典类型的类，代表整个Chain路径下的状态。内部定义一个成员变量（key）为messages，并annotated[list, add_messages]每次迭代更新时都会加入新的记录（即字典的value为列表类型，每次都会在其中加入新的元素）.
   - should_continue / call_model 两串业务逻辑代码,作用为被图中相应节点所调用，当逻辑运行至相关节点时，会调用此函数，函数的参数为当前Chain下的状态（一般为所有的对话记录）
   - 生成langgraph图（添加节点与边）
   - ![图片说明](rsc\graph.png)  
3. llm
   - 程序使用的llm模型对象(需要import llm_tools 中的工具，将tools与llm绑定)
4. llm_tools
   - 程序使用的llm工具集


