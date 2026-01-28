import tkinter as tk
from entities import Cat
import config

player = Cat(100,200)

root = tk.Tk()
root.title(config.WINDOW_TITLE)
root.geometry(f"{config.W}x{config.H}")

#Key binding 
def quit_game(event):
    root.destroy()

for key in config.QUIT_KEY:
    root.bind(key, quit_game)


root.mainloop()