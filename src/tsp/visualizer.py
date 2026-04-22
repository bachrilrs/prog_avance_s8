import matplotlib.pyplot as plt
import numpy as np
from .structure import DistanceGraph

class TSPVisualizer:
    """Visualisateur universel pour tous les algorithmes du TSP"""
    
    def __init__(self, graph: DistanceGraph):
        # On a juste besoin du graphe pour connaître les coordonnées (X, Y) des villes
        self.graph = graph
    
    def plot_path(self, path_names: list[str], title: str, distance: float):
        """Affiche n'importe quel chemin, peu importe l'algorithme qui l'a généré."""
        
        # Astuce : On utilise self.graph.index pour trouver les villes instantanément O(1)
        x = [self.graph.villes[self.graph.index[nom]].coord_X for nom in path_names]
        y = [self.graph.villes[self.graph.index[nom]].coord_Y for nom in path_names]
        
        x = np.array(x)
        y = np.array(y)

        plt.figure(figsize=(10, 6))

        # Tracer les points des villes
        plt.scatter(x, y, color='red', zorder=5, s=100)

        # Tracer les flèches
        u = np.diff(x)
        v = np.diff(y)
        plt.text(x[0]+0.5, y[0]+0.5, 'Point de départ', fontsize=8, c="#000000", 
                 ha='center', va='center', backgroundcolor="#66a0eb")
        plt.quiver(x[:-1], y[:-1], u, v, angles='xy', scale_units='xy', scale=1, 
                   color="#8C95E4", width=0.005, headwidth=3)
        
        # Afficher le nom des villes
        for i, ville_name in enumerate(path_names[:-1]): 
            plt.text(x[i], y[i], ville_name, fontsize=8, c="#000000", ha='right',
                     backgroundcolor="#66a0eb")
        
        # On utilise directement la distance passée en paramètre !
        plt.title(f'{title}\nDistance totale: {distance:.2f}')
        plt.xlabel('Coordonnée X')
        plt.ylabel('Coordonnée Y')
        plt.grid()
        plt.show()