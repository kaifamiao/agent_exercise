"""
示例1: Python调用大模型的基础示例
使用openai库调用大模型（兼容OpenAI API格式的模型）
"""

from openai import OpenAI

# 初始化客户端
# 这里可以配置不同的API端点，比如本地模型或兼容OpenAI API的模型服务
client = OpenAI(
    # 如果使用OpenAI官方服务，需要设置api_key
    # api_key="your-api-key-here",
    
    # 如果使用本地模型或兼容服务，可以设置base_url
    # base_url="http://localhost:8000/v1",  # 例如使用本地部署的模型
)

def call_llm_basic():
    """基础的大模型调用示例"""
    try:
        # 调用Chat Completions API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 或者使用其他模型名称
            messages=[
                {"role": "system", "content": "你是一个有用的AI助手。"},
                {"role": "user", "content": "请用一句话介绍Python编程语言。"}
            ],
            temperature=0.7,  # 控制输出的随机性
            max_tokens=100    # 最大生成token数
        )
        
        # 提取回复内容
        reply = response.choices[0].message.content
        print("模型回复:")
        print(reply)
        
        return reply
        
    except Exception as e:
        print(f"调用大模型时出错: {e}")
        return None


def call_llm_streaming():
    """流式调用大模型示例（实时返回结果）"""
    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "请写一首关于春天的短诗。"}
            ],
            stream=True  # 启用流式输出
        )
        
        print("流式输出:")
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()  # 换行
        
    except Exception as e:
        print(f"流式调用时出错: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("示例1: 基础大模型调用")
    print("=" * 50)
    
    # 基础调用
    print("\n1. 基础调用:")
    call_llm_basic()
    
    # 流式调用
    print("\n2. 流式调用:")
    call_llm_streaming()

