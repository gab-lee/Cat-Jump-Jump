import tkinter as tk
import os
import time
from PIL import Image, ImageTk
import config
import entities
from game_logic import isOnGround, ObstacleManager

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.set_initial_geometry()
        self.root.minsize(640, 360)
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.game_state = "Title"
        self.view_scale = 1.0
        self.last_update_time = None
        self.score = 0
        self.score_text_id = None
        self.score_text_id = self.canvas.create_text(config.W - 20, 20,text =f"Score: {self.score}",anchor="ne")

    def set_initial_geometry(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = min(config.W, int(screen_w * 0.9))
        win_h = min(config.H, int(screen_h * 0.9))
        pos_x = (screen_w - win_w) // 2
        pos_y = (screen_h - win_h) // 2
        self.root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

    #--- Key binding ---
    """
    Bind the keys in config to their respective functions
    """

    def key_binding(self):
        #Quit Game
        def quit_game(event):
            self.root.destroy()
        for key in config.QUIT_KEY:
            self.root.bind(key, quit_game)
        #Jump 
        def jump(event):
            if self.cat.jump_held:
                return #cannot limitless jump
            self.cat.jump_held = True 
            self.cat.jump(isOnGround(self.cat,self.ground))
        self.root.bind(config.JUMP_KEY, jump)

        def on_jump_release(event):
            self.cat.jump_held = False
        self.root.bind(config.JUMP_RELEASE_KEY, on_jump_release)

        def pause_game(event):
            self.show_menu_screen()
        self.root.bind(config.PAUSE_KEY, pause_game)

        def restart_game(event):
            if not self.game_state == "Game_Over":
                return 
            self.obstacles.clean_up(self.canvas,self)
            self.canvas.delete(self.game_over_text_id)
            self.canvas.delete(self.game_over_score_id)
            self.canvas.delete(self.game_over_hint_id)
            self.start_game()
        self.root.bind(config.RESTART_KEY, restart_game)

    #--- Display and resolution ---

    def enable_resize(self):
        #Trigger on_resize whenever the window is resized 
        self.resize_enabled = True 
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self,event):
        # Resize world objects using uniform scale derived from canvas dimensions.
        if not self.resize_enabled:
            return
        if event.widget != self.root:
            return
        self.apply_scale()

    def apply_scale(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return

        self.view_scale = min(w / config.W, h / config.H)
        self.canvas.coords(self.score_text_id, w - 20, 20)

        if hasattr(self, "cat"):
            self.cat.size = self.view_scale
            if self.game_state == "Game_Over":
                self.position_game_over_cat()
            else:
                self.canvas.coords(self.cat.sprite_id, self.cat.x * self.cat.size, self.cat.y * self.cat.size)
        if hasattr(self, "ground"):
            self.ground.size = self.view_scale
            self.canvas.coords(self.ground_display, self.ground.coords())
        if hasattr(self, "obstacles"):
            self.obstacles.obstacle_size = self.view_scale

    def position_game_over_cat(self):
        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2 + 20
        self.canvas.coords(self.cat.sprite_id, cx, cy)

    #--- Game Screens ---
    def show_title_screen(self):
        self.start_game()

    def show_running_screen(self):
        pass

    def show_menu_screen(self):
        #Triggered when game is paused
        pass

    def show_game_over_screen(self):
        if not self.game_state == "Game_Over":
            return
        self.position_game_over_cat()
        self.game_over_text_id = self.canvas.create_text(
                                        self.canvas.winfo_width() // 2,
                                        self.canvas.winfo_height() // 2 - 180,
                                        text="GAME OVER", fill="Black", font=("Helvetica", 42, "bold")
                                        )
        self.canvas.itemconfig(self.cat.sprite_id, image=self.cat.frames_lick[0])  # force visible frame
        self.game_over_score_id = self.canvas.create_text(
                                        self.canvas.winfo_width() // 2,
                                        self.canvas.winfo_height() // 2 - 120,
                                        text=f"Score: {self.score}", fill="Black", font=("Helvetica", 30, "bold")
                                        )
        self.game_over_hint_id = self.canvas.create_text(
                                        self.canvas.winfo_width() // 2,
                                        self.canvas.winfo_height() // 2 + 120,
                                        text="Press R to Restart", fill="Black", font=("Helvetica", 18)
                                        )

    #--- Game States ---

    def start_game(self):
        self.game_state = "Running"
        self.show_running_screen()
        self.score = 0
        self.create_player()
        self.create_ground()
        self.obstacles = ObstacleManager()
        self.apply_scale()
        self.last_update_time = time.perf_counter()
        self.root.after(100, lambda: self.obstacles.schedule_spawn(self))
        self.update()

    def game_over(self):
        self.game_state = "Game_Over"
        self.show_game_over_screen()

# --- ---

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
    
    def animate_cat(self,dt):
        self.cat.frame_timer += dt

        if not self.game_state == "Running":
            frames = self.cat.frames_lick
            frame_interval = config.frame_interval_licking
        else:
            frames = self.cat.frames_jump if self.cat.isJumping else self.cat.frames_run
            frame_interval = self.cat.frame_interval
        if self.cat.frame_timer >= frame_interval and frames:
            self.cat.frame_timer = 0.0
            self.cat.frame_index = (self.cat.frame_index + 1) % len(frames)
            self.canvas.itemconfig(self.cat.sprite_id, image=frames[self.cat.frame_index])

    def update(self):
        now = time.perf_counter()
        if self.last_update_time is None:
            self.last_update_time = now
        dt = min(now - self.last_update_time, 0.05)
        self.last_update_time = now
        dt_scale = dt / (config.FRAME_MS / 1000.0)

        self.animate_cat(dt)
        if self.game_state == "Running":
            collided,passed = self.obstacles.update(self.canvas,self.cat,dt_scale)
            self.score += passed
            if collided:
                self.game_over()
            self.cat.jumping(self.ground.height,dt)
            self.canvas.coords(self.cat.sprite_id, self.cat.x * self.cat.size, self.cat.y * self.cat.size)
            self.canvas.itemconfig(self.score_text_id, text=f"Score: {self.score}")
        self.root.after(config.FRAME_MS,self.update)
        

    def create_player(self):
        #initialise player 
        self.cat = entities.Cat(120,500)
        cat_jump_path = os.path.join(os.path.dirname(__file__), "assets", "cat_jump.gif")
        cat_run_path = os.path.join(os.path.dirname(__file__), "assets", "cat_run.gif")
        cat_lick_path = os.path.join(os.path.dirname(__file__), "assets", "cat_lick.gif")
        self.cat.frames_jump = self.load_gif_frames(cat_jump_path, scale = config.player_scale)
        self.cat.frames_run = self.load_gif_frames(cat_run_path, scale = config.player_scale)
        self.cat.frames_lick = self.load_gif_frames(cat_lick_path, scale = config.player_scale)
        self.cat.sprite_id = self.canvas.create_image(self.cat.x, self.cat.y, image=self.cat.frames_run[0])

    def create_ground(self):
        #initialise ground
        self.ground = entities.Ground(config.W,550)
        self.ground_display = self.canvas.create_rectangle(*self.ground.coords(), fill=config.ground_colour)

    def run(self):
        self.resize_enabled = False
        self.root.after(200, self.enable_resize)
        self.key_binding()
        self.show_title_screen()
        self.root.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()

