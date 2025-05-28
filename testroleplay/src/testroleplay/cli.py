"""
角色扮演系统命令行界面
"""
import os
from .controller import RolePlayController


def print_separator(title: str = ""):
    """打印分隔线"""
    if title:
        print(f"\n{'=' * 20} {title} {'=' * 20}")
    else:
        print("=" * 60)


def print_dialogue_response(response, game_context):
    """格式化打印对话响应"""
    print_separator("AI回复")
    print(f"💬 {game_context.ai_character}：{response.ai_reply}")

    print_separator("场景描述")
    print(f"🎭 {response.narration}")

    if response.internal_thoughts:
        print_separator("内心独白")
        print(f"💭 [{game_context.ai_character}的想法]：{response.internal_thoughts}")

    if response.system_message:
        print_separator("系统提示")
        print(f"🎯 {response.system_message}")

    if response.stage_change and response.stage_change.get('advance_stage'):
        print_separator("阶段变化")
        print(f"🚀 {response.stage_change.get('stage_completion_message', '进入下一阶段')}")


def print_game_status(controller: RolePlayController):
    """打印游戏状态"""
    status = controller.get_current_status()

    print_separator("游戏状态")
    print(f"📖 剧情：{status.get('scenario_name', 'N/A')}")
    print(f"🎭 你扮演：{status.get('user_character', 'N/A')}")
    print(f"🤖 AI扮演：{status.get('ai_character', 'N/A')}")
    print(f"📊 当前阶段：第{status.get('current_stage', 1)}阶段")
    print(f"🔄 对话轮次：{status.get('conversation_round', 0)}")

    print_separator("当前目标")
    print(f"🎯 你的目标：{status.get('current_user_objective', 'N/A')}")
    print(f"   状态：{status.get('user_objective_status', 'N/A')}")
    print(f"🎯 AI的目标：{status.get('current_ai_objective', 'N/A')}")
    print(f"   状态：{status.get('ai_objective_status', 'N/A')}")


def print_help():
    """打印帮助信息"""
    print_separator("帮助信息")
    print("💡 可用命令：")
    print("   /status  - 查看当前游戏状态")
    print("   /help    - 显示帮助信息")
    print("   /quit    - 退出游戏")
    print("   /restart - 重新开始游戏")
    print("\n直接输入文字即可与AI对话。")


def select_scenario():
    """选择剧情类型"""
    print_separator("选择剧情")
    print("请选择一个剧情类型：")
    print("1. 办公室上司与秘书")
    print("2. 高校教授与学生")
    print("3. 医生与护士")
    print("4. 总裁与助理")
    print("5. 自定义剧情")

    scenarios = {
        "1": "办公室上司与秘书",
        "2": "高校教授与学生",
        "3": "医生与护士",
        "4": "总裁与助理",
        "5": "自定义剧情"
    }

    while True:
        choice = input("\n请输入选项数字 (1-5): ").strip()
        if choice in scenarios:
            if choice == "5":
                custom_scenario = input("请描述你想要的剧情类型: ").strip()
                return custom_scenario if custom_scenario else scenarios["1"]
            return scenarios[choice]
        print("❌ 无效选择，请重新输入。")


def main():
    """主函数"""
    print_separator("角色扮演聊天系统")
    print("🎭 欢迎来到AI角色扮演世界！")
    print("💡 输入 /help 查看帮助信息")

    # 检查环境变量
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
        print("\n⚠️ 警告：未检测到API密钥，请设置 OPENAI_API_KEY 或 GOOGLE_API_KEY 环境变量")
        print("例如：export OPENAI_API_KEY='your-api-key'")

    controller = RolePlayController()

    # 选择并初始化剧情
    scenario_type = select_scenario()

    print(f"\n🎬 正在初始化剧情：{scenario_type}")
    print("⏳ 请稍等，AI正在创建剧情...")

    try:
        game_context = controller.initialize_scenario(scenario_type)

        print_separator("剧情介绍")
        print(f"📖 {game_context.scenario_name}")
        print(f"📝 {game_context.scenario_description}")

        print_separator("角色信息")
        print(f"🎭 你扮演：{game_context.user_character}")
        print(f"🤖 AI扮演：{game_context.ai_character}")

        print_separator("目标体系")
        print("🎯 你的三阶段目标：")
        for i, obj in enumerate(game_context.user_objectives, 1):
            print(f"   第{i}阶段：{obj.description}")

        print("\n🤖 AI的三阶段目标：")
        for i, obj in enumerate(game_context.ai_objectives, 1):
            print(f"   第{i}阶段：{obj.description}")

        print_separator("开始游戏")
        print(f"🎬 {game_context.opening_scene}")

        # 主游戏循环
        while True:
            print_separator()
            user_input = input("💬 你: ").strip()

            if not user_input:
                continue

            # 处理命令
            if user_input.startswith('/'):
                command = user_input.lower()

                if command == '/quit':
                    print("👋 谢谢游玩，再见！")
                    break
                elif command == '/help':
                    print_help()
                elif command == '/status':
                    print_game_status(controller)
                elif command == '/restart':
                    print("🔄 重新开始游戏...")
                    scenario_type = select_scenario()
                    game_context = controller.initialize_scenario(scenario_type)
                    print("✅ 游戏重新开始！")
                else:
                    print("❌ 未知命令，输入 /help 查看帮助")
                continue

            # 处理对话
            try:
                print("\n⏳ AI正在思考...")
                response = controller.process_user_message(user_input)
                print_dialogue_response(response, game_context)

                # 检查游戏是否结束
                if game_context.current_stage > 3:
                    print_separator("游戏完成")
                    print("🎉 恭喜！你已经完成了所有阶段的目标！")
                    print("💬 你可以继续与AI聊天，或输入 /restart 开始新游戏")

            except Exception as e:
                print(f"❌ 处理失败：{e}")
                print("💡 你可以重试，或输入 /restart 重新开始")

    except Exception as e:
        print(f"❌ 初始化失败：{e}")
        print("💡 请检查网络连接和API密钥设置")


if __name__ == "__main__":
    main()
