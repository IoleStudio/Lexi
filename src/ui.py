from customtkinter import *
from game import WordleGame
from constants import MAX_ATTEMPTS, WORD_LENGTH, GREEN, YELLOW, GRAY, TRANSPARENT
import math
from storage import load_stats, save_stats
from cell import Cell

class WordleUI:
    
    def __init__(self):
        self.game = WordleGame()

        self.root = CTk()
        self.root.title("Lexi")
        self.root.geometry("360x600")

        self.root.bind("<Key>", self.ecoute)

        # FRAMES
        self.main_frame = CTkFrame(self.root, fg_color="#202938", corner_radius=0)
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)#pack(expand=True, fill="both")
        self.overlay = CTkFrame(self.root, fg_color="#161D29", corner_radius=0)
        # victoire / defaites
        self.endgame_card = CTkFrame(self.overlay, fg_color="#4B5C79", corner_radius=25, width=10, height=10)
        self.endgame_card.grid_propagate(False)
        self.endgame_card.columnconfigure(0, weight=1)
        self.endgame_card.columnconfigure(1, weight=1)
        self.label_victoire = CTkLabel(self.endgame_card, text="You Win !", font=('Segeo UI', 40))
        self.label_word = CTkLabel(self.endgame_card, text="", font=('Segeo UI', 50))
        self.label_essai = CTkLabel(self.endgame_card, text="", font=('Segeo UI', 20))
        self.label_best_score = CTkLabel(self.endgame_card, text="", font=('Segeo UI', 20))
        self.button_new_game = CTkButton(self.endgame_card, text="New Game", command=self.new_game, font=('Segeo UI', 30), fg_color="#39D98A", corner_radius=15, width=200, text_color="#000", height=60)
        self.label_wins = CTkLabel(self.endgame_card, text="", font=('Segeo UI', 20))
        self.label_losses = CTkLabel(self.endgame_card, text="", font=('Segeo UI', 20))

        # Titre
        titre = CTkLabel(self.main_frame, text="L  e  x  i", font=('Segoe UI', 80), text_color="#FFFFFF")
        titre.pack(anchor="center", pady=5)

        # GRILLE
        self.grid_cells = CTkFrame(self.main_frame, fg_color="transparent")
        self.grid_cells.pack(anchor="center")
        self.cells = []
        self.create_cells()

        # VARIABLES
        self.ligne_courante = 0
        self.colonne_courante = 0
        self.current_guess = ""

        # Animations
        self.animation_t = 0
        self.animation_duration = 1

        # DATA
        self.data = load_stats()

    
    def run(self):
        self.root.mainloop()
    
    def create_cells(self):
        for row in range(MAX_ATTEMPTS):
            ligne = []
            for column in range(WORD_LENGTH):
                cell = Cell(self.grid_cells)
                cell.grid(row=row, column=column, padx=5, pady=5)
                ligne.append(cell)
            self.cells.append(ligne)
    
    def update_line(self):
        reponse = self.game.check_guess(self.current_guess)

        for colonne in range(len(reponse)):
            self.cells[self.ligne_courante][colonne].set_color(reponse[colonne][1])
        
        if self.game.is_win(self.current_guess):

            self.data["wins"] += 1
            if self.data["best_streak"] > int(self.game.return_attempts()) + 1:
                self.data["best_streak"] = int(self.game.return_attempts()) + 1
            self.data["current_streak"] = int(self.game.return_attempts()) + 1

            self.show_endgame()
            self.show_win()

            save_stats(self.data)

        
        self.game.add_attempt()

        if  not self.game.is_win(self.current_guess) and self.game.has_attempts_left() != True:

            self.data["losses"] += 1
            self.data["current_streak"] = int(self.game.return_attempts()) + 1

            self.show_endgame()
            self.show_lose()            

            save_stats(self.data)

        self.ligne_courante += 1
        self.colonne_courante = 0
        self.current_guess = ""
    
    def ecoute(self, event):
        touche_appuyee = event.keysym.lower()
        if touche_appuyee.isalpha() and len(touche_appuyee) == 1:
            self.handle_letter(touche_appuyee)
        elif touche_appuyee == "return":
            self.handle_enter()
        elif touche_appuyee == "backspace":
            self.handle_backspace()
    
    def handle_letter(self, letter):
        if self.colonne_courante < WORD_LENGTH:
            self.current_guess += letter
            self.cells[self.ligne_courante][self.colonne_courante].set_letter(letter)
            self.colonne_courante += 1
    
    def handle_enter(self):
        if self.game.is_valid_guess(self.current_guess) == True:
            self.update_line()
    
    def handle_backspace(self):
        if self.colonne_courante > 0:
            self.colonne_courante -= 1
            self.cells[self.ligne_courante][self.colonne_courante].clear()
            self.current_guess = self.current_guess[:-1]
    
    def animate_endgame(self):

        self.start_y = 10
        self.start_x = 10
        self.end_y = 250
        self.end_x = 300

        t = self.animation_t

        progress = 1 - math.exp(-6*t) * math.cos(8*t)

        y = self.start_y + (self.end_y - self.start_y) * progress
        x = self.start_y + (self.end_x - self.start_x) * progress

        self.endgame_card.configure(width=x, height=y)#place(
        #    relx=0.5,
        #    y=y,
        #    anchor="n"
        #)

        self.animation_t += 0.03

        if self.animation_t <= 1:
            self.root.after(16, self.animate_endgame)
        else:
            self.animation_t = 0
            self.animation_duration = 1
    
    def new_game(self):
        self.game.new_game()

        self.colonne_courante = 0
        self.ligne_courante = 0
        self.overlay.place_forget()
        self.endgame_card.place_forget()
        self.label_victoire.grid_forget()
        self.label_essai.grid_forget()
        self.label_best_score.grid_forget()
        self.button_new_game.grid_forget()

        self.root.bind("<Key>", self.ecoute)

        for irow in range(MAX_ATTEMPTS):
            for jcolumn in range(WORD_LENGTH):
                self.cells[irow][jcolumn].clear()        
        self.current_guess = ""
    
    def show_endgame(self):
        self.root.unbind('<Key>')
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay.lift()

        self.endgame_card.place(relx=0.5, rely=0.5, anchor="center")
        self.animate_endgame()
        self.animation_t = 0

    def show_win(self):
        self.label_victoire.grid(row=0, columnspan=2, pady=7)
        self.label_essai.configure(text=f"Score : {self.data["current_streak"]}")
        self.label_essai.grid(row=1, column=0, pady=4)#, padx=10)
        self.label_best_score.configure(text=f"Best Score : {self.data["best_streak"]}")
        self.label_best_score.grid(row=1, column=1, pady=4)#, padx=10)
        self.label_wins.configure(text=f"Wins : {self.data["wins"]}")
        self.label_wins.grid(row=2, column=0)
        self.label_losses.configure(text=f"Losses : {self.data["losses"]}")
        self.label_losses.grid(row=2, column=1)
        self.button_new_game.grid(row=3, columnspan=2, pady=15)

    def show_lose(self):
        self.label_victoire.configure(text="You lose.")
        self.label_victoire.grid(row=0, columnspan=2, pady=0)
        self.label_word.configure(text=self.game.return_word().upper())
        self.label_word.grid(row=1, columnspan=2)#, padx=10)
        self.label_essai.configure(text=f"Score : {self.data["current_streak"]}")
        self.label_essai.grid(row=2, column=0, pady=4)#, padx=10)
        self.label_best_score.configure(text=f"Best Score : {self.data["best_streak"]}")
        self.label_best_score.grid(row=2, column=1, pady=4)#, padx=10)
        self.label_wins.configure(text=f"Wins : {self.data["wins"]}")
        self.label_wins.grid(row=3, column=0)
        self.label_losses.configure(text=f"Losses : {self.data["losses"]}")
        self.label_losses.grid(row=3, column=1)
        self.button_new_game.grid(row=4, columnspan=2, pady=15)
