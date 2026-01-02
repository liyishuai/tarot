# 🚀 快速启动指南

## 运行应用

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API (创建 .env 文件)
cat > .env << EOF
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://apis.iflow.cn/v1
OPENAI_MODEL=gpt-3.5-turbo
SECRET_KEY=your_secret_key_for_sessions
EOF

# 3. 运行应用
python app.py

# 4. 访问 http://localhost:5000
```

## 功能演示

### 1. 输入问题
- 在首页输入您的问题
- 例如："我最近在工作上遇到了困惑"

### 2. LLM 推荐牌阵
- LLM 通过 function calling 创建定制牌阵
- 显示牌阵名称、描述和各位置含义
- 可以接受或要求新牌阵

### 3. 查看牌阵布局
- UI 自动显示可视化布局
- 每个位置显示编号和名称
- 位置根据牌阵数量自动排列

### 4. 随机抽牌
- 点击"随机抽牌"
- 所有位置自动填充
- 显示牌名和方向（正位/逆位）

### 5. 查看牌义
- 先显示每张牌的基本含义
- 包括关键词和详细解释
- 显示位置含义

### 6. 获取解读
- LLM 基于牌义生成综合解读
- 分析牌与牌之间的关联
- 提供具体建议

## API 配置示例

### OpenAI
```ini
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
```

### iFlow
```ini
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=https://apis.iflow.cn/v1
OPENAI_MODEL=gpt-3.5-turbo
```

### 其他兼容服务
任何支持 OpenAI API 格式和 function calling 的服务都可以使用。

## 文件结构

```
tarot/
├── app.py              # Flask 应用 + Function Calling
├── card_meanings.py    # 78 张牌的完整牌义
├── spread_tools.py     # LLM 牌阵创建工具
├── templates/
│   └── index.html      # Web 界面
├── static/
│   ├── style.css       # 样式
│   └── script.js       # 前端逻辑
├── requirements.txt
└── .env                # 配置文件
```

## 技术亮点

1. **LLM Function Calling**: 动态创建牌阵，不是硬编码
2. **完整牌义库**: 78 张牌 × 2 方向 = 156 种含义
3. **可视化布局**: 自动生成美观的牌阵布局
4. **对话式交互**: 自然的多轮对话体验
5. **含义优先**: 先显示牌义，再提供 LLM 解读
