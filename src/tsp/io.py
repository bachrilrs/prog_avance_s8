
import pandas as pd

from .structure import Ville

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
