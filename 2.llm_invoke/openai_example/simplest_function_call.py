"""
最最简单的函数调用示例
只演示1+1的计算
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


def add(a, b):
    """加法函数"""
    return a + b*2


# 1. 定义函数工具
functions = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个数字的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数字"},
                    "b": {"type": "number", "description": "第二个数字"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

# 2. 用户问：1+2等于多少？
print("用户问题: 1+1等于多少？\n")

# 3. 第一次调用：模型决定调用add函数
# 这一步决定了函数是否会被触发（根据用户问题和函数描述）
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "1+1等于多少？"}],
    tools=functions
)

message = response.choices[0].message

# 4. 如果模型请求调用函数
if message.tool_calls:
    tool_call = message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    
    print(f"模型调用函数: add({args['a']}, {args['b']})")
    
    # 5. 执行函数
    result = add(args['a'], args['b'])
    print(f"计算结果: {result}\n")
    
    # 6. 把结果发给模型，获取最终回复
    # 注意：这里的用户消息必须和第一次调用时保持一致！
    # 因为这是对话历史，模型需要看到完整的上下文才能正确回复
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "1+1等于多少？"},  # 必须和第49行一致
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": "add",
                        "arguments": tool_call.function.arguments
                    }
                }]
            },
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps({"result": result})
            }
        ],
        tools=functions
    )
    
    # 7. 显示最终答案
    print("=" * 40)
    print("最终答案:")
    print(final_response.choices[0].message.content)
    print("=" * 40)

