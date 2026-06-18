import random
import numpy as np
from agents.creature import Creature
from config import ELITE_FRACTION

class GeneticAlgorithm:
    def __init__(self, mutation_rate=0.1, mutation_strength=0.2):
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength

    def calculate_fitness(self, creatures):
        for creature in creatures:
            creature.fitness = (creature.food_collected + creature.survival_time * 0.01)

    def select_parents(self, creatures, num_parents):
        creatures = sorted(creatures, key=lambda c: c.fitness, reverse=True)
        return creatures[:num_parents]

    def crossover(self, genome1, genome2):
        child_genome = []
        for g1, g2 in zip(genome1, genome2):
            if random.random() < 0.5:
                child_genome.append(g1)
            else:
                child_genome.append(g2)
        return np.array(child_genome)

    def mutate(self, genome):
        genome = genome.copy()          # Bug 3 fix: don't mutate parent in-place
        for i in range(len(genome)):
            if random.random() < self.mutation_rate:
                genome[i] += np.random.normal(0, self.mutation_strength)
        return genome                   # Bug 1 fix: outside the for loop

    def create_next_generation(self, creatures, population_size):
        #self.calculate_fitness(creatures)
        #print("Max fitness:", max(c.fitness for c in creatures))
        #parents = self.select_parents(creatures, population_size // 4)
        #new_population = []
        self.calculate_fitness(creatures)
        print(f"Max fitness: {max(c.fitness for c in creatres):.2f}|" 
              f"Avg: {sum(c.fitness for c in creatures)/len(creatures):.2f}")
        parents= self.select_parents(creatures, population_size//4)

        #elitism-carry top n without mutation
        elite_count=max(1, int(poulation_size*ELITE_FRACTION))
        elites=parents[:elite_count]
        new_population=[]
        for elite in elites:
            child=Creature(
                random.uniform(0,800),
                random.uniform(0,600),
                genome=elite.get_genome()
            )
            new_population.append(child)

        while len(new_population) < population_size:
            def tournament_select(self,parents,k=3):
                competitors=random.sample(parents, min(k,len(parents)))
                return max(competitors, key=lambda c:c.fitness)
            parent1=self.tournament_select(parents)
            parent2=self.tournament_select(parents)
            genome2 = parent2.get_genome()
            child_genome = self.crossover(genome1, genome2)
            child_genome = self.mutate(child_genome)    # Bug 2 fix: mutate not mutation
            x = random.uniform(0, 800)
            y = random.uniform(0, 600)
            child = Creature(x, y, genome=child_genome)
            new_population.append(child)
        return new_population