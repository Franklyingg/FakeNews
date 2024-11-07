
'''
简单的读取网页内容demo
返回内容为html的document对象
'''


import bs4
from langchain_community.document_loaders import WebBaseLoader

page_url = "https://www.thepaper.cn/newsDetail_forward_29274719"


def search(page_url):
    loader = WebBaseLoader(web_paths=[page_url])
    docs = []
    for doc in loader.lazy_load():
        docs.append(doc)
    return docs

print(search(page_url)[0].page_content.strip())
