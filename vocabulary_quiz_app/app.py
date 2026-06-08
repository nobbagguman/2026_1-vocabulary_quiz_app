from __future__ import annotations

import random
import tkinter as tk

from tkinter import ttk, font

from vocabulary_quiz_app.quiz_logic import Word, check_answer, draw_word


class VocabularyQuizApp:
    def __init__(self, root: tk.Tk, words: list[Word]) -> None:
        #프로그램 초기 설정 및 필요한 변수(점수, 오답, 난이도 등) 초기화
        self.words = words
        self.rng = random.Random()
        self.current: Word | None = None
        self.checked = False
        self.score = 0
        self.total = 0
        self.wrong_words = []
        self.difficulty = "easy"


        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="NanumGothic", size=12)

        root.title("Vocabulary Quiz")
        root.geometry("600x350") # 창 사이즈를 늘림
        root.resizable(True, True) # 창 크기 조절 허용

        self.word_var = tk.StringVar(value="단어를 불러오는 중...")
        self.feedback_var = tk.StringVar(value="")
        self.score_var = tk.StringVar(value="Score: 0/0")

        ttk.Label(root, text="영단어").pack(pady=(16, 4))
        ttk.Label(root, textvariable=self.word_var, font=("NanumGothic", 24)).pack()

        self.answer_entry = ttk.Entry(root, font=("NanumGothic", 14))
        self.answer_entry.pack(pady=12, ipadx=6, ipady=4)

        buttons = ttk.Frame(root)
        buttons.pack(pady=6)

        self.check_button = ttk.Button(buttons, text="채점", command=self.check_current)
        self.check_button.pack(side=tk.LEFT, padx=6)

        self.next_button = ttk.Button(buttons, text="다음", command=self.next_word)
        self.next_button.pack(side=tk.LEFT, padx=6)

        ttk.Button(buttons, text="오답 보기", command=self.show_wrong_words).pack(
            side=tk.LEFT, padx=6
        )

        ttk.Button(buttons, text="Easy", command=lambda: self.set_difficulty("easy")).pack(
            side=tk.LEFT, padx=3
        )
        ttk.Button(buttons, text="Hard", command=lambda: self.set_difficulty("hard")).pack(
            side=tk.LEFT, padx=3
        )

        ttk.Label(root, textvariable=self.feedback_var).pack(pady=8)
        ttk.Label(root, textvariable=self.score_var).pack()

        self.next_word()

    def next_word(self) -> None:
        #난이도에 따라 단어 리스트를 필터링하여 새로운 문제를 가져오는 기능
        if self.difficulty == "easy":
            filtered = [w for w in self.words if len(w.term) <= 5]
        else:
            filtered = [w for w in self.words if len(w.term) > 5]

        if not filtered:
            filtered = self.words

        self.current = draw_word(filtered, self.rng)

        self.word_var.set(self.current.term)
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()

    def check_current(self) -> None:
        #사용자의 입력을 채점하고 점수 및 오답 리스트를 업데이트하는 기능
        if self.current is None or self.checked:
            return
        self.checked = True
        self.total += 1
        user_input = self.answer_entry.get()
        if check_answer(self.current, user_input):
            self.score += 1
            self.feedback_var.set("정답입니다!")
        else:
            self.feedback_var.set(f"오답입니다. 정답: {self.current.meaning}")
            self.wrong_words.append(self.current)
        self.score_var.set(f"Score: {self.score}/{self.total}")
        self.check_button.state(["disabled"])

    def show_wrong_words(self):
        #저장된 오답 단어들을 화면에 출력하는 기능
        if not self.wrong_words:    
            self.feedback_var.set("오답이 없습니다!")
            return

        text = "오답 목록\n"
        for w in self.wrong_words:
            text += f"{w.term} - {w.meaning}\n"

        self.feedback_var.set(text)
    
    def set_difficulty(self, level):
        #사용자가 선택한 난이도를 설정하고 상태를 표시하는 기능
        self.difficulty = level
        self.feedback_var.set(f"{level} 모드 선택됨")


