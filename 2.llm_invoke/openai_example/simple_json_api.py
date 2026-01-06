"""
最简单的JSON API调用示例
演示大模型如何调用一个返回JSON格式数据的函数
"""

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def get_data(id: str) -> dict:
    """
    模拟API调用，返回JSON格式的数据
    这个函数相当于一个真实的API接口
    """
    # 模拟API返回的JSON数据
    data = {
        "id": id,
        "name": "示例数据",
        "value": 100,
        "status": "active",
        "items": [
            {"item_id": "A001", "count": 5},
            {"item_id": "A002", "count": 3}
        ],
        "metadata": {
            "created_at": "2024-12-30",
            "updated_at": "2024-12-30"
        }
    }
    
    return data


# 1. 定义函数工具
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_data",
            "description": "根据ID获取数据，返回JSON格式的数据",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "数据ID"
                    }
                },
                "required": ["id"]
            }
        }
    }
]

# 2. 用户查询
user_query = "查询ID为123的数据"
print(f"用户查询: {user_query}\n")

# 3. 第一次调用：模型决定调用函数
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": user_query}],
    tools=functions
)

message = response.choices[0].message

# 4. 如果模型请求调用函数
if message.tool_calls:
    tool_call = message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    
    print(f"模型调用函数: get_data({args['id']})")
    
    # 5. 执行函数，获取JSON数据（模拟API调用）
    json_data = get_data(args['id'])
    
    print("\n函数返回的JSON数据:")
    print(json.dumps(json_data, ensure_ascii=False, indent=2))
    print()
    
    # 6. 将JSON数据发送回模型，让模型解析并生成回复
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": user_query},
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": "get_data",
                        "arguments": tool_call.function.arguments
                    }
                }]
            },
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(json_data, ensure_ascii=False)  # 返回JSON字符串
            }
        ],
        tools=functions
    )
    
    # 7. 显示最终回复
    print("=" * 50)
    print("最终回复:")
    print("=" * 50)
    print(final_response.choices[0].message.content)
    print("=" * 50)

