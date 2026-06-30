#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# SAMPLE DATA
# ============================================================

np.random.seed(42)

x = np.linspace(0, 100, 500)
y = np.sin(x / 5) * 10 + x * 0.5 + np.random.randn(500) * 2

# ============================================================
# PLOT SETUP
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    x,
    y,
    label="Sample Data",
    color="blue",
    linewidth=2,
)

ax.set_title("TradingView-style Zoom with Crosshairs", fontsize=14)
ax.set_xlabel("Bars")
ax.set_ylabel("Price")
ax.grid(True, alpha=0.3)
ax.legend()

# Move Y-axis to the right
ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")

# Store original limits
original_xlim = (x[0], x[-1])
original_ylim = (y.min() * 0.98, y.max() * 1.02)

ax.set_xlim(original_xlim)
ax.set_ylim(original_ylim)

# ============================================================
# CROSSHAIRS
# ============================================================

h_line = ax.axhline(
    color="gray",
    linestyle=":",
    linewidth=0.8,
    alpha=0.6,
    visible=False,
)

v_line = ax.axvline(
    color="gray",
    linestyle=":",
    linewidth=0.8,
    alpha=0.6,
    visible=False,
)


def on_mouse_move(event):
    """Show crosshairs under mouse."""
    if event.inaxes != ax:
        if h_line.get_visible():
            h_line.set_visible(False)
            v_line.set_visible(False)
            fig.canvas.draw_idle()
        return

    h_line.set_ydata([event.ydata, event.ydata])
    v_line.set_xdata([event.xdata, event.xdata])

    h_line.set_visible(True)
    v_line.set_visible(True)

    fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", on_mouse_move)

# ============================================================
# ZOOM FUNCTIONS
# ============================================================


def zoom_axis(axis, factor):
    """
    factor < 1 -> zoom in
    factor > 1 -> zoom out
    """

    if axis == "x":
        lo, hi = ax.get_xlim()
        center = (lo + hi) / 2
        half = (hi - lo) * factor / 2
        ax.set_xlim(center - half, center + half)

    else:
        lo, hi = ax.get_ylim()
        center = (lo + hi) / 2
        half = (hi - lo) * factor / 2
        ax.set_ylim(center - half, center + half)

    fig.canvas.draw_idle()


def zoom_x(direction):
    zoom_axis("x", 0.85 if direction == "in" else 1.15)


def zoom_y(direction):
    zoom_axis("y", 0.85 if direction == "in" else 1.15)


# ============================================================
# PAN FUNCTIONS
# ============================================================


def pan_left():
    lo, hi = ax.get_xlim()
    shift = (hi - lo) * 0.10
    ax.set_xlim(lo - shift, hi - shift)
    fig.canvas.draw_idle()


def pan_right():
    lo, hi = ax.get_xlim()
    shift = (hi - lo) * 0.10
    ax.set_xlim(lo + shift, hi + shift)
    fig.canvas.draw_idle()


def reset_view():
    ax.set_xlim(original_xlim)
    ax.set_ylim(original_ylim)
    fig.canvas.draw_idle()


# ============================================================
# MOUSE WHEEL ZOOM
# ============================================================


def on_scroll(event):
    if event.inaxes != ax:
        return

    direction = "in" if event.button == "up" else "out"

    # Detect whether cursor is near chart edges
    bbox = ax.get_window_extent()

    edge_x = bbox.width * 0.10
    edge_y = bbox.height * 0.10

    on_left_edge = event.x < bbox.x0 + edge_x
    on_right_edge = event.x > bbox.x1 - edge_x

    on_top_edge = event.y > bbox.y1 - edge_y
    on_bottom_edge = event.y < bbox.y0 + edge_y

    # TradingView-like behavior:
    # left/right edges -> Y zoom
    # anywhere else -> X zoom

    if on_left_edge or on_right_edge:
        zoom_y(direction)
    elif on_top_edge or on_bottom_edge:
        zoom_x(direction)
    else:
        zoom_x(direction)


fig.canvas.mpl_connect("scroll_event", on_scroll)

# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================


def on_key(event):
    if event.key == "left":
        pan_left()

    elif event.key == "right":
        pan_right()

    elif event.key == "r":
        reset_view()

    elif event.key == "ctrl+up":
        zoom_x("in")

    elif event.key == "ctrl+down":
        zoom_x("out")

    elif event.key == "shift+up":
        zoom_y("in")

    elif event.key == "shift+down":
        zoom_y("out")


fig.canvas.mpl_connect("key_press_event", on_key)

# ============================================================
# INFO
# ============================================================

print("\n📊 TradingView-style Controls")
print("────────────────────────────")
print("Move mouse                 → Crosshairs")
print("Mouse wheel (chart)        → X-axis zoom")
print("Mouse wheel (left/right)   → Y-axis zoom")
print("← / →                      → Pan left/right")
print("Ctrl+↑ / Ctrl+↓            → X zoom in/out")
print("Shift+↑ / Shift+↓          → Y zoom in/out")
print("r                          → Reset view")
print("\n✓ Coordinate readout removed")
print("✓ Y-axis on right side")

plt.tight_layout()
plt.show()