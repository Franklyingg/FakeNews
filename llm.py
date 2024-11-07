from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from llm_tools import Url,Url_parser
from exts import OPENAI_API_BASE,OPEN_API_KEY

tools = [Url,Url_parser]
tool_node = ToolNode(tools)
llm = ChatOpenAI(model_name="moonshot-v1-8k", base_url=OPENAI_API_BASE,api_key=OPEN_API_KEY).bind_tools(tools)