from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 初始化 OpenAI 模型（需要设置 OPENAI_API_KEY 环境变量）
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7
)

# 1. 非流式响应
print("=== 非流式响应 ===")
messages = [HumanMessage(content="用一句话介绍Python")]
response = llm.invoke(messages)
print(response.content)

# 2. 流式响应
print("\n=== 流式响应 ===")
messages = [HumanMessage(content="用一句话介绍Python")]
for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)
print()  # 换行

