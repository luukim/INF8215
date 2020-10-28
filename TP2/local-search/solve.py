
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

        opened_generators = [0 for _ in range(self.n_generator)]
        generators = list(range(0, self.n_generator))
        assigned_generators = [None for _ in range(self.n_device)]
        max_distance = 0 #distance maximale dans la solution
        distances = {}
        #solution initiale
        for i in range(self.n_device):
            assigned_generators[i] = random.randint(0, self.n_generator-1)

        for i in range(len(assigned_generators)) :
            j = assigned_generators[i]
            distances[(i, j)] = self.getDistance(i,j)

        max_distance = max(distances, key=distances.get)

        for i in range(self.n_device):
            # print(distances)
            # print(max_distance)
            neighbors = list(generators)
            neighbors.pop(max_distance[1])
            tempNeighbor = 0
            isSmaller = 0
            closestDistance = distances[max_distance]
            for j in neighbors:
                if closestDistance > self.getDistance(max_distance[0], j):
                    tempNeighbor = j
                    closestDistance = self.getDistance(max_distance[0],j)
                    isSmaller = 1

            # print(tempNeighbor)
            if isSmaller:
                assigned_generators[max_distance[0]] = tempNeighbor
            distances.pop(max_distance)
            #distances[(max_distance[0], tempNeighbor)] = closestDistance
            if (len(distances) == 0):
                break
            max_distance = max(distances, key=distances.get)

        for i in range(len(assigned_generators)):
            opened_generators[assigned_generators[i]] = 1

        
        self.instance.solution_checker(assigned_generators, opened_generators)
        total_cost = self.instance.get_solution_cost(assigned_generators, opened_generators)
        self.instance.plot_solution(assigned_generators, opened_generators, "local_search")

        print("[ASSIGNED-GENERATOR]", assigned_generators)
        print("[OPENED-GENERATOR]", opened_generators)
        print("[SOLUTION-COST]", total_cost)




