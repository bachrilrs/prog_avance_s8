
from turtle import distance

from .structure import DistanceGraph
from .solvers import KNN, TwoOpt
import matplotlib.pyplot as plt
import numpy as np


class KNNVisualizer:
    """Visualise les chemins TSP"""
    
    def __init__(self, graph: DistanceGraph, solver: KNN):
        self.graph = graph
        self.Knn_solver = solver
    
    def plot_path_knn(self, path_names: list[str], title: str = "Chemin TSP"):
        """Affiche un chemin"""
        # Convertir les noms de villes en coordonnées
        x = []
        y = []
        for ville_name in path_names:
            ville = next(v for v in self.graph.villes if v.nom == ville_name)
            x.append(ville.coord_X) # Longitude
            y.append(ville.coord_Y) # Latitude
        
        x = np.array(x)
        y = np.array(y)

        plt.figure(figsize=(10, 6))

        # Tracer les points des villes
        plt.scatter(x, y, color='red', zorder=5, s=100)


        u = np.diff(x)
        v = np.diff(y)
        plt.text(x[0]+0.5, y[0]+0.5, 'Point de départ', fontsize=8, c="#000000", ha='center', va='center', backgroundcolor="#66a0eb", visible=True)
        plt.quiver(x[:-1], y[:-1], u, v, angles='xy', scale_units='xy', scale=1, color="#8C95E4", width=0.005, headwidth=3)
        
        for i, ville_name in enumerate(path_names[:-1]): 
            plt.text(x[i], y[i], ville_name, fontsize=8, c="#000000", ha='right',
                    backgroundcolor="#66a0eb", visible=True)
        
        distance = self.Knn_solver.compute_path_distance(path_names)

        plt.title(f'{title}\nDistance: {distance:.2f}')
        plt.xlabel('Coordonnée X')
        plt.ylabel('Coordonnée Y')
        plt.grid()
        plt.show()

class TwoOptVisualizer:
    """Visualise les chemins TSP pour l'algorithme 2-opt"""
    
    def __init__(self, graph: DistanceGraph):
        self.graph = graph
        self.two_opt_solver = TwoOpt(graph)
    
    def plot_path_two_opt(self, path_names: list[str], title: str = "Chemin TSP"):
        """Affiche un chemin"""
        x = []
        y = []
        for ville_name in path_names:
            ville = next((v for v in self.graph.villes if v.nom == ville_name), None)
            if ville is None:
                raise ValueError(f"Ville '{ville_name}' not found in graph")
            x.append(ville.coord_X)
            y.append(ville.coord_Y)
        
        x = np.array(x)
        y = np.array(y)

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='red', zorder=5, s=100)

        u = np.diff(x)
        v = np.diff(y)
        plt.text(x[0]+0.5, y[0]+0.5, 'Point de départ', fontsize=8, c="#000000", 
                ha='center', va='center', backgroundcolor="#66a0eb")
        plt.quiver(x[:-1], y[:-1], u, v, angles='xy', scale_units='xy', scale=1, 
                  color="#8C95E4", width=0.005, headwidth=3)
        
        for i, ville_name in enumerate(path_names[:-1]): 
            plt.text(x[i], y[i], ville_name, fontsize=8, c="#000000", ha='right',
                    backgroundcolor="#66a0eb")
        

        distance = self.two_opt_solver.distance_route(path_names)

        plt.title(f'{title}\nDistance: {distance:.2f}')
        plt.xlabel('Coordonnée X')
        plt.ylabel('Coordonnée Y')
        plt.grid()
        plt.show()