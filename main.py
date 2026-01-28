import tkinter as tk
import config
import entities
import entities

player = entities.Cat(100,200)

root = tk.Tk()
root.title(config.WINDOW_TITLE)
root.geometry(f"{config.W}x{config.H}+{config.X}+{config.Y}")
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)
ground = canvas.create_rectangle(entities.ground_coords(config.W,config.H), fill="green")


#Key binding 
def quit_game(event):
    root.destroy()

for key in config.QUIT_KEY:
    root.bind(key, quit_game)

#resize
def on_resize(event):
    W = event.width
    H = event.height
    canvas.coords(ground,entities.ground_coords(W,H))

#Refresh
def update():
    pass


root.after(config.FRAME_MS, update)
root.bind("<Configure>", on_resize)
root.mainloop()