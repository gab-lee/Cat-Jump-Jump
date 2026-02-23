import tkinter as tk
import os
from PIL import Image, ImageTk
import config
import entities
from game_logic import isOnGround, ObstacleManager

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
        self.canvas.coords(self.cat.sprite_id, self.cat.x * self.cat.size, self.cat.y * self.cat.size)
        self.ground.size = w/config.W
        self.canvas.coords(self.ground_display,self.ground.coords())
        self.obstacles.obstacle_size = w/config.W

    def load_gif_frames(self,path, scale=1.0):
        img = Image.open(path)
        frames = []
        i = 0
        while True:
            try:
                img.seek(i)
                frame = img.convert("RGBA").copy()  # define frame first
                if scale != 1.0:
                    w, h = frame.size
                    frame = frame.resize((int(w * scale), int(h * scale)), Image.Resampling.NEAREST)
                frames.append(ImageTk.PhotoImage(frame))
                i += 1
            except EOFError:
                break
        return frames
    
    def update(self):
        if not self.running:
            return 
        
        self.obstacles.update(self.canvas)
        self.cat.jumping(self.ground.height)
        self.cat.frame_timer += config.FRAME_MS / 1000.0
        if self.cat.frame_timer >= self.cat.frame_interval and self.cat.frames_jump:
            frames = self.cat.frames_jump if self.cat.isJumping else self.cat.frames_run
            self.cat.frame_timer = 0.0
            self.cat.frame_index = (self.cat.frame_index + 1) % len(frames)
            self.canvas.itemconfig(self.cat.sprite_id, image=frames[self.cat.frame_index])
        self.canvas.coords(self.cat.sprite_id, self.cat.x * self.cat.size, self.cat.y * self.cat.size)
        self.root.after(config.FRAME_MS,self.update)

    def create_player(self):
        #initialise player 
        self.cat = entities.Cat(120,500)
        cat_jump_path = os.path.join(os.path.dirname(__file__), "assets", "cat_jump.gif")
        cat_run_path = os.path.join(os.path.dirname(__file__), "assets", "cat_run.gif")
        self.cat.frames_jump = self.load_gif_frames(cat_jump_path, scale = config.player_scale)
        self.cat.frames_run = self.load_gif_frames(cat_run_path, scale = config.player_scale)
        self.cat.sprite_id = self.canvas.create_image(self.cat.x, self.cat.y, image=self.cat.frames_run[0])

    
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
        self.root.after(100, lambda: self.obstacles.schedule_spawn(self))
        self.update()
        self.root.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()




