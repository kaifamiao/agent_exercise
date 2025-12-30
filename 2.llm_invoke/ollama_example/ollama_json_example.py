import json
import requests

OLLAMA_MODEL = "qwen3:latest"  # 你的本地模型名称
url = "http://localhost:11434/api/chat"

# 示例：要求模型输出 JSON 格式
TASK = "请列出3个Python的优点，并以JSON格式返回，包含'bullets'（列表）和'todo'（字符串）字段"

payload = {
    "model": OLLAMA_MODEL,
    "messages": [
        {"role": "system", "content": "你是严谨的助手，必须输出严格 JSON。"},
        {"role": "user", "content": TASK},
    ],
    "stream": False,
}

r = requests.post(url, json=payload, timeout=120)
r.raise_for_status()

# 获取模型返回的文本
text = r.json()["message"]["content"]
print("原始返回:")
print(text)
print("\n" + "="*50 + "\n")

# 解析 JSON（可能需要清理文本，去除可能的 markdown 代码块标记）
try:
    # 尝试直接解析
    data = json.loads(text)
except json.JSONDecodeError:
    # 如果失败，尝试去除 markdown 代码块标记
    cleaned_text = text.strip()
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]  # 移除 ```json
    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[3:]  # 移除 ```
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]  # 移除结尾的 ```
    data = json.loads(cleaned_text.strip())

# 使用解析后的数据
print("解析后的数据:")
if "bullets" in data:
    print("优点列表:")
    for bullet in data["bullets"]:
        print(f"  - {bullet}")
if "todo" in data:
    print(f"\n待办: {data['todo']}")

