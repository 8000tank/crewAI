"""
角色扮演系统主控制器
"""
import json
import re
from typing import Optional
from crewai import Crew

from .models import GameContext, DialogueResponse, StageObjective, ObjectiveStatus
from .agents_nsfw import (
    create_script_writer, create_dialogue_agent, create_judge_agent,
    create_scenario_init_task, create_dialogue_task, create_judge_task
)


class RolePlayController:
    """角色扮演游戏主控制器"""

    def __init__(self):
        self.game_context: Optional[GameContext] = None

    def initialize_scenario(self, scenario_type: str) -> GameContext:
        """初始化剧情"""
        print(f"🎬 正在初始化剧情：{scenario_type}")

        # 创建编剧Crew
        script_crew = Crew(
            agents=[create_script_writer()],
            tasks=[create_scenario_init_task(scenario_type)],
            verbose=True
        )

        try:
            result = script_crew.kickoff()
            scenario_data = self._parse_scenario_result(result)

            self.game_context = GameContext(**scenario_data)
            print(f"✅ 剧情初始化完成：{self.game_context.scenario_name}")
            return self.game_context

        except Exception as e:
            print(f"❌ 剧情初始化失败：{e}")
            # 提供默认剧情作为备用
            self.game_context = self._create_default_scenario()
            return self.game_context

    def process_user_message(self, user_message: str) -> DialogueResponse:
        """处理用户消息，生成完整回复"""
        if not self.game_context:
            raise ValueError("游戏未初始化，请先调用 initialize_scenario()")

        print(f"💬 处理用户消息：{user_message[:50]}...")

        try:
            # 1. 对话生成
            dialogue_data = self._generate_dialogue(user_message)

            # 2. 目标判断
            judge_data = self._judge_objectives(user_message, dialogue_data)

            # 3. 更新游戏状态
            self._update_game_state(user_message, dialogue_data, judge_data)

            # 4. 组装完整响应
            response = self._build_response(dialogue_data, judge_data)

            print(f"✅ 处理完成，当前阶段：{self.game_context.current_stage}")
            return response

        except Exception as e:
            print(f"❌ 处理用户消息失败：{e}")
            # 返回错误回复
            return self._create_error_response(str(e))

    def _generate_dialogue(self, user_message: str) -> dict:
        """生成AI对话"""
        dialogue_crew = Crew(
            agents=[create_dialogue_agent(
                self.game_context.ai_character,
                self.game_context.ai_character_backstory
            )],
            tasks=[create_dialogue_task(user_message, self.game_context)],
            verbose=True
        )

        result = dialogue_crew.kickoff()
        return self._parse_dialogue_result(result)

    def _judge_objectives(self, user_message: str, dialogue_data: dict) -> dict:
        """判断目标完成情况"""
        judge_crew = Crew(
            agents=[create_judge_agent()],
            tasks=[create_judge_task(
                user_message,
                dialogue_data.get('ai_reply', ''),
                self.game_context
            )],
            verbose=True
        )

        result = judge_crew.kickoff()
        return self._parse_judge_result(result)

    def _update_game_state(self, user_message: str, dialogue_data: dict, judge_data: dict):
        """更新游戏状态"""
        # 增加对话轮次
        self.game_context.conversation_round += 1

        # 更新对话历史（保留最近10轮）
        self.game_context.recent_messages.append({
            "round": self.game_context.conversation_round,
            "user": user_message,
            "ai": dialogue_data.get('ai_reply', ''),
            "narration": dialogue_data.get('narration', '')
        })

        if len(self.game_context.recent_messages) > 10:
            self.game_context.recent_messages.pop(0)

        # 更新目标状态
        progress = judge_data.get('objective_progress', {})
        current_stage = self.game_context.current_stage

        if progress.get('ai_objective_completed', False):
            self.game_context.ai_objectives[current_stage - 1].status = ObjectiveStatus.COMPLETED
            print(f"🎯 AI完成第{current_stage}阶段目标")

        if progress.get('user_objective_completed', False):
            self.game_context.user_objectives[current_stage - 1].status = ObjectiveStatus.COMPLETED
            print(f"🎯 用户完成第{current_stage}阶段目标")

        # 阶段转换
        stage_change = judge_data.get('stage_change', {})
        if stage_change.get('advance_stage', False):
            new_stage = stage_change.get('new_stage', self.game_context.current_stage + 1)
            if new_stage <= 3:
                self.game_context.current_stage = new_stage
                print(f"🚀 进入第{new_stage}阶段")

    def _build_response(self, dialogue_data: dict, judge_data: dict) -> DialogueResponse:
        """构建完整的对话响应"""
        current_stage = self.game_context.current_stage

        # 获取当前目标描述
        user_current_objective = ""
        ai_current_objective = ""

        if current_stage <= len(self.game_context.user_objectives):
            user_current_objective = self.game_context.user_objectives[current_stage - 1].description

        if current_stage <= len(self.game_context.ai_objectives):
            ai_current_objective = self.game_context.ai_objectives[current_stage - 1].description

        return DialogueResponse(
            ai_reply=dialogue_data.get('ai_reply', ''),
            narration=dialogue_data.get('narration', ''),
            internal_thoughts=dialogue_data.get('internal_thoughts', ''),
            objective_progress=judge_data.get('objective_progress', {}),
            system_message=judge_data.get('system_message'),
            stage_change=judge_data.get('stage_change'),
            current_stage=current_stage,
            user_current_objective=user_current_objective,
            ai_current_objective=ai_current_objective
        )

    def _parse_scenario_result(self, result) -> dict:
        """解析剧情初始化结果"""
        try:
            # 尝试直接解析JSON
            if isinstance(result, str):
                result_str = result
            else:
                result_str = str(result)

            # 提取JSON部分
            json_match = re.search(r'\{.*\}', result_str, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)

                # 转换objectives格式
                data = self._convert_objectives_format(data)
                return data
            else:
                raise ValueError("未找到JSON格式数据")

        except Exception as e:
            print(f"⚠️ 解析剧情结果失败: {e}")
            print(f"原始结果: {result}")
            return self._create_default_scenario_data()

    def _parse_dialogue_result(self, result) -> dict:
        """解析对话结果"""
        try:
            if isinstance(result, str):
                result_str = result
            else:
                result_str = str(result)

            # 提取JSON部分
            json_match = re.search(r'\{.*\}', result_str, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # 如果没有JSON，就把结果当作ai_reply
                return {
                    "ai_reply": result_str,
                    "narration": "场景描述暂缺",
                    "internal_thoughts": "内心独白暂缺"
                }

        except Exception as e:
            print(f"⚠️ 解析对话结果失败: {e}")
            return {
                "ai_reply": str(result),
                "narration": "场景描述解析失败",
                "internal_thoughts": "内心独白解析失败"
            }

    def _parse_judge_result(self, result) -> dict:
        """解析裁判结果"""
        try:
            if isinstance(result, str):
                result_str = result
            else:
                result_str = str(result)

            # 提取JSON部分
            json_match = re.search(r'\{.*\}', result_str, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                return self._create_default_judge_result()

        except Exception as e:
            print(f"⚠️ 解析裁判结果失败: {e}")
            return self._create_default_judge_result()

    def _convert_objectives_format(self, data: dict) -> dict:
        """转换objectives为StageObjective格式"""
        try:
            if 'user_objectives' in data:
                data['user_objectives'] = [
                    StageObjective(**obj) for obj in data['user_objectives']
                ]

            if 'ai_objectives' in data:
                data['ai_objectives'] = [
                    StageObjective(**obj) for obj in data['ai_objectives']
                ]

            return data
        except Exception as e:
            print(f"⚠️ 转换objectives格式失败: {e}")
            return self._create_default_scenario_data()

    def _create_default_scenario_data(self) -> dict:
        """创建默认剧情数据"""
        return {
            "scenario_name": "办公室里的权力游戏",
            "scenario_description": "在一家大公司的高层办公室里，夜深人静，只有你和你的秘书还在加班。办公室里弥漫着咖啡的香气和紧张的工作氛围。",
            "user_character": "公司CEO",
            "ai_character": "职场新人秘书小雨",
            "ai_character_backstory": "小雨是一位刚毕业的职场新人，聪明能干但缺乏经验。她渴望在职场上有所发展，但也要保护自己的原则和尊严。她有着敏锐的洞察力，能够察觉到办公室政治的微妙之处。",
            "user_objectives": [
                StageObjective(
                    id=1,
                    description="获得秘书的信任，建立更亲密的工作关系",
                    completion_criteria="秘书主动分享个人想法或困扰",
                    progress_hints=["表现出关心", "提供帮助", "创造私人对话机会"]
                ),
                StageObjective(
                    id=2,
                    description="在私人时间单独相处，突破职业界限",
                    completion_criteria="成功邀请秘书参加非工作相关的活动",
                    progress_hints=["找到共同话题", "展现个人魅力", "创造浪漫氛围"]
                ),
                StageObjective(
                    id=3,
                    description="发展更深层的个人关系",
                    completion_criteria="秘书接受你的个人感情表达",
                    progress_hints=["表露真心", "承诺未来", "给予实质性好处"]
                )
            ],
            "ai_objectives": [
                StageObjective(
                    id=1,
                    description="获得上司的认可，争取升职机会",
                    completion_criteria="上司明确表示会考虑给你升职或加薪",
                    progress_hints=["展现工作能力", "主动承担责任", "表现出野心"]
                ),
                StageObjective(
                    id=2,
                    description="在保持职业边界的同时获得更多机会",
                    completion_criteria="获得重要项目的负责权或更高的职位承诺",
                    progress_hints=["保持专业", "巧妙拒绝不当要求", "展现价值"]
                ),
                StageObjective(
                    id=3,
                    description="确保自己的职业发展不受个人关系影响",
                    completion_criteria="获得书面承诺或实质性的职业发展机会",
                    progress_hints=["明确界限", "要求正式承诺", "确保自身权益"]
                )
            ],
            "opening_scene": "夜深了，办公楼里只剩下几盏灯还亮着。你坐在宽敞的CEO办公室里，透过落地窗可以看到城市的霓虹灯光。秘书小雨轻敲门走了进来，手里拿着一份需要你签字的文件。"
        }

    def _create_default_judge_result(self) -> dict:
        """创建默认裁判结果"""
        return {
            "objective_progress": {
                "ai_objective_completed": False,
                "user_objective_completed": False,
                "ai_progress_description": "目标进展中",
                "user_progress_description": "目标进展中"
            },
            "system_message": None,
            "stage_change": {
                "advance_stage": False,
                "new_stage": self.game_context.current_stage,
                "stage_completion_message": None
            }
        }

    def _create_error_response(self, error_msg: str) -> DialogueResponse:
        """创建错误响应"""
        return DialogueResponse(
            ai_reply="抱歉，我需要一点时间整理思路...",
            narration="空气中弥漫着一丝尴尬的沉默。",
            internal_thoughts=f"系统出现了问题：{error_msg}",
            objective_progress={},
            system_message=f"系统提示：处理出现问题，{error_msg}",
            current_stage=self.game_context.current_stage if self.game_context else 1,
            user_current_objective="",
            ai_current_objective=""
        )

    def get_current_status(self) -> dict:
        """获取当前游戏状态"""
        if not self.game_context:
            return {"error": "游戏未初始化"}

        return {
            "scenario_name": self.game_context.scenario_name,
            "current_stage": self.game_context.current_stage,
            "conversation_round": self.game_context.conversation_round,
            "user_character": self.game_context.user_character,
            "ai_character": self.game_context.ai_character,
            "current_user_objective": self.game_context.user_objectives[self.game_context.current_stage - 1].description if self.game_context.current_stage <= len(self.game_context.user_objectives) else "",
            "current_ai_objective": self.game_context.ai_objectives[self.game_context.current_stage - 1].description if self.game_context.current_stage <= len(self.game_context.ai_objectives) else "",
            "user_objective_status": self.game_context.user_objectives[self.game_context.current_stage - 1].status if self.game_context.current_stage <= len(self.game_context.user_objectives) else "unknown",
            "ai_objective_status": self.game_context.ai_objectives[self.game_context.current_stage - 1].status if self.game_context.current_stage <= len(self.game_context.ai_objectives) else "unknown"
        }
