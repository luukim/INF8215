# -*- coding: utf-8 -*-
from generator_problem import GeneratorProblem
import random
import math


class Solve:

    def __init__(self, n_generator, n_device, seed):

        self.n_generator = n_generator
        self.n_device = n_device
        self.seed = seed

        self.instance = GeneratorProblem.generate_random_instance(self.n_generator, self.n_device, self.seed)

    def solve_naive(self):

        print("Solve with a naive algorithm")
        print("All the generators are opened, and the devices are associated to the closest one")

        opened_generators = [1 for _ in range(self.n_generator)]

        assigned_generators = [None for _ in range(self.n_device)]

        for i in range(self.n_device):
            closest_generator = min(range(self.n_generator),
                                    key=lambda j: self.instance.get_distance(self.instance.device_coordinates[i][0],
                                                                      self.instance.device_coordinates[i][1],
                                                                      self.instance.generator_coordinates[j][0],
                                                                      self.instance.generator_coordinates[j][1])              
                                    )

            assigned_generators[i] = closest_generator

        self.printSolution(assigned_generators, opened_generators)

    def solve_localSearch(self):
        print("Solve with a local search algorithm")
        generators = list(range(0, self.n_generator))
        opened_generators = [0 for _ in range(self.n_generator)]
        assigned_generators = [None for _ in range(self.n_device)]
        costs = {}
        #solution initiale
        for i in range(self.n_device):
            closest_generator = min(range(self.n_generator),
                                    key=lambda j: self.instance.get_distance(self.instance.device_coordinates[i][0],
                                                                      self.instance.device_coordinates[i][1],
                                                                      self.instance.generator_coordinates[j][0],
                                                                      self.instance.generator_coordinates[j][1])              
                                    )

            assigned_generators[i] = closest_generator
            
        for i in range(len(assigned_generators)) :
            opened_generators[assigned_generators[i]] = 1


        # for i in range(self.n_device):
        #     assigned_generators[i] = random.randint(0, self.n_generator-1)

        # for i in range(len(assigned_generators)) :
        #     j = assigned_generators[i]
        #     opened_generators[j] = 1

        best_solution = assigned_generators, opened_generators

        initial_temp = 90
        final_temp = .1
        alpha = 0.01
        current_temp = initial_temp
        
        while current_temp > final_temp :
            neighbors = self.getNeighbors(assigned_generators, opened_generators)
            best_neighbor = random.choice(list(neighbors.values()))
            cost_diff = self.getCost(best_solution[0], best_solution[1]) - self.getCost(best_neighbor[0], best_neighbor[1])
            if cost_diff > 0 :
                best_solution = best_neighbor
                assigned_generators = best_solution[0]
                opened_generators = best_solution[1]
            else :
                if random.uniform(0,1) < math.exp(cost_diff/current_temp):
                    best_solution = best_neighbor
                    assigned_generators = best_solution[0]
                    opened_generators = best_solution[1]
            current_temp -= alpha
            print(self.getCost(best_solution[0], best_solution[1]))

        self.printSolution(assigned_generators, opened_generators)
    
    def getCost(self, assigned_generators, opened_generators) :
        return self.instance.get_solution_cost(assigned_generators, opened_generators)
    
    def selectNeighbors(self, neighbors, generator, countGenerator):
        bestNeighbors = {}
        for key in neighbors:
            print(neighbors[key])
            if neighbors[key][0].count(generator) < countGenerator:
                bestNeighbors[key] = neighbors[key]
        return bestNeighbors

    def getNeighbors(self, assigned_generators, opened_generators) :
        neighbors = {}
        for i in range(self.n_device) :

            for j in range(self.n_generator) :
                opened_generators_temp = list(opened_generators)
                assigned_generators_temp = list(assigned_generators)
                if assigned_generators[i] != j :
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
        self.instance.plot_solution(assigned_generators, opened_generators, "local_search")

        print("[ASSIGNED-GENERATOR]", assigned_generators)
        print("[OPENED-GENERATOR]", opened_generators)
        print("[SOLUTION-COST]", total_cost)

    def getDistance(self, i, j) :
        return self.instance.get_distance(self.instance.device_coordinates[i][0],
                    self.instance.device_coordinates[i][1],
                    self.instance.generator_coordinates[j][0],
                    self.instance.generator_coordinates[j][1])

    def getZone(self, id, type):
        coordinates = (0,0)
        if type == 1 :
            coordinates = self.instance.generator_coordinates[id]
        elif type == 2 :
            coordinates = self.instance.device_coordinates[id]
        if (coordinates[0] >= 0 and 
            coordinates[0] <=  50 and
            coordinates[1] >= 50 and
            coordinates[1] <= 100) :
            return 1
        elif (coordinates[0] >= 50 and
        coordinates[0] <=  100 and
        coordinates[1] >= 50 and
        coordinates[1] <= 100) :
            return 2
        elif (coordinates[0] >= 0 and 
        coordinates[0] <=  50 and
        coordinates[1] >= 0 and
        coordinates[1] <= 100) :
            return 3
        elif (coordinates[0] >= 50 and 
        coordinates[0] <=  100 and
        coordinates[1] >= 0 and
        coordinates[1] <= 50) :
            return 4






