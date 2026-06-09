from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk, font

from vocabulary_quiz_app.quiz_logic import Word, check_answer, draw_word


class VocabularyQuizApp:
    def __init__(self, root: tk.Tk, words: list[Word]) -> None:
        # 프로그램 초기 상태와 UI 변수 설정
        self.root = root
        self.words = words
        self.rng = random.Random()

        self.current: Word | None = None
        self.checked = True
        self.score = 0
        self.total = 0
        self.game_over = False

        self.max_questions = 5
        self.time_limit = 10
        self.time_left = self.time_limit
        self.timer_id = None

        root.title("Vocabulary Quiz")
        root.geometry("500x340")

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="NanumGothic", size=12)

        self.word_var = tk.StringVar(value="")
        self.feedback_var = tk.StringVar(value="")
        self.score_var = tk.StringVar(value="Score: 0/0")
        self.timer_var = tk.StringVar(value="")
        self.q_var = tk.StringVar(value="")

        self.show_start_screen()

    def show_start_screen(self):
        # 시작 화면에서 문제 개수 선택 버튼 표시
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="문제 수 선택", font=("NanumGothic", 16)).pack(pady=30)
        ttk.Button(self.root, text="5문제 시작", command=lambda: self.start_game(5)).pack(pady=10)
        ttk.Button(self.root, text="10문제 시작", command=lambda: self.start_game(10)).pack(pady=10)

    def start_game(self, n):
        # 새로운 게임을 시작하고 상태 초기화
        self.max_questions = n
        self.score = 0
        self.total = 0
        self.checked = True
        self.game_over = False

        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, textvariable=self.q_var).pack()
        ttk.Label(self.root, text="영단어").pack(pady=(5, 4))
        ttk.Label(self.root, textvariable=self.word_var, font=("NanumGothic", 24)).pack()

        self.answer_entry = ttk.Entry(self.root, font=("NanumGothic", 14))
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind("<Return>", self.enter_action)

        buttons = ttk.Frame(self.root)
        buttons.pack()

        self.check_button = ttk.Button(buttons, text="채점", command=self.check_current)
        self.check_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(buttons, text="다음", command=self.next_word)
        self.next_button.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.root, textvariable=self.timer_var).pack(pady=5)
        ttk.Label(self.root, textvariable=self.feedback_var).pack()
        ttk.Label(self.root, textvariable=self.score_var).pack()

        self.next_word()

    def next_word(self):
        # 다음 문제를 불러오고 타이머 및 UI를 초기화
        if self.game_over:
            return

        if not self.checked:
            self.total += 1

        if self.total >= self.max_questions:
            self.end_game()
            return

        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.current = draw_word(self.words, self.rng)

        self.word_var.set(self.current.term)
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")

        self.q_var.set(f"Question: {self.total + 1} / {self.max_questions}")
        self.score_var.set(f"Score: {self.score} / {self.max_questions}")

        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()

        self.start_timer()

    def check_current(self):
        # 입력된 답을 채점하고 점수와 진행 상태를 업데이트
        if self.game_over:
            return

        if self.current is None or self.checked:
            return

        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.checked = True
        self.total += 1

        user_input = self.answer_entry.get()

        if check_answer(self.current, user_input):
            self.score += 1
            self.feedback_var.set("정답입니다!")
        else:
            self.feedback_var.set(f"오답입니다. 정답: {self.current.meaning}")

        self.score_var.set(f"Score: {self.score} / {self.max_questions}")
        self.check_button.state(["disabled"])

        if self.total >= self.max_questions:
            self.end_game()

    def start_timer(self):
        # 제한 시간 타이머를 시작
        self.time_left = self.time_limit
        self.update_timer()

    def update_timer(self):
        # 남은 시간을 감소시키고 시간 초과 시 자동 오답 처리
        self.timer_var.set(f"Time: {self.time_left}")

        if self.time_left <= 0:
            self.feedback_var.set(f"시간 초과! 오답입니다. 정답: {self.current.meaning}")

            self.total += 1
            self.score_var.set(f"Score: {self.score} / {self.max_questions}")

            self.checked = True
            self.check_button.state(["disabled"])
            return

        self.time_left -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def end_game(self):
        # 게임을 종료하고 결과와 재도전 버튼을 표시
        self.game_over = True

        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.feedback_var.set(f"게임 종료!\n최종 점수: {self.score}")

        self.check_button.state(["disabled"])
        self.next_button.state(["disabled"])

        ttk.Button(self.root, text="재도전", command=self.retry_game).pack(pady=15)

    def retry_game(self):
        # 상태를 초기화하고 시작 화면으로 돌아감
        self.score = 0
        self.total = 0
        self.timer_id = None
        self.show_start_screen()

    def enter_action(self, event):
        # Enter 키 입력 시 채점 또는 다음 문제로 진행
        if self.game_over:
            return

        if not self.checked:
            self.check_current()
        else:
            self.next_word()
