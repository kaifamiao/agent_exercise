"""
LangChain 最简单的调用示例
展示如何使用 LangChain 调用不同的 LLM
"""

import requests
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
# 最新版本：ChatOllama 从 langchain-ollama 导入
try:
    from langchain_ollama import ChatOllama
except ImportError:
    # 兼容旧版本
    from langchain_community.chat_models import ChatOllama


def check_ollama_connection(base_url="http://localhost:11434"):
    """检查 Ollama 服务是否可用"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            print(f"✓ Ollama 服务运行正常")
            print(f"  可用模型: {', '.join(model_names) if model_names else '无'}")
            return True, model_names
        else:
            print(f"✗ Ollama 服务响应异常: {response.status_code}")
            return False, []
    except requests.exceptions.RequestException as e:
        print(f"✗ 无法连接到 Ollama 服务 ({base_url})")
        print(f"  错误: {e}")
        print(f"  请确保 Ollama 正在运行: ollama serve")
        return False, []


# 示例1: 调用 OpenAI
print("=== OpenAI 调用 ===")
try:
    openai_llm = ChatOpenAI(model="gpt-3.5-turbo")
    response = openai_llm.invoke([HumanMessage(content="你好")])
    print(response.content)
except Exception as e:
    print(f"OpenAI 调用失败: {e}")
    print("提示: 请设置 OPENAI_API_KEY 环境变量")

# 示例2: 调用本地 Ollama
print("\n=== Ollama 调用 ===")
base_url = "http://localhost:11434"
is_available, available_models = check_ollama_connection(base_url)

if is_available:
    # 处理模型名称：去掉 :latest 标签，LangChain 只需要模型名
    if available_models:
        # 检查是否有 qwen3 相关的模型（匹配 qwen3 开头的任何版本）
        qwen_models = [m for m in available_models if m.startswith("qwen3")]
        if qwen_models:
            # 使用第一个 qwen 模型，去掉版本标签
            model_name = qwen_models[0].split(":")[0]
            print(f"使用模型: {model_name} (来自: {qwen_models[0]})")
        else:
            # 使用第一个可用模型
            model_name = available_models[0].split(":")[0]
            print(f"使用模型: {model_name} (来自: {available_models[0]})")
    else:
        print("  没有可用模型，请先拉取模型: ollama pull qwen3")
        exit(1)
    
    # 先测试直接调用 Ollama API 是否正常
    print("\n测试直接调用 Ollama API...")
    try:
        test_response = requests.post(
            f"{base_url}/api/chat",
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": "你好"}],
                "stream": False
            },
            timeout=30
        )
        if test_response.status_code == 200:
            print("✓ 直接 API 调用成功")
            print(f"  回复: {test_response.json()['message']['content']}")
        else:
            print(f"✗ 直接 API 调用失败: {test_response.status_code}")
            print(f"  响应: {test_response.text}")
    except Exception as e:
        print(f"✗ 直接 API 调用异常: {e}")
    
    # 使用 LangChain 调用
    print(f"\n使用 LangChain 调用模型: {model_name}")
    try:
        import os
        # 临时禁用代理，避免 localhost 请求被代理拦截
        old_no_proxy = os.environ.get("NO_PROXY", "")
        old_http_proxy = os.environ.pop("HTTP_PROXY", None)
        old_https_proxy = os.environ.pop("HTTPS_PROXY", None)
        if "localhost" not in old_no_proxy:
            os.environ["NO_PROXY"] = f"localhost,127.0.0.1,{old_no_proxy}".strip(",")
        
        try:
            # 方法1: 使用 ChatOllama（可能需要禁用代理）
            ollama_llm = ChatOllama(
                model=model_name,  # 只使用模型名，不带 :latest
                base_url=base_url,
                timeout=120,
                num_ctx=2048,
            )
            response = ollama_llm.invoke([HumanMessage(content="你好")])
            print(f"✓ LangChain 调用成功")
            print(f"回复: {response.content}")
        finally:
            # 恢复环境变量
            if old_http_proxy:
                os.environ["HTTP_PROXY"] = old_http_proxy
            if old_https_proxy:
                os.environ["HTTPS_PROXY"] = old_https_proxy
            os.environ["NO_PROXY"] = old_no_proxy
    except Exception as e:
        print(f"✗ LangChain 调用失败: {e}")
        print(f"  错误类型: {type(e).__name__}")
        
        # 尝试使用 OpenAI 兼容方式
        print(f"\n尝试使用 OpenAI 兼容方式...")
        try:
            from langchain_openai import ChatOpenAI as ChatOpenAICompat
            ollama_llm_compat = ChatOpenAICompat(
                model=model_name,
                base_url=f"{base_url}/v1",  # Ollama 的 OpenAI 兼容端点
                api_key="ollama",  # Ollama 不需要真实密钥
                timeout=120,
            )
            response = ollama_llm_compat.invoke([HumanMessage(content="你好")])
            print(f"✓ OpenAI 兼容方式调用成功")
            print(f"回复: {response.content}")
        except Exception as e2:
            print(f"✗ OpenAI 兼容方式也失败: {e2}")
            import traceback
            print(f"\n详细错误:\n{traceback.format_exc()}")
            print(f"\n提示:")
            print(f"  1. 确认模型名称: {model_name}")
            print(f"  2. 尝试直接运行: ollama run {model_name}")
            print(f"  3. 检查环境变量 HTTP_PROXY/HTTPS_PROXY，可能需要临时取消设置")
            print(f"  4. 检查 Ollama 日志")
else:
    print("跳过 Ollama 调用（服务不可用）")

