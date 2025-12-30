"""
使用 Ollama 官方 Python 包的示例
这是最直接、最简单的方式调用本地 Ollama 模型
"""

import ollama

# 初始化客户端（默认连接到 http://localhost:11434）
client = ollama.Client()

# 1. 非流式响应（一次性返回完整结果）
print("=== 非流式响应 ===")
response = client.chat(
    model="qwen3",  # 你的本地模型名称
    messages=[
        {"role": "user", "content": "用一句话介绍Python"}
    ]
)
print(response["message"]["content"])

# 2. 流式响应（实时返回，逐字显示）
print("\n=== 流式响应 ===")
stream = client.chat(
    model="qwen3",
    messages=[
        {"role": "user", "content": "用一句话介绍Python"}
    ],
    stream=True
)
for chunk in stream:
    if chunk["message"]["content"]:
        print(chunk["message"]["content"], end="", flush=True)
print()  # 换行

# 3. 生成文本（generate 方法，不需要消息格式）
print("\n=== 使用 generate 方法 ===")
response = ollama.generate(
    model="qwen3",
    prompt="用一句话介绍Python"
)
print(response["response"])

# 4. 流式生成
print("\n=== 流式 generate ===")
stream = ollama.generate(
    model="qwen3",
    prompt="用一句话介绍Python",
    stream=True
)
for chunk in stream:
    if chunk["response"]:
        print(chunk["response"], end="", flush=True)
print()  # 换行

# 5. 列出可用模型
print("\n=== 可用模型列表 ===")
try:
    models_response = ollama.list()
    # ollama.list() 返回的对象，使用属性访问
    for model in models_response.models:
        # Model 对象使用 model 属性存储模型名（不是 name）
        model_name = getattr(model, 'model', None)
        if model_name:
            print(f"  - {model_name}")
        else:
            # 尝试其他方式
            try:
                # 使用 model_dump() 转换为字典
                if hasattr(model, 'model_dump'):
                    model_dict = model.model_dump()
                    model_name = model_dict.get('model') or model_dict.get('name', 'unknown')
                else:
                    model_name = str(model)
                print(f"  - {model_name}")
            except Exception as e2:
                print(f"  - {model} (无法获取名称: {e2})")
except Exception as e:
    print(f"  获取模型列表失败: {e}")

