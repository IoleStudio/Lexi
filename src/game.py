import random

from storage import load_words
from constants import MAX_ATTEMPTS, GREEN, YELLOW, GRAY

class WordleGame:
    
    def __init__(self):
        self.word = self.choose_word()
        print(self.word)
        self.max_attempts = MAX_ATTEMPTS
        self.attempts = 0
    
    def choose_word(self):
        return random.choice(load_words())

    
    def get_word_length(self):
        return len(self.word)
    
    def is_valid_guess(self, guess):
        guess = guess.lower().strip()
        if len(guess) > len(self.word):
            return "trop long"
        if len(guess) < len(self.word):
            return "trop court"
        
        return True
    
    def is_win(self, guess):
        return guess == self.word
    
    def check_guess(self, guess):
        guess = guess.lower().strip()
        letters = [None] * len(self.word)
        copy = list(self.word)

        # Lettres parfaitements placées
        for indice,lettre in enumerate(guess):
            if lettre == self.word[indice]:
                letters[indice] = (lettre, GREEN)
                copy[indice] = None
        
        # Lettres dans le mot mais mal placées
        for indice,lettre in enumerate(guess):
            if letters[indice] is not None:
                continue
            if lettre in copy:
                letters[indice] = (lettre, YELLOW)
                copy[copy.index(lettre)] = None
            else:
                letters[indice] = (lettre, GRAY)
        
        return letters

    def new_game(self):
        self.word = self.choose_word()
        print(self.word)
        self.attempts = 0
    
    def add_attempt(self):
        self.attempts += 1
    
    def remaining_attempts(self):
        return self.max_attempts - self.attempts
    
    def has_attempts_left(self):
        return self.attempts < self.max_attempts
    
    def return_attempts(self):
        return self.attempts

    def return_word(self):
        return self.word