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
def enable_resize():
    root.bind("<Configure>", on_resize)

def on_resize(event):
    w = event.width
    h = event.height
    desired_h = int(w * config.ASPECT_H / config.ASPECT_W)
    
    if h != desired_h:
        root.geometry(f"{w}x{desired_h}")

    canvas.coords(ground,entities.ground_coords(w,h))

#Refresh
def update():
    pass


root.after(100,enable_resize)
root.after(config.FRAME_MS, update)
root.mainloop()