#!/usr/bin/env python3
"""
塔罗牌占卜应用
使用OpenAI兼容的LLM服务进行塔罗牌解读
"""

import os
import sys
import random
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

from tarot_cards import (
    get_all_cards,
    get_spread_info,
    list_all_spreads,
)

# 加载环境变量
load_dotenv()


class TarotReader:
    """塔罗牌占卜系统"""
    
    def __init__(self):
        """初始化塔罗占卜系统"""
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        if not api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        self.conversation_history = []
        self.selected_spread = None
        self.drawn_cards = []
    
    def chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """与LLM进行对话"""
        messages = []
        
        # 添加系统提示
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 添加历史对话
        messages.extend(self.conversation_history)
        
        # 添加用户消息
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            assistant_message = response.choices[0].message.content
            
            # 保存对话历史
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        except Exception as e:
            return f"调用LLM服务时出错: {str(e)}"
    
    def start_conversation(self):
        """开始对话，引导用户选择牌阵"""
        system_prompt = """你是一位经验丰富、充满智慧的塔罗牌占卜师。你的职责是：
1. 与来访者进行友好的对话，了解他们的问题和困惑
2. 根据他们的需求，推荐合适的塔罗牌阵
3. 在他们抽取塔罗牌后，为他们提供深刻、富有洞察力的解读

请用温暖、专业的语气与来访者交流。"""
        
        greeting = self.chat(
            "你好，我想进行塔罗占卜。",
            system_prompt=system_prompt
        )
        
        print("\n" + "="*50)
        print("塔罗占卜师:", greeting)
        print("="*50 + "\n")
    
    def interactive_conversation(self):
        """交互式对话，让用户与塔罗师对话"""
        print("(输入 'spreads' 查看所有牌阵，输入 'select' 选择牌阵并开始占卜)\n")
        
        while not self.selected_spread:
            user_input = input("你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'spreads':
                print("\n可用的塔罗牌阵:")
                print(list_all_spreads())
                print()
                continue
            
            if user_input.lower() == 'select':
                self.select_spread()
                break
            
            # 与LLM对话
            response = self.chat(user_input)
            print(f"\n塔罗占卜师: {response}\n")
    
    def select_spread(self):
        """选择塔罗牌阵"""
        print("\n请选择一个塔罗牌阵:")
        print(list_all_spreads())
        print()
        
        while True:
            spread_id = input("请输入牌阵编号 (1-5): ").strip()
            
            spread_info = get_spread_info(spread_id)
            if spread_info:
                self.selected_spread = spread_info
                print(f"\n已选择: {spread_info['name']}")
                print(f"说明: {spread_info['description']}")
                print(f"需要抽取 {len(spread_info['positions'])} 张牌\n")
                break
            else:
                print("无效的牌阵编号，请重新输入。\n")
    
    def draw_cards(self):
        """抽取塔罗牌"""
        if not self.selected_spread:
            print("请先选择牌阵!")
            return
        
        positions = self.selected_spread['positions']
        all_cards = get_all_cards()
        
        print("开始抽牌...\n")
        
        # Use a set to track drawn cards for O(1) lookup
        drawn_card_names = set()
        
        for i, position in enumerate(positions, 1):
            print(f"位置 {i}: {position}")
            
            while True:
                choice = input("  选择方式 - [r]随机抽取 或 [m]手动输入牌名: ").strip().lower()
                
                if choice == 'r':
                    # 随机抽取 - use set for efficient filtering
                    available_cards = [c for c in all_cards if c not in drawn_card_names]
                    card = random.choice(available_cards)
                    orientation = random.choice(['正位', '逆位'])
                    print(f"  抽到: {card} ({orientation})")
                    
                    self.drawn_cards.append({
                        'position': position,
                        'card': card,
                        'orientation': orientation
                    })
                    drawn_card_names.add(card)
                    print()
                    break
                
                elif choice == 'm':
                    # 手动输入
                    print(f"\n  可选的牌 (输入部分名称进行搜索):")
                    card_input = input("  输入牌名: ").strip()
                    
                    # 搜索匹配的牌 - case insensitive search
                    matching_cards = [c for c in all_cards if card_input.lower() in c.lower()]
                    
                    if not matching_cards:
                        print("  没有找到匹配的牌，请重试。\n")
                        continue
                    
                    if len(matching_cards) == 1:
                        card = matching_cards[0]
                    else:
                        print("  找到多张匹配的牌:")
                        for idx, c in enumerate(matching_cards, 1):
                            print(f"    {idx}. {c}")
                        
                        try:
                            card_idx = int(input("  选择编号: ").strip()) - 1
                            card = matching_cards[card_idx]
                        except (ValueError, IndexError):
                            print("  无效的选择，请重试。\n")
                            continue
                    
                    orientation = input("  方向 - [z]正位 或 [n]逆位: ").strip().lower()
                    orientation = '正位' if orientation == 'z' else '逆位'
                    
                    print(f"  已选择: {card} ({orientation})")
                    
                    self.drawn_cards.append({
                        'position': position,
                        'card': card,
                        'orientation': orientation
                    })
                    print()
                    break
                
                else:
                    print("  无效的选择，请输入 r 或 m。")
    
    def get_interpretation(self):
        """获取LLM解读"""
        if not self.drawn_cards:
            print("还没有抽牌!")
            return
        
        print("\n" + "="*50)
        print("正在请求塔罗占卜师为您解读...")
        print("="*50 + "\n")
        
        # 构建解读请求
        cards_description = f"牌阵: {self.selected_spread['name']}\n\n"
        cards_description += "抽到的牌:\n"
        
        for i, card_info in enumerate(self.drawn_cards, 1):
            cards_description += f"{i}. {card_info['position']}: {card_info['card']} ({card_info['orientation']})\n"
        
        interpretation_request = f"""现在来访者已经抽取了以下塔罗牌，请为他们提供详细的解读：

{cards_description}

请提供：
1. 每张牌在其位置上的含义
2. 牌与牌之间的关联和整体信息
3. 针对来访者问题的具体建议和指引

请用温暖、富有洞察力的语言进行解读。"""
        
        interpretation = self.chat(interpretation_request)
        
        print("塔罗占卜师的解读:")
        print("-" * 50)
        print(interpretation)
        print("-" * 50)
    
    def run(self):
        """运行塔罗占卜程序"""
        print("\n" + "🔮" * 20)
        print("欢迎来到塔罗占卜屋".center(40))
        print("🔮" * 20 + "\n")
        
        # 开始对话
        self.start_conversation()
        
        # 交互式对话
        self.interactive_conversation()
        
        # 抽牌
        self.draw_cards()
        
        # 获取解读
        self.get_interpretation()
        
        print("\n感谢您的使用！祝您生活愉快！🌟\n")


def main():
    """主函数"""
    try:
        reader = TarotReader()
        reader.run()
    except KeyboardInterrupt:
        print("\n\n再见！👋\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
