# app.py
import tkinter as tk
from ui import MathGameUI
from game_logic import MathGame
import sys
import os

def main():
    # 创建主窗口
    root = tk.Tk()
    
    # 设置窗口图标
    try:
        root.iconbitmap('images/icon.ico')
    except:
        pass
    
    # 创建游戏实例
    game = MathGame()
    
    # 创建UI
    app = MathGameUI(root, game)
    
    # 运行应用
    root.mainloop()

if __name__ == "__main__":
    main()