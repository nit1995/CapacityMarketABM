
from mesa import Model
from mesa.time import BaseScheduler
from discom_agent import DISCOMAgent
from generator_agent import GeneratorAgent
from regulator_agent import RegulatorAgent
from collections import defaultdict

class CapacityMarketModel(Model):
    def __init__(self, num_discoms, num_generators, years, market_type="centralized"):
        super().__init__()
        self.num_discoms = num_discoms
        self.num_generators = num_generators
        self.years = years
        self.market_type = market_type
        self.schedule = BaseScheduler(self)
        self.year = 0

        self.metrics = {
            'installed_capacity': [],
            'retired_generators': [],
            'new_generators': [],
            'total_procurement_cost': [],
            'unserved_energy': [],
            'technology_wise_capacity': []
        }

        self.regulator = RegulatorAgent(self.next_id(), self, market_type)
        self.schedule.add(self.regulator)

        for i in range(num_discoms):
            agent = DISCOMAgent(self.next_id(), self)
            self.schedule.add(agent)

        for j in range(num_generators):
            agent = GeneratorAgent(self.next_id(), self)
            self.schedule.add(agent)

    def step(self):
        print(f"\n--- Year {self.year} ---")
        pre_agents = len([a for a in self.schedule.agents if isinstance(a, GeneratorAgent)])
        self.schedule.step()
        post_agents = len([a for a in self.schedule.agents if isinstance(a, GeneratorAgent)])

        total_capacity = sum(a.capacity for a in self.schedule.agents if isinstance(a, GeneratorAgent))
        discom_costs = sum(a.total_cost for a in self.schedule.agents if isinstance(a, DISCOMAgent))
        unserved = sum(
            max(0, a.forecasted_peak_demand * 1.1 - a.procured_capacity)
            for a in self.schedule.agents if isinstance(a, DISCOMAgent)
        )

        techwise = defaultdict(float)
        for a in self.schedule.agents:
            if isinstance(a, GeneratorAgent):
                techwise[a.technology] += a.capacity

        self.metrics['installed_capacity'].append(total_capacity)
        self.metrics['retired_generators'].append(max(0, pre_agents - post_agents))
        self.metrics['new_generators'].append(max(0, post_agents - pre_agents))
        self.metrics['total_procurement_cost'].append(discom_costs)
        self.metrics['unserved_energy'].append(unserved)
        self.metrics['technology_wise_capacity'].append(dict(techwise))

        self.year += 1

    def report_results(self):
        print("\n--- Final Report ---")
        for agent in self.schedule.agents:
            if isinstance(agent, DISCOMAgent):
                print(f"DISCOM {agent.unique_id}: Total Cost = {agent.total_cost:.2f}, Procured = {agent.procured_capacity:.2f}, Demand = {agent.forecasted_peak_demand:.2f}")
