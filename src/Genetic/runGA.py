from GA import GeneticAlgorithm, Grid

import datetime
import time

import os
import zipfile

POPULATION = 500
GENERATIONS = 10

now = str(datetime.datetime.now())
now = now.replace(' ', '-').replace(':', '').split('.')[0]
os.mkdir(os.getcwd() + os.sep + 'results' + os.sep + now)

t1 = time.time()

grid = Grid((10,10), 10)
opt = GeneticAlgorithm(grid, POPULATION)

print 'Generation %s - Population: %s\n' % (opt.generation, len(opt.population))

t2 = time.time()

print 'Initial population calculation time: %0.3f min' % (float(t2 - t1) / 60.0)

for i in range(1, GENERATIONS + 1):
    print '========================================'
    print '\nOn generation %s - Population: %s\n' % (opt.generation, len(opt.population))
    
    opt.evolve()
    fitness_avg = opt.grade()
    avg_repeaters = (sum([len(x[1]) for x in opt.population]) / float(len(opt.population)))
    print 'Score of this population: %s' % fitness_avg
    print 'Avg. num repeaters: %s\n\n' % avg_repeaters
    f = open(os.getcwd() + os.sep + 'results' + os.sep + now + os.sep + 'generation%s_%s.txt' % (i, fitness_avg), 'w')
    f.write('Score of this population: %s\nAvg. Repeaters: %s\n\n' % (fitness_avg, avg_repeaters))
    f.write('Population (N=%s):\n\n' % len(opt.population))
    for idividual in opt.population:
        f.write('Score:%s\nNum. Repeaters:%s\nRepeaters:%s\n\n' % (idividual[0], len(idividual[1]), idividual[1]))

t2 = time.time()
#print 'Runtime: %0.3f sec' % float(t2 - t1)
print 'Runtime (including I/O): %0.3f min' % (float(t2 - t1) / 60.0)