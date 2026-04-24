import re

import pandas as pd
import numpy as np


class Pays:
    """Orchestre l'analyse complète du problème TSP"""

    def __init__(self, nom ,villes: list['Ville'] = None):  

        """ Args:
            nom: Nom du pays (ex: "France")
            villes: Liste de Ville chargées depuis load_cities()
        """

        from .solvers import KNN, LocalSearch, AlgoGenetique
        from .visualizer import TSPVisualizer
        
        self.nom = nom
        self.villes = villes
        
        # Crée le graphe de distances
        self.graph = DistanceGraph(self.villes)
        
        # Crée les solveurs
        self.knn = KNN(self.graph)
        self.local_search = LocalSearch(self.graph)
        
        # Crée le visualiseur
        self.visualizer = TSPVisualizer(self.graph)
        
        # Chemins trouvés à chaque étape
        self.knn.compute_all_paths()
        print(f"DEBUG : Chemin KNN trouvé : {self.knn.get_optimal_path()[1]}")  # Affiche le chemin KNN pour debug
        self.best_path_knn = Parcours(*self.knn.get_optimal_path())          # Generer le chemin KNN
        self.best_path_two_opt = None       # Après 2-OPT
        self.best_path_three_opt = None     # Après 3-OPT

        self.AlgoGenetique = AlgoGenetique(self.graph, self.best_path_knn if self.best_path_knn else None)
        
        # Distances correspondantes
        self.distance_knn = None
        self.distance_two_opt = None
        self.distance_three_opt = None
        
        # Points de départ
        self.start_city_knn = None
        self.start_city_two_opt = None
        self.start_city_three_opt = None
        
        # Temps de calcul (sera rempli plus tard)
        self.time_knn = None
        self.time_two_opt = None
        self.time_three_opt = None

        # Algo génétique 

        self.best_path_evolved = self._solve_algo_genetique(verbose=False)
        

    def solve(self, verbose: bool = False) -> None:
        """Résout le TSP en 3 étapes: KNN → 2-OPT → 3-OPT."""
        self._solve_knn(verbose)
        self._solve_two_opt(verbose)
        self._solve_three_opt(verbose)
        self._solve_algo_genetique(verbose)
        
        if verbose:
            self._print_summary()

    def _solve_knn(self, verbose: bool) -> None:
        """Étape 1: KNN amélioré - teste plusieurs stratégies."""
        
        # Version 1: Multi-start (rapide, robuste)
        if len(self.villes) > 200:
            self.knn.compute_all_paths(multistart=True, num_random=20)
        else:
            self.knn.compute_all_paths(multistart=False)
        
        self.start_city_knn, self.best_path_knn, self.distance_knn = (
            self.knn.get_optimal_path()
        )
        
        if verbose:
            print(f"[1/3] KNN: {self.distance_knn:.2f} depuis {self.start_city_knn}")

    def _solve_two_opt(self, verbose: bool) -> None:
        """Étape 2: 2-OPT - améliore le chemin KNN."""
        knn_path_open = self.best_path_knn[:-1]
        path_optimized, distance = self.local_search.two_opt(knn_path_open)
        
        self.best_path_two_opt = path_optimized + [path_optimized[0]]
        self.distance_two_opt = distance
        
        improvement = self._calculate_improvement(self.distance_knn, distance)
        if verbose:
            print(f"[2/3] 2-OPT: {distance:.2f} (amélioration: {improvement:.1f}%)")

    def _solve_three_opt(self, verbose: bool) -> None:
        """Étape 3: 3-OPT - améliore davantage le chemin."""
        path_open = self.best_path_two_opt[:-1]
        path_optimized, distance = self.local_search.three_opt(path_open)
        
        # Si pas d'amélioration, garde le résultat 2-OPT
        if distance < self.distance_two_opt:
            self.best_path_three_opt = path_optimized + [path_optimized[0]]
            self.distance_three_opt = distance
            improvement = self._calculate_improvement(self.distance_two_opt, distance)
            if verbose:
                print(f"[3/3] 3-OPT: {distance:.2f} (amélioration: {improvement:.1f}%)")
        else:
            self.best_path_three_opt = self.best_path_two_opt[:]
            self.distance_three_opt = self.distance_two_opt
            if verbose:
                print(f"[3/3] 3-OPT: pas d'amélioration")

    def _solve_algo_genetique(self, verbose: bool) -> None:
        self.best_path_evolved = self.AlgoGenetique(self.graph, self.best_path_knn).evolve_generations()
        return self.best_path_evolved

    def _calculate_improvement(self, distance_before: float, distance_after: float) -> float:
        """Calcule le pourcentage d'amélioration."""
        if distance_before == 0:
            return 0.0
        return ((distance_before - distance_after) / distance_before) * 100

    def _print_summary(self) -> None:
        """Affiche le résumé final."""
        total_improvement = self._calculate_improvement(self.distance_knn, self.distance_three_opt)
        
        print(f"\nRésumé: {self.nom} ({len(self.villes)} villes)")
        print(f"  KNN   → {self.distance_knn:.2f}")
        print(f"Chemin KNN: {' → '.join(self.best_path_knn)}")
        print(f"  2-OPT → {self.distance_two_opt:.2f}")
        print(f"Chemin 2-OPT: {' → '.join(self.best_path_two_opt)}")
        print(f"  3-OPT → {self.distance_three_opt:.2f}")
        print(f"Chemin 3-OPT: {' → '.join(self.best_path_three_opt)}")
        print(f"  Amélioration totale: {total_improvement:.1f}%\n")

    def get_best_path(self, algo: str = "three_opt") -> list[str]:
        """
        Retourne le meilleur chemin selon l'algorithme choisi.
        
        Args:
            algo: "knn", "two_opt", ou "three_opt"
        
        Returns:
            Liste de noms de villes (chemin fermé)
        """
        paths = {
            "knn": self.best_path_knn,
            "two_opt": self.best_path_two_opt,
            "three_opt": self.best_path_three_opt
        }
        return paths.get(algo, self.best_path_three_opt)

    def get_matrix_with_labels(self):
        """Retourne la matrice de distances avec labels"""
        return self.graph.get_dataframe()
    
    def get_distance(self, algo: str = "three_opt") -> float:
        """
        Retourne la distance selon l'algorithme choisi.
        
        Args:
            algo: "knn", "two_opt", ou "three_opt"
        
        Returns:
            Distance totale
        """
        distances = {
            "knn": self.distance_knn,
            "two_opt": self.distance_two_opt,
            "three_opt": self.distance_three_opt
        }
        return distances.get(algo, self.distance_three_opt)
    
    def print_best_path(self, algo: str = "three_opt") -> None:
        """
        Affiche le meilleur chemin en format lisible.
        
        Args:
            algo: "knn", "two_opt", ou "three_opt"
        """
        path = self.get_best_path(algo)
        distance = self.get_distance(algo)
        
        print(f"\n{algo.upper()} - Distance: {distance:.2f}")
        print(" → ".join(path))
    
    def visualize(self, algo: str = "three_opt") -> None:
        """
        Visualise le meilleur chemin trouvé.
        
        Args:
            algo: "knn", "two_opt", ou "three_opt"
        """
        path = self.get_best_path(algo)
        distance = self.get_distance(algo)
        title = f"{self.nom} - {algo.upper()}"
        
        self.visualizer.plot_path(path, title, distance)
    
    def get_matrix_with_labels(self) -> pd.DataFrame:
        """Retourne la matrice de distances avec labels"""
        return self.graph.get_dataframe()
    
    def print_all_knn_results(self) -> None:
        """Affiche les distances KNN pour chaque point de départ"""
        self.knn.print_distance_from_each_city()
    
    def __str__(self) -> str:
        """Représentation textuelle du pays"""
        if self.distance_three_opt is None:
            return f'{self.nom}: {len(self.villes)} villes (non résolu)'
        return (f'{self.nom}: {len(self.villes)} villes - '
                f'Distance finale: {self.distance_three_opt:.2f}')

            
    def compute_path_distance(self, path):
        """Calcule la distance totale d'un chemin"""

        indices = [self.graph.index[nom] for nom in path]
        rows = indices[:-1]
        cols = indices[1:]
        return np.sum(self.graph.matrix[rows, cols])
    
    def print_distance_from_each_city(self):
        """Affiche les distances pour chaque point de départ"""
        self.knn.print_distance_from_each_city()

    def print_from_a_city(self, nom_ville):
        """Affiche le chemin partant d'une ville"""
        return self.knn.print_from_a_city(nom_ville)
    
    def print_best_path(self):
        """Affiche le meilleur chemin trouvé"""
        if self.best_path is None:
            print("Veuillez d'abord appeler get_optimal_path()")
            return
        
        print(f"Meilleur chemin trouvé : {' -> '.join(self.best_path)}")
    
    def get_optimal_path(self):
        """Retourne le meilleur chemin après KNN, 2-opt et 3-opt"""
        start_point, path, distance = self.knn.get_optimal_path()
        self.best_path_knn = path
        
        # 2-opt
        knn_path_open = path[:-1]
        optimized_path_2opt, opt_distance_2 = self.two_opt.two_opt(knn_path_open)
        self.best_path_two_opt = optimized_path_2opt + [optimized_path_2opt[0]]

        # 3-opt (Prend le résultat du 2-opt pour l'améliorer encore plus)
        optimized_path_3opt, opt_distance_3 = self.two_opt.three_opt(optimized_path_2opt)
        self.best_path_three_opt = optimized_path_3opt + [optimized_path_3opt[0]]

        return start_point, path, distance
   
