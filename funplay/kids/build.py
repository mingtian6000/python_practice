# build_exe.py
import PyInstaller.__main__
import os
import shutil
from pathlib import Path

def build_executable():
    """使用 PyInstaller 打包应用"""
    
    # 确保有资源文件
    if not os.path.exists("sounds"):
        os.makedirs("sounds")
    if not os.path.exists("images"):
        os.makedirs("images")
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # 清理之前的构建
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # PyInstaller 配置
    args = [
        'app.py',
        '--name=小朋友的数学乐园',
        '--windowed',  # 不显示控制台窗口
        '--icon=images/icon.ico',  # 应用图标
        '--add-data=sounds;sounds',
        '--add-data=images;images',
        '--add-data=data;data',
        '--hidden-import=PIL',
        '--hidden-import=pygame',
        '--clean',  # 清理临时文件
        '--noconfirm',  # 覆盖输出目录而不确认
    ]
    
    # 执行打包
    PyInstaller.__main__.run(args)
    
    print("✅ 打包完成！")
    print("📁 可执行文件在 'dist' 目录中")

if __name__ == "__main__":
    build_executable()