from customtkinter import *
from constants import TRANSPARENT, CELL_BORDER, CELL_COLOR

class Cell:

    def __init__(self, parent):

        self.root = parent.winfo_toplevel()

        # VARIABLES
        self.width = 60
        self.height = 70

        
        self.frame_cell = CTkFrame(
                        parent,
                        height=self.height,
                        width=self.width,
                        fg_color="transparent",
            )
        self.frame_cell.pack_propagate(False)

        self.label_cell = CTkLabel(
                        self.frame_cell,
                        text="",
                        height=self.height,
                        width=self.width,
                        font=('Segoe UI', 37),
                        fg_color=CELL_COLOR,
                        border_width=1,
                        border_color=CELL_BORDER,
                        corner_radius=10                      
                    )


        self.direction = -1
        self.animating = False
    
    def set_letter(self, letter):
        self.label_cell.configure(text=letter)
    
    def clear(self):
        self.label_cell.configure(text="")
        self.set_color(TRANSPARENT)
    
    def set_color(self, color):
        self.label_cell.configure(fg_color=color)
    
    def get_letter(self):
        return self.label_cell.cget('text')
    
    def grid(self, row, column, padx, pady):
        self.frame_cell.grid(row=row, column=column, padx=padx, pady=pady)
        self.label_cell.place(relx=0.5, rely=0.5, anchor="center")
    
    def _update_size(self):
        self.frame_cell.configure(width=self.width, height=self.height)
        self.label_cell.configure(width=self.width, height=self.height)