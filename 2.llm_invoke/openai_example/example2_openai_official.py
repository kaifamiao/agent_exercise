"""
示例2: Python直接使用OpenAI官网接口
使用OpenAI官方SDK调用GPT模型
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def call_openai_gpt():
    """调用OpenAI GPT模型的基础示例"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # 或使用 "gpt-4", "gpt-4-turbo" 等
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的Python编程助手。"
                },
                {
                    "role": "user",
                    "content": "解释一下Python中的列表推导式，并给一个例子。"
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # 获取回复
        assistant_message = response.choices[0].message.content
        print("GPT回复:")
        print(assistant_message)
        print("\n" + "-" * 50)
        
        # 打印使用信息
        print(f"使用的模型: {response.model}")
        print(f"消耗的tokens: {response.usage.total_tokens}")
        print(f"  - 输入tokens: {response.usage.prompt_tokens}")
        print(f"  - 输出tokens: {response.usage.completion_tokens}")
        
        return assistant_message
        
    except Exception as e:
        print(f"调用OpenAI API时出错: {e}")
        if "api_key" in str(e).lower() or "authentication" in str(e).lower():
            print("提示: 请确保设置了正确的OPENAI_API_KEY环境变量")
        return None


def call_openai_with_functions():
    """使用函数调用（Function Calling）的示例"""
    try:
        # 定义函数工具
        functions = [
            {
                "name": "get_weather",
                "description": "获取指定城市的天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，例如：北京、上海"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "温度单位"
                        }
                    },
                    "required": ["city"]
                }
            }
        ]
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "北京今天天气怎么样？"
                }
            ],
            functions=functions,
            function_call="auto"  # 让模型自动决定是否调用函数
        )
        
        message = response.choices[0].message
        
        # 检查是否调用了函数
        if message.function_call:
            print("模型请求调用函数:")
            print(f"函数名: {message.function_call.name}")
            print(f"参数: {message.function_call.arguments}")
        else:
            print("模型回复:")
            print(message.content)
            
    except Exception as e:
        print(f"函数调用示例出错: {e}")


def call_openai_streaming():
    """OpenAI流式调用示例"""
    try:
        print("流式输出:")
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "用Python写一个简单的计算器函数，支持加减乘除。"
                }
            ],
            stream=True
        )
        
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        
        print("\n")
        return full_response
        
    except Exception as e:
        print(f"流式调用出错: {e}")
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("示例2: 使用OpenAI官方API")
    print("=" * 50)
    
    # 基础调用
    print("\n1. 基础GPT调用:")
    # call_openai_gpt()
    
    # 流式调用
    print("\n2. 流式调用:")
    # call_openai_streaming()
    
    # 函数调用示例
    print("\n3. 函数调用示例:")
    call_openai_with_functions()

