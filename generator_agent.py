
from mesa import Agent
import random

class GeneratorAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
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
            print(
                f"Generator {self.unique_id} retiring due to sustained unprofitability."
            )
            self.remove()
            return

        # Investment decision based on return
        expected_profit = self.last_year_revenue - self.last_year_cost
        if expected_profit > 0 and random.random() < 0.2:
            new_capacity = GeneratorAgent(self.model)
            print(
                f"New Generator {new_capacity.unique_id} added due to expected profitability."
            )
