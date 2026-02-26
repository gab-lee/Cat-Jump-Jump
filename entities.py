import config

class Cat:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vertical_velocity = 0 
        self.isJumping = False
        self.size = 1
        self.radius = self.size * 50 
        #input state flags
        self.jump_held = False
        self.jump_hold_time = 0.0
        #animation
        self.frames_run = []
        self.frames_jump = []
        self.frames_lick = []
        self.frame_index = 0
        self.frame_timer = 0.0
        self.frame_interval = config.frame_interval_running  # seconds per frame
        self.sprite_id = None
    
    def coords(self):
        base = (self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)
        return tuple(map(lambda v: v * self.size, base))
    
    def jump(self,isOnGround: bool):
        #Triggered when jump is triggered 
        if not isOnGround: #Verify cat is on ground
            return 
        self.frame_index = 0 #reset frame
        self.isJumping = True 
        self.vertical_velocity = -config.MIN_JUMP_VELOCITY #min jump velocity
        self.jump_hold_time = 0.0 

    def jumping(self,ground_y,dt):
        #animation
        if not self.isJumping: 
            self.frame_interval = config.frame_interval_running
            return
        self.frame_interval = config.frame_interval_jumping
        #physics
        if self.jump_held and self.jump_hold_time < config.JUMP_HOLD_MAX_TIME and self.vertical_velocity < 0:
            self.jump_hold_time += dt
            self.vertical_velocity -= config.JUMP_HOLD_ACCEL
            
            if self.vertical_velocity < -config.JUMP_VELOCITY:
                self.vertical_velocity = -config.JUMP_VELOCITY
        
        # Per-frame physics 
        self.y += self.vertical_velocity
        self.vertical_velocity += config.GRAVITY    

        #Landing
        if self.y + self.radius >= ground_y :
            self.y = ground_y - self.radius
            self.vertical_velocity = 0
            self.isJumping = False
            self.jump_hold_time = 0.0

class Obstacle:
    def __init__(self, spawn_x, ground_y, w, h, speed):
        self.width = w
        self.height =h
        self.x = spawn_x
        self.y = ground_y
        self.speed = speed

    def coords(self,size):
        base = (self.x, self.y-self.height, self.x+self.width, self.y)
        return tuple(map(lambda v: v * size, base))
    def move(self):
        self.x = self.x - self.speed 

    def isCollided(self,cat,size):
        cx1,cy1,cx2,cy2 = cat.coords()
        ox1,oy1,ox2,oy2 = self.coords(size)
        return not (
            ox2 < cx1 or  # obstacle left of cat
            ox1 > cx2 or  # obstacle right of cat
            oy2 < cy1 or  # obstacle above cat
            oy1 > cy2     # obstacle below cat
        )
    def isOffScreen(self,canvas,size):
        ox1,oy1,ox2,oy2 = self.coords(size)
        return ox2 < 0

class Ground:
    def __init__(self,width,height):
        self.width = width 
        self.height = height
        self.size = 1
    def coords(self):
        base = (0, self.height, self.width,config.H)
        return tuple(map(lambda v: v * self.size, base))