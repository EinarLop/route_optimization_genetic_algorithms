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
    def __init__(self, num_vehicles, number_customers, customer_locations, items, orders, population_size,max_load_vehicle):
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

    def evaluate_constraint_1(self, individual):
        fitness_score = 0
        arr_idx_sub_sub_orders = list(range(len(self.sub_sub_orders)))
        for item in arr_idx_sub_sub_orders:
            if individual.count(item) == 0:
                fitness_score += 10
            elif individual.count(item) > 1:
                fitness_score += 10
        return fitness_score

    def evaluate_constraint_2(self, individual):
        pass
    def calculate_individual_fitness(self, individual):
        fitness_score = 0
        fitness_score += self.evaluate_constraint_1(individual)
        fitness_score += self.evaluate_constraint_2(individual)
        return fitness_score

    def calculate_population_fitness(self):
        for individual in self.population:
           fitness_score = self.calculate_individual_fitness(individual)
           self.population_fitness.append(fitness_score)
        print(self.population_fitness)

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
        
    def get_routes_total_distance(self, individual: List[int]) -> float:
        total_distance = 0.0
        vehicle_routes = self.decode_routes(individual)
        vehicles_distances = defaultdict(float)
        for vehicle, route in vehicle_routes.items():
            if len(route) > 1:
                for i in range(len(route) - 1):
                    vehicles_distances[vehicle] += self.euclidean_distance(route[i], route[i + 1])
            total_distance += vehicles_distances[vehicle]
        return total_distance
        

    def run(self):
        self.extract_sub_sub_orders()
        self.generate_initial_population()
        self.calculate_population_fitness()


test = RouteOptimization(2, number_customers, customer_locations, items, orders, 1000, 60)

test.run()