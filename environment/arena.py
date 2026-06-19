import random
import math
from agents.creature import Creature

class Arena:
    def __init__(self, width=800, height=600,population_size=20, food_count=30):
        self.width=width
        self.height=height
        self.population_size=population_size
        self.food_count=food_count

        self.creatures=[]
        self.foods=[]

        self.spawn_population()
        self.spawn_food()

    def spawn_population(self):
        self.creatures=[]
        for i in range(self.population_size):
            x=random.uniform(0,self.width)
            y=random.uniform(0,self.height)
            creature=Creature(x,y)
            self.creatures.append(creature)

    def spawn_food(self):
        self.foods=[]
        for i in range(self.food_count):
            x=random.uniform(0,self.width)
            y=random.uniform(0,self.height)
            self.foods.append((x,y))
        
    def distance(self,x1,y1,x2,y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2)
        
    def nearest_food(self, creature):
        nearest=None
        min_dist=float("inf")
        for fx,fy in self.foods:
            d=self.distance(creature.x,creature.y,fx,fy)
            if d<min_dist:
                min_dist=d
                nearest=(fx,fy)
        return nearest,min_dist
        
    def update(self):
        for creature in self.creatures:
            if not creature.alive:
                continue
            food,dist_food=self.nearest_food(creature)
            if food is None:
                continue
            fx,fy=food
            angle_to_food=math.atan2(fy-creature.y, fx-creature.x)
            distance_to_food=min(dist_food/200,1)
            angle_norm=(angle_to_food % (2*math.pi))/(2*math.pi)

            nearest_enemy_dist=self.nearest_enemy_distance(creature)
            distance_to_enemy=min(nearest_enemy_dist/200,1.0)

            inputs=creature.perceive(distance_to_food,angle_norm,distance_to_enemy)
            creature.update(inputs)
            
            if dist_food<10:
                creature.health+=10
                creature.food_collected+=1
                self.foods.remove(food)
            if len(self.foods) == 0:
                self.spawn_food()     


    def nearest_enemy_distance(self,creature):
        min_dist=float("inf")
        for other in self.creatures:
            if other is creature or not other.alive:
                continue
            d = self.distance(creature.x,creature.y,other.x,other.y)
            if d< min_dist:
                min_dist=d
        return min_dist if min_dist != float("inf") else 200