# -*- coding: utf-8 -*-
from generator_problem import GeneratorProblem
import random


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
            assigned_generators[i] = random.randint(0, self.n_generator-1)

        for i in range(len(assigned_generators)) :
            j = assigned_generators[i]
            opened_generators[j] = 1

        solutions_found = {} #pour stocker toutes les solutions trouvées et retourner à une meilleure précédente si nécessaire
        best_solution = assigned_generators, opened_generators
        solutions_found[self.instance.get_solution_cost(best_solution[0], best_solution[1])] = best_solution

        #voisins possibles
        neighbors = {}
        for i in range(self.n_device) :
            opened_generators_temp = list(opened_generators)
            assigned_generators_temp = list(assigned_generators)
            for j in range(self.n_generator) :
                if assigned_generators[i] != j :
                    assigned_generators_temp[i] = j
                    opened_generators_temp[j] = 1
                    if assigned_generators_temp[i] not in assigned_generators_temp :
                        opened_generators_temp[j] = 0
                    new_solution = assigned_generators_temp, opened_generators_temp
                neighbors[self.instance.get_solution_cost(new_solution[0], new_solution[1])] = new_solution




                




        zone1 = {}
        zone2 = {}
        zone3 = {}
        zone4 = {}

        for generator in generators :
            zone = self.getZone(generator, 1)
            if zone == 1 :
                zone1[generator] = self.instance.opening_cost[generator]
            elif zone == 2 :
                zone2[generator] = self.instance.opening_cost[generator]
            elif zone == 3 :
                zone3[generator] = self.instance.opening_cost[generator]
            elif zone == 4 :
                zone4[generator] = self.instance.opening_cost[generator]

        costs[1] = zone1
        costs[2] = zone2
        costs[3] = zone3
        costs[4] = zone4

        for i in range(self.n_device):
            zone = self.getZone(i,2)
            min_cost_gen = min(costs[zone], key=costs[zone].get)
            opened_generators[assigned_generators[i]] = 0
            assigned_generators[i] = min_cost_gen
            opened_generators[min_cost_gen] = 1
        
        self.printSolution(assigned_generators, opened_generators)

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






