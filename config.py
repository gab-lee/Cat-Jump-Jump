#Window size 
WINDOW_TITLE = "Cat Jump Jump" #application title 
W, H, X, Y = 1280, 720, 300,100 #application size
ASPECT_W = 16
ASPECT_H = 9

#FPS
FPS = 60
FRAME_MS = int(1000/FPS) 

#Keys
QUIT_KEY = ["q","<Escape>"]
JUMP_KEY = "<space>"

#Physics constant 
GRAVITY = 0.8 
JUMP_VELOCITY = 14

#Colour
cat_colour = "black"
ground_colour = "green"
obstacle_colour = "red"