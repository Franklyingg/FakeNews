from langchain_core.tools import tool
from exts import OPENAI_API_BASE,OPEN_API_KEY


@tool
def Url_parser(query: str):
    '''通过给出的URL，获取所需新闻的内容'''
    from langchain_community.document_loaders import WebBaseLoader
    page_url = query
    loader = WebBaseLoader(web_paths=[page_url])
    docs = []
    for doc in loader.lazy_load():
        docs.append(doc)
    return docs[0].page_content.strip()

@tool
def Url(query: str):
    '''通过URL来判断网站是否权威'''
    from langchain_community.llms.moonshot import Moonshot
    llm = Moonshot(model_name="moonshot-v1-8k", api_key=OPEN_API_KEY)
    res = llm.invoke("判断一下这个URL是不是权威新闻网站的URL{}".format(query))
    return res

