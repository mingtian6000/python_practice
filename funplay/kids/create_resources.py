# create_resources.py
import os
from pathlib import Path
import pygame
import json

def create_resource_files():
    """创建必要的资源文件"""
    
    # 创建目录
    Path("sounds").mkdir(exist_ok=True)
    Path("images").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    
    # 创建空的进度文件
    if not os.path.exists("data/progress.json"):
        with open("data/progress.json", 'w') as f:
            json.dump([], f, indent=2)
    
    print("✅ 资源文件创建完成！")

if __name__ == "__main__":
    create_resource_files()