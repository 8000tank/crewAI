"""
LLM配置模块 - 配置支持NSFW的模型
"""
import os
from crewai import LLM


def get_nsfw_compatible_llm() -> LLM:
    """获取支持NSFW内容的LLM模型"""
    google_api_key = os.getenv('GOOGLE_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if google_api_key:
        # 使用Gemini模型 - 支持NSFW内容
        print("✅ 使用 Gemini 2.0 Flash 模型 (支持NSFW)")
        return LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=google_api_key
        )
    elif openai_api_key:
        # OpenAI模型有NSFW限制，但仍可作为备用
        print("⚠️ 使用 OpenAI 模型 (可能有NSFW限制)")
        return LLM(
            model="gpt-4o-mini",
            api_key=openai_api_key
        )
    else:
        # 默认尝试使用系统环境中的模型
        print("🔄 使用默认模型配置")
        return LLM(model="gpt-4o-mini")


def configure_agents_with_nsfw_llm():
    """为Agent配置支持NSFW的LLM"""
    return get_nsfw_compatible_llm()
