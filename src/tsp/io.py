
import pandas as pd

from .structure import Ville , Pays

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
def process_pays_travel(file_path: str, nom_pays: str, separator: str = ";", all_paths: bool = False, show_matrix: bool = False):
    """Traite l'analyse TSP pour un seul pays."""
    try:
        villes = load_cities(file_path, separator)
        pays = Pays(nom_pays, villes)

        print(f"--- Analyse en cours pour : {nom_pays} ---")

        
        if show_matrix:
            print("\nMatrice de distances :")
            print(pays.get_matrix_with_labels())
        
        print("\nCalcul des chemins...")
        pays.compute_all_paths()
        
        if all_paths:
            print("\nDistance totale par point de départ :")
            pays.print_distance_from_each_city()
        
        # --- KNN ---
        print("\n--- Meilleur chemin trouvé avec KNN ---")
        start_point, knn_path, knn_distance = pays.get_optimal_path()

        print(f"Point de départ: {start_point}")
        print(f"Distance KNN: {knn_distance:.2f}")

        # --- 2-OPT ---
        print("\n--- Meilleur chemin trouvé avec 2-opt ---")
        knn_path_open = knn_path[:-1]  
        
        optimal_path_open, opt_distance = pays.two_opt.two_opt(knn_path_open)
        optimal_path_closed = optimal_path_open + [optimal_path_open[0]]  
        
        print(f"Distance 2-OPT: {opt_distance:.2f}")
        
        improvement = knn_distance - opt_distance
        improvement_pct = (improvement / knn_distance) * 100
        print(f"Amélioration: {improvement:.2f} ({improvement_pct:.1f}%)")
        
        pays.best_path_knn = knn_path
        pays.best_path_two_opt = optimal_path_closed  
        
        # --- 3-OPT ---
        print("\n--- Meilleur chemin trouvé avec 3-opt ---")
        optimal_path_open_3, opt_distance_3 = pays.two_opt.three_opt(optimal_path_open)
        optimal_path_closed_3 = optimal_path_open_3 + [optimal_path_open_3[0]]
        
        print(f"Distance 3-OPT: {opt_distance_3:.2f}")

        improvement_2_to_3 = opt_distance - opt_distance_3
        if improvement_2_to_3 > 0:
            improvement_pct_3 = (improvement_2_to_3 / opt_distance) * 100
            print(f"Amélioration de 2-opt vers 3-opt: {improvement_2_to_3:.2f} ({improvement_pct_3:.1f}%)")
        else:
            print("Le 3-opt n'a pas trouvé de meilleur chemin que le 2-opt.")
            
        pays.best_path_three_opt = optimal_path_closed_3    


        return pays

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        return None
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        raise
