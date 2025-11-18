import math
import random

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

orders = {
    1: [{'item': 3, 'unit': 2}, {'item': 1, 'unit': 3}],
    2: [{'item': 2, 'unit': 6}],
    3: [{'item': 7, 'unit': 4}, {'item': 5, 'unit': 2}],
    4: [{'item': 3, 'unit': 8}],
    5: [{'item': 6, 'unit': 5}, {'item': 9, 'unit': 2}],
}

class RouteOptimization:
    def __init__(self, num_vehicles, number_customers, customer_locations, items, orders, population_size):
        self.population = []
        self.num_vehicles = num_vehicles
        self.customers = list(range(1, number_customers+1))
        self.customer_locations = customer_locations
        self.items = items
        self.orders = orders
        self.population_size = population_size
        self.population_fitness = []

    def generate_individual(self):
        # Considering that the worst case scenario is to go back to the warehouse after each customer
        max_length_per_vehicle = math.ceil((len(self.customers) * 2) / self.num_vehicles)
        # Considering that 0 represents the warehouse
        min_val = 0
        max_val = self.customers[-1]

        vehicles = []

        for i in range(self.num_vehicles):
            current_vehicle_length = random.randint(1, max_length_per_vehicle)
            current_vehicle_load = [random.randint(min_val, max_val) for _ in range(current_vehicle_length)]
            vehicles.append(current_vehicle_load)
        return vehicles

    def generate_population(self):
        return [self.generate_individual() for x in range(self.population_size)]

    # Each customer is visited only once.
    def evaluate_constraint_1(self, individual):
        flatten_individual = [item for sublist in individual for item in sublist]

        if len(flatten_individual) < len(self.customers):
            return False

        for customer in self.customers:
            if flatten_individual.count(customer) != 1:
                return False

        return True

    def calculate_fitness(self, individual):
        current_fitness = 0
        if not self.evaluate_constraint_1(individual):
            current_fitness += -100
        else:
            current_fitness += 100
        return current_fitness

    def evaluate_population(self):
        print(self.customers)
        self.population_fitness = []
        for individual in self.population:
            calculate_fitness = self.calculate_fitness(individual)
            self.population_fitness.append(calculate_fitness)

    def run(self):
        self.population = self.generate_population()
        self.evaluate_population()
        print(sorted(self.population_fitness)[-1])

test = RouteOptimization(2, number_customers, customer_locations, items, orders, 100)

test.run()