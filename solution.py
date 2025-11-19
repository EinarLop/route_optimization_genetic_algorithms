import math
import random
from collections import defaultdict

number_customers = 5

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

    def calculate_individual_fitness(self, individual):
        fitness_score = 0
        return fitness_score

    def calculate_population_fitness(self):
        for individual in self.population:
           fitness_score = self.calculate_individual_fitness(individual)
           self.population_fitness.append(fitness_score)

    def euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


    def run(self):
        self.extract_sub_sub_orders()
        self.generate_initial_population()

test = RouteOptimization(2, number_customers, customer_locations, items, orders, 1000, 60)

test.run()