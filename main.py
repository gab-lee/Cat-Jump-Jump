import tkinter as tk
import config
import entities
from game_logic import isOnGround, schedule_spawn, ObstacleManager

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.W}x{config.H}+{config.X}+{config.Y}")
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.running = True 

    def key_binding(self):
        #Quit Game
        def quit_game(event):
            self.root.destroy()
        for key in config.QUIT_KEY:
            self.root.bind(key, quit_game)
        #Jump 
        def jump(event):
            self.cat.jump(isOnGround(self.cat,self.ground))
        self.root.bind(config.JUMP_KEY, jump)

    def enable_resize(self):
        #Trigger on_resize whenever the window is resized 
        self.resize_enabled = True 
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self,event):
        #resize window based on the width of the window
        if not self.resize_enabled:
            return
        w = event.width
        h = event.height
        desired_h = int(w * config.ASPECT_H / config.ASPECT_W)
        
        if h != desired_h:
            self.root.geometry(f"{w}x{desired_h}")

        self.cat.size = w/config.W
        self.canvas.coords(self.cat_display,self.cat.coords())
        self.ground.size = w/config.W
        self.canvas.coords(self.ground_display,self.ground.coords())
        #self.canvas.obstacles(ground,groudn coords)
    
    def update(self):
        if not self.running:
            return 
        
        self.obstacles.update(self.canvas)
        self.cat.jumping(self.ground.height)
        self.canvas.coords(self.cat_display,self.cat.coords())
        self.root.after(config.FRAME_MS,self.update)

    def create_player(self):
        #initialise player 
        self.cat = entities.Cat(120,500)
        self.cat_display = self.canvas.create_oval(*self.cat.coords(), fill=config.cat_colour)
    
    def create_ground(self):
        #initialise ground
        self.ground = entities.Ground(1280,550)
        self.ground_display = self.canvas.create_rectangle(*self.ground.coords(), fill=config.ground_colour)

    def run(self):
        self.resize_enabled = False
        self.root.after(200, self.enable_resize)
        self.key_binding()
        self.create_player()
        self.create_ground()
        self.obstacles = ObstacleManager()
        self.root.after(100, lambda: schedule_spawn(self))
        self.update()
        self.root.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()





