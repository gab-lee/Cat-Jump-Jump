import config

class Cat:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vertical_velocity = 0 
        self.isJumping = False
        self.size = 1
        self.radius = self.size * 50 
        #animation
        self.frames_run = []
        self.frames_jump = []
        self.frame_index = 0
        self.frame_timer = 0.0
        self.frame_interval = 0.08  # seconds per frame
        self.sprite_id = None
    
    def coords(self):
        base = (self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)
        return tuple(map(lambda v: v * self.size, base))
    
    def jump(self,isOnGround: bool):
        if not isOnGround:
            return 
        self.frame_index = 0 #reset frame
        self.isJumping = True 
        self.vertical_velocity = -config.JUMP_VELOCITY
    
    def jumping(self,ground_y):
        if not self.isJumping:
            return
        self.y += self.vertical_velocity
        self.vertical_velocity += config.GRAVITY        
        print(self.y)
        if self.y + self.radius > ground_y :
            self.isJumping = False
            self.y = ground_y - self.radius

class Obstacle:
    def __init__(self, spawn_x, ground_y, w, h, speed):
        self.width = w
        self.height =h
        self.x = spawn_x
        self.y = ground_y
        self.speed = speed
        self.size =1 

    def coords(self):
        base = (self.x, self.y-self.height, self.x+self.width, self.y)
        return tuple(map(lambda v: v * self.size, base))
    def move(self):
        self.x = self.x - self.speed 

class Ground:
    def __init__(self,width,height):
        self.width = width 
        self.height = height
        self.size = 1
    def coords(self):
        base = (0, self.height, self.width,config.H)
        return tuple(map(lambda v: v * self.size, base))