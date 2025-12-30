from openai import OpenAI

client = OpenAI(api_key="your-api-key-here")

# 1. 非流式响应（一次性返回完整结果）
print("=== 非流式响应 ===")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "用一句话介绍Python"}]
)
print(response.choices[0].message.content)

# 2. 流式响应（实时返回，逐字显示）
print("\n=== 流式响应 ===")
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "用一句话介绍Python"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()  # 换行

