"""
OpenAI调用天气API示例
演示如何使用OpenAI的Function Calling功能调用外部天气API
使用免费的天气API（无需API key）
"""

from openai import OpenAI
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def translate_city_to_english(city: str) -> str:
    """
    将中文城市名转换为英文（Open-Meteo地理编码API需要）
    """
    city_map = {
        "北京": "Beijing",
        "上海": "Shanghai",
        "广州": "Guangzhou",
        "深圳": "Shenzhen",
        "杭州": "Hangzhou",
        "成都": "Chengdu",
        "南京": "Nanjing",
        "武汉": "Wuhan",
        "西安": "Xi'an",
        "重庆": "Chongqing"
    }
    return city_map.get(city, city)


def get_weather_from_openmeteo(city: str, unit: str = "celsius") -> dict:
    """
    使用 Open-Meteo 免费天气API（不需要API key）
    网址: https://open-meteo.com
    """
    try:
        # 首先需要获取城市的地理坐标
        city_english = translate_city_to_english(city)
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocoding_params = {
            "name": city_english,
            "count": 1,
            "language": "zh"
        }
        
        geo_response = requests.get(geocoding_url, params=geocoding_params, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return None
        
        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location.get("name", city)
        
        # 获取天气数据
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto"
        }
        
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data["current"]
        
        # 温度单位转换
        temp = current["temperature_2m"]
        if unit == "fahrenheit":
            temp = temp * 9 / 5 + 32
            temp_unit = "°F"
        else:
            temp_unit = "°C"
        
        # 天气代码转换为描述
        weather_codes = {
            0: "晴朗", 1: "大部分晴朗", 2: "部分多云", 3: "阴天",
            45: "雾", 48: "沉积霜雾",
            51: "小雨", 53: "中雨", 55: "大雨",
            61: "小雨", 63: "中雨", 65: "大雨",
            71: "小雪", 73: "中雪", 75: "大雪",
            80: "小雨", 81: "中雨", 82: "大雨",
            85: "小雪", 86: "大雪",
            95: "雷暴", 96: "雷暴带冰雹", 99: "强雷暴带冰雹"
        }
        weather_desc = weather_codes.get(current["weather_code"], "未知")
        
        return {
            "city": city_name,
            "temperature": round(temp, 1),
            "description": weather_desc,
            "humidity": int(current["relative_humidity_2m"]),
            "wind_speed": round(current["wind_speed_10m"] / 3.6, 1),  # 转换为m/s
            "unit": temp_unit
        }
    except Exception as e:
        print(f"Open-Meteo API调用失败: {e}")
        return None


def get_weather_from_wttr(city: str, unit: str = "celsius") -> dict:
    """
    使用 wttr.in 免费天气API（不需要API key）
    网址: https://wttr.in
    """
    try:
        # wttr.in 支持中文城市名
        city_encoded = city.replace(" ", "+")
        url = f"https://wttr.in/{city_encoded}?format=j1&lang=zh"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data["current_condition"][0]
        
        # 温度转换
        temp_c = float(current["temp_C"])
        if unit == "fahrenheit":
            temp = float(current["temp_F"])
            temp_unit = "°F"
        else:
            temp = temp_c
            temp_unit = "°C"
        
        return {
            "city": city,
            "temperature": temp,
            "description": current["lang_zh"][0]["value"] if current.get("lang_zh") else current["weatherDesc"][0]["value"],
            "humidity": int(current["humidity"]),
            "wind_speed": float(current["windspeedKmph"]) / 3.6,  # 转换为m/s
            "unit": temp_unit
        }
    except Exception as e:
        print(f"wttr.in API调用失败: {e}")
        return None


