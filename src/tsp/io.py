import os
import pandas as pd
from .structure import Ville, DistanceGraph, Pays


def load_cities(filepath, separator=";"):
    """Charge les villes depuis un fichier CSV avec noms uniques."""
    df = pd.read_csv(filepath, sep=separator, header=None)

    if df.shape[1] != 3:
        raise ValueError(f"Le fichier doit avoir 3 colonnes, trouvé {df.shape[1]}")

    df.columns = ["nom", "latitude", "longitude"]

    villes = []
    seen = {}

    for _, row in df.iterrows():
        base_name = str(row["nom"]).strip()

        if base_name in seen:
            seen[base_name] += 1
            nom = f"{base_name}_{seen[base_name]}"
        else:
            seen[base_name] = 1
            nom = base_name

        ville = Ville(nom)
        ville.coord_X = float(row["longitude"])
        ville.coord_Y = float(row["latitude"])
        villes.append(ville)

    return villes


def export_results_csv(pays, base_name=None):
    """Exporte les meilleurs résultats avec le nom du pays."""
    if base_name is None:
        base_name = pays.nom
    
    if base_name.startswith("results/"):
        base_name = base_name.replace("results/", "")
    filepath = f"results/{base_name}_results.csv"
    os.makedirs("results", exist_ok=True)
    
    lignes = []
    for algo_name, path_obj in pays.best_overall.items():
        lignes.append({
            'Algorithme': algo_name.upper(),
            'Point de Départ': path_obj.point_depart,
            'Distance': round(path_obj.distance_path, 2),
            'Temps (s)': round(path_obj.temps_execution, 4),
        })
    
    df = pd.DataFrame(lignes)
    df.to_csv(filepath, index=False)
    print(f"{filepath}")


def export_comparison_csv(pays, base_name=None):
    """Exporte comparaison avec les algos disponibles (version robuste)."""
    if base_name is None:
        base_name = pays.nom

    if base_name.startswith("results/"):
        base_name = base_name.replace("results/", "")
    
    filepath = f"results/{base_name}_comparison.csv"
    os.makedirs("results", exist_ok=True)

    available_algos = [algo for algo in ['knn', 'two_opt', 'three_opt'] 
                       if pays.results[algo]]
    
    if not available_algos:
        print("Aucun résultat disponible pour la comparaison")
        return
    
    lignes = []
    
    all_start_cities = [set(pays.results[algo].keys()) for algo in available_algos]
    common_start_cities = set.intersection(*all_start_cities) if all_start_cities else set()
    
    if not common_start_cities:
        print("Aucune ville de départ commune entre tous les algos")
        return
    
    for start_city in sorted(common_start_cities):
        ligne = {'Point Départ': start_city}
        
        for algo in available_algos:
            if start_city in pays.results[algo]:
                dist = pays.results[algo][start_city].distance_path
                ligne[algo.upper()] = round(dist, 2)
        
        if len(available_algos) >= 2:
            first_dist = pays.results[available_algos[0]][start_city].distance_path
            last_dist = pays.results[available_algos[-1]][start_city].distance_path
            improvement = ((first_dist - last_dist) / first_dist) * 100
            ligne['Amélioration (%)'] = round(improvement, 2)
        
        lignes.append(ligne)
    
    df = pd.DataFrame(lignes)
    if 'Amélioration (%)' in df.columns:
        df = df.sort_values('Amélioration (%)', ascending=False)
    
    df.to_csv(filepath, index=False)
    print(f"✓ {filepath}")