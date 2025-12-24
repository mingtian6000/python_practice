# ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import pygame
from PIL import Image, ImageTk
import random
import threading
import time
from datetime import datetime
import os

class MathGameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.is_celebrating = False
        
        # 初始化Pygame音效
        pygame.mixer.init()
        
        # 加载音效
        self.sounds = self.load_sounds()
        
        # 设置窗口
        self.root.title("🌟 小朋友的数学乐园 🌟")
        self.root.geometry("900x700")
        self.root.configure(bg='#FFE4E1')  # 浅粉色背景
        
        # 加载图片
        self.images = self.load_images()
        
        # 设置彩虹色
        self.colors = ['#FF6B6B', '#FFD166', '#06D6A0', '#118AB2', '#073B4C', 
                      '#EF476F', '#FFD166', '#06D6A0', '#118AB2', '#073B4C']
        
        # 创建界面
        self.setup_ui()
        
        # 开始新游戏
        self.start_new_game()
    
    def load_sounds(self):
        """加载音效"""
        sounds = {}
        sound_files = {
            'correct': 'sounds/correct.wav',
            'wrong': 'sounds/wrong.wav',
            'celebration': 'sounds/celebration.wav',
            'click': 'sounds/click.wav',
            'background': 'sounds/background.mp3'
        }
        
        # 如果音效文件不存在，创建默认的
        for name, filepath in sound_files.items():
            if not os.path.exists(filepath):
                # 这里可以添加创建默认音效的代码
                pass
        
        return sounds
    
    def load_images(self):
        """加载图片资源"""
        images = {}
        
        # 尝试加载卡通图片
        try:
            # 这里可以添加加载本地图片的代码
            # 或者使用简单的图形
            pass
        except:
            # 如果图片不存在，使用颜色方块代替
            pass
        
        return images
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#FFE4E1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg='#FFE4E1')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame, 
            text="🎯 小朋友的数学乐园 🎯", 
            font=('Comic Sans MS', 28, 'bold'),
            fg='#FF6B6B',
            bg='#FFE4E1'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="每天25道题，成为数学小天才！",
            font=('Comic Sans MS', 16),
            fg='#118AB2',
            bg='#FFE4E1'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # 进度和分数区域
        info_frame = tk.Frame(main_frame, bg='#FFE4E1')
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            info_frame, 
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate',
            style="red.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 20))
        
        # 分数显示
        self.score_label = tk.Label(
            info_frame,
            text="分数: 0/25",
            font=('Comic Sans MS', 18, 'bold'),
            fg='#06D6A0',
            bg='#FFE4E1'
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        # 题目显示区域
        self.question_frame = tk.Frame(main_frame, bg='#FFFFFF', relief=tk.RAISED, borderwidth=3)
        self.question_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=('Comic Sans MS', 48, 'bold'),
            fg='#073B4C',
            bg='#FFFFFF',
            wraplength=800
        )
        self.question_label.pack(expand=True)
        
        # 答案输入区域
        input_frame = tk.Frame(main_frame, bg='#FFE4E1')
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            input_frame,
            text="请输入答案:",
            font=('Comic Sans MS', 18),
            fg='#118AB2',
            bg='#FFE4E1'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(
            input_frame,
            textvariable=self.answer_var,
            font=('Comic Sans MS', 24),
            width=10,
            justify='center',
            bd=3,
            relief=tk.SUNKEN
        )
        self.answer_entry.pack(side=tk.LEFT, padx=(0, 20))
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        # 提交按钮
        submit_button = tk.Button(
            input_frame,
            text="✅ 提交答案",
            font=('Comic Sans MS', 18, 'bold'),
            bg='#06D6A0',
            fg='white',
            activebackground='#04B486',
            activeforeground='white',
            padx=30,
            pady=10,
            command=self.check_answer,
            cursor='hand2'
        )
        submit_button.pack(side=tk.LEFT)
        
        # 数字键盘
        self.create_number_pad(main_frame)
        
        # 控制按钮区域
        control_frame = tk.Frame(main_frame, bg='#FFE4E1')
        control_frame.pack(fill=tk.X)
        
        # 新游戏按钮
        new_game_button = tk.Button(
            control_frame,
            text="🔄 新游戏",
            font=('Comic Sans MS', 16),
            bg='#118AB2',
            fg='white',
            padx=20,
            pady=10,
            command=self.start_new_game,
            cursor='hand2'
        )
        new_game_button.pack(side=tk.LEFT, padx=5)
        
        # 查看进度按钮
        progress_button = tk.Button(
            control_frame,
            text="📊 查看进度",
            font=('Comic Sans MS', 16),
            bg='#FFD166',
            fg='black',
            padx=20,
            pady=10,
            command=self.show_progress,
            cursor='hand2'
        )
        progress_button.pack(side=tk.LEFT, padx=5)
        
        # 退出按钮
        exit_button = tk.Button(
            control_frame,
            text="🚪 退出",
            font=('Comic Sans MS', 16),
            bg='#FF6B6B',
            fg='white',
            padx=20,
            pady=10,
            command=self.root.quit,
            cursor='hand2'
        )
        exit_button.pack(side=tk.LEFT, padx=5)
        
        # 底部信息
        bottom_frame = tk.Frame(main_frame, bg='#FFE4E1')
        bottom_frame.pack(fill=tk.X, pady=(20, 0))
        
        today = datetime.now().strftime("%Y年%m月%d日")
        date_label = tk.Label(
            bottom_frame,
            text=f"📅 今天日期: {today}",
            font=('Comic Sans MS', 12),
            fg='#666666',
            bg='#FFE4E1'
        )
        date_label.pack(side=tk.LEFT)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("red.Horizontal.TProgressbar", 
                       background='#06D6A0',
                       troughcolor='#FFE4E1')
    
    def create_number_pad(self, parent):
        """创建数字键盘"""
        pad_frame = tk.Frame(parent, bg='#FFE4E1')
        pad_frame.pack(fill=tk.X, pady=(0, 20))
        
        numbers = [
            ['7', '8', '9', '←'],
            ['4', '5', '6', 'C'],
            ['1', '2', '3', '✔'],
            ['0', '00', '.', '✕']
        ]
        
        for i, row in enumerate(numbers):
            row_frame = tk.Frame(pad_frame, bg='#FFE4E1')
            row_frame.pack()
            for j, num in enumerate(row):
                color = '#118AB2' if num in ['←', 'C', '✔', '✕'] else '#FF6B6B'
                btn = tk.Button(
                    row_frame,
                    text=num,
                    font=('Comic Sans MS', 20, 'bold'),
                    width=6,
                    height=2,
                    bg=color,
                    fg='white',
                    activebackground='#FFD166',
                    activeforeground='black',
                    command=lambda n=num: self.on_number_pad_click(n),
                    cursor='hand2',
                    relief=tk.RAISED,
                    bd=3
                )
                btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def on_number_pad_click(self, value):
        """数字键盘点击事件"""
        current = self.answer_var.get()
        
        if value == '←':
            # 退格
            self.answer_var.set(current[:-1])
        elif value == 'C':
            # 清空
            self.answer_var.set('')
        elif value == '✔':
            # 提交
            self.check_answer()
        elif value == '✕':
            # 关闭键盘
            pass
        else:
            # 添加数字
            self.answer_var.set(current + value)
    
    def start_new_game(self):
        """开始新游戏"""
        self.game.start_daily_challenge()
        self.answer_var.set('')
        self.update_question()
        self.update_score()
        self.answer_entry.focus()
    
    def update_question(self):
        """更新题目显示"""
        question = self.game.get_current_question()
        if question:
            self.question_label.config(text=f"第 {self.game.current_question + 1} 题: {question}")
            
            # 更新进度条
            progress = (self.game.current_question / self.game.total_questions) * 100
            self.progress_var.set(progress)
            
            # 随机改变题目颜色
            color = random.choice(self.colors)
            self.question_label.config(fg=color)
    
    def update_score(self):
        """更新分数显示"""
        self.score_label.config(text=f"分数: {self.game.score}/{self.game.total_questions}")
    
    def check_answer(self):
        """检查答案"""
        answer = self.answer_var.get().strip()
        if not answer:
            messagebox.showinfo("提示", "请输入答案哦！")
            return
        
        is_correct, completed, next_question = self.game.submit_answer(answer)
        
        # 播放音效
        if is_correct:
            self.show_correct_feedback()
        else:
            self.show_wrong_feedback()
        
        # 更新分数
        self.update_score()
        
        if completed:
            # 游戏结束
            self.show_final_results()
        else:
            # 继续下一题
            self.answer_var.set('')
            self.update_question()
            self.answer_entry.focus()
    
    def show_correct_feedback(self):
        """显示正确反馈"""
        # 改变背景色
        self.question_frame.config(bg='#D4EDDA')
        self.question_label.config(bg='#D4EDDA')
        
        # 显示正确提示
        self.show_popup_message("✅ 太棒了！答对了！", "#D4EDDA")
        
        # 恢复背景色
        self.root.after(500, self.reset_question_frame)
    
    def show_wrong_feedback(self):
        """显示错误反馈"""
        # 改变背景色
        self.question_frame.config(bg='#F8D7DA')
        self.question_label.config(bg='#F8D7DA')
        
        # 显示错误提示
        self.show_popup_message("❌ 再试试看！", "#F8D7DA")
        
        # 恢复背景色
        self.root.after(500, self.reset_question_frame)
    
    def reset_question_frame(self):
        """恢复题目框背景色"""
        self.question_frame.config(bg='#FFFFFF')
        self.question_label.config(bg='#FFFFFF')
    
    def show_popup_message(self, message, color):
        """显示弹出消息"""
        popup = tk.Toplevel(self.root)
        popup.wm_overrideredirect(True)
        popup.wm_attributes("-topmost", True)
        
        # 获取主窗口位置
        x = self.root.winfo_rootx() + 100
        y = self.root.winfo_rooty() + 200
        
        popup.geometry(f"+{x}+{y}")
        
        label = tk.Label(
            popup,
            text=message,
            font=('Comic Sans MS', 24, 'bold'),
            fg='white',
            bg=color,
            padx=20,
            pady=10
        )
        label.pack()
        
        # 1秒后自动关闭
        popup.after(1000, popup.destroy)
    
    def show_final_results(self):
        """显示最终结果"""
        score = self.game.score
        total = self.game.total_questions
        percentage = (score / total) * 100
        
        if percentage == 100:
            # 全对，触发庆祝效果
            self.celebrate_victory()
            message = f"🎉 太厉害了！全对！🎉\n\n你获得了 {score}/{total} 分！\n真是个数学小天才！"
        elif percentage >= 80:
            message = f"👍 很棒！\n\n你获得了 {score}/{total} 分！\n继续加油哦！"
        elif percentage >= 60:
            message = f"😊 不错！\n\n你获得了 {score}/{total} 分！\n再来一次会更好！"
        else:
            message = f"💪 继续努力！\n\n你获得了 {score}/{total} 分！\n每天进步一点点！"
        
        result = messagebox.showinfo("游戏结束", message)
        
        if result == 'ok':
            self.start_new_game()
    
    def celebrate_victory(self):
        """庆祝胜利"""
        if self.is_celebrating:
            return
        
        self.is_celebrating = True
        
        # 创建庆祝窗口
        celebrate_window = tk.Toplevel(self.root)
        celebrate_window.title("🎉 恭喜全对！ 🎉")
        celebrate_window.geometry("600x400")
        celebrate_window.configure(bg='#FFD700')
        celebrate_window.wm_attributes("-topmost", True)
        
        # 居中显示
        x = self.root.winfo_rootx() + 150
        y = self.root.winfo_rooty() + 150
        celebrate_window.geometry(f"+{x}+{y}")
        
        # 庆祝内容
        tk.Label(
            celebrate_window,
            text="🎉 太棒了！全对！ 🎉",
            font=('Comic Sans MS', 32, 'bold'),
            fg='#FF6B6B',
            bg='#FFD700'
        ).pack(pady=20)
        
        tk.Label(
            celebrate_window,
            text="🎁 你获得了神秘奖励！ 🎁",
            font=('Comic Sans MS', 24),
            fg='#118AB2',
            bg='#FFD700'
        ).pack(pady=10)
        
        # 显示星星
        stars_frame = tk.Frame(celebrate_window, bg='#FFD700')
        stars_frame.pack(pady=20)
        
        for _ in range(5):
            tk.Label(
                stars_frame,
                text="⭐",
                font=('Comic Sans MS', 36),
                fg='#FF6B6B',
                bg='#FFD700'
            ).pack(side=tk.LEFT, padx=10)
        
        # 关闭按钮
        tk.Button(
            celebrate_window,
            text="继续挑战！",
            font=('Comic Sans MS', 20, 'bold'),
            bg='#06D6A0',
            fg='white',
            padx=30,
            pady=10,
            command=celebrate_window.destroy
        ).pack(pady=20)
        
        # 播放庆祝动画
        self.animate_confetti(celebrate_window)
        
        # 5秒后自动关闭
        celebrate_window.after(5000, celebrate_window.destroy)
        
        # 庆祝结束
        celebrate_window.wait_window()
        self.is_celebrating = False
    
    def animate_confetti(self, window):
        """彩色纸屑动画"""
        colors = ['#FF6B6B', '#FFD166', '#06D6A0', '#118AB2', '#EF476F']
        
        for _ in range(50):
            x = random.randint(0, 600)
            y = random.randint(0, 400)
            color = random.choice(colors)
            
            label = tk.Label(
                window,
                text="✨",
                font=('Comic Sans MS', random.randint(20, 30)),
                fg=color,
                bg='#FFD700'
            )
            label.place(x=x, y=y)
            
            # 动画移动
            self.move_confetti(label, window)
    
    def move_confetti(self, label, window):
        """移动纸屑"""
        if window.winfo_exists():
            x = label.winfo_x() + random.randint(-5, 5)
            y = label.winfo_y() + random.randint(2, 8)
            
            if y > 400:
                y = 0
                x = random.randint(0, 600)
            
            label.place(x=x, y=y)
            window.after(50, lambda: self.move_confetti(label, window))
    
    def show_progress(self):
        """显示学习进度"""
        progress_data = self.game.get_progress_report()
        
        if not progress_data:
            messagebox.showinfo("学习进度", "还没有学习记录哦，开始第一天的挑战吧！")
            return
        
        # 创建进度窗口
        progress_window = tk.Toplevel(self.root)
        progress_window.title("📊 学习进度报告")
        progress_window.geometry("800x600")
        
        # 添加滚动条
        canvas = tk.Canvas(progress_window, bg='white')
        scrollbar = tk.Scrollbar(progress_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 显示标题
        tk.Label(
            scrollable_frame,
            text="📈 学习进度报告",
            font=('Comic Sans MS', 24, 'bold'),
            fg='#118AB2',
            bg='white'
        ).pack(pady=20)
        
        # 显示每次学习记录
        for i, session in enumerate(reversed(progress_data[-10:]), 1):  # 显示最近10次
            date = session.get("date", "未知日期")
            time = session.get("time", "未知时间")
            score = session.get("score", 0)
            total = session.get("total", 25)
            percentage = session.get("percentage", 0)
            
            frame = tk.Frame(
                scrollable_frame,
                bg='#F0F8FF',
                relief=tk.RAISED,
                borderwidth=2
            )
            frame.pack(fill=tk.X, padx=20, pady=5, ipadx=10, ipady=10)
            
            # 序号
            tk.Label(
                frame,
                text=f"第{i}次",
                font=('Comic Sans MS', 16, 'bold'),
                fg='#FF6B6B',
                bg='#F0F8FF'
            ).pack(side=tk.LEFT, padx=20)
            
            # 日期时间
            tk.Label(
                frame,
                text=f"{date} {time}",
                font=('Comic Sans MS', 14),
                fg='#666666',
                bg='#F0F8FF'
            ).pack(side=tk.LEFT, padx=20)
            
            # 分数
            tk.Label(
                frame,
                text=f"分数: {score}/{total}",
                font=('Comic Sans MS', 16, 'bold'),
                fg='#06D6A0',
                bg='#F0F8FF'
            ).pack(side=tk.LEFT, padx=20)
            
            # 百分比
            tk.Label(
                frame,
                text=f"正确率: {percentage:.1f}%",
                font=('Comic Sans MS', 16),
                fg='#118AB2',
                bg='#F0F8FF'
            ).pack(side=tk.LEFT, padx=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 显示今天的分数
        today_score, today_total = self.game.get_today_score()
        if today_score > 0:
            tk.Label(
                progress_window,
                text=f"今日分数: {today_score}/{today_total}",
                font=('Comic Sans MS', 18, 'bold'),
                fg='#FF6B6B',
                bg='white'
            ).pack(pady=10)