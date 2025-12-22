# 🤖 双 Agent 自由对话系统

使用本地 Ollama 的 deepseek-r1:32b 模型实现两个 AI Agent 的自由对话。

## ✨ 功能特点

- 🎭 **双 Agent 对话**：两个具有不同性格的 AI Agent 进行自然对话
- 🎯 **自定义主题**：你可以输入任何话题，让两个 Agent 围绕主题展开讨论
- 💬 **流式输出**：实时显示 AI 的思考和回复过程
- 💾 **对话保存**：可选择保存完整的对话记录

## 📋 前置要求

1. **安装 Ollama**
   ```bash
   # macOS
   brew install ollama
   
   # 或从官网下载：https://ollama.ai
   ```

2. **下载 deepseek-r1:32b 模型**
   ```bash
   ollama pull deepseek-r1:32b
   ```

3. **启动 Ollama 服务**
   ```bash
   ollama serve
   ```

## 🚀 快速开始

### 方法 1：使用启动脚本（推荐）

```bash
./run.sh
```

### 方法 2：手动运行

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行程序
python agent_conversation.py
```

## 🎮 使用方法

1. 运行程序后，输入对话主题（例如：人工智能的未来、旅行的意义、美食文化等）
2. 输入对话轮数（默认 5 轮）
3. 观看两个 Agent 自动对话
4. 对话结束后，可选择保存对话记录

## 👥 Agent 角色

- **小明**：乐观开朗、充满好奇心的年轻人，说话风格活泼
- **小红**：理性冷静、善于分析的思考者，说话风格严谨

## 📝 示例

```
请输入对话主题：人工智能的未来
请输入对话轮数：3

--- 第 1 轮 ---
💬 小明: 哇！人工智能的未来听起来超酷的！...
💬 小红: 确实如此！从技术角度来看，人工智能的发展...

--- 第 2 轮 ---
💬 小明: 说得太棒了！...
💬 小红: 你提到的这些观点都很有见地...
```

## 🛠️ 自定义

你可以修改 `agent_conversation.py` 中的 Agent 性格设置：

```python
agent1 = OllamaAgent(
    name="你的名字",
    personality="你的性格描述"
)
```

## 📦 项目结构

```
.
├── agent_conversation.py  # 主程序
├── requirements.txt       # Python 依赖
├── run.sh                # 启动脚本
└── venv/                 # 虚拟环境
```

## 🔧 故障排除

### Ollama 连接失败

确保 Ollama 服务正在运行：
```bash
# 检查 Ollama 是否运行
curl http://localhost:11434/api/tags

# 如果没有运行，启动服务
ollama serve
```

### 模型未找到

确保已下载 deepseek-r1:32b 模型：
```bash
ollama list
ollama pull deepseek-r1:32b
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

