


import numpy as np
import copy
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


    def two_opt(self, path: list[str]) -> tuple[list[str], float]:
        """2-opt local search - assumes CLOSED path (returns to start)"""
        best_path = path[:]
        improved = True
        n = len(best_path)
        
        while improved:
            improved = False
            
            for i in range(n - 1):
                for j in range(i + 2, n):

                    if i == 0 and j == n - 1:
                        continue
                    
                    a_idx = self.index_ville[best_path[i]]
                    b_idx = self.index_ville[best_path[i + 1]]
                    c_idx = self.index_ville[best_path[j]]
                    d_idx = self.index_ville[best_path[(j + 1) % n]]
                    
                    old_distance = (self.matrix_distance[a_idx][b_idx] + self.matrix_distance[c_idx][d_idx])
                    new_distance = (self.matrix_distance[a_idx][c_idx] + self.matrix_distance[b_idx][d_idx])
                    
                    if new_distance < old_distance:
                        best_path[i + 1:j + 1] = best_path[i + 1:j + 1][::-1]
                        improved = True
                        break
                
                if improved:
                    break
        
        total_distance = self.distance_route(best_path)
        return best_path, total_distance
    
    def distance(p1, p2):
        """Return Euclidean distance between two points."""
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

    def three_opt(self, path):
        """
        path: list of city indices representing a Hamiltonian cycle
        self.matrix_distance: dict mapping city index to (x, y) tuple
        Returns a new path after applying 3-opt moves until no improvement.
        """
        improved = True
        n = len(path)
        # Ensure path is a cycle: first city = last city
        if path[0] != path[-1]:
            path = path + [path[0]]
            n += 1

        while improved:
            improved = False
            best_delta = 0
            best_tour = None

            for i in range(1, n-2):
                for j in range(i+1, n-1):
                    for k in range(j+1, n):
                        # Current edges
                        A, B = self.index_ville[path[i-1]], self.index_ville[path[i]]
                        C, D = self.index_ville[path[j-1]], self.index_ville[path[j]]
                        E, F = self.index_ville[path[k-1]], self.index_ville[path[k]]

                        # Compute current distance
                        cur = (self.distance(self.matrix_distance[A], self.matrix_distance[B]) +
                            self.distance(self.matrix_distance[C], self.matrix_distance[D]) +
                            self.distance(self.matrix_distance[E], self.matrix_distance[F]))

                        # 7 possible reconnections
                        # 1) A-D, C-B, E-F
                        new1 = (self.distance(self.matrix_distance[A], self.matrix_distance[D]) +
                                self.distance(self.matrix_distance[C], self.matrix_distance[B]) +
                                self.distance(self.matrix_distance[E], self.matrix_distance[F]))
                        delta1 = new1 - cur

                        # 2) A-D, C-F, E-B
                        new2 = (self.distance(self.matrix_distance[A], self.matrix_distance[D]) +
                                self.distance(self.matrix_distance[C], self.matrix_distance[F]) +
                                self.distance(self.matrix_distance[E], self.matrix_distance[B]))
                        delta2 = new2 - cur

                        # 3) A-C, B-D, E-F
                        new3 = (self.distance(self.matrix_distance[A], self.matrix_distance[C]) +
                                self.distance(self.matrix_distance[B], self.matrix_distance[D]) +
                                self.distance(self.matrix_distance[E], self.matrix_distance[F]))
                        delta3 = new3 - cur

                        # 4) A-C, B-E, D-F
                        new4 = (self.distance(self.matrix_distance[A], self.matrix_distance[C]) +
                                self.distance(self.matrix_distance[B], self.matrix_distance[E]) +
                                self.distance(self.matrix_distance[D], self.matrix_distance[F]))
                        delta4 = new4 - cur

                        # 5) A-E, B-D, C-F
                        new5 = (self.distance(self.matrix_distance[A], self.matrix_distance[E]) +
                                self.distance(self.matrix_distance[B], self.matrix_distance[D]) +
                                self.distance(self.matrix_distance[C], self.matrix_distance[F]))
                        delta5 = new5 - cur

                        # 6) A-B, C-E, D-F
                        new6 = (self.distance(self.matrix_distance[A], self.matrix_distance[B]) +
                                self.distance(self.matrix_distance[C], self.matrix_distance[E]) +
                                self.distance(self.matrix_distance[D], self.matrix_distance[F]))
                        delta6 = new6 - cur

                        # 7) A-B, C-D, E-F (original, skip)

                        deltas = [delta1, delta2, delta3, delta4, delta5, delta6]
                        if min(deltas) < best_delta:
                            best_delta = min(deltas)
                            # Apply the move corresponding to best_delta
                            if best_delta == delta1:
                                new_tour = (path[:i] + [B] + path[i+1:j] + [C] +
                                            path[j+1:k] + [D] + path[k+1:])
                            elif best_delta == delta2:
                                new_tour = (path[:i] + [B] + path[i+1:j] + [E] +
                                            path[j+1:k] + [C] + path[k+1:])
                            elif best_delta == delta3:
                                new_tour = (path[:i] + [C] + path[i:j] + [B] +
                                            path[j+1:k] + [D] + path[k+1:])
                            elif best_delta == delta4:
                                new_tour = (path[:i] + [C] + path[i:j] + [E] +
                                            path[j+1:k] + [B] + path[k+1:])
                            elif best_delta == delta5:
                                new_tour = (path[:i] + [E] + path[i:j] + [B] +
                                            path[j+1:k] + [C] + path[k+1:])
                            elif best_delta == delta6:
                                new_tour = path[:i] + path[i:j] + path[j:k] + path[k:]
                            best_tour = new_tour

            if best_tour is not None:
                path = best_tour
                improved = True
        return path