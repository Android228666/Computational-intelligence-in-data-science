import numpy as np
import matplotlib.pyplot as plt


def simulate_buffon(N, L, D):  
    """
    Przeprowadza symulację eksperementu igły Buddona metodą Monte Carlo.

    Parametry: 
    ----------
    N : int
        Liczba rzutów igłą (rozmiar próby).
    L : float 
        Długość igły.
    D : float
        Odległość między równoległymi liniami na podłodze.
    ----------

    Zwraca: 
    ----------
    y_center : numpy.ndarray
        Wylosowane pionowe połozenia środków igieł (zakres 0 do D).
    theta : numpy.ndarray
        Wylosowane kąty nachylenia igieł w radianach (zakres 0 do pi/2).
    is_hit : numpy.ndarrray
        Tablica wartości logicznych (True, jeśli igła przcina linię)
    pi_est : float
        Oszacowana wartość liczby Pi na podstawie wyników symulacji.
    ----------
    """
    # Łosujemy połozenie środka igły (y) i kąt (theta)
    y_center = np.random.uniform(0, D, N)
    theta = np.random.uniform(0, np.pi/2, N)

    # Sprawdzenie warunku trafienia igły
    is_hit = np.logical_or(y_center <= (L/2)*np.sin(theta), \
    y_center >= D - (L/2)*np.sin(theta))
    
    hits = np.sum(is_hit) 
    # print("hits: ", hits)

    pi_est = (2*L*N) / (D*hits) if hits > 0 else 0 
    return y_center, theta, is_hit, pi_est


# -- PARAMETRY --
N_visual = 500
D = 1
L = 0.5

# --- Rysunek 1: WIZUALIZACJA IGIEŁ ---
plt.figure(figsize = (12, 6))
plt.suptitle("Igły Buffona")
plt.subplot(1, 2, 1)

y_c, th, hits, _ = simulate_buffon(N_visual, L, D)
x_c = np.random.uniform(0, 5, N_visual) # to dla wizualizacji

for i in range(N_visual):
    dx = (L/2) * np.cos(th[i])
    dy = (L/2) * np.sin(th[i])
    color = 'blue' if hits[i] else 'red'
    plt.plot([x_c[i]-dx, x_c[i]+dx], [y_c[i]-dy, y_c[i]+dy], color=color, alpha=0.6)

# Rysowanie linii podłogi
for line in range(-1, 3):
    plt.axhline(y = line*D, color="black", linestyle="-", linewidth=1)
plt.title(f"Symulacja: niebieskie = trafienia (N={N_visual})")

# --- Rysunek 2: BOXPLOTY (Zbiezność) ---
plt.subplot(1, 2, 2)

iterations = [100, 500, 1000, 5000, 10000, 100000, 1000000]
data_to_plot = []
for n in iterations:
    estimates = []
    for _ in range(50):
        _, _, _, pi_val = simulate_buffon(n, L, D)
        estimates.append(pi_val)
    data_to_plot.append(estimates)

plt.boxplot(data_to_plot, tick_labels=iterations)
plt.axhline(y = np.pi, color="r", linestyle="--", label = "Prawdziwe $\pi$")
plt.title("Rozkład oszacowań $\pi$ vs Liczba rzutów")
plt.xlabel("Liczba rzutów (N)")
plt.ylabel("Oszacowane $\pi$")
plt.legend()
plt.tight_layout()
plt.show()