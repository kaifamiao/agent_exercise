# Python调用大模型示例

本目录包含两个Python示例，演示如何调用大模型。

## 文件说明

1. **example1_basic_llm.py** - 基础的大模型调用示例
   - 展示如何使用openai库调用大模型
   - 支持基础调用和流式调用
   - 可适配本地模型或兼容OpenAI API的服务

2. **example2_openai_official.py** - 使用OpenAI官方API的示例
   - 直接调用OpenAI官网的GPT模型
   - 包含基础调用、流式调用和函数调用示例
   - 展示token使用统计

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 示例1: 基础大模型调用

```bash
python example1_basic_llm.py
```

**注意**: 
- 如果使用本地模型，需要修改`base_url`指向你的模型服务地址
- 如果使用OpenAI服务，需要设置`api_key`

### 示例2: OpenAI官方API

1. 首先设置API密钥（推荐使用环境变量）:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. 运行示例:
   ```bash
   python example2_openai_official.py
   ```

## 配置说明

### 环境变量方式（推荐）

创建`.env`文件:
```
OPENAI_API_KEY=your-api-key-here
```

然后在代码中使用`python-dotenv`加载:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 直接设置（不推荐用于生产环境）

在代码中直接设置API密钥（仅用于测试）:
```python
client = OpenAI(api_key="your-api-key-here")
```

## 主要功能

- ✅ 基础对话调用
- ✅ 流式输出（实时返回）
- ✅ 函数调用（Function Calling）
- ✅ Token使用统计
- ✅ 错误处理

## 注意事项

1. **API密钥安全**: 不要将API密钥提交到代码仓库，使用环境变量或配置文件
2. **费用控制**: 注意API调用费用，合理设置`max_tokens`参数
3. **错误处理**: 生产环境需要完善的错误处理和重试机制
4. **模型选择**: 根据需求选择合适的模型（gpt-3.5-turbo性价比高，gpt-4效果更好但更贵）

