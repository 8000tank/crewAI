"""
角色扮演系统核心数据模型
"""
from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum


class ObjectiveStatus(str, Enum):
    """目标状态枚举"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class StageObjective(BaseModel):
    """阶段性目标"""
    id: int
    description: str
    status: ObjectiveStatus = ObjectiveStatus.NOT_STARTED
    completion_criteria: str
    progress_hints: List[str] = []


class GameContext(BaseModel):
    """游戏上下文 - 存储在内存中，依赖LLM上下文"""
    scenario_name: str
    scenario_description: str
    user_character: str
    ai_character: str
    ai_character_backstory: str = ""
    current_stage: int = 1

    # 三阶段目标
    user_objectives: List[StageObjective] = []
    ai_objectives: List[StageObjective] = []

    # 当前对话轮次
    conversation_round: int = 0

    # 最近的对话历史（用于上下文）
    recent_messages: List[Dict] = []

    # 开场白
    opening_scene: str = ""


class DialogueResponse(BaseModel):
    """结构化的对话响应"""
    ai_reply: str  # AI角色的直接回复
    narration: str  # 旁白描述（情景、动作、神情等）
    internal_thoughts: str  # AI角色内心独白
    objective_progress: Dict  # 目标进展情况
    system_message: Optional[str] = None  # 系统提示消息
    stage_change: Optional[Dict] = None  # 阶段变化信息
    current_stage: int = 1  # 当前阶段
    user_current_objective: str = ""  # 用户当前目标
    ai_current_objective: str = ""  # AI当前目标
