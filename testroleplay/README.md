# 角色扮演聊天系统

基于 CrewAI 框架的多Agent角色扮演聊天系统。支持复杂的剧情设定、对抗性目标体系和沉浸式对话体验。

## 功能特点

- 🎭 **多Agent协作**: 编剧、对话、裁判三个AI Agent分工协作
- 🎯 **对抗目标体系**: 三阶段对抗性目标，营造剧情张力
- 💬 **沉浸式对话**: 结构化对话响应，包含旁白和内心独白
- 🎬 **多样剧情**: 支持多种剧情类型和自定义场景
- 🔄 **状态管理**: 实时追踪游戏进度和目标完成情况

## 安装和运行

### 1. 环境要求

- Python >= 3.10
- OpenAI API Key 或 Google AI API Key

### 2. 安装依赖

```bash
# 克隆项目
cd testroleplay

# 安装依赖
pip install -r requirements.txt
# 或使用 crewai 命令
crewai install
```

### 3. 配置API密钥

设置环境变量：

```bash
# 使用 OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# 或使用 Google Gemini
export GOOGLE_API_KEY="your-google-api-key"
```

### 4. 运行系统

```bash
# 方式1: 直接运行演示脚本
python roleplay_demo.py

# 方式2: 使用模块方式
python -m testroleplay.main

# 方式3: 使用 crewai 命令
crewai run
```

## 使用指南

### 游戏流程

1. **选择剧情**: 从预设剧情中选择或自定义剧情类型
2. **查看设定**: 了解角色背景和三阶段目标体系
3. **开始对话**: 与AI角色进行沉浸式对话
4. **完成目标**: 逐步实现阶段性目标，推进剧情发展

### 命令说明

游戏中可使用以下命令：

- `/status` - 查看当前游戏状态和目标进度
- `/help` - 显示帮助信息
- `/restart` - 重新开始游戏
- `/quit` - 退出游戏

### 目标机制

- **对抗关系**: 用户和AI的目标相互对抗，营造剧情冲突
- **完成顺序**: AI必须先完成阶段目标，用户才能完成同阶段目标
- **三个阶段**: 每个剧情包含三个递进的阶段目标
- **智能判断**: 由裁判Agent判断目标完成情况

## 系统架构

```
角色扮演系统
├── 数据模型 (models.py)
│   ├── GameContext - 游戏上下文
│   ├── DialogueResponse - 对话响应
│   └── StageObjective - 阶段目标
├── Agent定义 (agents.py)
│   ├── 编剧Agent - 剧情和目标设计
│   ├── 对话Agent - AI角色扮演
│   └── 裁判Agent - 目标判断和进度控制
├── 主控制器 (controller.py)
│   └── RolePlayController - 游戏流程控制
└── 用户界面 (cli.py)
    └── 命令行交互界面
```

## 示例剧情

系统预设了多种剧情类型：

- **办公室权力游戏**: 上司与秘书的职场博弈
- **高校师生关系**: 教授与学生的学术互动
- **医院情缘**: 医生与护士的专业合作
- **商业谈判**: 总裁与助理的商务往来

## 自定义和扩展

### 添加新剧情

1. 在 `agents.py` 中的 `create_scenario_init_task` 函数中添加新的剧情类型
2. 确保剧情包含对抗性的三阶段目标设计

### 调整Agent行为

1. 修改 `agents.py` 中的Agent定义和prompt
2. 调整对话生成和目标判断的逻辑

### 扩展功能

- 添加持久化存储（目前为MVP版本，使用内存存储）
- 集成更多LLM模型
- 添加图形用户界面
- 支持多人游戏模式

## 技术特点

- **轻量级设计**: MVP版本专注核心功能，无外部依赖
- **CrewAI框架**: 充分利用多Agent协作能力
- **结构化输出**: 清晰的数据格式，便于扩展
- **错误处理**: 完善的异常处理和降级机制

## 故障排除

### 常见问题

1. **API密钥错误**: 确保正确设置环境变量
2. **网络连接问题**: 检查网络连接和API服务状态
3. **依赖安装失败**: 尝试使用 `pip install --upgrade` 更新包

### 调试模式

设置 `verbose=True` 可查看详细的Agent执行日志。

## 贡献

欢迎提交Issues和Pull Requests来改进系统功能。

## 许可证

本项目基于 MIT 许可证开源。