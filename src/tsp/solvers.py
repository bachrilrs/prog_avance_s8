


import numpy as np

from .structure import DistanceGraph

class KNN:
    """Implémentation de l'algorithme KNN pour trouver un chemin à travers les villes"""
    
    def __init__(self, graph: DistanceGraph):
        self.graph = graph
        self.villes = graph.villes
        self.matrix_distance = graph.matrix
        self.index_ville = graph.index
        self.paths = {}
    
    def knn_with_matrix(self, start=0):
        
        n = len(self.matrix_distance)
        visited = [False] * n
        path = [self.villes[start].nom]
        visited[self.index_ville[self.villes[start].nom]] = True

        current = start
        for _ in range(n-1):
            nearest = None
            nearest_dist = float('inf')

            for j in range(n):
                if not visited[j] and self.matrix_distance[current][j] < nearest_dist:
                    nearest_dist = self.matrix_distance[current][j]
                    nearest = j
            
            path.append(self.villes[nearest].nom)
            visited[nearest] = True
            current = nearest
        path.append(self.villes[start].nom)  # Retour à la ville de départ

        self.paths[f"{self.villes[start].nom}"] = path

    def compute_path_distance(self, path):
        indices = [self.index_ville[nom] for nom in path]
        rows = indices[:-1]
        cols = indices[1:]
        return np.sum(self.matrix_distance[rows, cols])

    def compute_all_paths(self):
        """Résout depuis tous les points de départ"""
        for i in range(len(self.villes)):
            self.knn_with_matrix(i)

    def print_distance_from_each_city(self):
        for ville in self.paths.keys():
            print(f"Distance totale partant de {ville} : {self.compute_path_distance(self.paths[ville])}")

    def print_from_a_city(self, nom_ville):
        if nom_ville in self.paths.keys():
            return self.paths[nom_ville]
    
    def get_optimal_path(self):
        distances = {}
        for ville in self.paths.keys():
            distances[ville] = self.compute_path_distance(self.paths[ville])
        
        start_point = min(distances, key=distances.get)
        best_path = self.paths[start_point]
        
        return start_point, best_path, distances[start_point]


class TwoOpt:
    """Implémentation de l'algorithme K-Opt pour améliorer une solution initiale du TSP"""

    def __init__(self,graph: DistanceGraph):
        self.graph = graph
        self.villes = graph.villes
        self.matrix_distance = graph.matrix
        self.index_ville = graph.index
        self.paths = {}

    def distance_route(self, path):
        """calculer path d'un chemin"""
        total = 0
        n = len(path)
        
        for i in range(n):
            current_city = self.index_ville[path[i]]
            next_city = self.index_ville[path[(i + 1) % n]]  # % n pour boucler
            total += self.matrix_distance[current_city][next_city]
        
        return total


    def compute_path_distance(self, path):
        """2-opt local search for closed TSP tour"""
        best_path = path[:]
        improved = True
        n = len(best_path)
        
        while improved:
            improved = False
            
            for i in range(n - 1):
                for j in range(i + 2, n):
                    #
                    if i == 0 and j == n - 1:
                        continue
                    
                    
                    a_idx = self.index_ville[best_path[i]]
                    b_idx = self.index_ville[best_path[i + 1]]
                    
                    c_idx = self.index_ville[best_path[j]]
                    d_idx = self.index_ville[best_path[(j + 1) % n]]
                    
                    
                    old_distance = (
                        self.matrix_distance[a_idx][b_idx] +
                        self.matrix_distance[c_idx][d_idx]
                    )
                    
                    
                    new_distance = (
                        self.matrix_distance[a_idx][c_idx] +
                        self.matrix_distance[b_idx][d_idx]
                    )
                    
                    
                    if new_distance < old_distance:
                        best_path[i + 1:j + 1] = best_path[i + 1:j + 1][::-1]
                        improved = True
                        break
                
                if improved:
                    break
        
        total_distance = self.distance_route(best_path)
        return best_path, total_distance