from __future__ import annotations

from vocabulary_quiz_app.quiz_logic import Word

WORDS: list[Word] = [
    #단어 추가 (hard 모드에서의 긴 단어 추가 + easy 모드용 짧은 단어 추가)
    Word(term="apple", meaning="사과"),
    Word(term="book", meaning="책"),
    Word(term="chair", meaning="의자"),
    Word(term="door", meaning="문"),
    Word(term="flower", meaning="꽃"),
    Word(term="friend", meaning="친구"),
    Word(term="music", meaning="음악"),
    Word(term="school", meaning="학교"),
    Word(term="summer", meaning="여름"),
    Word(term="water", meaning="물"),
    Word(term="dog", meaning="개"),
    Word(term="cat", meaning="고양이"),
    Word(term="pen", meaning="펜"),
    Word(term="bag", meaning="가방"),
    Word(term="food", meaning="음식"),
    Word(term="car", meaning="자동차"),
    Word(term="tree", meaning="나무"),
    Word(term="sun", meaning="태양"),
    Word(term="moon", meaning="달"),
    Word(term="love", meaning="사랑"),
    Word(term="computer", meaning="컴퓨터"),
    Word(term="science", meaning="과학"),
    Word(term="language", meaning="언어"),
    Word(term="library", meaning="도서관"),
    Word(term="education", meaning="교육"),
    Word(term="analysis", meaning="분석"),
    Word(term="development", meaning="개발"),
    Word(term="dictionary", meaning="사전"),
    Word(term="application", meaning="응용"),
    Word(term="information", meaning="정보"),
]
