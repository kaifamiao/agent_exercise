"""
最简单的函数调用示例
演示如何让OpenAI调用一个简单的数学计算函数（如1+1）
"""

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def calculate(a: float, b: float, operation: str = "add") -> float:
    """
    简单的数学计算函数
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        result = a / b if b != 0 else None
    else:
        result = None
    
    return result


def simple_function_call_example():
    """
    最简单的函数调用示例
    """
    # 1. 定义函数工具
    functions = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "执行简单的数学计算，支持加法、减法、乘法、除法",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "第一个数字"
                        },
                        "b": {
                            "type": "number",
                            "description": "第二个数字"
                        },
                        "operation": {
                            "type": "string",
                            "enum": ["add", "subtract", "multiply", "divide"],
                            "description": "运算类型：add(加法), subtract(减法), multiply(乘法), divide(除法)"
                        }
                    },
                    "required": ["a", "b", "operation"]
                }
            }
        }
    ]
    
    # 2. 用户查询
    user_query = "帮我计算1+1等于多少？"
    print(f"用户问题: {user_query}\n")
    
    # 3. 第一次调用：让模型决定是否调用函数
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": user_query
            }
        ],
        tools=functions,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    # 4. 检查模型是否请求调用函数
    if message.tool_calls:
        print("模型请求调用函数:")
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"  函数名: {function_name}")
            print(f"  参数: {function_args}\n")
            
            # 5. 执行函数调用
            if function_name == "calculate":
                a = function_args.get("a")
                b = function_args.get("b")
                operation = function_args.get("operation")
                
                result = calculate(a, b, operation)
                print(f"函数计算结果: {result}\n")
                
                # 6. 将函数结果发送回模型，获取最终回复
                final_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": user_query
                        },
                        {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": function_name,
                                        "arguments": tool_call.function.arguments
                                    }
                                }
                            ]
                        },
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"result": result}, ensure_ascii=False)
                        }
                    ],
                    tools=functions
                )
                
                # 7. 显示最终回复
                final_message = final_response.choices[0].message
                print("=" * 50)
                print("最终回复:")
                print("=" * 50)
                print(final_message.content)
                print("=" * 50)
    else:
        print("模型直接回复（未调用函数）:")
        print(message.content)


def multiple_examples():
    """
    多个计算示例
    """
    examples = [
        "1+1等于多少？",
        "帮我算一下10乘以5",
        "100减去25是多少？",
        "50除以2等于多少？"
    ]
    
    functions = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "执行简单的数学计算，支持加法、减法、乘法、除法",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "第一个数字"
                        },
                        "b": {
                            "type": "number",
                            "description": "第二个数字"
                        },
                        "operation": {
                            "type": "string",
                            "enum": ["add", "subtract", "multiply", "divide"],
                            "description": "运算类型：add(加法), subtract(减法), multiply(乘法), divide(除法)"
                        }
                    },
                    "required": ["a", "b", "operation"]
                }
            }
        }
    ]
    
    for query in examples:
        print(f"\n{'='*60}")
        print(f"问题: {query}")
        print('='*60)
        
        # 第一次调用
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": query}],
            tools=functions,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments)
                a = function_args.get("a")
                b = function_args.get("b")
                operation = function_args.get("operation")
                
                result = calculate(a, b, operation)
                
                # 第二次调用获取最终回复
                final_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": query},
                        {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [{
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments
                                }
                            }]
                        },
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"result": result}, ensure_ascii=False)
                        }
                    ],
                    tools=functions
                )
                
                print(f"答案: {final_response.choices[0].message.content}")


if __name__ == "__main__":
    print("=" * 60)
    print("最简单的函数调用示例：数学计算")
    print("=" * 60)
    print()
    
    # 单个示例
    simple_function_call_example()
    
    # 多个示例（可选）
    # print("\n\n")
    # print("=" * 60)
    # print("多个计算示例")
    # print("=" * 60)
    # multiple_examples()

