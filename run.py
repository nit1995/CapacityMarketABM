
from model import CapacityMarketModel
import matplotlib.pyplot as plt

model = CapacityMarketModel(num_discoms=5, num_generators=20, years=10, market_type="centralized")

for i in range(model.years):
    model.step()

model.report_results()

# Visualization
years = list(range(model.years))
installed_capacity = model.metrics['installed_capacity']
retired_generators = model.metrics['retired_generators']
new_generators = model.metrics['new_generators']
total_procurement_cost = model.metrics['total_procurement_cost']
unserved_energy = model.metrics['unserved_energy']
tech_capacity = model.metrics['technology_wise_capacity']

plt.figure(figsize=(12, 6))
plt.plot(years, installed_capacity, label='Installed Capacity (MW)')
plt.plot(years, retired_generators, label='Retired Generators')
plt.plot(years, new_generators, label='New Generators')
plt.plot(years, total_procurement_cost, label='Total DISCOM Cost (₹)', linestyle='--')
plt.plot(years, unserved_energy, label='Unserved Energy (MW)', linestyle=':')
plt.xlabel("Year")
plt.ylabel("Value")
plt.title("Capacity Market Simulation Metrics")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot technology-wise capacity
plt.figure(figsize=(12, 6))
for tech in tech_capacity[0].keys():
    plt.plot(years, [tc.get(tech, 0) for tc in tech_capacity], label=f'{tech} Capacity (MW)')
plt.xlabel("Year")
plt.ylabel("Installed Capacity (MW)")
plt.title("Technology-wise Installed Capacity")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
