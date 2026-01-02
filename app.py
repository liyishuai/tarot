#!/usr/bin/env python3
"""
塔罗牌占卜 Web 应用
使用 Flask 提供 Web UI，LLM 通过 function calling 创建牌阵
"""

import os
import json
import random
import requests
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from card_meanings import get_card_meaning, ALL_CARD_MEANINGS
from spread_tools import create_spread, SPREAD_CREATION_TOOL

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "tarot-secret-key-change-in-production")

# LLM API 配置
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://apis.iflow.cn/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


def get_all_cards():
    """获取所有78张塔罗牌"""
    return list(ALL_CARD_MEANINGS.keys())


def call_llm(messages, tools=None):
    """调用 LLM API，支持 function calling"""
    if not API_KEY:
        return {"type": "text", "content": "错误：未配置 API 密钥"}
    
    try:
        payload = {
            "model": MODEL,
            "messages": messages
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        choice = response.json()["choices"][0]
        message = choice["message"]
        
        # 检查是否有 tool_calls
        if message.get("tool_calls"):
            return {
                "type": "tool_call",
                "tool_calls": message["tool_calls"],
                "message": message
            }
        else:
            return {
                "type": "text",
                "content": message.get("content", "")
            }
    except Exception as e:
        return {"type": "text", "content": f"LLM调用错误: {str(e)}"}


@app.route("/")
def index():
    """主页"""
    return render_template("index.html")


@app.route("/api/cards")
def get_cards():
    """获取所有卡牌"""
    cards = get_all_cards()
    return jsonify({"cards": cards})


@app.route("/api/start_reading", methods=["POST"])
def start_reading():
    """开始占卜会话，LLM 推荐牌阵"""
    data = request.json
    question = data.get("question", "")
    
    # 初始化会话
    session["conversation"] = []
    session["question"] = question
    session["drawn_cards"] = []
    session["spread"] = None
    
    # 与 LLM 对话，使用 function calling 来推荐牌阵
    system_prompt = """你是一位经验丰富、充满智慧的塔罗牌占卜师。

当用户提出问题时，你需要：
1. 理解他们的问题和需求
2. 使用 create_spread 工具为他们创建一个合适的塔罗牌阵
3. 牌阵应该根据用户的问题定制，包含3-10个位置
4. 每个位置都要有清晰的名称和含义，说明在牌阵中代表什么

创建牌阵后，向用户解释这个牌阵为什么适合他们的问题。"""
    
    user_message = f"你好，我想进行塔罗占卜。我的问题是：{question}" if question else "你好，我想进行塔罗占卜。"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    # 调用 LLM，提供 spread creation tool
    result = call_llm(messages, tools=[SPREAD_CREATION_TOOL])
    
    if result["type"] == "tool_call":
        # LLM 调用了 create_spread
        tool_call = result["tool_calls"][0]
        function_args = json.loads(tool_call["function"]["arguments"])
        
        # 执行工具调用
        spread = create_spread(
            name=function_args["name"],
            description=function_args["description"],
            positions=function_args["positions"]
        )
        
        session["spread"] = spread
        
        # 将工具调用结果返回给 LLM
        messages.append(result["message"])
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": json.dumps(spread, ensure_ascii=False)
        })
        
        # 再次调用 LLM 获取解释
        final_result = call_llm(messages)
        response_text = final_result["content"] if final_result["type"] == "text" else "牌阵已创建"
        
        session["conversation"] = messages + [{"role": "assistant", "content": response_text}]
        session.modified = True
        
        return jsonify({
            "response": response_text,
            "spread": spread,
            "has_spread": True,
            "success": True
        })
    else:
        # 没有调用工具，返回普通响应
        session["conversation"] = messages + [{"role": "assistant", "content": result["content"]}]
        session.modified = True
        
        return jsonify({
            "response": result["content"],
            "has_spread": False,
            "success": True
        })


@app.route("/api/accept_spread", methods=["POST"])
def accept_spread():
    """用户接受推荐的牌阵"""
    if "spread" not in session or not session["spread"]:
        return jsonify({"error": "No spread in session"}), 400
    
    return jsonify({
        "spread": session["spread"],
        "success": True
    })


