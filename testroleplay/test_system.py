#!/usr/bin/env python
"""
角色扮演系统测试脚本
"""

import os
import sys

# 添加src路径到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))  # noqa: E402

from testroleplay.controller import RolePlayController


def test_basic_functionality():
    """测试基本功能"""
    print("🧪 开始测试角色扮演系统...")

    # 检查API密钥
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
        print("⚠️ 警告：未设置API密钥，将使用模拟模式测试")
        return test_without_api()

    try:
        # 初始化控制器
        controller = RolePlayController()
        print("✅ 控制器初始化成功")

        # 测试剧情初始化
        print("\n📝 测试剧情初始化...")
        game_context = controller.initialize_scenario("办公室上司与秘书")
        print(f"✅ 剧情初始化成功：{game_context.scenario_name}")

        # 测试状态获取
        print("\n📊 测试状态获取...")
        status = controller.get_current_status()
        print(f"✅ 状态获取成功，当前阶段：{status['current_stage']}")

        # 测试对话处理
        print("\n💬 测试对话处理...")
        response = controller.process_user_message("你好，我是新来的CEO")
        print(f"✅ 对话处理成功")
        print(f"AI回复：{response.ai_reply[:100]}...")

        print("\n🎉 所有基本功能测试通过！")
        return True

    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def test_without_api():
    """无API密钥的模拟测试"""
    print("🧪 执行模拟测试...")

    try:
        # 测试数据模型
        from testroleplay.models import GameContext, StageObjective, DialogueResponse

        # 创建测试对象
        objective = StageObjective(
            id=1,
            description="测试目标",
            completion_criteria="测试标准",
            progress_hints=["提示1", "提示2"]
        )
        print("✅ StageObjective 创建成功")

        game_context = GameContext(
            scenario_name="测试剧情",
            scenario_description="测试描述",
            user_character="测试用户",
            ai_character="测试AI",
            user_objectives=[objective],
            ai_objectives=[objective]
        )
        print("✅ GameContext 创建成功")

        response = DialogueResponse(
            ai_reply="测试回复",
            narration="测试旁白",
            internal_thoughts="测试独白",
            objective_progress={}
        )
        print("✅ DialogueResponse 创建成功")

        print("\n🎉 模拟测试通过！数据模型工作正常。")
        print("💡 要进行完整测试，请设置 OPENAI_API_KEY 或 GOOGLE_API_KEY")
        return True

    except Exception as e:
        print(f"❌ 模拟测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_creation():
    """测试Agent创建"""
    print("\n🤖 测试Agent创建...")

    try:
        from testroleplay.agents_nsfw import create_script_writer, create_dialogue_agent, create_judge_agent

        script_writer = create_script_writer()
        print("✅ 编剧Agent创建成功")

        dialogue_agent = create_dialogue_agent("测试角色", "测试背景")
        print("✅ 对话Agent创建成功")

        judge_agent = create_judge_agent()
        print("✅ 裁判Agent创建成功")

        return True

    except Exception as e:
        print(f"❌ Agent创建测试失败：{e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("🎭 角色扮演系统测试")
    print("=" * 60)

    # 测试1：基本功能
    test1_passed = test_basic_functionality()

    # 测试2：Agent创建
    test2_passed = test_agent_creation()

    # 总结
    print("\n" + "=" * 60)
    print("📋 测试结果总结")
    print("=" * 60)

    if test1_passed and test2_passed:
        print("🎉 所有测试通过！系统准备就绪。")
        print("💡 运行 'python roleplay_demo.py' 开始游戏")
    else:
        print("❌ 部分测试失败，请检查错误信息")

    return test1_passed and test2_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
