#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

n = np.linspace(1, 650, 500)

I2 = 10
I3 = 5
G = 100
P = 50

knn = n**2
two_opt = I2 * n**2
three_opt = I3 * n**3
genetic = G * P * n

plt.figure(figsize=(10, 6))

plt.plot(n, knn, label="KNN : O(n²)", linewidth=2)
plt.plot(n, two_opt, label="2-OPT : O(I₂·n²)", linewidth=2)
plt.plot(n, three_opt, label="3-OPT : O(I₃·n³)", linewidth=2)
plt.plot(n, genetic, label="AG : O(G·P·n)", linewidth=2)

plt.yscale("log")
plt.title("Complexité théorique approximative des algorithmes TSP")
plt.xlabel("Nombre de villes n")
plt.ylabel("Coût relatif (échelle logarithmique)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("complexite_algorithmes.png", dpi=300)
plt.show()