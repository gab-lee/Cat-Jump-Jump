WINDOW_TITLE = "Cat Jump Jump" #application title 
W, H = 1280, 720 #application size

#Keys
QUIT_KEY = ["q","<Escape>"]
JUMP_KEY = "<space>"


""" 
#'q': quit game
def quit_game(event):
    root.destroy()
root.bind("q", quit_game)

#'space': jump
def jump(event):
    canvas.coords(cat, 200,400,400,600)
    print("jumping")
root.bind("<space>",jump)

#create 60FPS game 
global x 
global y 

#scaling window 
def on_resize(event):
    x = event.width
    y = event.height
    canvas.coords(ground, 0,0.8*y,x, y)
    canvas.coords(cat, 0.1*x,0.8*y,0.2*x, 0.7*y)


root.bind("<Configure>", on_resize)

def update():
    global x
    speed = 5 
    x = x-speed
    print(f"updating{x}")
    canvas.coords(ground, 0,0.8*y,x, y)
    root.after(16,update) #60FPS



#Game setup
root = tk.Tk()
root.title("Cat jump jump")
root.geometry(f"{W}x{H}+{L}+{R}")
canvas = tk.Canvas(root, width = W, height=H, bg="white")
canvas.pack(fill="both", expand=True)

update() """