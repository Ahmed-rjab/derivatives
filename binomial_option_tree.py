import math
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox

# Professional light theme palette
COLORS = {
    "figure_bg": "#e9edf2",
    "panel_bg": "#f2f4f7",
    "node_fill": "#dbeafe",
    "node_edge": "#1e3a8a",
    "edge": "#334155",
    "title": "#0f172a",
    "text": "#0f172a",
    "error": "#b91c1c",
    "slider_track": "#dde3ea",
    "slider_active": "#0f766e",
    "input_bg": "#eef2f6",
    "input_edge": "#94a3b8",
}

def compute_tree(s0, k, u, d, r, t, steps):
    if steps < 1:
        raise ValueError("steps must be at least 1")
    if u <= d:
        raise ValueError("u must be greater than d")

    dt = t / steps
    p = (math.exp(r * dt) - d) / (u - d)
    if p < 0 or p > 1:
        raise ValueError("Choose parameters with 0 <= p <= 1")

    discount = math.exp(-r * dt)
    stock_prices = {}
    option_values = {}

    for i in range(steps + 1):
        down_moves = steps - i
        price = s0 * (u ** i) * (d ** down_moves)
        stock_prices[(steps, i)] = price
        option_values[(steps, i)] = max(0, price - k)

    for step in range(steps - 1, -1, -1):
        for i in range(step + 1):
            price = s0 * (u ** i) * (d ** (step - i))
            stock_prices[(step, i)] = price
            val_up = option_values[(step + 1, i + 1)]
            val_down = option_values[(step + 1, i)]
            option_values[(step, i)] = discount * (p * val_up + (1 - p) * val_down)

    return stock_prices, option_values, dt


def build_graph(steps, stock_prices, option_values):
    graph = nx.DiGraph()
    pos = {}
    labels = {}

    for step in range(steps + 1):
        for i in range(step + 1):
            node_id = f"{step}_{i}"
            graph.add_node(node_id)
            pos[node_id] = (step, i - (step - i))
            labels[node_id] = f"S: {stock_prices[(step, i)]:.2f}\nC: {option_values[(step, i)]:.2f}"
            if step < steps:
                graph.add_edge(node_id, f"{step + 1}_{i + 1}")
                graph.add_edge(node_id, f"{step + 1}_{i}")

    return graph, pos, labels


def draw_tree(ax, s0, k, u, d, r, t, steps):
    ax.clear()
    ax.set_facecolor(COLORS["panel_bg"])
    try:
        stock_prices, option_values, dt = compute_tree(s0, k, u, d, r, t, steps)
        graph, pos, labels = build_graph(steps, stock_prices, option_values)
        nx.draw(
            graph,
            pos,
            ax=ax,
            with_labels=False,
            node_size=3800,
            node_color=COLORS["node_fill"],
            edgecolors=COLORS["node_edge"],
            linewidths=1.4,
            edge_color=COLORS["edge"],
            arrowsize=14,
            arrows=True,
        )
        nx.draw_networkx_labels(
            graph,
            pos,
            labels=labels,
            ax=ax,
            font_size=9,
            font_weight="bold",
            font_color=COLORS["text"],
        )
        ax.set_title(
            f"Binomial Option Tree (dt={dt:.3f}, steps={steps})",
            fontsize=14,
            fontweight="semibold",
            color=COLORS["title"],
            pad=12,
        )
    except ValueError as exc:
        ax.text(
            0.5,
            0.5,
            str(exc),
            ha="center",
            va="center",
            transform=ax.transAxes,
            color=COLORS["error"],
            fontsize=11,
            fontweight="semibold",
        )
        ax.set_title("Invalid Parameter Combination", color=COLORS["error"], fontsize=14, fontweight="semibold")

    ax.axis("off")


# Initial values
S0 = 100.0
K = 100.0
u = 1.1
d = 0.9
r = 0.05
T = 1.0
steps = 2

# Main figure + room for sliders
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor(COLORS["figure_bg"])
plt.subplots_adjust(left=0.1, right=0.95, top=0.92, bottom=0.38)

draw_tree(ax, S0, K, u, d, r, T, steps)

# Slider controls
ax_s0 = plt.axes((0.12, 0.30, 0.58, 0.03))
ax_k = plt.axes((0.12, 0.26, 0.58, 0.03))
ax_u = plt.axes((0.12, 0.22, 0.58, 0.03))
ax_d = plt.axes((0.12, 0.18, 0.58, 0.03))
ax_r = plt.axes((0.12, 0.14, 0.58, 0.03))
ax_t = plt.axes((0.12, 0.10, 0.58, 0.03))
ax_steps = plt.axes((0.12, 0.06, 0.58, 0.03))

