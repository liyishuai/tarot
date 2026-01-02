# 🔮 Tarot - 塔罗牌占卜 Web 应用

一个使用 OpenAI 兼容 LLM 服务的交互式塔罗牌占卜 Web 应用。

## ✨ 功能特性

- 🤖 **智能对话**: 使用 OpenAI 兼容的 LLM 服务与用户进行多轮对话
- 🎴 **LLM 创建牌阵**: LLM 通过 function calling 根据用户问题动态创建定制牌阵
- 🔮 **Web 界面**: 现代化的 Web UI，可视化的牌阵布局
- 📋 **完整牌义**: 内置所有 78 张塔罗牌的正位和逆位含义
- 🎲 **随机抽牌**: 自动随机抽牌功能
- 🌟 **智能解读**: LLM 结合牌义提供专业解读
- 🌍 **中文支持**: 完整的中文界面和解读

## 📋 系统要求

- Python 3.7+
- OpenAI 兼容的 LLM API 服务

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API

复制 `.env.example` 到 `.env` 并填入你的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```ini
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://apis.iflow.cn/v1
OPENAI_MODEL=gpt-3.5-turbo
SECRET_KEY=your_secret_key_for_sessions
```

### 3. 运行应用

```bash
python app.py
```

访问 http://localhost:5000 开始使用。

## 📖 使用说明

### 基本流程

1. **输入问题**: 在 Web 界面输入你的问题
2. **LLM 推荐牌阵**: 
   - LLM 通过 function calling 创建适合你问题的牌阵
   - 可以接受推荐，或要求创建新牌阵
3. **查看牌阵布局**: 
   - UI 自动适配显示牌阵的可视化布局
   - 每个位置标明含义
4. **抽取塔罗牌**: 
   - 点击"随机抽牌"自动抽取所有位置的牌
   - 牌会放置在对应的位置上
5. **查看牌义**: 
   - 先显示每张牌的基本含义（关键词和牌义）
   - 包括位置含义
6. **获得解读**: 
   - LLM 基于牌义提供综合解读和建议

## 🎯 核心特性

### LLM Function Calling

应用使用 OpenAI function calling 让 LLM 动态创建牌阵：

```python
SPREAD_CREATION_TOOL = {
    "type": "function",
    "function": {
        "name": "create_spread",
        "description": "创建一个塔罗牌阵...",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "positions": {"type": "array", ...}
            }
        }
    }
}
```

### 牌义数据库

包含完整的 78 张牌义：
- **22 张大阿尔卡纳**: 从愚者到世界，每张牌都有详细的正位和逆位含义
- **56 张小阿尔卡纳**: 权杖、圣杯、宝剑、星币各 14 张

每张牌包括：
- 关键词
- 详细含义
- 正位和逆位的不同解释

### 可视化牌阵布局

系统自动为不同数量的位置生成合适的布局：
- 1-10 个位置有预定义的美观布局
- 超过 10 个位置使用网格布局
- 所有布局都是响应式的

## 🛠️ 技术栈

- **Python 3**: 主要编程语言
- **Flask**: Web 框架
- **OpenAI API**: LLM 服务（支持任何兼容的 API）
- **HTML/CSS/JavaScript**: 前端界面

## 📝 项目结构

```
tarot/
├── app.py                # Flask 应用主文件
├── card_meanings.py      # 78 张牌的完整牌义数据库
├── spread_tools.py       # 牌阵创建工具（供 LLM 调用）
├── templates/
│   └── index.html        # Web 界面模板
├── static/
│   ├── style.css         # 样式文件
│   └── script.js         # 前端 JavaScript
├── requirements.txt      # Python 依赖
├── .env.example          # 环境变量示例
└── README.md             # 项目文档
```

## 🎨 界面截图

应用包含以下界面：

1. **问题输入页**: 用户输入他们的问题
2. **牌阵推荐对话**: 显示 LLM 的推荐和解释
3. **可视化牌阵**: 根据牌阵自动布局，显示每个位置
4. **牌义展示**: 先显示每张牌的含义
5. **综合解读**: LLM 基于牌义的深度解读

## 🔧 配置选项

支持多种 LLM 服务：

- **OpenAI**: `https://api.openai.com/v1`
- **iFlow**: `https://apis.iflow.cn/v1`
- **Azure OpenAI**: 自定义 endpoint
- **本地模型**: 任何 OpenAI 兼容的 API

## 📄 许可证

本项目采用 Apache License 2.0 许可证。

## ⚠️ 免责声明

本应用仅供娱乐和自我探索使用。塔罗牌解读不应作为专业建议的替代品。
