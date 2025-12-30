"""
LangChain 最简单的调用示例
展示如何使用 LangChain 调用不同的 LLM
"""

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage


# 示例2: 调用本地 Ollama
print("\n=== Ollama 调用 ===")
try:
    from langchain_ollama import ChatOllama
except ImportError:
    from langchain_community.chat_models import ChatOllama

ollama_llm = ChatOllama(model="qwen3")
response = ollama_llm.invoke([HumanMessage(content="你好")])
print(response.content)

