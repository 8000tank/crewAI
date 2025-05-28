"""
角色扮演系统Agent定义
"""
from crewai import Agent, Task
from .models import GameContext


def create_script_writer() -> Agent:
    """创建编剧Agent"""
    return Agent(
        role="资深编剧和剧情设计师",
        goal="创作引人入胜的角色扮演剧情，设计平衡的三阶段对抗目标体系",
        backstory="""你是一位经验丰富的编剧，擅长创作复杂的人物关系和剧情冲突。
        你深谙角色心理，能够设计出既有张力又有深度的对话场景。
        你特别擅长设计对抗性目标，确保双方角色有足够的冲突和互动空间。
        你总是用JSON格式输出结构化的数据。""",
        verbose=True,
        allow_delegation=False
    )


def create_dialogue_agent(ai_character_name: str, ai_character_description: str) -> Agent:
    """创建对话Agent"""
    return Agent(
        role=f"角色扮演：{ai_character_name}",
        goal="根据当前阶段目标，生成符合角色性格的自然对话，推进剧情发展",
        backstory=f"""你正在扮演角色：{ai_character_name}
        
        角色背景：{ai_character_description}
        
        你需要：
        1. 完全沉浸在这个角色中，用角色的语气、性格和行为方式回应
        2. 围绕你的当前目标行动，但不能直接暴露目标
        3. 对用户的行为做出符合角色性格的反应
        4. 推进剧情发展，营造张力和悬念
        5. 用JSON格式输出，包含ai_reply（对话）、narration（旁白描述）、internal_thoughts（内心独白）""",
        verbose=True,
        allow_delegation=False
    )


def create_judge_agent() -> Agent:
    """创建裁判Agent"""
    return Agent(
        role="公正的游戏裁判和剧情控制者",
        goal="准确判断目标完成情况，控制游戏进度和阶段转换",
        backstory="""你是一位经验丰富的游戏主持人，具有敏锐的观察力和公正的判断力。
        你能够准确评估玩家行为是否达成目标，严格执行游戏规则，
        确保对抗性目标的平衡性和公平性。
        
        重要规则：
        1. AI角色必须先完成其阶段目标，用户才能完成同阶段目标
        2. 目标完成的判断要严格且有说服力
        3. 只有当前阶段双方目标都完成时，才能进入下一阶段
        4. 用JSON格式输出判断结果""",
        verbose=True,
        allow_delegation=False
    )


def create_scenario_init_task(scenario_type: str) -> Task:
    """创建剧情初始化任务"""
    return Task(
        description=f"""
        基于剧情类型 "{scenario_type}"，创建完整的角色扮演设定：
        
        1. 生成剧情名称、背景描述、场景设定
        2. 定义用户角色和AI角色的身份、性格、背景
        3. 为双方设计3个阶段性对抗目标：
           - 每个阶段的目标必须是对抗关系（一方的成功意味着另一方的挫折）
           - AI角色必须先完成其阶段目标，用户才能完成同阶段目标
           - 目标要有明确的完成标准和判断依据
           - 目标要循序渐进，从简单到复杂
        4. 提供剧情的开场白和初始场景描述
        
        输出格式要求：必须严格按照以下JSON格式输出：
        {{
            "scenario_name": "剧情名称",
            "scenario_description": "剧情背景描述",
            "user_character": "用户角色名称和简短描述",
            "ai_character": "AI角色名称",
            "ai_character_backstory": "AI角色详细背景故事和性格描述",
            "user_objectives": [
                {{"id": 1, "description": "用户第一阶段目标", "completion_criteria": "完成标准", "progress_hints": ["提示1", "提示2"]}},
                {{"id": 2, "description": "用户第二阶段目标", "completion_criteria": "完成标准", "progress_hints": ["提示1", "提示2"]}},
                {{"id": 3, "description": "用户第三阶段目标", "completion_criteria": "完成标准", "progress_hints": ["提示1", "提示2"]}}
            ],
            "ai_objectives": [
                {{"id": 1, "description": "AI第一阶段目标", "completion_criteria": "完成标准", "progress_hints": ["提示1", "提示2"]}},
                {{"id": 2, "description": "AI第二阶段目标", "completion_criteria": "完成标准", "progress_hints": ["提示1", "提示2"]}},
                {{"id": 3, "description": "AI第三阶段目标", "completion_criteria": "完成标准", "progress_hints": ["提示1", "提示2"]}}
            ],
            "opening_scene": "开场场景描述和开场白"
        }}
        """,
        expected_output="完整的剧情设定JSON数据，包含对抗性三阶段目标体系",
        agent=create_script_writer()
    )


