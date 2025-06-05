
from mesa import Agent
import random

class DISCOMAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.forecasted_peak_demand = random.uniform(500, 1000)
        self.procured_capacity = 0
        self.total_cost = 0

    def step(self):
        self.forecasted_peak_demand *= 1.03
        needed_capacity = self.forecasted_peak_demand * 1.1

        if self.model.market_type == "centralized":
            procured, cost = self.model.regulator.centralized_auction(self, needed_capacity)
        else:
            procured, cost = self.model.regulator.bilateral_contracts(self, needed_capacity)

        self.procured_capacity = procured
        self.total_cost += cost
