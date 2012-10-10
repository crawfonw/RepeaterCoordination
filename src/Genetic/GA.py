from copy import deepcopy
from math import sqrt
from operator import add
from random import choice, randint, random

def point_enclosed_by_circle(center, radius, p):
    return sqrt((center[0] - p[0])**2 + (center[1] - p[1])**2) <= radius

class Grid():    
    def __init__(self, center, radius, scale=1):
        self.center = (center[0]*scale, center[1]*scale)
        self.radius = radius*scale
        self.points = self.generate_points()
        self.points = self.prune_points()
        self.size = len(self.points)
    
    def generate_points(self):
        points = []
        for i in range(self.radius * 2 + 1):
            for j in range(self.radius * 2 + 1):
                points.append((i,j))
        return points
    
    def prune_points(self):
        new_points = []
        for point in self.points:
            if point_enclosed_by_circle(self.center, self.radius, point):
                new_points.append(point)
        return new_points

class Repeater():    
    def __init__(self, xy, r): #xy is a 2-tuple
        self.loc = xy
        self.radius = r
        
    def __str__(self):
        return 'Repeater at %s of r %s' % (self.loc, self.radius)
        
    __repr__ = __str__

class GeneticAlgorithm():    
    def __init__(self, grid, pop_count):
        self.grid = grid
        self.population = self.generate_population(pop_count)
        self.generation = 0

    def crossover(self, male, female, half):
        return choice([male[:half] + female[half:], male[half:] + female[:half]])
    
    def individual(self, repeater_radius = 5):
        repeaters = []
        remaining_points = deepcopy(self.grid.points)
        num_repeaters = randint(1, self.grid.size)
        for i in range(num_repeaters):
            point = choice(remaining_points)
            remaining_points.remove(point)
            repeaters.append(Repeater(point, repeater_radius))
        return repeaters
            
    def generate_population(self, count):
        pop = []
        for i in range(count):
            x = self.individual()
            f = self.fitness(x)
            pop.append((f, x))
        return pop
    
    def fitness(self, individual):
        #highest coverage
        points_covered = 0
        for repeater in individual:
            for point in self.grid.points:
                if point_enclosed_by_circle(repeater.loc, repeater.radius, point):
                    points_covered += 1
        return 1.0 / (min(points_covered, self.grid.size) / float(len(individual)))
    
    def grade(self):
        summed = reduce(add, (x[0] for x in self.population))
        return summed / (len(self.population) * 1.0)
        
    def mutate(self, individual):
        remaining_points = deepcopy(self.grid.points)
        for repeater in individual:
            if repeater.loc in remaining_points:
                remaining_points.remove(repeater.loc)
        r = randint(1, len(individual)) - 1
        point = choice(remaining_points)
        individual[r].loc = point
        return individual
    
    def evolve(self, retain=0.1, random_select=0.05, mutate=0.01):
        graded = [x for x in sorted(self.population)]
        retain_length = int(len(graded)*retain)
        parents = graded[:retain_length]
        
        for individual in graded[retain_length:]:
            if random_select > random():
                parents.append(individual)
        
        for i in range(len(parents)):
            if mutate > random():
                mutated_individual = self.mutate(parents[i][1])
                parents[i] = (self.fitness(mutated_individual), mutated_individual)
    
        desired_length = len(self.population) - len(parents)
        children = []
        while len(children) < desired_length:
            male = choice(parents)[1]
            female = choice(parents)[1]
            if male != female:
                half = len(male) / 2
                child = self.crossover(male, female, half)
                children.append(child)
                
        weighted_children = []
        for i, child in enumerate(children):
            #print '\nIndividual: %s' % (i + 1)
            weighted_children.append((self.fitness(child), child))
        
        parents.extend(weighted_children)
        self.population = parents
        self.generation += 1