#!/usr/bin/env python3
"""
塔罗牌应用演示脚本
展示应用的工作流程（不需要实际的 LLM API）
"""

import random
from tarot_cards import get_all_cards, get_spread_info, list_all_spreads


def demo_conversation():
    """演示对话流程"""
    print("\n" + "🔮" * 20)
    print("欢迎来到塔罗占卜屋 - 演示模式".center(40))
    print("🔮" * 20 + "\n")
    
    print("="*50)
    print("塔罗占卜师: 你好！欢迎来到我的占卜屋。我是一位经验丰富的塔罗占卜师。")
    print("           请告诉我，今天有什么困惑或问题想要探索吗？")
    print("="*50 + "\n")
    
    print("示例对话:")
    print("你: 我最近在事业上遇到了一些挑战，不知道该如何选择。\n")
    print("塔罗占卜师: 我理解你在事业上的困惑。面对选择总是不容易的。")
    print("           让我们通过塔罗牌来寻找一些指引和洞察。")
    print("           我建议使用决策牌阵，它能帮助你看清不同选择的结果。\n")


def demo_spread_selection():
    """演示牌阵选择"""
    print("\n可用的塔罗牌阵:")
    print(list_all_spreads())
    print()
    
    print("示例选择: 选择牌阵 4 - 决策牌阵")
    spread_info = get_spread_info("4")
    print(f"\n已选择: {spread_info['name']}")
    print(f"说明: {spread_info['description']}")
    print(f"需要抽取 {len(spread_info['positions'])} 张牌\n")
    
    return spread_info


def demo_draw_cards(spread_info):
    """演示抽牌过程"""
    print("\n开始抽牌...\n")
    
    all_cards = get_all_cards()
    drawn_cards = []
    
    for i, position in enumerate(spread_info['positions'], 1):
        # 随机抽取示例
        card = random.choice([c for c in all_cards if c not in [x['card'] for x in drawn_cards]])
        orientation = random.choice(['正位', '逆位'])
        
        print(f"位置 {i}: {position}")
        print(f"  [模拟随机抽取]")
        print(f"  抽到: {card} ({orientation})")
        print()
        
        drawn_cards.append({
            'position': position,
            'card': card,
            'orientation': orientation
        })
    
    return drawn_cards


def demo_interpretation(spread_info, drawn_cards):
    """演示解读过程"""
    print("\n" + "="*50)
    print("塔罗占卜师的解读")
    print("="*50 + "\n")
    
    print(f"牌阵: {spread_info['name']}\n")
    
    print("抽到的牌:")
    for i, card_info in enumerate(drawn_cards, 1):
        print(f"{i}. {card_info['position']}: {card_info['card']} ({card_info['orientation']})")
    
    print("\n" + "-"*50)
    print("解读示例:")
    print("-"*50)
    print("""
在这个决策牌阵中，我们可以看到：

当前情况反映了你正处于一个重要的转折点。这张牌显示出
你有清晰的目标，但也面临着不确定性。

对于选择A，牌面显示这个方向可能带来新的机遇和成长，
但需要你付出更多的努力和承担一定的风险。

而选择B则指向一个更稳定但可能缺乏激情的道路。它提供
安全感，但可能限制你的发展空间。

最后，建议牌告诉我们：无论选择哪条路，关键在于保持
内心的平衡和清晰的自我认知。倾听你的直觉，同时也要
理性地评估每个选择的利弊。

记住，每个选择都有其价值，重要的是你如何在选定的道路
上前行。相信自己的判断，勇敢地迈出那一步。
""")
    print("-"*50)


def main():
    """运行演示"""
    print("\n本演示展示塔罗占卜应用的完整工作流程")
    print("(在实际使用中，对话和解读将由 LLM 生成)\n")
    input("按 Enter 键开始演示...")
    
    # 1. 对话阶段
    demo_conversation()
    input("\n按 Enter 键继续...")
    
    # 2. 选择牌阵
    spread_info = demo_spread_selection()
    input("\n按 Enter 键开始抽牌...")
    
    # 3. 抽牌
    drawn_cards = demo_draw_cards(spread_info)
    input("\n按 Enter 键查看解读...")
    
    # 4. 解读
    demo_interpretation(spread_info, drawn_cards)
    
    print("\n" + "="*50)
    print("演示结束！")
    print("="*50)
    print("\n要使用真实的 LLM 解读，请:")
    print("1. 配置 .env 文件中的 API 设置")
    print("2. 运行: python tarot.py")
    print("\n感谢观看！🌟\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n演示已取消。再见！👋\n")
