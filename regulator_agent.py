
from mesa import Agent
import random

class RegulatorAgent(Agent):
    def __init__(self, unique_id, model, market_type):
        super().__init__(unique_id, model)
        self.reserve_margin = 0.1
        self.market_type = market_type

    def centralized_auction(self, discom, needed_capacity):
        generators = [a for a in self.model.schedule.agents if hasattr(a, 'bid_price')]
        generators.sort(key=lambda g: g.bid_price())

        total = 0
        cost = 0
        for g in generators:
            g.available = random.random() > 0.05
            if not g.available:
                continue
            alloc = min(g.capacity, needed_capacity - total)
            total += alloc
            bid = g.bid_price()
            alloc_cost = bid * alloc
            cost += alloc_cost
            g.last_year_revenue = alloc_cost
            if alloc < g.capacity:
                g.years_unprofitable += 1
            else:
                g.years_unprofitable = 0
            if total >= needed_capacity:
                break
        return total, cost

    def bilateral_contracts(self, discom, needed_capacity):
        generators = [a for a in self.model.schedule.agents if hasattr(a, 'bid_price')]
        random.shuffle(generators)
        total = 0
        cost = 0
        for g in generators:
            g.available = random.random() > 0.05
            if not g.available:
                continue
            alloc = min(g.capacity, needed_capacity - total)
            price = g.bid_price() * (1 + 0.1 * random.random())
            alloc_cost = price * alloc
            total += alloc
            cost += alloc_cost
            g.last_year_revenue = alloc_cost
            if alloc < g.capacity:
                g.years_unprofitable += 1
            else:
                g.years_unprofitable = 0
            if total >= needed_capacity:
                break
        return total, cost

    def step(self):
        pass
