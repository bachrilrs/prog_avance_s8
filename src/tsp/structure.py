import time

import pandas as pd
import numpy as np


class Pays:
    """Orchestre l'analyse complète du problème TSP"""

    def __init__(self, nom ,villes: list['Ville'] = None):
        """ Args:
            nom: Nom du pays (ex: "France")
            villes: Liste de Ville chargées depuis load_cities()
        """

        from .solvers import KNN, TwoOpt, ThreeOpt, AlgoGenetique
        from .visualizer import TSPVisualizer
        
        self.nom = nom
        self.graph = DistanceGraph(villes)
        
        # Initialisation des solveurs
        self.knn_solver = KNN(self.graph)
        self.two_opt_solver = TwoOpt(self.graph)
        self.three_opt_solver = ThreeOpt(self.graph)
        self.ga_solver = AlgoGenetique(self.graph)
        self.visualizer = TSPVisualizer(self.graph)

        # Stockage des résultats (Objets Parcours)
        self.results= {}

    def __str__(self) -> str:
        """Représentation textuelle du pays"""
        if self.distance_three_opt is None:
            return f'{self.nom}: {len(self.villes)} villes (non résolu)'
        return (f'{self.nom}: {len(self.villes)} villes - '
                f'Distance finale: {self.distance_three_opt:.2f}')
        

    def run_full_analysis(self):
        print(f"\n Analyse TSP : {self.nom} ")
        
        # 1. KNN
        start_time = time.time()
        path_knn = self.knn_solver.solve(verbose=True)
        temps_knn = time.time() - start_time
        
        # On stocke un dictionnaire avec le path ET le temps
        self.results['knn'] = path_knn

        print(f"Temps d'exécution KNN: {temps_knn:.4f} secondes\n\n")

        # 2. Two-Opt (basé sur KNN)
        path_for_opt = path_knn.path[:-1]
        
        start_time = time.time()
        path_2opt = self.two_opt_solver.solve(path_for_opt)
        temps_2opt = time.time() - start_time
        
        self.results['two_opt'] = path_2opt
        print(f"\nTemps d'exécution 2-OPT: {temps_2opt:.4f} secondes\n\n")


        # 3. Three-Opt (basé sur Two-Opt)
        start_time = time.time()
        path_3opt = self.three_opt_solver.solve(path_2opt)
        temps_3opt = time.time() - start_time
        print(f"Temps d'exécution 3-OPT: {temps_3opt:.4f} secondes\n\n")
        
        self.results['three_opt'] = path_3opt 

        # 4. Algo Génétique
        start_time = time.time()
        path_ga = self.ga_solver.solve(initial_path=path_for_opt)
        temps_ga = time.time() - start_time
        
        self.results['ga'] = path_ga
        print(f"Temps d'exécution Algorithme Génétique: {temps_ga:.4f} secondes\n\n")
        print(f"Parcours GA: {' -> '.join(path_ga.path)} - Distance: {path_ga.distance_path:.2f}")

    def print_summary(self) -> None:
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

    def _calculate_improvement(self, distance_before: float, distance_after: float) -> float:
        """Calcule le pourcentage d'amélioration."""
        if distance_before == 0:
            return 0.0
        return ((distance_before - distance_after) / distance_before) * 100
    
    def get_best_path(self, algo: str ) -> list[str]:
        """
        Retourne le meilleur chemin selon l'algorithme choisi.
        
        Args:
            algo: "knn", "two_opt", ou "three_opt"
        
        Returns:
            Liste de noms de villes (chemin fermé)"""
        if algo not in self.results:
            raise ValueError(f"Algorithme '{algo}' non trouvé. Choisissez parmi: {list(self.results.keys())}")
        paths = {
            "knn": self.results['knn'].path,
            "two_opt": self.results['two_opt'].path,
            "three_opt": self.results['three_opt'].path,
            "ga": self.results['ga'].path}
        
        return paths.get(algo)
    
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
        return distances.get(algo)
    
    def print_best_path(self, algo: str) -> None:
        """
        Affiche le meilleur chemin en format lisible.
        Args:
            algo: "knn", "two_opt", ou "three_opt"
        """

        if algo not in self.results:
            raise ValueError(f"Algorithme '{algo}' non trouvé. Choisissez parmi: {list(self.results.keys())}")
        
        path = self.get_best_path(algo)
        distance = self.get_distance(algo)
        
        print(f"\n{algo.upper()} - Distance: {distance:.2f}")
        print(" -> ".join(path))
    
    def visualize(self, algo: str = "three_opt") -> None:
        """Visualise le meilleur chemin trouvé.
        Args:
            algo: "knn", "two_opt", ou 'three_opt'"""
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
        # return np.linalg.norm(other-self)
    
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

class Path:
    """Représente un path (chemin) dans le TSP"""

    #TODO cette classe gere les path, on ne va plus utiliser de variables classique pour stocker les path

    def __init__(self,path: list[str], distance_path: float):
        self.path = path
        self.point_depart = path[0] if path else None
        self.distance_path = distance_path

class Solution:
    """Représente une solution complète pour un pays, avec tous les path et distances associés, avec les differents algos"""
    
    def __init__(self, pays: 'Pays'):
        self.pays = pays
        self.graph = pays.graph
        self.dataframe_resultats = None

    def _tronquer_chemin(self, chemin: list[str], max_villes: int = 6) -> str:
        """Helper : Raccourcit l'affichage du chemin s'il est trop long pour le tableau."""
        if len(chemin) <= max_villes:
            return " -> ".join(chemin)
        
        # Affiche les 3 premières et les 3 dernières villes
        debut = " -> ".join(chemin[:3])
        fin = " -> ".join(chemin[-3:])
        return f"{debut} ... -> {fin}"

def generer_matrice(self) -> pd.DataFrame:
        """Génère un DataFrame (matrice) contenant toutes les statistiques comparatives."""
        lignes = []
        
        distance_reference = None
        if 'knn' in self.pays.results:
            # On va chercher la distance à l'intérieur de la nouvelle structure
            distance_reference = self.pays.results['knn']['path'].distance_path

        # On itère sur le dictionnaire contenant nos données enrichies
        for nom_algo, data in self.pays.results.items():
            
            # Extraction propre
            path = data['path']
            temps_exec = data['temps']
            
            amelioration = 0.0
            if distance_reference and distance_reference > 0:
                amelioration = ((distance_reference - path.distance_path) / distance_reference) * 100

            lignes.append({
                'Algorithme': nom_algo.upper(),
                'Point de Départ': path.point_depart,
                'Distance Totale': round(path.distance_path, 2),
                'Amélioration (%)': round(amelioration, 2),
                'Temps (s)': round(temps_exec, 4), # On utilise le temps ici !
                'Aperçu du Chemin': self._tronquer_chemin(path.path)
            })

        self.dataframe_resultats = pd.DataFrame(lignes)
        
        if not self.dataframe_resultats.empty:
            self.dataframe_resultats.set_index('Algorithme', inplace=True)
            
        return self.dataframe_resultats