@app.route("/api/request_new_spread", methods=["POST"])
def request_new_spread():
    """用户请求新的牌阵"""
    data = request.json
    feedback = data.get("feedback", "")
    
    if "conversation" not in session:
        return jsonify({"error": "No active session"}), 400
    
    user_message = f"这个牌阵不太适合我的需求。{feedback}。请为我设计一个新的牌阵。"
    
    session["conversation"].append({"role": "user", "content": user_message})
    
    # 再次调用 LLM 创建新牌阵
    result = call_llm(session["conversation"], tools=[SPREAD_CREATION_TOOL])
    
    if result["type"] == "tool_call":
        tool_call = result["tool_calls"][0]
        function_args = json.loads(tool_call["function"]["arguments"])
        
        spread = create_spread(
            name=function_args["name"],
            description=function_args["description"],
            positions=function_args["positions"]
        )
        
        session["spread"] = spread
        
        # 添加到对话历史
        session["conversation"].append(result["message"])
        session["conversation"].append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": json.dumps(spread, ensure_ascii=False)
        })
        
        final_result = call_llm(session["conversation"])
        response_text = final_result["content"] if final_result["type"] == "text" else "新牌阵已创建"
        
        session["conversation"].append({"role": "assistant", "content": response_text})
        session.modified = True
        
        return jsonify({
            "response": response_text,
            "spread": spread,
            "success": True
        })
    else:
        return jsonify({
            "response": result["content"],
            "success": False
        })


@app.route("/api/draw_cards", methods=["POST"])
def draw_cards():
    """随机抽牌"""
    if "spread" not in session or not session["spread"]:
        return jsonify({"error": "No spread selected"}), 400
    
    spread = session["spread"]
    positions = spread["positions"]
    
    all_cards = get_all_cards()
    drawn = []
    used_cards = set()
    
    for pos in positions:
        available = [c for c in all_cards if c not in used_cards]
        card = random.choice(available)
        orientation = random.choice(["正位", "逆位"])
        
        meaning = get_card_meaning(card, orientation)
        
        card_info = {
            "position": pos["name"],
            "position_meaning": pos["meaning"],
            "card": card,
            "orientation": orientation,
            "keywords": meaning["keywords"],
            "meaning": meaning["meaning"]
        }
        
        drawn.append(card_info)
        used_cards.add(card)
    
    session["drawn_cards"] = drawn
    session.modified = True
    
    return jsonify({
        "cards": drawn,
        "success": True
    })


@app.route("/api/get_interpretation", methods=["POST"])
def get_interpretation():
    """获取LLM解读"""
    if "drawn_cards" not in session or not session["drawn_cards"]:
        return jsonify({"error": "No cards drawn"}), 400
    
    drawn_cards = session["drawn_cards"]
    question = session.get("question", "未指定问题")
    spread = session.get("spread", {})
    
    # 构建包含牌义的提示
    cards_info = f"牌阵：{spread.get('name', '未命名牌阵')}\n"
    cards_info += f"牌阵说明：{spread.get('description', '')}\n\n"
    cards_info += "抽到的牌及其含义：\n\n"
    
    for i, card_info in enumerate(drawn_cards, 1):
        cards_info += f"【位置 {i}：{card_info['position']}】\n"
        cards_info += f"位置含义：{card_info['position_meaning']}\n"
        cards_info += f"抽到的牌：{card_info['card']} ({card_info['orientation']})\n"
        cards_info += f"关键词：{card_info['keywords']}\n"
        cards_info += f"基本含义：{card_info['meaning']}\n\n"
    
    interpretation_request = f"""来访者的问题：{question}

{cards_info}

现在，请作为塔罗占卜师，基于以上每张牌的基本含义，为来访者提供详细的解读：

1. 首先总结整体牌面传达的信息和能量
2. 然后逐一解读每张牌在其位置上的具体含义，结合来访者的问题
3. 分析牌与牌之间的关联和相互影响
4. 最后给出针对来访者问题的具体建议和指引

请用温暖、富有洞察力的语言进行解读，让来访者感受到你的智慧和关怀。"""
    
    messages = session.get("conversation", [])
    messages.append({"role": "user", "content": interpretation_request})
    
    result = call_llm(messages)
    interpretation = result["content"] if result["type"] == "text" else "解读生成失败"
    
    session["conversation"] = messages + [{"role": "assistant", "content": interpretation}]
    session.modified = True
    
    return jsonify({
        "interpretation": interpretation,
        "cards": drawn_cards,
        "success": True
    })


if __name__ == "__main__":
    # 创建必要的目录
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    app.run(debug=True, host="0.0.0.0", port=5000)
