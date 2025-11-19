from itertools import cycle
import math
import random
from collections import defaultdict, deque
from typing import Dict, List, Tuple

number_customers = 5

vehicle_capacity = 60.0  # in kilograms

customer_locations = {
    1: (35, 115),
    2: (50, 140),
    3: (70, 100),
    4: (40, 80),
    5: (25, 60),
}

items = {
    1: 1.2,
    2: 3.8,
    3: 7.5,
    4: 0.9,
    5: 15.4,
    6: 12.1,
    7: 4.3,
    8: 19.7,
    9: 8.6,
    10: 2.5
}

warehouse_location = (0,0)

orders = {
    1: [{'item': 3, 'unit': 2}, {'item': 1, 'unit': 3}],
    2: [{'item': 2, 'unit': 6}],
    3: [{'item': 7, 'unit': 4}, {'item': 5, 'unit': 2}],
    4: [{'item': 3, 'unit': 8}],
    5: [{'item': 6, 'unit': 5}, {'item': 9, 'unit': 2}],
}

class RouteOptimization:
    def __init__(self, num_vehicles, number_customers, customer_locations, items, orders, population_size,max_load_vehicle, mutation_rate, generations):
        self.population = []
        self.num_vehicles = num_vehicles
        self.customers = list(range(1, number_customers+1))
        self.customer_locations = customer_locations
        self.items = items
        self.orders = orders
        self.population_size = population_size
        self.population_fitness = []
        self.order_weights = {}
        self.max_load_vehicle = max_load_vehicle
        self.sub_sub_orders = []
        self.mutation_rate = mutation_rate
        self.generations = generations

    def extract_sub_sub_orders(self):
        for key, value in self.orders.items():
            for sub_order in value:
                current_sub_sub_order = {
                    'item': sub_order['item'],
                    'cords': customer_locations[key],
                    'weight': items[sub_order['item']]
                }
                for _ in range(sub_order['unit']):
                    self.sub_sub_orders.append(current_sub_sub_order)

    def generate_initial_population(self):
        self.population = []
        arr_idx_sub_sub_orders = list(range(len(self.sub_sub_orders)))
        for _ in range(self.population_size):
            temp = arr_idx_sub_sub_orders.copy()
            random.shuffle(temp)
            self.population.append(temp)

    # All items need to be delivered
    # Items can only be delivered once
    def evaluate_constraint_1(self, individual):
        fitness_score = 0
        arr_idx_sub_sub_orders = list(range(len(self.sub_sub_orders)))
        for item in arr_idx_sub_sub_orders:
            if individual.count(item) == 0:
                fitness_score += 10
                print("Constraint 1 applied")
            elif individual.count(item) > 1:
                fitness_score += 10
                print("Constraint 1 applied")

        return fitness_score

    def euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def decode_routes(self, individual: List[int]) -> Dict[int, Tuple[float, float]]:
        vehicle_iterator = cycle(range(self.num_vehicles))
        vehicle_routes = {vehicle: [warehouse_location] for vehicle in range(self.num_vehicles)}
        vehicle_loads = defaultdict(float)
        genotype_deque = deque(individual)
        for vehicle in vehicle_iterator:
            while genotype_deque:
                shipment_key = genotype_deque.popleft()
                if vehicle_loads[vehicle] + self.sub_sub_orders[shipment_key]['weight'] <= vehicle_capacity:
                    vehicle_loads[vehicle] += self.sub_sub_orders[shipment_key]['weight']
                    if vehicle_routes[vehicle][-1] != self.sub_sub_orders[shipment_key]['cords']:
                        vehicle_routes[vehicle].append(self.sub_sub_orders[shipment_key]['cords'])
                else:
                    break
            vehicle_routes[vehicle].append(warehouse_location)
            vehicle_loads[vehicle] = 0.0
            if not genotype_deque:
                break
        return vehicle_routes

    # Minimizing the distance of the routes
    def evaluate_constraint_2(self, individual: List[int]) -> float:
        total_distance = 0.0
        vehicle_routes = self.decode_routes(individual)
        vehicles_distances = defaultdict(float)
        for vehicle, route in vehicle_routes.items():
            if len(route) > 1:
                for i in range(len(route) - 1):
                    vehicles_distances[vehicle] += self.euclidean_distance(route[i], route[i + 1])
            total_distance += vehicles_distances[vehicle]
        return total_distance

    def calculate_individual_fitness(self, individual):
        fitness_score = 0
        fitness_score += self.evaluate_constraint_1(individual)
        fitness_score += self.evaluate_constraint_2(individual)
        return fitness_score

    def calculate_population_fitness(self):
        self.population_fitness = []
        for individual in self.population:
           fitness_score = self.calculate_individual_fitness(individual)
           self.population_fitness.append(fitness_score)

    # Selection based on elitism, the two parents with the max fitness are selected
    # Returns best individuals
    def select_parents(self):
        sorted_indices_and_values = sorted(enumerate(self.population_fitness), key=lambda x: x[1])
        index_of_max1 = sorted_indices_and_values[0][0]
        index_of_max2 = sorted_indices_and_values[1][0]
        # print(f"Parent 1 : {self.population[index_of_max1]}")
        print(f"Parent 1 Fitness: {self.population_fitness[index_of_max1]}")
        # print(f"Parent 2 : {self.population[index_of_max2]}")
        print(f"Parent 2 Fitness: {self.population_fitness[index_of_max2]}")

        return self.population[index_of_max1], self.population[index_of_max2]

    def ox1_crossover(self, parent_1, parent_2):
        size = len(parent_1)
        # Choose two random crossover points
        cx_point1, cx_point2 = sorted(random.sample(range(size), 2))

        # Initialize child with None (or -1)
        child = [None] * size

        # 2. Copy the sub-segment from Parent 1
        child[cx_point1:cx_point2] = parent_1[cx_point1:cx_point2]

        # 3. Fill remaining slots with Parent 2 genes
        # Start reading P2 and filling Child from the index immediately after the second cut
        p2_index = cx_point2
        child_index = cx_point2

        filled_count = 0
        total_to_fill = size - (cx_point2 - cx_point1)

        while filled_count < total_to_fill:
            # Get gene from P2, wrapping around using modulo
            gene = parent_2[p2_index % size]

            # If gene is not already in the child, insert it
            if gene not in child:
                child[child_index % size] = gene
                child_index += 1
                filled_count += 1

            p2_index += 1

        return child

    def generate_new_population(self, parent_1, parent_2):
        self.population = []
        while len(self.population) < self.population_size:
            # Generate a pair of children
            child_1 = self.ox1_crossover(parent_1, parent_2)
            child_2 = self.ox1_crossover(parent_2, parent_1)

            # Add first child
            self.population.append(child_1)

            # Add second child only if we haven't reached size n yet
            if len(self.population) < self.population_size:
                self.population.append(child_2)

    def swap_mutation(self):
        for individual in self.population:
            if random.random() < self.mutation_rate:
                idx1, idx2 = random.sample(range(len(individual)), 2)
                individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

    def run(self):
        self.extract_sub_sub_orders()
        self.generate_initial_population()

        for i in range(self.generations):
            print(f"Generation {i+1}")
            self.calculate_population_fitness()
            parent_1, parent_2 = self.select_parents()
            self.generate_new_population(parent_1, parent_2)
            self.swap_mutation()

test = RouteOptimization(2, number_customers, customer_locations, items, orders, 100, 60,0.1,100)

test.run()