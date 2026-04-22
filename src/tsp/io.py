
import re

import pandas as pd

from .structure import Ville
from .structure import Pays

def load_cities(filepath: str, separator: str = ";") -> list[Ville]:
    """Charge les villes depuis un fichier CSV"""
    df = pd.read_csv(filepath, sep=separator, header=None)
    df.columns = ['Ville', 'latitude', 'longitude'] 
    
    villes = []
    for _, row in df.iterrows():
        ville = Ville(row['Ville'])
        ville.coord_X = row['longitude'] 
        ville.coord_Y = row['latitude'] 
        villes.append(ville)
    
    return villes


# def process_pays_travel(file_path: str, nom_pays, separator: str = ";", all_paths = False, show_matrix = False):
#     try:
#         # Charger les villes
#         villes = load_cities(file_path, separator)
        
#         # Créer l'objet pays
#         pays = Pays(nom_pays, villes)

#         print(f"--- Analyse terminée pour : {file_path} ---")
        
#         if show_matrix:
#             print("\nMatrice de distances :")
#             print(pays.get_matrix_with_labels())
        
#         print("\nChemin trouvés :")
#         pays.compute_all_paths()
        
#         if all_paths:
#             print("\nDistance totale par point de départ :")
#             pays.print_distance_from_each_city()
        
        
#         print("\nMeilleur chemin trouvé avec KNN:")
#         start_point, path, distance = pays.get_optimal_path()


#         print(f"Point de départ {start_point}")
#         print(f"Chemin {path}")
#         print(f"Distance KNN : {distance}")

#         print("\nMeilleur chemin trouvé avec 2-opt:")

#         chemin_optimal_2opt, distance_2opt = pays.two_opt.two_opt(pays.best_path_knn)

#         pays.best_path_two_opt = chemin_optimal_2opt
#         print(f"Chemin {chemin_optimal_2opt}")
#         print(f"Distance OPT : {distance_2opt}")

#         print(f"Différence entre KNN et Two_opt {distance - distance_2opt}")
        
        

#     except FileNotFoundError:
#         print(f"Erreur : Le fichier {file_path} est introuvable.")
#     except Exception as e:
#         print(f"Une erreur est survenue : {e}")

#     return pays


def process_pays_travel(file_path: str, nom_pays, separator: str = ";", all_paths=False, show_matrix=False):
    try:
        villes = load_cities(file_path, separator)
        pays = Pays(nom_pays, villes)

        print(f"--- Analyse terminée pour : {file_path} ---")
        
        if show_matrix:
            print("\nMatrice de distances :")
            print(pays.get_matrix_with_labels())
        
        print("\nChemin trouvés :")
        pays.compute_all_paths()
        
        if all_paths:
            print("\nDistance totale par point de départ :")
            pays.print_distance_from_each_city()
        
        # === MEILLEUR CHEMIN KNN ===
        print("\nMeilleur chemin trouvé avec KNN:")
        start_point, knn_path, knn_distance = pays.get_optimal_path()

        print(f"Point de départ: {start_point}")
        print(f"Chemin: {knn_path}")
        print(f"Distance KNN: {knn_distance:.2f}")

        # === MEILLEUR CHEMIN 2-OPT ===
        print("\nMeilleur chemin trouvé avec 2-opt:")
        
        # Passer le chemin SANS la dernière répétition
        knn_path_open = knn_path[:-1]  # ['A', 'B', 'C'] au lieu de ['A', 'B', 'C', 'A']
        
        optimal_path_open, opt_distance = pays.two_opt.two_opt(knn_path_open)
        optimal_path_closed = optimal_path_open + [optimal_path_open[0]]  # Re-fermer pour affichage
        
        print(f"Chemin: {optimal_path_closed}")
        print(f"Distance 2-OPT: {opt_distance:.2f}")

        # === COMPARAISON ===
        improvement = knn_distance - opt_distance
        improvement_pct = (improvement / knn_distance) * 100
        
        print(f"\nAmélioration: {improvement:.2f} ({improvement_pct:.1f}%)")
        
        # Stocker (chemin FERMÉ pour la visualisation)
        pays.best_path_knn = knn_path
        pays.best_path_two_opt = optimal_path_closed  # Chemin fermé
        
        return pays

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        raise