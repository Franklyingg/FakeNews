import os
import re

from langchain_core.tools import tool
from exts import OPENAI_API_BASE,OPEN_API_KEY


@tool
def Url_parser(query: str):
    '''输入URL，获取所需新闻内容'''
    from langchain_community.document_loaders import WebBaseLoader
    page_url = query
    loader = WebBaseLoader(web_paths=[page_url])
    docs = []
    for doc in loader.lazy_load():
        docs.append(doc)
    from langchain_community.llms.moonshot import Moonshot
    llm = Moonshot(model_name="moonshot-v1-8k", api_key=OPEN_API_KEY)
    res = llm.invoke("优化下面文章的格式，提取其中的所有新闻内容 \n{}".format(docs[0].page_content.strip()))
    return res

@tool
def Url_Tool(query: str):
    '''通过URL来判断网站是否权威'''
    from langchain_community.llms.moonshot import Moonshot
    llm = Moonshot(model_name="moonshot-v1-8k", api_key=OPEN_API_KEY)
    res = llm.invoke("判断一下这个URL是不是权威新闻网站的URL{}".format(query))
    return res

@tool
def Phrase_Tool(query:str):
    '''输入新闻内容,检测新闻是否存在挑衅性和情绪化的语言'''
    from langchain_community.llms.moonshot import Moonshot
    llm = Moonshot(model_name="moonshot-v1-8k", api_key=OPEN_API_KEY)
    res = llm.invoke("判断一下新闻中是否存在挑衅性和情绪化的语言，请认真判断，不要误判。你只能返回格式化的信息内容，如存在请以[{'原文':'文章内容'：'问题':'文字存在的问题'}]的列表形式返回,若不存在请单独返回空列表[]，不要返回任何无关内容。"+" \n {article}".format(article=query))
    return res

@tool
def Language_Tool(query: str):
    '''输入新闻内容，旨在识别新闻报道中的语法错误、措辞错误、引号的误用或全部大写的单词'''
    from langchain_community.llms.moonshot import Moonshot
    llm = Moonshot(model_name="moonshot-v1-8k", api_key=OPEN_API_KEY)
    res = llm.invoke("识别一下新闻中存在的语法错误,措辞错误，引号无用和是否存在全部大写的单词请认真判断，不要误判。你只能返回格式化的信息内容，如存在请以[{'原文':'文章内容'：'问题':'文字存在的问题'}]的列表形式返回,若不存在请单独返回空列表[]，不要返回任何无关内容。"+" \n {article}".format(article=query))
    return res

@tool
def Search_Tool(query: str):
    '''输入新闻内容，搜索获取互联网中相关内容,用于搜索其他媒体资源报道的任何冲突信息'''
    from langchain_community.llms.moonshot import Moonshot
    llm = Moonshot(model_name="moonshot-v1-8k", api_key=OPEN_API_KEY)
    llm2 = Moonshot(model_name="moonshot-v1-32k", api_key=OPEN_API_KEY)
    title = llm.invoke("阅读一下新闻，查找或生成新闻标题，20字以内 \n {article}".format(article=query))

    os.environ["SEARCHAPI_API_KEY"] = 'wpcriK7bESpT4LRVfpjpMz6u'
    from langchain_community.tools import SearchAPIResults
    search = SearchAPIResults()
    s_res = search.invoke(title)
    chinese_chars = re.findall(r'[\u4e00-\u9fff]+', s_res)
    res = ''.join(chinese_chars)
    f = llm2.invoke("比对一下下面给出的两段信息,第一段为原始新闻，第二段为互联网搜索的相关信息,判断一下原始新闻是否为假新闻.你只能返回格式化的信息内容，你只有三个回答： 是 不是 无法判断，不要返回其他任何无关内容。 \n 原始新闻{article1} \n互联网信息：{article2}".format(article1=query,article2=res[:10000]))
    return f

@tool
def Commonsense_Tool(query: str):
    '''输入新闻内容，旨在评估新闻报道的合理性，并寻找与常识识别任何矛盾之处'''
    from langchain_community.llms.moonshot import Moonshot
    llm = Moonshot(model_name="moonshot-v1-8k", api_key=OPEN_API_KEY)
    res = llm.invoke("评估新闻报道的合理性，并寻找与常识识别任何矛盾之处，不要误判。你只能返回格式化的信息内容，如存在，请仅以[{'原文':'文章内容'：'问题':'文字存在的问题'}]的列表形式返回,若不存在仅单独返回空列表[]，不要返回任何其他无关内容。"+" \n {article}".format(article=query))
    return res

@tool
def Standing_Tool(query: str):
    '''输入新闻内容，旨在评估新闻报道的合理性，并寻找与常识识别任何矛盾之处'''
    from langchain_community.llms.moonshot import Moonshot
    llm = Moonshot(model_name="moonshot-v1-8k", api_key=OPEN_API_KEY)
    res = llm.invoke("检测新闻是否宣传特定观点，而不是呈现客观事实，不要误判。你只能返回格式化的信息内容，如存在，请仅以[{'原文':'文章内容'：'问题':'文字存在的问题'}]的列表形式返回,若不存在仅单独返回空列表[]，不要返回任何无关内容。"+" \n {article}".format(article=query))
    return res


