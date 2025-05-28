#!/usr/bin/env python
"""
角色扮演系统主入口文件
"""

import sys
import warnings
from .cli import main as cli_main

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    运行角色扮演系统
    """
    cli_main()


def main():
    """
    主函数
    """
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command in ['--help', '-h', 'help']:
            print("角色扮演聊天系统")
            print("使用方法: python -m testroleplay.main")
            print("或直接运行: python main.py")
            return

    run()


if __name__ == "__main__":
    main()
