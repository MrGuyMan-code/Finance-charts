#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

# --- Create simple data ---
x = np.linspace(0, 10, 100)
y = np.sin(x)

# --- Create the plot ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, 'b-', linewidth=2)
ax.set_title('TEST: Crosshair Demo', fontsize=16)
ax.grid(True, alpha=0.3)

# --- Create crosshair lines ---
# Horizontal line
h_line = ax.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.8)
h_line.set_visible(False)

# Vertical line  
v_line = ax.axvline(x=0, color='red', linestyle='--', linewidth=2, alpha=0.8)
v_line.set_visible(False)

# --- Text for coordinates ---
coord_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                     fontsize=12, verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

print("Crosshair test running... Move your mouse over the chart!")

# --- Mouse movement handler ---
def on_move(event):
    print(f"Mouse moved! In axes: {event.inaxes is not None}")  # Debug print
    
    if event.inaxes != ax:
        h_line.set_visible(False)
        v_line.set_visible(False)
        coord_text.set_text('')
        fig.canvas.draw_idle()
        return
    
    # Get position
    x_pos = event.xdata
    y_pos = event.ydata
    
    print(f"Position: X={x_pos:.2f}, Y={y_pos:.2f}")  # Debug print
    
    # Get limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    # Update horizontal line
    h_line.set_xdata([xlim[0], xlim[1]])
    h_line.set_ydata([y_pos, y_pos])
    h_line.set_visible(True)
    
    # Update vertical line
    v_line.set_xdata([x_pos, x_pos])
    v_line.set_ydata([ylim[0], ylim[1]])
    v_line.set_visible(True)
    
    # Update text
    coord_text.set_text(f'X: {x_pos:.2f}\nY: {y_pos:.2f}')
    
    fig.canvas.draw_idle()

# Connect the event
fig.canvas.mpl_connect('motion_notify_event', on_move)

plt.tight_layout()
plt.show()