def get_weather_from_api(city: str, unit: str = "celsius") -> dict:
    """
    调用免费天气API获取天气信息
    按顺序尝试：Open-Meteo -> wttr.in
    """
    print(f"正在获取 {city} 的天气信息...")
    
    # 1. 尝试 Open-Meteo（推荐）
    print("尝试 Open-Meteo API...")
    result = get_weather_from_openmeteo(city, unit)
    if result:
        print("✅ 使用 Open-Meteo API 成功\n")
        return result
    
    # 2. 尝试 wttr.in
    print("尝试 wttr.in API...")
    result = get_weather_from_wttr(city, unit)
    if result:
        print("✅ 使用 wttr.in API 成功\n")
        return result
    
    # 如果都失败
    print("❌ 所有免费天气API都调用失败")
    return None


def call_weather_with_openai(user_query: str):
    """
    使用OpenAI的Function Calling功能调用天气API
    """
    try:
        # 定义天气查询函数工具
        functions = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "获取指定城市的当前天气信息，包括温度、天气描述、湿度、风速等",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市名称，例如：北京、上海、广州、深圳"
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "温度单位，celsius表示摄氏度，fahrenheit表示华氏度",
                                "default": "celsius"
                            }
                        },
                        "required": ["city"]
                    }
                }
            }
        ]
        
        # 第一步：发送用户查询，让模型决定是否调用函数
        print(f"用户查询: {user_query}\n")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个天气查询助手。当用户询问天气时，你需要调用get_weather函数获取天气信息，然后用友好的方式向用户解释天气情况。"
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
                "content": "你是一个天气查询助手。当用户询问天气时，你需要调用get_weather函数获取天气信息，然后用友好的方式向用户解释天气情况。"
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
        
        # 检查模型是否请求调用函数
        if message.tool_calls:
            print("模型请求调用天气API:")
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"  函数名: {function_name}")
                print(f"  参数: {function_args}\n")
                
                # 执行函数调用
                if function_name == "get_weather":
                    city = function_args.get("city")
                    unit = function_args.get("unit", "celsius")
                    
                    # 调用天气API
                    weather_data = get_weather_from_api(city, unit)
                    
                    if not weather_data:
                        weather_data = {
                            "city": city,
                            "error": "无法获取天气数据，请稍后重试"
                        }
                    
                    print(f"天气API返回数据: {weather_data}\n")
                    
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
                    
                    # 添加函数执行结果
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(weather_data, ensure_ascii=False)
                    })
            
            # 第二步：将函数执行结果发送回模型，让模型生成最终回复
            print("将天气数据发送给模型，生成最终回复...\n")
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
            
            return final_message.content, weather_data
            
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


def test_weather_api_directly(city: str = "Beijing"):
    """
    直接测试天气API调用，用于调试
    """
    print("=" * 60)
    print("直接测试免费天气API")
    print("=" * 60)
    print(f"测试城市: {city}\n")
    
    result = get_weather_from_api(city)
    if result:
        print("✅ API调用成功！")
        print(f"城市: {result['city']}")
        print(f"温度: {result['temperature']}{result['unit']}")
        print(f"天气: {result['description']}")
        print(f"湿度: {result['humidity']}%")
        print(f"风速: {result['wind_speed']} m/s")
    else:
        print("❌ API调用失败")


def main():
    """主函数"""
    print("=" * 60)
    print("OpenAI调用免费天气API示例")
    print("=" * 60)
    print()
    
    # 示例查询
    # queries = [
    #     "北京今天天气怎么样？",
    #     "上海现在的温度是多少？用摄氏度告诉我",
    #     "广州的天气情况如何？",
    # ]

    queries = [
        "成都今天天气怎么样？"
    ]

    
    # 可以取消注释下面的代码，让用户输入查询
    # user_input = input("请输入您的天气查询（或按Enter使用示例）: ").strip()
    # if user_input:
    #     queries = [user_input]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"示例 {i}:")
        print(f"{'='*60}\n")
        call_weather_with_openai(query)
        print("\n")


if __name__ == "__main__":
    import sys
    
    # 如果传入参数 "test"，则直接测试API
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_city = sys.argv[2] if len(sys.argv) > 2 else "Beijing"
        test_weather_api_directly(test_city)
    else:
        main()
