class Cat:
    def __init__(self,x,y):
        self.x = x
        self.y = y

#ground
def ground_coords(width,height):
    return (0, 0.8 * height, width, height)