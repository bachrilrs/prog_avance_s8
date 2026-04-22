import pandas as pd
import numpy as np

class Pays:
    """Orchestre l'analyse complète du problème TSP"""

    def __init__(self, nom ,villes: list['Ville'] = None):  
        self.nom = nom
        self.villes = villes if villes is not None else []
        self.graph = DistanceGraph(self.villes)
        

        self.best_path_two_opt = None
        self.best_path_three_opt = None

        self.calculer_distances()
        
        from .solvers import KNN
        from .solvers import LocalSearch
        from .visualizer import TSPVisualizer
        # Créer le solveur KNN
        self.knn = KNN(self.graph)
        self.best_path_knn = None

        #Twoopt 
        self.two_opt = LocalSearch(self.graph)


        # Créer le visualizer
        self.visualizer_knn = TSPVisualizer(self.graph)
        self.visualizer_two_opt = TSPVisualizer(self.graph)



        self.matrix_df = self.graph.get_dataframe()

    def __str__(self):
        return f'{self.nom}: {", ".join([v.nom for v in self.villes])}'

    def calculer_distances(self):
        """Calcule les distances entre toutes les villes"""
        for v in self.villes:
            for ville in self.villes:
                if v.nom != ville.nom:
                    v.distance[f'{ville.nom}'] = v.eucledian_distance(ville)
                else:
                    v.distance[f'{ville.nom}'] = 0

    def get_matrix_with_labels(self):
        """Retourne la matrice de distances avec labels"""
        return self.graph.get_dataframe()
    
    def compute_all_paths(self):
        """Résout depuis tous les points de départ"""
        self.knn.compute_all_paths()
            
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
        self.distance = {}

    def __str__(self):
        return f'{self.nom} coordonées X : {self.__coord_X}, coorodonées Y: {self.__coord_Y}'
    
    def eucledian_distance(self, other):
        return np.sqrt((other.coord_X - self.coord_X)**2 + (other.coord_Y - self.coord_Y)**2)
    

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

class DistanceGraph:
    """Gère la matrice de distances entre villes"""
    
    def __init__(self, villes: list[Ville]):
        self.villes = villes
        self.index = {v.nom: i for i, v in enumerate(villes)}
        self.matrix = self._build_matrix()
    
    def _build_matrix(self) -> np.ndarray:
        """Construit la matrice de distances"""
        n = len(self.villes)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                matrix[i][j] = self.villes[i].eucledian_distance(self.villes[j])
        
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
