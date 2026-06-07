from __future__ import annotations

import random
import tkinter as tk

from tkinter import ttk, font

from vocabulary_quiz_app.quiz_logic import Word, check_answer, draw_word


class VocabularyQuizApp:
    def __init__(self, root: tk.Tk, words: list[Word]) -> None:
        self.words = words
        self.rng = random.Random()
        self.current: Word | None = None
        self.checked = False
        self.score = 0
        self.total = 0
        self.fail_count = 0
        self.game_over = False  
        self.last_answer_correct = False
        self.first_load = True
        self.just_wrong = False



        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="NanumGothic", size=12)

        root.title("Vocabulary Quiz")
        root.geometry("420x280")
        root.resizable(False, False)

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
        ttk.Button(buttons, text="다음", command=self.next_word).pack(
            side=tk.LEFT, padx=6
        )

        ttk.Label(root, textvariable=self.feedback_var).pack(pady=8)
        ttk.Label(root, textvariable=self.score_var).pack()

        self.next_word()

    def next_word(self) -> None:
        if self.game_over:
            return

        # ✅ 첫 실행은 카운트 안 함
        if self.first_load:
            self.first_load = False
        else:
            # ✅ 채점 안 하고 next 눌렀을 경우
            if not self.checked:
                self.total += 1      # 문제 넘겼으니까 total 증가
                self.fail_count += 1 # 기회 감소

            # ✅ 오답 직후 next → 이미 fail_count 줄었으므로 건너뜀
            elif self.just_wrong:
                pass

            # ✅ 정답 후 next → 아무 변화 없음
            else:
                pass

        # ✅ 게임 종료 체크
        if self.fail_count >= 3:
            self.end_game()
            return

        # ✅ 다음 문제 로드
        self.current = draw_word(self.words, self.rng)
        self.word_var.set(self.current.term)
        self.answer_entry.delete(0, tk.END)

        # ✅ 상태 표시 업데이트
        self.update_status_text()

        # ✅ 점수 표시 업데이트 (중요🔥)
        self.score_var.set(f"Score: {self.score}/{self.total}")

        # ✅ 상태 초기화
        self.checked = False
        self.last_answer_correct = False
        self.just_wrong = False

        self.check_button.state(["!disabled"])
        self.answer_entry.focus()

    def check_current(self) -> None:
        if self.current is None or self.game_over:
            return

        if self.checked:
            return

        self.total += 1   # 🔥 최우선
        self.checked = True

        user_input = self.answer_entry.get()

        if check_answer(self.current, user_input):
            self.score += 1
            self.last_answer_correct = True
            self.just_wrong = False   # ✅ 정답이면 리셋
            self.update_status_text("정답입니다!")
        else:
            self.fail_count += 1
            self.last_answer_correct = False
            self.just_wrong = True    # ✅ 오답 기록
            self.update_status_text(f"오답입니다. 정답: {self.current.meaning}")

        # ✅ 항상 업데이트
        self.score_var.set(f"Score: {self.score}/{self.total}")

        self.check_button.state(["disabled"])

        if self.fail_count >= 3:
            self.end_game()


    def end_game(self):
        self.game_over = True

    # ✅ score 숨기기
        self.score_var.set("")   # ← 핵심!!!

        self.update_status_text(f"기회 3회 소진으로 게임 종료!\n최종 점수: {self.score}")

        self.check_button.state(["disabled"])

        for widget in self.check_button.master.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.state(["disabled"])

        end_button = ttk.Button(self.word_var._root(), text="결과 보기", command=self.show_result)
        end_button.pack(pady=10)

    
    def update_status_text(self, message=""):
        remaining = 3 - self.fail_count

        status = f"남은 기회: {remaining}/3"

        if message:
            self.feedback_var.set(f"{message}\n{status}")
        else:
            self.feedback_var.set(status)

