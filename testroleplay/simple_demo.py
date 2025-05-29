#!/usr/bin/env python
"""
角色扮演系统简单演示
这是一个最简化的使用示例
"""

import os
import sys

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))  # noqa: E402


def simple_demo():
    """简单演示函数"""
    print("🎭 角色扮演系统演示")
    print("=" * 50)

    # 检查环境
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
        print("⚠️ 请先设置 API 密钥:")
        print("export OPENAI_API_KEY='your-key'")
        print("或")
        print("export GOOGLE_API_KEY='your-key'")
        return

    try:
        # 导入必要模块
        from testroleplay.controller import RolePlayController

        # 创建控制器
        controller = RolePlayController()
        print("✅ 系统初始化成功")

        # 初始化剧情
        print("\n🎬 正在创建剧情...")
        game_context = controller.initialize_scenario("办公室上司与秘书")

        print(f"\n📖 剧情：{game_context.scenario_name}")
        print(f"🎭 你扮演：{game_context.user_character}")
        print(f"🤖 AI扮演：{game_context.ai_character}")

        print(f"\n🎬 开场：")
        print(game_context.opening_scene)

        print(f"\n🎯 你的第一阶段目标：")
        print(game_context.user_objectives[0].description)

        # 简单对话测试
        print(f"\n💬 开始对话测试...")
        response = controller.process_user_message("Hi小雨，这么晚还在加班辛苦了，话说你今天穿的真性感")

        print(f"\n🤖 {game_context.ai_character}：{response.ai_reply}")
        print(f"\n🎭 旁白：{response.narration}")

        if response.internal_thoughts:
            print(f"\n💭 内心独白：{response.internal_thoughts}")

        print("\n✅ 演示完成！系统工作正常。")
        print("运行 'python roleplay_demo.py' 开始完整游戏体验")

    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    simple_demo()
