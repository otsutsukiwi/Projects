import random
import sys
import os
from time import sleep

words_list = ["otaku", "manga", "cosplay", "kawaii", "sakura", "ramen", "sushi", "shonen", "shoujo", "seinen", "josei", "harem", "mecha", "tsundere", "yandere", "chibi", "kemonomimi", "bishounen", "waifu", "senpai"]

def game(guess_bank, rand_word):
    selection = words_list[int(rand_word)]
    word = []
    print(selection)
    check = 0
    for i in selection:
        if i in guess_bank:
            word.append(i)
            check += 1
            if check >= len(selection):
                return f"```You have guessed the word ({selection}) correctly!\ntype >hangman to play again```"
        else:
            word.append("_")
    string = "`" + ' '.join(word) + "`"
    return string