class Ville:
    """classe ville"""

    def __init__(self, nom):
        self.nom = nom
        self.__coord_X = None
        self.__coord_Y = None

    @property
    def coord_X(self):
        return self.__coord_X
    
    @property
    def coord_Y(self):
        return self.__coord_Y

    @coord_X.setter
    def coord_X(self,x):
        self.__coord_X = x

    @coord_Y.setter
    def coord_Y(self,y):
        self.__coord_Y = y

    def __str__(self):
        return f'{self.nom} coordonées X : {self.__coord_X}, coorodonées Y: {self.__coord_Y}'
    
    def eucledian_distance(self, other):
        return np.sqrt((other.coord_X - self.coord_X)**2 + (other.coord_Y - self.coord_Y)**2)
    
class DistanceGraph:
    """Gère la matrice de distances entre villes"""
    
    def __init__(self, villes: list[Ville]):

        self.villes = villes                              # Liste des Ville
        self.index = {v.nom: i for i, v in enumerate(villes)}  # Dict nom -> indice
        self.matrix = self._build_matrix()                # Matrice distances (n x n)
        self.matrix_df = self.get_dataframe()

    def _build_matrix(self) -> np.ndarray:
        """Construit la matrice de distances"""
        n = len(self.villes)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1, n):
                matrix[i][j] = self.villes[i].eucledian_distance(self.villes[j])
                matrix[j][i] = matrix[i][j]  
        return matrix
    
    def get_distance(self, ville1_idx: int, ville2_idx: int) -> float:
        """Retourne la distance entre deux villes par indice"""
        return self.matrix[ville1_idx, ville2_idx]
    

    def path_distance(self, path):
        indices = [self.index[nom] for nom in path]
        # créé tous les couples nécessaires pour calculer la distance totale
        rows = indices[:-1]
        cols = indices[1:]
        return np.sum(self.matrix[rows, cols])
    
    def get_dataframe(self) -> pd.DataFrame:
        """Retourne la matrice sous forme de DataFrame avec labels"""
        noms = [v.nom for v in self.villes]
        return pd.DataFrame(self.matrix, index=noms, columns=noms)

class Parcours:
    """Représente un parcours (chemin) dans le TSP"""

    #TODO cette classe gere les parcours, on ne va plus utiliser de variables classique pour stocker les parcours

    def __init__(self, parcours: list[str], distance_path: float):
        self.parcours = parcours
        self.point_depart = parcours[0] if parcours else None
        self.distance_path = distance_path