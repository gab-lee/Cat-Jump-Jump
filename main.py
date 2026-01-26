import tkinter as tk

W, H, L, R = 1200, 800, 150, 80

#Game setup
root = tk.Tk()
root.title("Cat jump jump")
root.geometry(f"{W}x{H}+{L}+{R}")

def quit_game(event):
    root.destroy()

root.bind("q", quit_game)

root.mainloop()