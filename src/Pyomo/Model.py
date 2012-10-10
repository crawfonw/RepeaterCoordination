from coopr.pyomo import *
from coopr.opt import *
from math import sqrt

M = AbstractModel()

diam = 80
grdSize = 1
towRad = 20
regRad = diam/2

M.xCrd = RangeSet(1,diam*grdSize)
M.yCrd = RangeSet(1,diam*grdSize)

M.loc = Var(M.xCrd, M.yCrd, within=Binary)
#M.loc = Var(M.xCrd, M.yCrd, bounds=(0,1))

def calcNumTowers(M):
   return sum(M.loc[i,j] for i in M.xCrd for j in M.yCrd)
M.minTowers = Objective(rule=calcNumTowers, sense=minimize)

def ensureCover(M,k,t):
   locCover = 0
   if sqrt((diam/2-k)**2 + (diam/2-t)**2) <= regRad:
      for i in range(1,diam*grdSize+1):
         for j in range(1,diam*grdSize+1):
            if sqrt((k-i)**2 + (t-j)**2) <= towRad:
               locCover = locCover + M.loc[i,j]
      return locCover >= 1
   else:
      return Constraint.Skip
M.covTowers = Constraint(M.xCrd, M.yCrd, rule=ensureCover)

# Create a problem instance
instance = M.create()

# Indicate which solver to use
Opt = SolverFactory("glpk")

# Don't keep temporary files
Opt.keepFiles = False

# Generate a solution
Soln = Opt.solve(instance)
Soln.write()
