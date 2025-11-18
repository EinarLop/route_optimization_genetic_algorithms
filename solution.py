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

    def euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def generate_order_weights(self):
        for key, value in self.orders.items():
            for order in value:

                if self.order_weights.get(key) is None:
                    self.order_weights[key] = 0

                self.order_weights[key] += items[order['item']] * order['unit']

        print(self.order_weights)


    def generate_individual(self):
        # Considering that the worst case scenario is to go back to the warehouse after each customer
        max_length_per_vehicle = math.ceil((len(self.customers) * 2) / self.num_vehicles)
        # Considering that 0 represents the warehouse
        min_val = 0
        max_val = self.customers[-1]

        vehicles = []

        for i in range(self.num_vehicles):
            # Min. length of 3, vehicle needs to at least consider warehouse, 1 stop and return to warehouse
            current_vehicle_length = random.randint(3, max_length_per_vehicle)
            current_vehicle_load = [random.randint(min_val, max_val) for _ in range(current_vehicle_length)]
            vehicles.append(current_vehicle_load)
        return vehicles

    def generate_population(self):
        return [self.generate_individual() for x in range(self.population_size)]

    # CHANGE TO CONSIDER SUB ORDERS
    # Each customer is visited only once. Returns fitness score
    def evaluate_constraint_1(self, individual):
        flatten_individual = [item for sublist in individual for item in sublist]

        if len(flatten_individual) < len(self.customers):
            return 100

        for customer in self.customers:
            if flatten_individual.count(customer) != 1:
                return 100
        return 0

    # Route starts and ends at warehouse. Returns fitness score.
    def evaluate_constraint_2(self, individual):
        current_fitness = 0
        for vehicle in individual:
            if vehicle[0] != 0 and vehicle[-1] != 0:
                current_fitness += 100
            else:
                current_fitness += 0
        return current_fitness

    # Overload is not allowed
    def evaluate_constraint_3(self, individual):
        pass

    def calculate_fitness(self, individual):
        current_fitness = 0
        current_fitness += self.evaluate_constraint_1(individual)
        current_fitness += self.evaluate_constraint_2(individual)
        if current_fitness == 0:
            print("Constraint 3 Evaluation:")
            current_fitness += self.evaluate_constraint_3(individual)

        return current_fitness

    def evaluate_population(self):
        self.population_fitness = []
        for i, individual in enumerate(self.population):
            calculate_fitness = self.calculate_fitness(individual)
            self.population_fitness.append(calculate_fitness)

            print(f"Individual {i} : {self.population[i]}, \n Fitness: {self.population_fitness[i]}")

    def run(self):
        self.generate_order_weights()
        self.population = self.generate_population()
        self.evaluate_population()

test = RouteOptimization(2, number_customers, customer_locations, items, orders, 1000, 60)

test.run()