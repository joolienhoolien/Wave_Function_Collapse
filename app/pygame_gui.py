import pygame
from solver import Solver

if __name__ == "__main__":
    pygame.init()
    #Any intro gui options go here
    #Maybe you click "solve puzzle!" then it goes to the following code...
    #Step 1 and 2 - create tiles and a grid
    solver = Solver()
    #Step 3 goes here, any adjustments on the front end before running...
    #Step 4, solve!
    while True: #Can change the "True" to a setting...
        solver.solve_next()
        #TODO: render new solver.grid state here!
    #can have other solver methods for slower solving potentially.
        #or just other arguments in the solve method
    #Step 5... anything we want to do like save to file or go back to step 1 or whatever
