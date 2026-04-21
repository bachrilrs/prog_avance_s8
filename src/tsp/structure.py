import pandas as pd
import numpy as np

from pprint import pprint


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
    
    # def path_distance(self, path_indices: list[int]) -> float:
    #     """Calcule la distance totale d'un chemin (liste d'indices)"""
    #     return np.sum(self.matrix[path_indices[:-1], path_indices[1:]])
    
    def get_dataframe(self) -> pd.DataFrame:
        """Retourne la matrice sous forme de DataFrame avec labels"""
        noms = [v.nom for v in self.villes]
        return pd.DataFrame(self.matrix, index=noms, columns=noms)
