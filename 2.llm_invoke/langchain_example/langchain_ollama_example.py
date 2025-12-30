import requests
from langchain_core.messages import HumanMessage
# 最新版本：ChatOllama 从 langchain-ollama 导入
try:
    from langchain_ollama import ChatOllama, Ollama
except ImportError:
    # 兼容旧版本
    from langchain_community.chat_models import ChatOllama
    from langchain_community.llms import Ollama

base_url = "http://localhost:11434"
model_name = "qwen3"  # 你的本地模型名称

# 检查 Ollama 服务
print("检查 Ollama 服务...")
try:
    response = requests.get(f"{base_url}/api/tags", timeout=5)
    if response.status_code == 200:
        models = response.json().get("models", [])
        model_names = [m.get("name", "").split(":")[0] for m in models]
        if model_names:
            print(f"✓ 可用模型: {', '.join(model_names)}")
            if model_name not in model_names:
                print(f"⚠ 模型 '{model_name}' 不存在，使用第一个可用模型: {model_names[0]}")
                model_name = model_names[0]
        else:
            print("⚠ 没有可用模型")
    else:
        print(f"✗ Ollama 服务响应异常")
        exit(1)
except Exception as e:
    print(f"✗ 无法连接到 Ollama 服务: {e}")
    print("  请确保 Ollama 正在运行: ollama serve")
    exit(1)

# 方式1: 使用 ChatOllama（推荐，支持消息格式）
print(f"\n=== 方式1: 使用 ChatOllama (模型: {model_name}) ===")
try:
    llm = ChatOllama(
        model=model_name,
        base_url=base_url,
        timeout=120
    )

    # 非流式响应
    print("\n--- 非流式响应 ---")
    messages = [HumanMessage(content="用一句话介绍Python")]
    response = llm.invoke(messages)
    print(response.content)

    # 流式响应
    print("\n--- 流式响应 ---")
    messages = [HumanMessage(content="用一句话介绍Python")]
    for chunk in llm.stream(messages):
        if chunk.content:
            print(chunk.content, end="", flush=True)
    print()  # 换行
except Exception as e:
    print(f"✗ ChatOllama 调用失败: {e}")

# 方式2: 使用 Ollama（传统方式，直接文本输入输出）
print(f"\n=== 方式2: 使用 Ollama（文本模式，模型: {model_name}） ===")
try:
    llm_text = Ollama(
        model=model_name,
        base_url=base_url,
        timeout=120
    )

    # 非流式
    print("\n--- 非流式响应 ---")
    response = llm_text.invoke("用一句话介绍Python")
    print(response)

    # 流式
    print("\n--- 流式响应 ---")
    for chunk in llm_text.stream("用一句话介绍Python"):
        print(chunk, end="", flush=True)
    print()  # 换行
except Exception as e:
    print(f"✗ Ollama 调用失败: {e}")

