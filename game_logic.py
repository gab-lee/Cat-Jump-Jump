import config
import random 
import entities

def isOnGround(cat: object,ground: object) -> bool:
    #return True if cat is touching the ground 
    if cat.y + cat.radius >= ground.height:
        return True 
    #return False if the cat is not on the ground 
    return False

class ObstacleManager:
    def __init__(self):
        self.obstacles = [] #list of dictionaries of obstacles
        self.spawn_min_rate = int((config.JUMP_VELOCITY/config.GRAVITY)*100*2.0)
        self.spawn_max_rate = int((config.JUMP_VELOCITY/config.GRAVITY)*100)
        self.obstacle_size = 1
        self.spawn_after_id = None

    def spawn(self,canvas,spawn_x,ground_y):
        h = random.randint(40,180)
        w = random.randint(25,50)
        speed = 10
        obs = entities.Obstacle(spawn_x, ground_y, w, h, speed)
        obs_id = canvas.create_rectangle(*obs.coords(self.obstacle_size), fill=config.obstacle_colour)
        self.obstacles.append({"obj": obs, "id": obs_id})

    def schedule_spawn(self,game: object):
        # Spawn in world coordinates so timing/distance stays consistent across resolutions.
        spawn_x = config.W + 600
        game.obstacles.spawn(game.canvas, spawn_x, game.ground.height)
        # schedule next spawn
        delay = random.randint(self.spawn_max_rate,self.spawn_min_rate)
        self.spawn_after_id = game.root.after(delay, lambda: self.schedule_spawn(game))


    def update(self,canvas,cat,dt_scale=1.0) -> bool:
        for obstacle in self.obstacles[:]:
            if obstacle["obj"].isCollided(cat, self.obstacle_size):
                return (True,0)
            elif obstacle["obj"].isOffScreen(canvas,self.obstacle_size):
                canvas.delete(obstacle["id"])
                self.obstacles.remove(obstacle)
                return (False,1)
            obstacle["obj"].move(dt_scale)
            canvas.coords(obstacle["id"],*obstacle["obj"].coords(self.obstacle_size))
        return (False,0)

    def end_game(self):
        return True

    def clean_up(self,canvas,game):
        for obstacle in self.obstacles:
            canvas.delete(obstacle["id"])
        self.obstacles.clear()
        if self.spawn_after_id is not None:
            game.root.after_cancel(self.spawn_after_id)  # stop pending spawn callback
            self.spawn_after_id = None
