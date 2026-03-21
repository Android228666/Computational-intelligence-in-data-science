import numpy as np
import matplotlib.pyplot as plt

def simulate_buffon(N, L, D):  
    """
    Performs a simulation of Buffon's needle experiment using the Monte Carlo method.

    Parameters: 
    ----------
    N : int
        Number of needle tosses (sample size).
    L : float 
        Length of the needle.
    D : float
        Distance between parallel lines on the floor.

    Returns: 
    -------
    y_center : numpy.ndarray
        Randomized vertical positions of needle centers (range 0 to D).
    theta : numpy.ndarray
        Randomized needle inclination angles in radians (range 0 to pi/2).
    is_hit : numpy.ndarray
        Boolean array (True if the needle crosses a line).
    pi_est : float
        Estimated value of Pi based on simulation results.
    """
    # Randomize needle center position (y) and angle (theta)
    y_center = np.random.uniform(0, D, N)
    theta = np.random.uniform(0, np.pi/2, N)

    # Check for line crossing condition
    # The needle hits if it crosses the bottom line (0) or the top line (D)
    is_hit = np.logical_or(y_center <= (L/2)*np.sin(theta), \
                           y_center >= D - (L/2)*np.sin(theta))
    
    hits = np.sum(is_hit) 

    # Formula: Pi approx (2 * L * N) / (D * hits)
    pi_est = (2*L*N) / (D*hits) if hits > 0 else 0 
    return y_center, theta, is_hit, pi_est


# --- PARAMETERS ---
N_visual = 500
D = 1.0
L = 0.5

# --- Figure 1: NEEDLE VISUALIZATION ---
plt.figure(figsize=(12, 6))
plt.suptitle("Buffon's Needle Experiment")
plt.subplot(1, 2, 1)

y_c, th, hits, _ = simulate_buffon(N_visual, L, D)
x_c = np.random.uniform(0, 5, N_visual) # x-coordinates for visualization only

for i in range(N_visual):
    dx = (L/2) * np.cos(th[i])
    dy = (L/2) * np.sin(th[i])
    color = 'blue' if hits[i] else 'red'
    plt.plot([x_c[i]-dx, x_c[i]+dx], [y_c[i]-dy, y_c[i]+dy], color=color, alpha=0.6)

# Drawing floor lines
for line in range(-1, 3):
    plt.axhline(y=line*D, color="black", linestyle="-", linewidth=1)

plt.title(f"Simulation: blue = hits (N={N_visual})")
plt.ylim(-0.2, D + 0.2)

# --- Figure 2: BOXPLOTS (Convergence Analysis) ---
plt.subplot(1, 2, 2)

iterations = [100, 500, 1000, 5000, 10000, 100000, 1000000]
data_to_plot = []
for n in iterations:
    estimates = []
    for _ in range(50): # 50 repetitions for each N to get distribution data
        _, _, _, pi_val = simulate_buffon(n, L, D)
        estimates.append(pi_val)
    data_to_plot.append(estimates)

plt.boxplot(data_to_plot, tick_labels=iterations)
plt.axhline(y=np.pi, color="r", linestyle="--", label="True $\pi$")
plt.title("Distribution of $\pi$ Estimates vs. Number of Tosses")
plt.xlabel("Number of Tosses (N)")
plt.ylabel("Estimated $\pi$")
plt.legend()

plt.tight_layout()
plt.show()