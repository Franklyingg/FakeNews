'''
互联网搜索
'''
import os

from langchain_community.tools import SearchAPIResults
os.environ["SEARCHAPI_API_KEY"] = 'wpcriK7bESpT4LRVfpjpMz6u'

search = SearchAPIResults()



res = search.invoke("特朗普是否选上总统的英文新闻")
print(type(res),res[:6000])