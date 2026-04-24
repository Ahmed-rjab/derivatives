import numpy   as np

PREMIUM = 21.7
MULTIPLIER = 100
S_T = 320
SPOT = 360

gross_payoff = np.max(SPOT - S_T, 0) * MULTIPLIER

init_cost = PREMIUM * MULTIPLIER

net_profit = gross_payoff - init_cost 

print(net_profit)