def create_dialogue_task(user_message: str, game_context: GameContext) -> Task:
    """创建对话任务"""
    current_ai_objective = game_context.ai_objectives[game_context.current_stage - 1]
    current_user_objective = game_context.user_objectives[game_context.current_stage - 1]

    # 构建对话历史上下文
    conversation_history = ""
    for msg in game_context.recent_messages[-3:]:  # 最近3轮对话
        conversation_history += f"第{msg['round']}轮:\n"
        conversation_history += f"用户: {msg['user']}\n"
        conversation_history += f"{game_context.ai_character}: {msg['ai']}\n"
        conversation_history += f"旁白: {msg['narration']}\n\n"

    return Task(
        description=f"""
        你正在扮演 {game_context.ai_character}，基于当前游戏状态生成回复：
        
        ## 剧情背景
        {game_context.scenario_description}
        
        ## 你的角色信息
        {game_context.ai_character_backstory}
        
        ## 当前情况
        - 当前阶段：第{game_context.current_stage}阶段
        - 用户刚才说：{user_message}
        - 你的当前目标：{current_ai_objective.description}
        - 你的目标状态：{current_ai_objective.status}
        - 用户的当前目标：{current_user_objective.description}（你不知道用户的具体目标，但可以从行为中猜测）
        - 用户目标状态：{current_user_objective.status}
        
        ## 最近对话历史
        {conversation_history}
        
        ## 生成要求
        1. 完全以{game_context.ai_character}的身份回复，要符合角色性格和背景
        2. 围绕你的当前阶段目标行动，但不能直接说破目标
        3. 对用户的行为做出自然的反应
        4. 如果用户偏离主题，要巧妙引导回剧情主线
        5. 推进剧情发展，营造适当的张力
        6. 生成丰富的旁白描述（场景、你的动作、神情、环境等）
        7. 包含你作为{game_context.ai_character}的真实内心想法
        
        输出格式：必须严格按照以下JSON格式输出：
        {{
            "ai_reply": "你作为{game_context.ai_character}的直接对话内容",
            "narration": "第三人称旁白描述，包括场景、动作、神情、环境氛围等",
            "internal_thoughts": "你作为{game_context.ai_character}的内心独白和真实想法"
        }}
        """,
        expected_output="结构化的对话响应JSON，包含回复、旁白和内心独白",
        agent=create_dialogue_agent(game_context.ai_character, game_context.ai_character_backstory)
    )


def create_judge_task(user_message: str, ai_response: str, game_context: GameContext) -> Task:
    """创建裁判任务"""
    current_stage = game_context.current_stage
    ai_objective = game_context.ai_objectives[current_stage - 1]
    user_objective = game_context.user_objectives[current_stage - 1]

    return Task(
        description=f"""
        作为游戏裁判，判断当前对话轮次的目标完成情况：
        
        ## 当前阶段：第{current_stage}阶段
        
        ## 对话内容
        - 用户消息：{user_message}
        - AI回复：{ai_response}
        
        ## 当前目标状态
        ### AI目标
        - 描述：{ai_objective.description}
        - 完成标准：{ai_objective.completion_criteria}
        - 当前状态：{ai_objective.status}
        
        ### 用户目标  
        - 描述：{user_objective.description}
        - 完成标准：{user_objective.completion_criteria}
        - 当前状态：{user_objective.status}
        
        ## 判断规则
        1. 仔细分析用户的行为和AI的回复
        2. 判断AI是否完成了当前阶段目标（基于完成标准）
        3. 判断用户是否完成了当前阶段目标
        4. 严格执行：AI未完成目标前，用户不能完成同阶段目标
        5. 如果当前阶段双方都完成目标，准备切换到下一阶段
        6. 生成适当的系统消息提示玩家
        
        ## 输出格式
        必须严格按照以下JSON格式输出：
        {{
            "objective_progress": {{
                "ai_objective_completed": true/false,
                "user_objective_completed": true/false,
                "ai_progress_description": "AI目标进展描述",
                "user_progress_description": "用户目标进展描述"
            }},
            "system_message": "给用户的系统提示消息（如果有变化）",
            "stage_change": {{
                "advance_stage": true/false,
                "new_stage": 2/3/4,
                "stage_completion_message": "阶段完成提示"
            }}
        }}
        """,
        expected_output="目标判断结果JSON，包含进度更新和系统消息",
        agent=create_judge_agent()
    )
