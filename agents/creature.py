import numpy as np
import random
from agents.brain import Brain
from config import CREATURE_SPEED, HEALTH_DECAY

class Creature:
    def __init__(self, x,y, genome=None):
        self.x=x
        self.y=y

        self.health=100
        self.alive=True

        self.food_collected=0
        self.damage_dealt=0
        self.survival_time=0

        self.brain=Brain(genome=genome)
        self.speed=CREATURE_SPEED

        self.fitness=0
    
    def perceive(self, distance_to_food, angle_to_food,distance_to_enemy=1.0):
        inputs=[distance_to_food,angle_to_food,distance_to_enemy,self.health/100]
        return inputs
    
    def decide(self, inputs):
        outputs=self.brain.forward(inputs)
        return outputs
    
    def move(self, move_direction, width=800, height=600):
        angle=move_direction*2*np.pi
        dx=self.speed*np.cos(angle)
        dy=self.speed*np.sin(angle)
        self.x+=dx
        self.y+=dy
        self.x=max(0,min(self.x, width))
        self.y=max(0,min(self.y, height))
    
    def calculate_fitness(self):
        self.fitness=(self.food_collected * 10)+ (self.survival_time * 0.01)

    def update(self,inputs):
        if not self.alive:
            return
        outputs=self.decide(inputs)
        move_direction=outputs[0]
        self.move(move_direction)
        self.health-=HEALTH_DECAY
        self.survival_time+=1
        if self.health<=0:
            self.alive=False
        
    def get_genome(self):
        return self.brain.to_genome()


