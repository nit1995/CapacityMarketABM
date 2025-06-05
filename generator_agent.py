
from mesa import Agent
import random

class GeneratorAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.capacity = random.uniform(50, 500)
        self.technology = random.choice(["coal", "solar", "wind", "battery"])
        self.fixed_cost = random.uniform(1000, 2000)
        self.available = True
        self.years_unprofitable = 0
        self.last_year_revenue = 0
        self.last_year_cost = self.fixed_cost

    def bid_price(self):
        return self.fixed_cost / 12  # Monthly price

    def step(self):
        self.available = random.random() > 0.05

        # Retirement decision
        if self.years_unprofitable >= 3:
            print(f"Generator {self.unique_id} retiring due to sustained unprofitability.")
            self.model.schedule.remove(self)
            return

        # Investment decision based on return
        expected_profit = self.last_year_revenue - self.last_year_cost
        if expected_profit > 0 and random.random() < 0.2:
            new_capacity = GeneratorAgent(self.model.next_id(), self.model)
            self.model.schedule.add(new_capacity)
            print(f"New Generator {new_capacity.unique_id} added due to expected profitability.")
