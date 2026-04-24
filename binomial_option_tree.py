import math
import networkx as nx
import matplotlib.pyplot as plt

# --- 1. Define Parameters ---
S0 = 100.0     # Initial Stock Price
K = 100.0      # Strike Price
u = 1.1        # Up factor
d = 0.9        # Down factor
r = 0.05       # Risk-free rate
T = 1.0        # Time to expiration in years
steps = 2      # Number of steps in the tree

# Calculate step-adjusted variables
dt = T / steps
p = (math.exp(r * dt) - d) / (u - d)
discount = math.exp(-r * dt)

# Dictionaries to store calculated values mapped by (step, up_moves)
stock_prices = {}
option_values = {}

# --- 2. Calculate Terminal Payoffs (Time = 2) ---
for i in range(steps + 1):
    # i represents the number of upward moves
    down_moves = steps - i
    price = S0 * (u ** i) * (d ** down_moves)
    stock_prices[(steps, i)] = price
    option_values[(steps, i)] = max(0, price - K)  # European Call formula

# --- 3. Backward Induction (Time = 1 to 0) ---
for step in range(steps - 1, -1, -1):
    for i in range(step + 1):
        # Calculate stock price at this node
        price = S0 * (u ** i) * (d ** (step - i))
        stock_prices[(step, i)] = price
        
        # Calculate option value based on the two future nodes
        val_up = option_values[(step + 1, i + 1)]
        val_down = option_values[(step + 1, i)]
        option_values[(step, i)] = discount * (p * val_up + (1 - p) * val_down)

# --- 4. Build and Visualize the Tree ---
G = nx.DiGraph()
pos = {}
labels = {}

# Create nodes, set positions for plotting, and format text labels
for step in range(steps + 1):
    for i in range(step + 1):
        node_id = f"{step}_{i}"
        G.add_node(node_id)
        
        # X-axis is the step. Y-axis is the vertical spread (Up moves - Down moves)
        pos[node_id] = (step, i - (step - i)) 
        
        # Format the text inside the bubble
        labels[node_id] = f"S: {stock_prices[(step, i)]:.2f}\nC: {option_values[(step, i)]:.2f}"
        
        # Connect nodes with directional edges
        if step < steps:
            G.add_edge(node_id, f"{step+1}_{i+1}") # Path if stock goes up
            G.add_edge(node_id, f"{step+1}_{i}")   # Path if stock goes down

# Plotting settings
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=False, node_size=4000, node_color="lightgreen", arrows=True)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_weight="bold")

plt.title(f"Binomial Option Tree (T={T} year, dt={dt:.2f})")
plt.axis("off")
plt.show()