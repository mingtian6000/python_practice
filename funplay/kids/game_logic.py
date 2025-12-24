# game_logic.py
import random
import json
from datetime import datetime
from pathlib import Path
import pygame
import sys
import os

class MathGame:
    def __init__(self):
        self.difficulty = 1
        self.score = 0
        self.current_question = 0
        self.total_questions = 25
        self.questions = []
        self.answers = []
        self.user_answers = []
        self.start_time = None
        self.data_file = "data/progress.json"
        
        # 确保目录存在
        Path("data").mkdir(exist_ok=True)
        Path("sounds").mkdir(exist_ok=True)
        Path("images").mkdir(exist_ok=True)
    
    def generate_question(self):
        """生成一道30以内的加减法题"""
        question_types = [
            self.generate_two_number_addition,
            self.generate_two_number_subtraction,
            self.generate_three_number_mixed,
            self.generate_with_parentheses,
            self.generate_fill_in_blank
        ]
        
        # 随机选择一种题型
        generator = random.choice(question_types)
        question, answer = generator()
        
        # 确保结果在30以内
        if isinstance(answer, (int, float)):
            if answer > 30 or answer < 0:
                return self.generate_question()  # 重新生成
        
        return question, answer
    
    def generate_two_number_addition(self):
        """生成两个数的加法题"""
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        while a + b > 30:
            a = random.randint(1, 15)
            b = random.randint(1, 15)
        return f"{a} + {b} = ?", a + b
    
    def generate_two_number_subtraction(self):
        """生成两个数的减法题"""
        a = random.randint(10, 30)
        b = random.randint(1, a)
        return f"{a} - {b} = ?", a - b
    
    def generate_three_number_mixed(self):
        """生成三个数的混合运算题"""
        ops = ['+', '-']
        a = random.randint(1, 15)
        b = random.randint(1, 15)
        c = random.randint(1, 15)
        op1 = random.choice(ops)
        op2 = random.choice(ops)
        
        # 计算答案
        if op1 == '+':
            temp = a + b
        else:
            temp = a - b
        
        if op2 == '+':
            result = temp + c
        else:
            result = temp - c
        
        # 确保结果在0-30之间
        if 0 <= result <= 30:
            return f"{a} {op1} {b} {op2} {c} = ?", result
        else:
            return self.generate_three_number_mixed()
    
    def generate_with_parentheses(self):
        """生成带括号的题目"""
        ops = ['+', '-']
        a = random.randint(1, 15)
        b = random.randint(1, 15)
        c = random.randint(1, 15)
        
        # 两种括号位置
        if random.random() > 0.5:
            # (a op b) op c
            op1 = random.choice(ops)
            op2 = random.choice(ops)
            if op1 == '+':
                temp = a + b
            else:
                temp = a - b
            
            if op2 == '+':
                result = temp + c
            else:
                result = temp - c
            
            if 0 <= result <= 30:
                return f"({a} {op1} {b}) {op2} {c} = ?", result
        else:
            # a op (b op c)
            op1 = random.choice(ops)
            op2 = random.choice(ops)
            if op2 == '+':
                temp = b + c
            else:
                temp = b - c
            
            if op1 == '+':
                result = a + temp
            else:
                result = a - temp
            
            if 0 <= result <= 30:
                return f"{a} {op1} ({b} {op2} {c}) = ?", result
        
        return self.generate_with_parentheses()
    
    def generate_fill_in_blank(self):
        """生成填空题"""
        types = [
            self.generate_fill_first,
            self.generate_fill_middle,
            self.generate_fill_last
        ]
        return random.choice(types)()
    
    def generate_fill_first(self):
        """_ + b = c 类型"""
        b = random.randint(1, 20)
        c = random.randint(b + 1, 30)
        a = c - b
        return f"_ + {b} = {c}", a
    
    def generate_fill_middle(self):
        """a + _ = c 类型"""
        a = random.randint(1, 20)
        c = random.randint(a + 1, 30)
        b = c - a
        return f"{a} + _ = {c}", b
    
    def generate_fill_last(self):
        """a + b = _ 类型"""
        a = random.randint(1, 15)
        b = random.randint(1, 15)
        c = a + b
        if c <= 30:
            return f"{a} + {b} = _", c
        return self.generate_fill_last()
    
    def start_daily_challenge(self):
        """开始每日挑战"""
        self.questions = []
        self.answers = []
        self.user_answers = []
        self.score = 0
        self.current_question = 0
        self.start_time = datetime.now()
        
        for _ in range(self.total_questions):
            question, answer = self.generate_question()
            self.questions.append(question)
            self.answers.append(answer)
        
        return self.get_current_question()
    
    def get_current_question(self):
        """获取当前题目"""
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None
    
    def submit_answer(self, answer):
        """提交答案"""
        if self.current_question < len(self.answers):
            correct = self.answers[self.current_question]
            is_correct = False
            
            # 处理可能的整数和字符串比较
            try:
                user_answer = int(answer)
                if user_answer == correct:
                    is_correct = True
                    self.score += 1
            except:
                pass
            
            self.user_answers.append({
                "question": self.questions[self.current_question],
                "user_answer": answer,
                "correct_answer": correct,
                "is_correct": is_correct
            })
            
            self.current_question += 1
            
            # 检查是否完成
            completed = self.current_question >= self.total_questions
            if completed:
                self.save_progress()
            
            return is_correct, completed, self.get_current_question()
        
        return False, True, None
    
    def save_progress(self):
        """保存学习进度"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = []
            
            end_time = datetime.now()
            time_taken = (end_time - self.start_time).total_seconds()
            
            session_data = {
                "date": self.start_time.strftime("%Y-%m-%d"),
                "time": self.start_time.strftime("%H:%M:%S"),
                "score": self.score,
                "total": self.total_questions,
                "percentage": (self.score / self.total_questions) * 100,
                "time_taken": time_taken,
                "answers": self.user_answers
            }
            
            data.append(session_data)
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"保存进度时出错: {e}")
    
    def get_progress_report(self):
        """获取进度报告"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                return data
        except:
            pass
        return []
    
    def get_today_score(self):
        """获取今天的分数"""
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                today_scores = [s for s in data if s.get("date") == today]
                if today_scores:
                    return today_scores[-1]["score"], today_scores[-1]["total"]
        except:
            pass
        return 0, 0