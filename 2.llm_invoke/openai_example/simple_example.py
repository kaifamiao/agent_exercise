import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# OpenAI 配置
# 从环境变量读取 API key（.env 文件中设置 OPENAI_API_KEY）
# 也可以设置 base_url（如果使用 OpenAI 兼容的服务）
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")  # 可选，默认为 OpenAI 官方地址

client = OpenAI(
    api_key=api_key,
    base_url=base_url if base_url else None  # 如果不设置则使用默认值
)

# 1. 非流式响应（一次性返回完整结果）
print("=== 非流式响应 ===")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "用一句话介绍Python"}]
)
print(response.choices[0].message.content)

# 2. 流式响应（实时返回，逐字显示）
print("\n=== 流式响应 ===")
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "用一句话介绍Python"}],
    stream=True
)
for chunk in stream:
    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()  # 换行

