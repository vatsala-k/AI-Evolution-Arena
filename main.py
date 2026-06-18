import pygame
from environment.arena import Arena
from evolution.genetic_algo import GeneticAlgorithm

pygame.init()
font=pygame.font.SysFont("monospace",16)
from config import WIDTH, HEIGHT, FPS, STEPS_PER_GENERATION

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("AI EVOLUTION ARENA")
clock=pygame.time.Clock()

arena=Arena(width=WIDTH, height=HEIGHT)
ga=GeneticAlgorithm()

generation=1
step=0
steps_per_generation=STEPS_PER_GENERATION
clock.tick(FPS)

def draw_stats(screen,generation,step,creatures):
    alive=sum(1 for c in creatures if c.alive)
    best_fitness=max((c.fitness for c in creatures),default=0)
    avg_fitness=sum(c.fitness for c in creatures)/len(creatures) if creatures else 0
    stats=[
        f"Generation :{generation}",
        f"Step: {step}/{steps_per_generation}",
        f"Alive: {alive}/{len(creatures)}",
        f"Best fit: {best_fitness:.2f}",
        f"Avg fit: {avg_fitness:.2f}",
    ]
    for i, line in enumerate(stats):
        surface=font.render(line,True,(220,220,220))
        screen.blit(surface,(10,10+i*20))

running=True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    arena.update()
    step+=1

    if step>=steps_per_generation:
        print(f"Generation {generation} completed")
        #create new generation
        new_creatures=ga.create_next_generation(arena.creatures,arena.population_size)

        arena.creatures=new_creatures
        arena.spawn_food()
        step=0
        generation+=1
    
    screen.fill((30,30,30))
    draw_stats(screen,generation,step,arena.creatures)

    #food
    for food in arena.foods:
        pygame.draw.circle(screen,(0,250,0),(int(food[0]),int(food[1])),4)
    
    for creature in arena.creatures:
        if creature.alive:
            color=(0,120,255)
        else:
            color=(100,100,100)
        pygame.draw.circle(screen,color,(int(creature.x),int(creature.y)),6)
        
    pygame.display.flip()
pygame.quit()


