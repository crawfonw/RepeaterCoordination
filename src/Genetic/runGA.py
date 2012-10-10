from GA import GeneticAlgorithm, Grid

import datetime
import time

import os
import zipfile

POPULATION = 5
GENERATIONS = 5

t1 = time.time()

print 'Generation 0 - Population: %s\n' % POPULATION
p = population(POPULATION)

t2 = time.time()

print 'Initial population calculation time: %0.3f min' % (float(t2 - t1) / 60.0)

for i in range(1, GENERATIONS + 1):
    print '========================================'
    print '\nOn generation %s - Population: %s\n' % (i, len(p))
    
    p = evolve(p, retain=0.1)
    fitness_avg = grade(p)
    print 'Score of this population: %s\n\n' % fitness_avg
    for i in p:
        print 'Repeater at %s' % i

t2 = time.time()
#print 'Runtime: %0.3f sec' % float(t2 - t1)
print 'Runtime: %0.3f min' % (float(t2 - t1) / 60.0)