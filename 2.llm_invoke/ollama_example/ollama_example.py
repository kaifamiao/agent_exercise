from openai import OpenAI

# 连接本地 Ollama（默认端口 11434）
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama 不需要真实密钥，但需要提供
)

# 1. 非流式响应（一次性返回完整结果）
print("=== 非流式响应 ===")
response = client.chat.completions.create(
    model="qwen3:latest",  # 你的本地模型名称
    messages=[{"role": "user", "content": "用一句话介绍Python"}]
)
print(response.choices[0].message.content)

# 2. 流式响应（实时返回，逐字显示）
print("\n=== 流式响应 ===")
stream = client.chat.completions.create(
    model="qwen3:latest",
    messages=[{"role": "user", "content": "用一句话介绍Python"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()  # 换行

