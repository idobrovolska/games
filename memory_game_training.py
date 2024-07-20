'''
we're implementing the class of object - card, and a class of main event - game. the second contains methods 
to handle subevents, bonded to several objects - event handlers (create the grid with buttons-cards, click on 
TWO cards and check if they are similar).
*it's good to set the activity status to cards to make them inactive when they're played.
the program asks the user about grid size (quantity of cards he wants to guess).
'''

import tkinter as tk
from tkinter import simpledialog, messagebox
from random import shuffle
from PIL import Image, ImageTk

class Card:
    def __init__(self, master, game, front_image_path, back_image_path):
        self.master = master
        self.game = game  
        self.front_image_path = front_image_path
        self.back_image_path = back_image_path
        self.button = tk.Button(master, command = self.on_click)
        self.is_flipped = False
        self.active = True  
        self.update_image()

    def update_image(self):
        if self.is_flipped:
            self.front_image = self.load_image(self.front_image_path)
            self.button.config(image = self.front_image)
        else:
            self.back_image = self.load_image(self.back_image_path)
            self.button.config(image = self.back_image)

    def load_image(self, path):
        img = Image.open(path)
        img = img.resize((self.button.winfo_width(), self.button.winfo_height()), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def on_click(self):
        if self.active and not self.is_flipped and len(self.game.flipped_cards) < 2:
            self.flip()
            self.game.on_card_click(self)  

    def flip(self):
        self.is_flipped = not self.is_flipped
        self.update_image()

    def set_inactive(self):
        self.active = False
        self.button.config(state=tk.DISABLED)
        self.button.config(image=self.front_image)  
        self.button.config(relief=tk.SUNKEN)



class MemoryGame:
    def __init__(self, root, rows, columns):
        self.root = root
        self.rows = rows
        self.columns = columns
        self.cards = []
        self.flipped_cards = []
        self.front_images = []  
        self.back_image_path = 'back.jpg' 
        self.validate_card_count()
        self.create_cards()
        self.root.bind("<Configure>", self.on_configure) 
        self.all_cards_flipped = False

    def validate_card_count(self):
        total_cards = self.rows * self.columns
        if total_cards % 2 != 0:
            messagebox.showerror("Invalid Grid Size", "The total number of cards must be even. Please try again.")
            self.root.destroy()

    def create_cards(self):
        self.front_images = [f'front{i}.jpg' for i in range(1, (self.rows * self.columns // 2) + 1)] * 2
        shuffle(self.front_images)

        for r in range(self.rows):
            for c in range(self.columns):
                front_image = self.front_images.pop()
                card = Card(self.root, self, front_image, self.back_image_path)  
                card.button.grid(row=r, column=c, sticky=tk.N+tk.E+tk.S+tk.W)
                self.cards.append(card)

        for r in range(self.rows):
            self.root.grid_rowconfigure(r, weight=1)
            for c in range(self.columns):
                self.root.grid_columnconfigure(c, weight=1)

    def on_card_click(self, card):
        if len(self.flipped_cards) < 2:
            self.flipped_cards.append(card)
            if len(self.flipped_cards) == 2:
                self.root.after(1000, self.check_cards)  

    def check_cards(self):
        if len(self.flipped_cards) == 2:
            card1, card2 = self.flipped_cards
            if card1.front_image_path != card2.front_image_path:
                card1.flip()
                card2.flip()
            else:
                card1.set_inactive()
                card2.set_inactive()
            self.flipped_cards.clear()

        if all(not card.active for card in self.cards):
            self.all_cards_flipped = True
            messagebox.showinfo("Congratulations!", "You've matched all pairs! Well done!")
            self.root.destroy()


    def on_configure(self, event):
        button_width = event.width // self.columns
        button_height = event.height // self.rows
        for card in self.cards:
            card.button.config(width = button_width, height = button_height)
            card.update_image()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Memory training")  
    root.geometry("400x300")  
    rows = simpledialog.askinteger("Input", "Enter number of rows:", minvalue = 2, maxvalue = 10)
    columns = simpledialog.askinteger("Input", "Enter number of columns:", minvalue = 2, maxvalue = 10)
    
    try:
        game = MemoryGame(root, rows, columns)
        root.mainloop()
    except ValueError as e:
        print(e)
        root.destroy()
