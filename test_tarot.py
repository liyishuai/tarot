#!/usr/bin/env python3
"""
塔罗牌应用测试脚本
验证核心功能而不需要实际的 API 调用
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from tarot_cards import (
    get_all_cards,
    get_spread_info,
    list_all_spreads,
    MAJOR_ARCANA,
    MINOR_ARCANA,
)


def test_cards():
    """测试塔罗牌数据"""
    print("测试塔罗牌数据...")
    
    # 测试总数
    all_cards = get_all_cards()
    assert len(all_cards) == 78, f"应该有78张牌，实际有{len(all_cards)}张"
    assert len(MAJOR_ARCANA) == 22, f"应该有22张大阿尔卡纳，实际有{len(MAJOR_ARCANA)}张"
    
    minor_count = sum(len(cards) for cards in MINOR_ARCANA.values())
    assert minor_count == 56, f"应该有56张小阿尔卡纳，实际有{minor_count}张"
    
    # 测试每个花色
    for suit, cards in MINOR_ARCANA.items():
        assert len(cards) == 14, f"{suit}应该有14张牌，实际有{len(cards)}张"
    
    print("✓ 塔罗牌数据测试通过")


def test_spreads():
    """测试牌阵数据"""
    print("\n测试牌阵数据...")
    
    # 测试所有牌阵
    spreads_text = list_all_spreads()
    assert "单张牌阵" in spreads_text
    assert "三张牌阵" in spreads_text
    assert "凯尔特十字牌阵" in spreads_text
    
    # 测试单个牌阵
    spread = get_spread_info("1")
    assert spread is not None
    assert spread["name"] == "单张牌阵"
    assert len(spread["positions"]) == 1
    
    spread = get_spread_info("2")
    assert spread is not None
    assert len(spread["positions"]) == 3
    
    spread = get_spread_info("5")
    assert spread is not None
    assert len(spread["positions"]) == 10
    
    # 测试无效牌阵
    spread = get_spread_info("99")
    assert spread is None
    
    print("✓ 牌阵数据测试通过")


def test_card_selection():
    """测试卡牌选择功能"""
    print("\n测试卡牌选择功能...")
    
    import random
    all_cards = get_all_cards()
    
    # 测试随机选择
    selected = random.choice(all_cards)
    assert selected in all_cards
    
    # 测试避免重复 - use set for efficient O(1) lookup
    drawn = []
    drawn_set = set()
    for _ in range(10):
        available = [c for c in all_cards if c not in drawn_set]
        card = random.choice(available)
        assert card not in drawn_set
        drawn.append(card)
        drawn_set.add(card)
    
    assert len(drawn) == 10
    assert len(set(drawn)) == 10  # 确保没有重复
    
    print("✓ 卡牌选择测试通过")


def test_search():
    """测试卡牌搜索功能"""
    print("\n测试卡牌搜索功能...")
    
    all_cards = get_all_cards()
    
    # 搜索测试
    search_term = "愚者"
    matching = [c for c in all_cards if search_term in c]
    assert len(matching) > 0
    assert any("愚者" in c for c in matching)
    
    search_term = "权杖"
    matching = [c for c in all_cards if search_term in c]
    assert len(matching) == 14  # 14张权杖牌
    
    # 测试大小写不敏感搜索
    search_term_lower = "fool"
    matching_lower = [c for c in all_cards if search_term_lower.lower() in c.lower()]
    assert len(matching_lower) > 0
    assert any("Fool" in c for c in matching_lower)
    
    # 测试部分匹配
    search_term_partial = "王"
    matching_partial = [c for c in all_cards if search_term_partial in c]
    assert len(matching_partial) > 0  # 应该找到王牌、国王等
    
    print("✓ 卡牌搜索测试通过")


def main():
    """运行所有测试"""
    print("=" * 50)
    print("开始测试塔罗牌应用核心功能")
    print("=" * 50)
    
    try:
        test_cards()
        test_spreads()
        test_card_selection()
        test_search()
        
        print("\n" + "=" * 50)
        print("所有测试通过！✨")
        print("=" * 50)
        return 0
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
