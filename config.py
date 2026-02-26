#Window size 
WINDOW_TITLE = "Cat Jump Jump" #application title 
W, H, X, Y = 1280, 720, 125,125 #application size
ASPECT_W = 16
ASPECT_H = 9

#Character size
player_scale = 4.0

#FPS
FPS = 60
FRAME_MS = int(1000/FPS) 
frame_interval_running = 0.06
frame_interval_jumping = 0.09

#Keys
QUIT_KEY = ["q","<Escape>"]
JUMP_KEY = "<space>"
JUMP_RELEASE_KEY = "<KeyRelease-space>"

#Physics constant 
GRAVITY = 1.0
MIN_JUMP_VELOCITY = 10
JUMP_VELOCITY = 20
JUMP_HOLD_MAX_TIME = 1.0
JUMP_HOLD_ACCEL = 0.8   # per frame boost while held

#Colour
cat_colour = "black"
ground_colour = "green"
obstacle_colour = "red"
