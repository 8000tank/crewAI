#!/usr/bin/env python
"""
角色扮演系统演示脚本
直接运行此文件即可开始游戏
"""

import os
import sys

# 添加src路径到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))  # noqa: E402

from testroleplay.cli import main

if __name__ == "__main__":
    main()
