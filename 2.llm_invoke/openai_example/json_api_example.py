"""
OpenAI调用返回JSON的函数示例
演示如何让大模型调用一个返回JSON格式数据的函数（模拟API返回）
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


def get_user_info(user_id: str) -> dict:
    """
    模拟API调用，返回JSON格式的用户信息
    这相当于一个真实的API返回
    """
    # 模拟数据库查询
    users_db = {
        "001": {
            "user_id": "001",
            "name": "张三",
            "age": 28,
            "email": "zhangsan@example.com",
            "city": "北京",
            "status": "active",
            "created_at": "2023-01-15",
            "balance": 1250.50
        },
        "002": {
            "user_id": "002",
            "name": "李四",
            "age": 32,
            "email": "lisi@example.com",
            "city": "上海",
            "status": "active",
            "created_at": "2022-11-20",
            "balance": 3200.00
        },
        "003": {
            "user_id": "003",
            "name": "王五",
            "age": 25,
            "email": "wangwu@example.com",
            "city": "深圳",
            "status": "inactive",
            "created_at": "2024-03-10",
            "balance": 500.25
        }
    }
    
    user_info = users_db.get(user_id)
    
    if not user_info:
        return {
            "success": False,
            "error": "用户不存在",
            "user_id": user_id
        }
    
    # 返回JSON格式的数据（模拟API返回）
    return {
        "success": True,
        "data": user_info,
        "timestamp": "2024-12-30T10:30:00Z"
    }


def get_all_users() -> dict:
    """
    获取所有用户信息，返回JSON格式的用户列表
    用于回答"有几个用户"等问题
    """
    # 模拟数据库查询 - 返回所有用户
    users_db = {
        "001": {
            "user_id": "001",
            "name": "张三",
            "age": 28,
            "email": "zhangsan@example.com",
            "city": "北京",
            "status": "active",
            "created_at": "2023-01-15",
            "balance": 1250.50
        },
        "002": {
            "user_id": "002",
            "name": "李四",
            "age": 32,
            "email": "lisi@example.com",
            "city": "上海",
            "status": "active",
            "created_at": "2022-11-20",
            "balance": 3200.00
        },
        "003": {
            "user_id": "003",
            "name": "王五",
            "age": 25,
            "email": "wangwu@example.com",
            "city": "深圳",
            "status": "inactive",
            "created_at": "2024-03-10",
            "balance": 500.25
        }
    }
    
    # 返回JSON格式的数据（模拟API返回）
    return {
        "success": True,
        "total": len(users_db),
        "users": list(users_db.values()),
        "timestamp": "2024-12-30T10:30:00Z"
    }


def call_json_api_with_openai(user_query: str):
    """
    使用OpenAI的Function Calling功能调用返回JSON的函数
    """
    try:
        # 定义函数工具
        functions = [
            {
                "type": "function",
                "function": {
                    "name": "get_user_info",
                    "description": "根据用户ID获取单个用户信息，返回JSON格式的用户数据，包括姓名、年龄、邮箱、城市、状态、余额等信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "用户ID，例如：001、002、003"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_all_users",
                    "description": "获取所有用户信息列表，返回JSON格式的数据，包括用户总数和所有用户的详细信息。用于回答'有几个用户'、'所有用户'、'用户列表'等问题",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]
        
        print(f"用户查询: {user_query}\n")
        
        # 第一步：发送用户查询，让模型决定是否调用函数
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个用户数据查询助手。当用户询问用户信息、用户数量时，你需要调用相应的函数获取JSON格式的数据，然后解析并友好地向用户解释这些数据。如果用户问'有几个用户'或类似问题，应该调用get_all_users函数。"
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            tools=functions,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        messages = [
            {
                "role": "system",
                "content": "你是一个数据查询助手。当用户询问用户信息、用户数量、商品信息时，你需要调用相应的函数获取JSON格式的数据，然后解析并友好地向用户解释这些数据。如果用户问'有几个用户'，应该调用get_all_users函数。"
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
        
        # 检查模型是否请求调用函数
        if message.tool_calls:
            print("模型请求调用函数:")
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"  函数名: {function_name}")
                print(f"  参数: {function_args}\n")
                
                # 执行函数调用（模拟API调用，返回JSON）
                json_result = None
                
                if function_name == "get_user_info":
                    user_id = function_args.get("user_id")
                    json_result = get_user_info(user_id)
                    
                elif function_name == "get_all_users":
                    json_result = get_all_users()
                
                # 打印返回的JSON数据
                print("函数返回的JSON数据:")
                print(json.dumps(json_result, ensure_ascii=False, indent=2))
                print()
                
                # 将函数调用结果添加到消息历史
                messages.append({
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
                })
                
                # 添加函数执行结果（JSON格式）
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(json_result, ensure_ascii=False)
                })
            
            # 第二步：将JSON结果发送回模型，让模型解析并生成最终回复
            print("将JSON数据发送给模型，让模型解析并生成回复...\n")
            final_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=functions
            )
            
            final_message = final_response.choices[0].message
            print("=" * 60)
            print("最终回复:")
            print("=" * 60)
            print(final_message.content)
            print("=" * 60)
            
            return final_message.content, json_result
            
        else:
            # 模型没有调用函数，直接返回回复
            print("模型直接回复（未调用函数）:")
            print(message.content)
            return message.content, None
            
    except Exception as e:
        print(f"调用OpenAI API时出错: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def main():
    """主函数"""
    print("=" * 60)
    print("OpenAI调用返回JSON的函数示例")
    print("=" * 60)
    print()
    
    # 示例查询


    queries = [
        "余额小于1000的用户"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"示例 {i}:")
        print(f"{'='*60}\n")
        call_json_api_with_openai(query)
        print("\n")


if __name__ == "__main__":
    main()

