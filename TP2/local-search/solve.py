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

        self.instance.solution_checker(assigned_generators, opened_generators)
        total_cost = self.instance.get_solution_cost(assigned_generators, opened_generators)
        self.instance.plot_solution(assigned_generators, opened_generators, "naive")

        print("[ASSIGNED-GENERATOR]", assigned_generators)
        print("[OPENED-GENERATOR]", opened_generators)
        print("[SOLUTION-COST]", total_cost)


    def getDistance(self, i, j) :
        return self.instance.get_distance(self.instance.device_coordinates[i][0],
                    self.instance.device_coordinates[i][1],
                    self.instance.generator_coordinates[j][0],
                    self.instance.generator_coordinates[j][1])


    def solve_localSearch(self):
        print("Solve with a local search algorithm")
        visited_solutions = []

        opened_generators = [0 for _ in range(self.n_generator)]
        generators = list(range(0, self.n_generator))
        assigned_generators = [None for _ in range(self.n_device)]
        costs = {}
        #solution initiale
        for i in range(self.n_device):
            assigned_generators[i] = random.randint(0, self.n_generator-1)

        for i in range(len(assigned_generators)) :
            j = assigned_generators[i]
            costs[(i, j)] = self.getDistance(i,j)
            if not opened_generators[j]:
                costs[(i, j)] += self.instance.opening_cost[j]
                opened_generators[j] = 1
        solution_cost = self.instance.get_solution_cost(assigned_generators, opened_generators)
        for device_generator in costs:
            neighbors = list(generators) #liste des voisins possibles
            neighbors.pop(device_generator[1]) #on retire le voisin (generateur) dont le coût est le plus grand
            cost = 0
            assigned_generators[device_generator[0]] = -1
            if device_generator[1] not in assigned_generators :
                cost = solution_cost - self.getDistance(device_generator[0],device_generator[1]) - self.instance.opening_cost[device_generator[1]]
                opened_generators[device_generator[1]] = 0
            else :
                cost = solution_cost - self.getDistance(device_generator[0],device_generator[1])
            foundNewSolution = False
            for j in neighbors:
                if j not in assigned_generators :
                    new_cost = cost + self.getDistance(device_generator[0],j) + self.instance.opening_cost[j]
                else : 
                    new_cost = cost + self.getDistance(device_generator[0],j)
                if new_cost < solution_cost:
                    foundNewSolution = True
                    if not opened_generators[j]:
                        device_generator = self.getDistance(device_generator[0],j) + self.instance.opening_cost[j]
                    else : 
                        device_generator = self.getDistance(device_generator[0],j)
                    opened_generators[j] = 1
                    solution_cost = new_cost
                    assigned_generators[device_generator[0]] = j
            if not foundNewSolution :
                assigned_generators[device_generator[0]] = device_generator[1]
                opened_generators[device_generator[1]] = 1

        self.instance.solution_checker(assigned_generators, opened_generators)
        total_cost = self.instance.get_solution_cost(assigned_generators, opened_generators)
        self.instance.plot_solution(assigned_generators, opened_generators, "local_search")

        print("[ASSIGNED-GENERATOR]", assigned_generators)
        print("[OPENED-GENERATOR]", opened_generators)
        print("[SOLUTION-COST]", total_cost)




