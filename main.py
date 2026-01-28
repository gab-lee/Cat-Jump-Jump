import tkinter as tk

W, H, L, R = 1200, 800, 150, 80

#Game setup
root = tk.Tk()
root.title("Cat jump jump")
root.geometry(f"{W}x{H}+{L}+{R}")
canvas = tk.Canvas(root, width=0.8*W, height=0.8*H, bg="white")
canvas.pack(fill="both", expand=True)

cat = canvas.create_oval(200,600,400,400)
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

#keyboard binding








root.mainloop()

