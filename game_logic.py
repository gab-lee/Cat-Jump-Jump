import config
import random 
import entities

def isOnGround(cat: object,ground: object) -> bool:
    #return True if cat is touching the ground 
    if cat.y + cat.radius >= ground.height:
        print("Cat on ground")
        return True 
    #return False if the cat is not on the ground 
    print("Cat not on ground")
    return False

def schedule_spawn(game: object):
    spawn_x = game.canvas.winfo_width() + 600
    game.obstacles.spawn(game.canvas, spawn_x, game.ground.height)
    # schedule next spawn
    game.root.after(500, lambda: schedule_spawn(game))

class ObstacleManager:
    def __init__(self):
        self.obstacles = [] #list of dictionaries of obstacles
    def spawn(self,canvas,spawn_x,ground_y):
        h = random.randint(40,90)
        w = random.randint(25,50)
        speed = 5
        obs = entities.Obstacle(spawn_x, ground_y, w, h, speed)
        obs_id = canvas.create_rectangle(*obs.coords(), fill=config.obstacle_colour)
        self.obstacles.append({"obj": obs, "id": obs_id})
    def update(self,canvas):
        for obstacle in self.obstacles:
            obstacle["obj"].move()
            canvas.coords(obstacle["id"],*obstacle["obj"].coords())
    def clean_up(self):
        pass