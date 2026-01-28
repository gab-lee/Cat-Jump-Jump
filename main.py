import tkinter as tk

W, H, L, R = 1280, 720, 300, 80

#Game setup
root = tk.Tk()
root.title("Cat jump jump")
root.geometry(f"{W}x{H}+{L}+{R}")
canvas = tk.Canvas(root, width = W, height=H, bg="white")
canvas.pack(fill="both", expand=True)

cat = canvas.create_oval(0.1*W,0.8*H,0.3*W,0.6*H)
ground = canvas.create_rectangle(0,600,1200,800, fill="Blue")

#'q': quit game
def quit_game(event):
    root.destroy()
root.bind("q", quit_game)

#'space': jump
def jump(event):
    canvas.coords(cat, 200,400,400,600)
    print("jumping")
root.bind("<space>",jump)

#scaling window 
def on_resize(event):
    width = event.width
    height = event.height
    canvas.coords(ground, 0,0.8*height,width, height)
    canvas.coords(cat, 0.1*width,0.8*height,0.2*width, 0.7*height)
    print(width, height)

root.bind("<Configure>", on_resize)







root.mainloop()

