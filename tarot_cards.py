"""塔罗牌数据定义"""

# 78张塔罗牌定义
MAJOR_ARCANA = [
    "0. 愚者 (The Fool)",
    "1. 魔术师 (The Magician)",
    "2. 女祭司 (The High Priestess)",
    "3. 女皇 (The Empress)",
    "4. 皇帝 (The Emperor)",
    "5. 教皇 (The Hierophant)",
    "6. 恋人 (The Lovers)",
    "7. 战车 (The Chariot)",
    "8. 力量 (Strength)",
    "9. 隐士 (The Hermit)",
    "10. 命运之轮 (Wheel of Fortune)",
    "11. 正义 (Justice)",
    "12. 倒吊人 (The Hanged Man)",
    "13. 死神 (Death)",
    "14. 节制 (Temperance)",
    "15. 恶魔 (The Devil)",
    "16. 高塔 (The Tower)",
    "17. 星星 (The Star)",
    "18. 月亮 (The Moon)",
    "19. 太阳 (The Sun)",
    "20. 审判 (Judgement)",
    "21. 世界 (The World)",
]

MINOR_ARCANA = {
    "权杖 (Wands)": [
        "权杖王牌", "权杖二", "权杖三", "权杖四", "权杖五",
        "权杖六", "权杖七", "权杖八", "权杖九", "权杖十",
        "权杖侍从", "权杖骑士", "权杖王后", "权杖国王"
    ],
    "圣杯 (Cups)": [
        "圣杯王牌", "圣杯二", "圣杯三", "圣杯四", "圣杯五",
        "圣杯六", "圣杯七", "圣杯八", "圣杯九", "圣杯十",
        "圣杯侍从", "圣杯骑士", "圣杯王后", "圣杯国王"
    ],
    "宝剑 (Swords)": [
        "宝剑王牌", "宝剑二", "宝剑三", "宝剑四", "宝剑五",
        "宝剑六", "宝剑七", "宝剑八", "宝剑九", "宝剑十",
        "宝剑侍从", "宝剑骑士", "宝剑王后", "宝剑国王"
    ],
    "星币 (Pentacles)": [
        "星币王牌", "星币二", "星币三", "星币四", "星币五",
        "星币六", "星币七", "星币八", "星币九", "星币十",
        "星币侍从", "星币骑士", "星币王后", "星币国王"
    ],
}

# 获取所有塔罗牌
def get_all_cards():
    """获取所有78张塔罗牌"""
    all_cards = MAJOR_ARCANA.copy()
    for suit_cards in MINOR_ARCANA.values():
        all_cards.extend(suit_cards)
    return all_cards

# 塔罗牌阵定义
SPREADS = {
    "1": {
        "name": "单张牌阵",
        "description": "用一张牌快速了解当下的情况或得到简单的指引",
        "positions": [
            "当前状况/核心问题"
        ]
    },
    "2": {
        "name": "三张牌阵",
        "description": "经典的过去-现在-未来牌阵，了解事情的发展轨迹",
        "positions": [
            "过去/起因",
            "现在/当下",
            "未来/结果"
        ]
    },
    "3": {
        "name": "关系牌阵",
        "description": "探索两个人之间的关系动态",
        "positions": [
            "你的立场",
            "对方的立场",
            "关系的未来发展"
        ]
    },
    "4": {
        "name": "决策牌阵",
        "description": "帮助你在两个选择之间做出决定",
        "positions": [
            "当前情况",
            "选择A的结果",
            "选择B的结果",
            "最佳建议"
        ]
    },
    "5": {
        "name": "凯尔特十字牌阵",
        "description": "最经典和全面的塔罗牌阵，深入探索问题的各个方面",
        "positions": [
            "1. 当前状况",
            "2. 挑战/阻碍",
            "3. 过去影响",
            "4. 近期未来",
            "5. 意识层面",
            "6. 潜意识层面",
            "7. 建议",
            "8. 外部影响",
            "9. 希望与恐惧",
            "10. 最终结果"
        ]
    }
}

def get_spread_info(spread_id):
    """获取牌阵信息"""
    return SPREADS.get(spread_id)

def list_all_spreads():
    """列出所有可用的牌阵"""
    result = []
    for spread_id, spread_info in SPREADS.items():
        result.append(f"{spread_id}. {spread_info['name']} - {spread_info['description']}")
    return "\n".join(result)
