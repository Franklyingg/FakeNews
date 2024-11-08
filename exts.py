import os



'''
付费API,勿滥用,将于2025/2/1日取消授权
'''

os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "fakenews"

OPENAI_API_BASE = 'https://api.moonshot.cn/v1'
OPEN_API_KEY = 'sk-AbEqfrS5M7avPzwcfK1FdnAuI0ztiG5rbg29o8K85WSe8ETz'