txt_s0 = plt.axes((0.74, 0.30, 0.14, 0.03))
txt_k = plt.axes((0.74, 0.26, 0.14, 0.03))
txt_u = plt.axes((0.74, 0.22, 0.14, 0.03))
txt_d = plt.axes((0.74, 0.18, 0.14, 0.03))
txt_r = plt.axes((0.74, 0.14, 0.14, 0.03))
txt_t = plt.axes((0.74, 0.10, 0.14, 0.03))
txt_steps = plt.axes((0.74, 0.06, 0.14, 0.03))

s_s0 = Slider(ax_s0, "S0", 10.0, 300.0, valinit=S0)
s_k = Slider(ax_k, "K", 10.0, 300.0, valinit=K)
s_u = Slider(ax_u, "u", 1.01, 2.0, valinit=u)
s_d = Slider(ax_d, "d", 0.01, 0.99, valinit=d)
s_r = Slider(ax_r, "r", 0.0, 0.2, valinit=r)
s_t = Slider(ax_t, "T", 0.1, 5.0, valinit=T)
s_steps = Slider(ax_steps, "steps", 1, 8, valinit=steps, valstep=1)

b_s0 = TextBox(txt_s0, "", initial=f"{S0:.2f}")
b_k = TextBox(txt_k, "", initial=f"{K:.2f}")
b_u = TextBox(txt_u, "", initial=f"{u:.3f}")
b_d = TextBox(txt_d, "", initial=f"{d:.3f}")
b_r = TextBox(txt_r, "", initial=f"{r:.3f}")
b_t = TextBox(txt_t, "", initial=f"{T:.2f}")
b_steps = TextBox(txt_steps, "", initial=f"{steps:d}")


def style_slider(slider):
    slider.ax.set_facecolor(COLORS["slider_track"])
    slider.poly.set_facecolor(COLORS["slider_active"])
    slider.valtext.set_color(COLORS["text"])
    slider.label.set_color(COLORS["text"])
    slider.label.set_fontweight("semibold")
    for spine in slider.ax.spines.values():
        spine.set_edgecolor("none")


def style_textbox(box):
    box.ax.set_facecolor(COLORS["input_bg"])
    for spine in box.ax.spines.values():
        spine.set_edgecolor(COLORS["input_edge"])
        spine.set_linewidth(1.0)
    if hasattr(box, "text_disp"):
        box.text_disp.set_color(COLORS["text"])


for slider in [s_s0, s_k, s_u, s_d, s_r, s_t, s_steps]:
    style_slider(slider)

for box in [b_s0, b_k, b_u, b_d, b_r, b_t, b_steps]:
    style_textbox(box)

sync_state = {"updating": False}


def on_change(_):
    draw_tree(
        ax,
        s_s0.val,
        s_k.val,
        s_u.val,
        s_d.val,
        s_r.val,
        s_t.val,
        int(s_steps.val),
    )
    sync_state["updating"] = True
    b_s0.set_val(f"{s_s0.val:.2f}")
    b_k.set_val(f"{s_k.val:.2f}")
    b_u.set_val(f"{s_u.val:.3f}")
    b_d.set_val(f"{s_d.val:.3f}")
    b_r.set_val(f"{s_r.val:.3f}")
    b_t.set_val(f"{s_t.val:.2f}")
    b_steps.set_val(f"{int(s_steps.val):d}")
    sync_state["updating"] = False
    fig.canvas.draw_idle()


def bind_textbox(box, slider, formatter, parser=float):
    def _submit(text):
        if sync_state["updating"]:
            return
        try:
            value = parser(text)
            slider.set_val(value)
        except ValueError:
            sync_state["updating"] = True
            box.set_val(formatter(slider.val))
            sync_state["updating"] = False

    box.on_submit(_submit)


bind_textbox(b_s0, s_s0, lambda v: f"{v:.2f}")
bind_textbox(b_k, s_k, lambda v: f"{v:.2f}")
bind_textbox(b_u, s_u, lambda v: f"{v:.3f}")
bind_textbox(b_d, s_d, lambda v: f"{v:.3f}")
bind_textbox(b_r, s_r, lambda v: f"{v:.3f}")
bind_textbox(b_t, s_t, lambda v: f"{v:.2f}")
bind_textbox(b_steps, s_steps, lambda v: f"{int(v):d}", parser=lambda x: int(float(x)))


s_s0.on_changed(on_change)
s_k.on_changed(on_change)
s_u.on_changed(on_change)
s_d.on_changed(on_change)
s_r.on_changed(on_change)
s_t.on_changed(on_change)
s_steps.on_changed(on_change)

plt.show()