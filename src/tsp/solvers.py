


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
    

    def three_opt(self, path: list[str]) -> tuple[list[str], float]:
            """
            Implémentation 3-opt optimisée (First Improvement) et corrigée.
            """
            best_path = path[:]
            if best_path[0] != best_path[-1]:
                best_path.append(best_path[0])
                
            n = len(best_path)
            improved = True

            while improved:
                improved = False
                
                for i in range(1, n - 2):
                    for j in range(i + 1, n - 1):
                        for k in range(j + 1, n):
                            
                            # Indices des 6 villes aux frontières des 3 arêtes coupées
                            A, B = self.index_ville[best_path[i-1]], self.index_ville[best_path[i]]
                            C, D = self.index_ville[best_path[j-1]], self.index_ville[best_path[j]]
                            E, F = self.index_ville[best_path[k-1]], self.index_ville[best_path[k]]

                            d = self.matrix_distance
                            cur = d[A][B] + d[C][D] + d[E][F]

                            # Les 7 reconnexions possibles (avec les Deltas exacts correspondants)
                            # 1: 2-opt (inverse segment 2)
                            d1 = d[A][C] + d[B][D] + d[E][F] - cur
                            # 2: 2-opt (inverse segment 3)
                            d2 = d[A][B] + d[C][E] + d[D][F] - cur
                            # 3: 2-opt (inverse segment 2 et 3)
                            d3 = d[A][C] + d[B][E] + d[D][F] - cur
                            # 4: 3-opt pur (échange segment 2 et 3)
                            d4 = d[A][D] + d[E][B] + d[C][F] - cur
                            # 5: 3-opt pur (segment 3 inversé, puis segment 2)
                            d5 = d[A][E] + d[D][B] + d[C][F] - cur
                            # 6: 3-opt pur (segment 3 normal, segment 2 inversé)
                            d6 = d[A][D] + d[E][C] + d[B][F] - cur
                            # 7: 3-opt pur (segment 3 inversé, segment 2 inversé)
                            d7 = d[A][E] + d[D][C] + d[B][F] - cur

                            deltas = [d1, d2, d3, d4, d5, d6, d7]
                            min_delta = min(deltas)

                            # Si on trouve une amélioration franche (on évite les micro-bugs de flottants)
                            if min_delta < -1e-5:
                                idx = deltas.index(min_delta)
                                
                                seg1 = best_path[:i]
                                seg2 = best_path[i:j]
                                seg3 = best_path[j:k]
                                seg4 = best_path[k:]
                                
                                # On applique EXACTEMENT la reconstruction qui correspond au Delta gagnant
                                if idx == 0:
                                    best_path = seg1 + seg2[::-1] + seg3 + seg4
                                elif idx == 1:
                                    best_path = seg1 + seg2 + seg3[::-1] + seg4
                                elif idx == 2:
                                    best_path = seg1 + seg2[::-1] + seg3[::-1] + seg4
                                elif idx == 3:
                                    best_path = seg1 + seg3 + seg2 + seg4
                                elif idx == 4:
                                    best_path = seg1 + seg3[::-1] + seg2 + seg4
                                elif idx == 5:
                                    best_path = seg1 + seg3 + seg2[::-1] + seg4
                                elif idx == 6:
                                    best_path = seg1 + seg3[::-1] + seg2[::-1] + seg4
                                
                                improved = True
                                break # On sort de la boucle k (First Improvement)
                        if improved: 
                            break # On sort de la boucle j
                    if improved: 
                        break # On sort de la boucle i et on relance le While !

            # Retourne le chemin ouvert
            open_path = best_path[:-1]
            total_distance = self.distance_route(open_path)
            
            return open_path, total_distance