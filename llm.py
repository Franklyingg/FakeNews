from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from llm_tools import Url_Tool,Url_parser,Search_Tool,Standing_Tool,Phrase_Tool,Commonsense_Tool,Language_Tool
from exts import OPENAI_API_BASE,OPEN_API_KEY

tools = [Url_Tool,Url_parser,Search_Tool,Standing_Tool,Phrase_Tool,Commonsense_Tool,Language_Tool]
tool_node = ToolNode(tools)
llm = ChatOpenAI(model_name="moonshot-v1-8k", base_url=OPENAI_API_BASE,api_key=OPEN_API_KEY).bind_tools(tools)