# 角色扮演系统使用指南

## 快速开始

### 1. 环境准备

确保你已经安装了必要的依赖：

```bash
cd testroleplay
pip install -r requirements.txt
```

### 2. 设置API密钥

你需要设置OpenAI或Google的API密钥：

```bash
# 方式1: 使用 OpenAI
export OPENAI_API_KEY="sk-your-openai-api-key"

# 方式2: 使用 Google Gemini
export GOOGLE_API_KEY="your-google-api-key"

# 方式3: 创建 .env 文件
echo "OPENAI_API_KEY=sk-your-openai-api-key" > .env
```

### 3. 运行系统

```bash
# 快速演示
python simple_demo.py

# 完整游戏体验
python roleplay_demo.py

# 或使用模块方式
python -m testroleplay.main
```

## 系统功能详解

### 1. 多Agent协作

系统由三个专业化的AI Agent组成：

#### 编剧Agent
- **职责**: 创建剧情设定和目标体系
- **能力**: 生成角色背景、对抗性目标、开场场景
- **输出**: 完整的剧情JSON数据

#### 对话Agent  
- **职责**: 扮演AI角色，生成对话
- **能力**: 角色一致性、情绪表达、剧情推进
- **输出**: 结构化对话响应（回复+旁白+内心独白）

#### 裁判Agent
- **职责**: 判断目标完成情况，控制游戏进度
- **能力**: 客观评估、阶段转换、系统提示
- **输出**: 进度评估和状态更新

### 2. 对抗目标体系

#### 设计原则
- **对抗关系**: 用户和AI的目标相互冲突
- **阶段性**: 三个递进的目标阶段
- **依赖顺序**: AI必须先完成目标，用户才能完成

#### 示例：办公室剧情
```
用户目标1: 获得秘书信任 ←→ AI目标1: 获得升职机会
用户目标2: 突破职业界限 ←→ AI目标2: 保持职业边界
用户目标3: 发展个人关系 ←→ AI目标3: 确保职业发展
```

### 3. 游戏流程

```
1. 选择剧情类型
   ↓
2. AI生成剧情设定
   ↓
3. 展示角色和目标
   ↓
4. 开始对话循环
   ↓
5. 实时判断目标进度
   ↓
6. 阶段转换和结束
```

## 命令参考

### 游戏内命令

- `/status` - 查看游戏状态
- `/help` - 显示帮助
- `/restart` - 重新开始
- `/quit` - 退出游戏

### 开发者命令

```bash
# 测试系统
python test_system.py

# 查看详细日志（设置环境变量）
export CREWAI_VERBOSE=true
python roleplay_demo.py
```

## 自定义配置

### 1. 添加新剧情类型

在 `src/testroleplay/agents.py` 的 `create_scenario_init_task` 函数中添加：

```python
# 在选择逻辑中添加新类型
if scenario_type == "你的新剧情类型":
    # 定义具体的剧情要求
```

### 2. 调整Agent行为

修改Agent的prompt来调整行为：

```python
# 在 agents.py 中修改 Agent 的 backstory
backstory = """
你的自定义角色描述...
具体的行为要求...
"""
```

### 3. 修改目标判断逻辑

在 `create_judge_task` 中调整判断标准：

```python
# 修改判断规则
"严格执行：[你的自定义规则]"
```

## 故障排除

### 常见错误

#### 1. 导入错误
```bash
ModuleNotFoundError: No module named 'testroleplay'
```
**解决方案**: 确保在项目根目录运行，或使用正确的Python路径

#### 2. API密钥错误
```bash
openai.error.AuthenticationError
```
**解决方案**: 检查API密钥是否正确设置

#### 3. 网络连接超时
```bash
requests.exceptions.ConnectTimeout
```
**解决方案**: 检查网络连接，考虑使用代理

### 调试技巧

#### 1. 启用详细日志
```bash
export CREWAI_VERBOSE=true
python roleplay_demo.py
```

#### 2. 查看JSON输出
在controller.py中添加调试打印：
```python
print(f"调试: {result}")  # 在解析前打印原始结果
```

#### 3. 使用测试模式
```bash
python test_system.py  # 运行基础测试
```

## 高级功能

### 1. 批量测试

创建测试脚本来验证不同剧情：

```python
scenarios = ["办公室", "学校", "医院"]
for scenario in scenarios:
    controller = RolePlayController()
    game_context = controller.initialize_scenario(scenario)
    # 测试逻辑
```

### 2. 数据分析

分析对话质量和目标完成率：

```python
def analyze_conversation(game_context):
    # 分析对话轮次
    # 计算目标完成时间
    # 评估对话质量
```

### 3. 扩展集成

将系统集成到其他应用：

```python
from testroleplay.controller import RolePlayController

# 在你的应用中使用
controller = RolePlayController()
response = controller.process_user_message(user_input)
# 处理response数据
```

## 最佳实践

### 1. 提示词优化
- 使用具体的角色描述
- 明确目标和约束条件
- 提供充足的上下文

### 2. 错误处理
- 使用try-catch捕获异常
- 提供友好的错误信息
- 实现降级处理机制

### 3. 性能优化
- 控制对话历史长度
- 合理设置Agent参数
- 监控API调用频率

## 贡献指南

欢迎提交改进建议！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 支持

遇到问题请查看：
- 项目README.md
- 这个使用指南
- 提交Issue报告bug