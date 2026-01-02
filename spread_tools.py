"""塔罗牌阵构建工具 - 供 LLM 调用"""

def create_spread(name: str, description: str, positions: list) -> dict:
    """
    创建一个塔罗牌阵
    
    Args:
        name: 牌阵名称
        description: 牌阵描述
        positions: 位置列表，每个位置是一个包含 name 和 meaning 的字典
                  例如: [{"name": "过去", "meaning": "影响当前情况的过去事件"}]
    
    Returns:
        牌阵定义字典
    """
    return {
        "name": name,
        "description": description,
        "positions": positions,
        "layout": generate_layout(len(positions))
    }


def generate_layout(num_positions: int) -> list:
    """
    根据位置数量生成牌阵布局坐标
    
    Args:
        num_positions: 位置数量
    
    Returns:
        坐标列表 [{"x": x, "y": y}, ...]
    """
    layouts = {
        1: [{"x": 50, "y": 50}],
        
        2: [
            {"x": 35, "y": 50},
            {"x": 65, "y": 50}
        ],
        
        3: [
            {"x": 30, "y": 50},
            {"x": 50, "y": 50},
            {"x": 70, "y": 50}
        ],
        
        4: [
            {"x": 50, "y": 30},
            {"x": 30, "y": 60},
            {"x": 70, "y": 60},
            {"x": 50, "y": 80}
        ],
        
        5: [
            {"x": 50, "y": 20},
            {"x": 25, "y": 45},
            {"x": 75, "y": 45},
            {"x": 35, "y": 75},
            {"x": 65, "y": 75}
        ],
        
        6: [
            {"x": 30, "y": 30},
            {"x": 70, "y": 30},
            {"x": 30, "y": 50},
            {"x": 70, "y": 50},
            {"x": 30, "y": 70},
            {"x": 70, "y": 70}
        ],
        
        7: [
            {"x": 50, "y": 15},
            {"x": 25, "y": 35},
            {"x": 50, "y": 35},
            {"x": 75, "y": 35},
            {"x": 30, "y": 60},
            {"x": 70, "y": 60},
            {"x": 50, "y": 80}
        ],
        
        10: [  # 凯尔特十字
            {"x": 45, "y": 45},  # 1. 中心
            {"x": 55, "y": 45},  # 2. 交叉
            {"x": 45, "y": 25},  # 3. 上方
            {"x": 45, "y": 65},  # 4. 下方
            {"x": 25, "y": 45},  # 5. 左侧
            {"x": 65, "y": 45},  # 6. 右侧
            {"x": 80, "y": 80},  # 7. 底部外侧
            {"x": 80, "y": 60},  # 8. 中部外侧
            {"x": 80, "y": 40},  # 9. 上部外侧
            {"x": 80, "y": 20}   # 10. 顶部外侧
        ]
    }
    
    # 如果有预定义布局，使用它
    if num_positions in layouts:
        return layouts[num_positions]
    
    # 否则生成网格布局
    cols = min(num_positions, 3)
    rows = (num_positions + cols - 1) // cols
    
    layout = []
    for i in range(num_positions):
        row = i // cols
        col = i % cols
        x = 20 + (60 / (cols - 1 if cols > 1 else 1)) * col if cols > 1 else 50
        y = 20 + (60 / (rows - 1 if rows > 1 else 1)) * row if rows > 1 else 50
        layout.append({"x": x, "y": y})
    
    return layout


# 为 LLM 提供的函数定义
SPREAD_CREATION_TOOL = {
    "type": "function",
    "function": {
        "name": "create_spread",
        "description": "创建一个塔罗牌阵。根据用户的问题和需求，设计合适的牌阵布局，包括牌阵名称、描述和各个位置的含义。",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "牌阵的名称，例如：'三张牌阵：过去-现在-未来'、'关系牌阵'、'决策牌阵'"
                },
                "description": {
                    "type": "string",
                    "description": "牌阵的详细描述，说明这个牌阵适合什么样的问题和情况"
                },
                "positions": {
                    "type": "array",
                    "description": "牌阵中每个位置的定义",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "位置的名称，例如：'过去'、'当前状况'、'潜在挑战'"
                            },
                            "meaning": {
                                "type": "string",
                                "description": "这个位置代表的含义，例如：'影响当前情况的过去事件和经历'"
                            }
                        },
                        "required": ["name", "meaning"]
                    }
                }
            },
            "required": ["name", "description", "positions"]
        }
    }
}


# 预设的一些经典牌阵示例（供参考）
CLASSIC_SPREADS = {
    "single": {
        "name": "单张指引牌",
        "description": "用一张牌快速了解当下的情况或获得简单的指引",
        "positions": [
            {"name": "核心信息", "meaning": "当前最重要的信息或指引"}
        ]
    },
    
    "past_present_future": {
        "name": "时间线牌阵",
        "description": "了解事情的发展轨迹，从过去到未来",
        "positions": [
            {"name": "过去", "meaning": "影响当前情况的过去事件和经历"},
            {"name": "现在", "meaning": "当前的状况和你所处的位置"},
            {"name": "未来", "meaning": "如果按当前轨迹发展，可能的结果"}
        ]
    },
    
    "relationship": {
        "name": "关系动态牌阵",
        "description": "探索两个人之间的关系",
        "positions": [
            {"name": "你的位置", "meaning": "你在这段关系中的立场和感受"},
            {"name": "对方的位置", "meaning": "对方在这段关系中的立场和感受"},
            {"name": "关系能量", "meaning": "关系本身的能量和特质"},
            {"name": "建议", "meaning": "如何改善或发展这段关系"}
        ]
    },
    
    "decision": {
        "name": "决策牌阵",
        "description": "帮助在多个选择之间做出决定",
        "positions": [
            {"name": "当前情况", "meaning": "你现在所处的状况"},
            {"name": "选择A的结果", "meaning": "如果选择第一个选项可能的结果"},
            {"name": "选择B的结果", "meaning": "如果选择第二个选项可能的结果"},
            {"name": "隐藏因素", "meaning": "需要考虑的隐藏因素或盲点"},
            {"name": "最佳建议", "meaning": "综合考虑后的最佳行动方向"}
        ]
    },
    
    "celtic_cross": {
        "name": "凯尔特十字牌阵",
        "description": "最经典和全面的牌阵，深入探索问题的各个方面",
        "positions": [
            {"name": "当前状况", "meaning": "你现在的处境和核心问题"},
            {"name": "挑战/横切因素", "meaning": "当前面临的挑战或影响因素"},
            {"name": "根基/潜意识", "meaning": "问题的根源或潜意识影响"},
            {"name": "近期过去", "meaning": "刚刚过去的影响和经历"},
            {"name": "可能的未来", "meaning": "如果情况不改变，可能的发展"},
            {"name": "近期未来", "meaning": "即将到来的影响和事件"},
            {"name": "你的立场", "meaning": "你对这个情况的态度和感受"},
            {"name": "外部影响", "meaning": "他人和环境对你的影响"},
            {"name": "希望与恐惧", "meaning": "你内心的希望和担忧"},
            {"name": "最终结果", "meaning": "综合所有因素后的可能结果"}
        ]
    }
}


def get_classic_spread(spread_type: str) -> dict:
    """
    获取预设的经典牌阵
    
    Args:
        spread_type: 牌阵类型 (single, past_present_future, relationship, decision, celtic_cross)
    
    Returns:
        牌阵定义
    """
    spread = CLASSIC_SPREADS.get(spread_type, CLASSIC_SPREADS["single"])
    return create_spread(
        name=spread["name"],
        description=spread["description"],
        positions=spread["positions"]
    )
