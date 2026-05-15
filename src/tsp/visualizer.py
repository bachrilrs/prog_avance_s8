"""Visualisation des résultats TSP."""

import os
import matplotlib.pyplot as plt
import numpy as np
from .structure import DistanceGraph


class TSPVisualizer:
    """Visualisateur pour les solutions TSP."""
    
    def __init__(self, graph: DistanceGraph, country_name: str = None):
        self.graph = graph
        self.country_name = country_name or "TSP"
            
    def plot_path(self, path, title=None, save_path=None):
        """Trace un chemin avec des flèches et labels."""
        if title is None:
            title = f"{self.country_name} - {path.algo_name} - Distance: {path.distance_path:.2f}"
        
        x = [self.graph.villes[self.graph.index[nom]].coord_X for nom in path.path]
        y = [self.graph.villes[self.graph.index[nom]].coord_Y for nom in path.path]
        
        nb_villes = len(path.path) - 1
        x = np.array(x)
        y = np.array(y)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.scatter(x, y, color="#D4AE4F", s=150, zorder=5, edgecolors="#D4AE4F", linewidth=2)
        
        u = np.diff(x)
        v = np.diff(y)
        ax.quiver(x[:-1], y[:-1], u, v, angles='xy', scale_units='xy', scale=1,
                color='#2E86AB', width=0.004, headwidth=4, alpha=0.7)
        
        for i, nom in enumerate(path.path[:-1]):
            ax.text(x[i], y[i] + 0.5, nom, fontsize=9, ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        ax.scatter(x[0], y[0], color='green', s=300, marker='*', zorder=10, 
                edgecolors='darkgreen', linewidth=2, label='Départ')
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('X', fontsize=11)
        ax.set_ylabel('Y', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')
        
        plt.tight_layout()
        
        # Si save_path est fourni, l'utiliser; sinon utiliser le default
        if save_path is None:
            save_path = f"results/{self.country_name}_{path.algo_name}_{nb_villes}_path.png"
        
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
        
        plt.close()  # Fermer la figure pour libérer la mémoire
    
    def plot_comparison(self, best_overall, save_path=None):
        """Trace les meilleurs chemins côte à côte."""
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True) if save_path else None
        
        paths = list(best_overall.values())
        n_plots = len(paths)
        n_cols = 2
        n_rows = (n_plots + 1) // 2
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 6 * n_rows))
        if n_plots == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        for ax, path in zip(axes, paths):
            x = [self.graph.villes[self.graph.index[nom]].coord_X for nom in path.path]
            y = [self.graph.villes[self.graph.index[nom]].coord_Y for nom in path.path]
            
            x = np.array(x)
            y = np.array(y)
            
            ax.scatter(x, y, color="#D4AE4F", s=100, zorder=5)
            
            u = np.diff(x)
            v = np.diff(y)
            ax.quiver(x[:-1], y[:-1], u, v, angles='xy', scale_units='xy', scale=1,
                     color='#2E86AB', width=0.003, alpha=0.7)
            
            ax.scatter(x[0], y[0], color='green', s=200, marker='*', zorder=10)
            
            title = f"{path.algo_name}\nDistance: {path.distance_path:.2f} | Temps: {path.temps_execution:.4f}s"
            ax.set_title(title, fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
        
        for i in range(len(paths), len(axes)):
            axes[i].axis('off')
        
        fig.suptitle(f"{self.country_name} - Comparaison des Algorithmes", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {save_path}")
        
        plt.close()
    
    def plot_distances_comparison(self, best_overall, save_path=None):
        """Trace histogramme des distances."""
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True) if save_path else None
        
        algos = list(best_overall.keys())
        distances = [best_overall[algo].distance_path for algo in algos]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ["#BA4545", '#4ECDC4', '#45B7D1', '#FFA07A'][:len(algos)]
        bars = ax.bar(algos, distances, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
        
        for bar, dist in zip(bars, distances):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{dist:.2f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Distance', fontsize=12, fontweight='bold')
        ax.set_title(f'{self.country_name} - Distance par Algorithme', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {save_path}")
        
        plt.close()

    def plot_all_results(self, best_overall, save_dir="results/"):
        """Génère tous les plots d'un coup."""
        
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"Génération des plots pour {self.country_name}...")
        
        # 1. Meilleur chemin par algo
        for algo_name, path in best_overall.items():
            filename = f"{self.country_name}_{algo_name}_path.png"
            self.plot_path(
                path,
                save_path=os.path.join(save_dir, filename)
            )
        
        # 2. Comparaison
        if len(best_overall) > 0:
            comparison_file = f"{self.country_name}_comparison.png"
            self.plot_comparison(
                best_overall, 
                save_path=os.path.join(save_dir, comparison_file)
            )
        
        # 3. Histogramme distances
        if len(best_overall) > 0:
            distances_file = f"{self.country_name}_distances.png"
            self.plot_distances_comparison(
                best_overall, 
                save_path=os.path.join(save_dir, distances_file)
            )
        
        print(f"✓ Tous les plots générés pour {self.country_name} dans '{save_dir}'")