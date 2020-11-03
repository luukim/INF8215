# -*- coding: utf-8 -*-
# Thien-Kim Loisel-Luu 1834378
# Souhaila Melloul 1835144
# Mourad Younes 1832387
from generator_problem import GeneratorProblem
import random


class Solve:

    def __init__(self, n_generator, n_device, seed):

        self.n_generator = n_generator
        self.n_device = n_device
        self.seed = seed
        self.instance = GeneratorProblem.generate_random_instance(self.n_generator, self.n_device, self.seed)

    def solve(self):
        print("Solve with a local search algorithm")
        opened_generators = [0 for _ in range(self.n_generator)]
        assigned_generators = [None for _ in range(self.n_device)]

        for i in range(self.n_device):
            assigned_generators[i] = random.randint(0, self.n_generator-1)

        for i in range(len(assigned_generators)) :
            j = assigned_generators[i]
            opened_generators[j] = 1

        solutions_found = {}
        best_solution = assigned_generators, opened_generators
        solutions_found[self.instance.get_solution_cost(best_solution[0], best_solution[1])] = best_solution
        banned_generators = []
            
        for i in range(self.n_device*5):
            neighbors = self.getNeighbors(assigned_generators, opened_generators, banned_generators)
            countGenerator = 0
            index = 1
            while countGenerator == 0:
                maxOpeningCost = sorted(self.instance.opening_cost)[-index]
                generator = self.instance.opening_cost.index(maxOpeningCost)
                countGenerator = assigned_generators.count(generator)
                if countGenerator == 1:
                    banned_generators.append(generator)
                index += 1

            selected_neighbors = self.selectNeighbors(neighbors, generator, countGenerator)
            if selected_neighbors:
                best_neighbor_cost = min(selected_neighbors, key=float)
                best_neighbor = selected_neighbors[best_neighbor_cost]
                best_solution = best_neighbor[0], best_neighbor[1]
                assigned_generators = best_solution[0]
                opened_generators = best_solution[1]

        self.printSolution(assigned_generators, opened_generators)
    
    def selectNeighbors(self, neighbors, generator, countGenerator):
        bestNeighbors = {}
        for key in neighbors:
            if neighbors[key][0].count(generator) < countGenerator:
                bestNeighbors[self.instance.opening_cost[generator]] = neighbors[key]
        return bestNeighbors

    def getNeighbors(self, assigned_generators, opened_generators, banned_generators) :
        neighbors = {}
        for i in range(self.n_device) :
            for j in range(self.n_generator) :
                opened_generators_temp = list(opened_generators)
                assigned_generators_temp = list(assigned_generators)
                if assigned_generators[i] != j and j not in banned_generators :
                    oldGenerator = assigned_generators_temp[i]
                    assigned_generators_temp[i] = j
                    opened_generators_temp[j] = 1
                    if oldGenerator not in assigned_generators_temp :
                        opened_generators_temp[oldGenerator] = 0
                    new_solution = assigned_generators_temp, opened_generators_temp
                    neighbors[self.instance.get_solution_cost(new_solution[0], new_solution[1])] = new_solution
        return neighbors


    def printSolution(self, assigned_generators, opened_generators) :
        self.instance.solution_checker(assigned_generators, opened_generators)
        total_cost = self.instance.get_solution_cost(assigned_generators, opened_generators)
        self.instance.plot_solution(assigned_generators, opened_generators)

        print("[ASSIGNED-GENERATOR]", assigned_generators)
        print("[OPENED-GENERATOR]", opened_generators)
        print("[SOLUTION-COST]", total_cost)
