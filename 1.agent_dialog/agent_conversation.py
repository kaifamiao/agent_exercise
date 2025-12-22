#!/usr/bin/env python3
"""
两个 AI Agent 自由对话程序
使用本地 Ollama 的 llama3.1:latest 模型
"""

import requests
import json
import time
from typing import List, Dict


class OllamaAgent:
    """使用 Ollama API 的 Agent"""
    
    def __init__(self, name: str, personality: str, model: str = "llama3.1:latest"):
        self.name = name
        self.personality = personality
        self.model = model
        self.api_url = "http://localhost:11434/api/chat"
        self.conversation_history: List[Dict] = []
        
    def set_system_prompt(self, topic: str, viewpoint: str = ""):
        """设置系统提示词"""
        viewpoint_instruction = f"\n你的观点是：{viewpoint}\n请坚持这个观点，用有说服力的论据来支持你的立场。" if viewpoint else ""
        system_message = {
            "role": "system",
            "content": f"""你是 {self.name}，{self.personality}
当前对话主题是：{topic}{viewpoint_instruction}
请围绕这个主题进行自然、有趣的对话。保持你的个性特点，表达你的观点和想法。
回复要简洁自然，不要太长，就像真实的对话一样。"""
        }
        self.conversation_history = [system_message]
    
    def respond(self, message: str = None) -> str:
        """生成回复"""
        if message:
            self.conversation_history.append({
                "role": "user",
                "content": message
            })

        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "stream": True
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=120, stream=True)
            response.raise_for_status()

            assistant_message = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "message" in chunk and "content" in chunk["message"]:
                            content = chunk["message"]["content"]
                            assistant_message += content
                            print(content, end="", flush=True)
                    except json.JSONDecodeError:
                        continue

            print()  # 换行

            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except requests.exceptions.RequestException as e:
            return f"[错误: {str(e)}]"


def main():
    """主函数"""
    print("=" * 60)
    print("🤖 双 Agent 对话系统")
    print("=" * 60)
    print()
    
    # 创建两个具有不同性格和观点的 Agent
    agent1 = OllamaAgent(
        name="小明",
        personality="一个乐观开朗、充满好奇心的年轻人，喜欢探索新事物，说话风格活泼"
    )

    agent2 = OllamaAgent(
        name="小红",
        personality="一个理性冷静、善于分析的思考者，喜欢深入思考问题，说话风格严谨"
    )

    # 获取对话主题
    print("请输入对话主题（例如：先有鸡还是先有蛋、旅行的意义、美食文化等）")
    topic = input("主题: ").strip()

    if not topic:
        topic = "先有鸡还是先有蛋"
        print(f"使用默认主题: {topic}")

    print()
    print(f"📌 对话主题: {topic}")

    # 根据主题设置观点
    viewpoint1 = ""
    viewpoint2 = ""

    if "先有鸡还是先有蛋" in topic or "鸡" in topic and "蛋" in topic:
        viewpoint1 = "先有蛋。从进化论角度看，鸡是由其他物种进化而来的，第一只真正意义上的鸡必然是从蛋中孵化出来的。"
        viewpoint2 = "先有鸡。没有鸡就不可能有鸡蛋，必须先有能下蛋的鸡，才能有鸡蛋的存在。"
        print(f"💡 {agent1.name}的观点: {viewpoint1}")
        print(f"💡 {agent2.name}的观点: {viewpoint2}")

    print()

    # 设置系统提示
    agent1.set_system_prompt(topic, viewpoint1)
    agent2.set_system_prompt(topic, viewpoint2)
    
    # 获取对话轮数
    try:
        rounds = int(input("请输入对话轮数（默认5轮）: ").strip() or "5")
    except ValueError:
        rounds = 5
    
    print()
    print("=" * 60)
    print("🎬 对话开始")
    print("=" * 60)
    print()
    
    # 开始对话
    current_message = f"嗨！我们来聊聊关于「{topic}」这个话题吧，你有什么想法？"
    
    for round_num in range(rounds):
        print(f"--- 第 {round_num + 1} 轮 ---")
        print()
        
        # Agent 1 回复
        print(f"💬 {agent1.name}: ", end="", flush=True)
        response1 = agent1.respond(current_message)
        print()

        time.sleep(1)  # 短暂延迟，让对话更自然

        # Agent 2 回复
        print(f"💬 {agent2.name}: ", end="", flush=True)
        response2 = agent2.respond(response1)
        print()
        
        # 更新消息，让下一轮继续
        current_message = response2
        
        time.sleep(1)
    
    print("=" * 60)
    print("✅ 对话结束")
    print("=" * 60)
    
    # 询问是否保存对话
    save = input("\n是否保存对话记录？(y/n): ").strip().lower()
    if save == 'y':
        filename = f"conversation_{int(time.time())}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"对话主题: {topic}\n")
            f.write("=" * 60 + "\n\n")
            for i, msg in enumerate(agent1.conversation_history[1:], 1):
                role = "小明" if msg["role"] == "assistant" else "小红"
                f.write(f"{role}: {msg['content']}\n\n")
        print(f"✅ 对话已保存到: {filename}")


if __name__ == "__main__":
    main()

