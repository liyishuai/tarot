# 🔮 Tarot - 塔罗牌占卜应用

一个使用 OpenAI 兼容 LLM 服务的交互式塔罗牌占卜应用。

## ✨ 功能特性

- 🤖 **智能对话**: 使用 OpenAI 兼容的 LLM 服务与用户进行多轮对话
- 🃏 **多种牌阵**: 支持单张牌、三张牌、关系牌阵、决策牌阵和凯尔特十字牌阵
- 🎲 **灵活抽牌**: 支持随机抽牌和手动选择牌
- 📖 **智能解读**: 使用 LLM 提供专业的塔罗牌解读
- 🌍 **中文支持**: 完整的中文界面和解读

## 📋 系统要求

- Python 3.7+
- OpenAI 兼容的 LLM API 服务 (如 OpenAI、Azure OpenAI、本地部署的模型等)

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
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

**支持的 API 配置示例:**

- **OpenAI 官方 API:**
  ```ini
  OPENAI_API_KEY=sk-...
  OPENAI_BASE_URL=https://api.openai.com/v1
  OPENAI_MODEL=gpt-3.5-turbo
  ```

- **Azure OpenAI:**
  ```ini
  OPENAI_API_KEY=your_azure_key
  OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment
  OPENAI_MODEL=gpt-35-turbo
  ```

- **本地部署模型 (如 Ollama, LocalAI):**
  ```ini
  OPENAI_API_KEY=not-needed
  OPENAI_BASE_URL=http://localhost:11434/v1
  OPENAI_MODEL=llama2
  ```

### 3. 运行程序

```bash
python tarot.py
```

## 📖 使用说明

### 基本流程

1. **开始对话**: 程序启动后，塔罗占卜师会与你打招呼
2. **交流问题**: 与占卜师对话，说明你的问题和困惑
3. **选择牌阵**: 
   - 输入 `spreads` 查看所有可用的牌阵
   - 输入 `select` 开始选择牌阵
4. **抽取塔罗牌**: 
   - 每个位置可选择 `r` (随机抽取) 或 `m` (手动输入)
   - 手动输入时可以搜索牌名
5. **获得解读**: 占卜师会为你的牌阵提供详细解读

### 可用的牌阵

1. **单张牌阵**: 快速了解当下情况
2. **三张牌阵**: 过去-现在-未来，了解发展轨迹
3. **关系牌阵**: 探索两人关系动态
4. **决策牌阵**: 帮助在两个选择间做决定
5. **凯尔特十字牌阵**: 最全面的牌阵，深入探索问题

### 示例对话

```
🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮
          欢迎来到塔罗占卜屋          
🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮

==================================================
塔罗占卜师: 你好！欢迎来到塔罗占卜屋...
==================================================

(输入 'spreads' 查看所有牌阵，输入 'select' 选择牌阵并开始占卜)

你: 我最近在工作上遇到了一些困惑

塔罗占卜师: 我理解你的困惑...

你: select

请选择一个塔罗牌阵:
1. 单张牌阵 - 用一张牌快速了解当下的情况或得到简单的指引
2. 三张牌阵 - 经典的过去-现在-未来牌阵，了解事情的发展轨迹
...
```

## 🃏 塔罗牌说明

本应用包含完整的 78 张塔罗牌：
- **22 张大阿尔卡纳 (Major Arcana)**: 从愚者到世界
- **56 张小阿尔卡纳 (Minor Arcana)**: 
  - 权杖 (Wands) 14张
  - 圣杯 (Cups) 14张
  - 宝剑 (Swords) 14张
  - 星币 (Pentacles) 14张

每张牌都支持正位和逆位解读。

## 🛠️ 技术栈

- **Python 3**: 主要编程语言
- **OpenAI Python SDK**: 与 LLM API 交互
- **python-dotenv**: 环境变量管理

## 📝 项目结构

```
tarot/
├── tarot.py           # 主程序文件
├── tarot_cards.py     # 塔罗牌数据定义
├── requirements.txt   # Python 依赖
├── .env.example       # 环境变量示例
├── .gitignore         # Git 忽略文件
└── README.md          # 项目文档
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 Apache License 2.0 许可证。详见 [LICENSE](LICENSE) 文件。

## ⚠️ 免责声明

本应用仅供娱乐和自我探索使用。塔罗牌解读不应作为专业建议的替代品。对于重要的人生决策，请咨询相关专业人士。