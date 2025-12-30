import json
import requests

OLLAMA_MODEL = "qwen3:latest"  # 你的本地模型名称
url = "http://localhost:11434/api/chat"

# 1. 非流式响应（一次性返回完整结果）
print("=== 非流式响应 ===")
payload = {
    "model": OLLAMA_MODEL,
    "messages": [
        {"role": "user", "content": "用一句话介绍Python"}
    ],
    "stream": False,
}

r = requests.post(url, json=payload, timeout=120)
r.raise_for_status()

text = r.json()["message"]["content"]
print(text)

# 2. 流式响应（实时返回，逐字显示）
print("\n=== 流式响应 ===")
payload_stream = {
    "model": OLLAMA_MODEL,
    "messages": [
        {"role": "user", "content": "用一句话介绍Python"}
    ],
    "stream": True,
}

r_stream = requests.post(url, json=payload_stream, stream=True, timeout=120)
r_stream.raise_for_status()

for line in r_stream.iter_lines():
    if line:
        chunk = json.loads(line)
        if "message" in chunk and "content" in chunk["message"]:
            content = chunk["message"]["content"]
            print(content, end="", flush=True)
print()  # 换行

