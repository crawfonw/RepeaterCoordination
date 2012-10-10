Repeater Coordination
=====================

What
----
This is a simple project that attempts to computationally produce an optimal solution
to the disk covering problem (http://mathworld.wolfram.com/DiskCoveringProblem.html).

Why
---
The project was written for Rose-Hulman's Mathematical Modeling course and is based on
problem B from COMAP's 2011 MCM contest.
The original question can be found here http://www.comap.com/undergraduate/contests/mcm/contests/2011/problems/.

How
---
The code is written in Python and two different implementations are provided.

The first uses the Pyomo modeling language (https://software.sandia.gov/trac/coopr) and the
GNU Linear Programming Kit (http://www.gnu.org/software/glpk/) to produce a solution.

The second employs a genetic-algorithm technique (http://mathworld.wolfram.com/GeneticAlgorithm.html).

Future
------
Currently, the provided implementations attempt to solve the disk covering problem. For
the 2011 problem B from MCM, we would like to place the circles so that each circle's
center is inside or touching another's radius.