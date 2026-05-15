#!/usr/bin/env python3
"""
TSP Solver Pipeline: Simple multi-country runner with genetic algorithm support.
"""
import os
import time
from datetime import datetime
from src.tsp import load_cities, Pays, export_results_csv, export_comparison_csv, TSPVisualizer
import traceback

# Configuration
COUNTRIES_CONFIG = {
    "France650": {
        "csv_file": "data/fr.csv",
        "algorithms": ["knn", "2opt", "3opt"],
        "config": {
            "2opt": {"max_no_improve": 10},
            "3opt": {"max_iterations": 5, "timeout": 3600},
        }
    },
    "France100": {
        "csv_file": "data/fr-100.csv",
        "algorithms": ["knn", "2opt", "3opt", "genetic"],
        "config": {
            "genetic": {"population_size": 100, "generations": 500},
        }
    },
    "France50": {
        "csv_file": "data/fr-50.csv",
        "algorithms": ["knn", "2opt", "3opt", "genetic"],
        "config": {
            "genetic": {"population_size": 50, "generations": 300},
        }
    },
    "France10": {
        "csv_file": "data/fr-10.csv",
        "algorithms": ["knn", "2opt", "3opt", "genetic"],
        "config": {
            "genetic": {"population_size": 20, "generations": 100},
        }
    },
}

def run_algorithm(pays, algo, verbose=False, **kwargs):
    """Run a single algorithm on Pays object."""
    algo_map = {
        "knn": pays.run_knn_only,
        "2opt": pays.run_two_opt_only,
        "3opt": pays.run_three_opt_best_only,
        "genetic": pays.run_ga_only,
    }
    
    if algo not in algo_map:
        raise ValueError(f"Unknown algorithm: {algo}")
    
    algo_map[algo](verbose=verbose, **kwargs)


def process_country(country_name, config, save_dir):
    """Process a single country: load, run algorithms, export results, generate plots."""
    country_save_dir = os.path.join(save_dir, country_name)
    os.makedirs(country_save_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"PROCESSING: {country_name}")
    print(f"{'='*60}")
    
    try:
        # Load cities
        print(f"[1/5] Loading cities from {config['csv_file']}...")
        villes = load_cities(config['csv_file'])
        print(f"  First 5 cities: {[v.nom for v in villes[:5]]}")
        pays = Pays(country_name, villes=villes)
        print(f"✓ {len(villes)} cities loaded")
        
        # Run algorithms
        print(f"\n[2/5] Running algorithms: {', '.join(config['algorithms'])}...")
        algorithms = config['algorithms']
        for idx, algo in enumerate(algorithms, 1):
            algo_config = config.get('config', {}).get(algo, {})
            print(f"  [{idx}/{len(algorithms)}] Running {algo.upper()}...")
            
            run_algorithm(pays, algo, verbose=False, **algo_config)
            export_results_csv(pays, os.path.join(country_save_dir, f"{country_name}_{algo}"))
            
            if algo != "knn":
                try:
                    export_comparison_csv(pays, os.path.join(country_save_dir, f"{country_name}_{algo}"))
                except KeyError as e:
                    print(f" Comparison skip (different start cities): {e}")
        
        # Generate visualizations
        print(f"\n[3/5] Generating visualizations...")
        try:
            viz = TSPVisualizer(pays.graph, country_name=country_name)
            meilleur = pays.meilleur_global()
            
            if meilleur is None:
                print("⚠️  No best path found, skipping visualization")
            else:
                print(f"  Best path: {meilleur.algo_name} - {len(meilleur.path)} cities")
                
                # Plot individual best path
                viz.plot_path(
                    meilleur, 
                    save_path=os.path.join(country_save_dir, f"{country_name}_best_path.png")
                )
                
                # Plot comparison grid
                viz.plot_comparison(
                    pays.best_overall, 
                    save_path=os.path.join(country_save_dir, f"{country_name}_comparison.png")
                )
                
                # Plot distances histogram
                viz.plot_distances_comparison(
                    pays.best_overall, 
                    save_path=os.path.join(country_save_dir, f"{country_name}_distances.png")
                )

                viz.plot_all_results(
                    pays.results,
                    save_path=os.path.join(country_save_dir, f"{country_name}_all_results.png")
                )
                
                print("✓ All visualizations saved")
                
        except Exception as viz_error:
            print(f"⚠️  Visualization error (non-blocking): {viz_error}")
            traceback.print_exc()
        
        # Save summary dataframe
        print(f"\n[4/5] Saving summary...")
        df = pays.to_results_dataframe()
        summary_path = os.path.join(country_save_dir, f"{country_name}_summary.csv")
        df.to_csv(summary_path, index=False)
        print(f"✓ Summary saved: {summary_path}")
        
        # List all generated files
        print(f"\n[5/5] Generated files:")
        files = sorted(os.listdir(country_save_dir))
        for f in files:
            file_path = os.path.join(country_save_dir, f)
            size = os.path.getsize(file_path)
            size_str = f"{size/1024:.1f}K" if size > 1024 else f"{size}B"
            print(f"  ✓ {f:<50} ({size_str})")
        
        print(f"\n✓ {country_name} completed successfully\n")
        return True
        
    except Exception as e:
        print(f"\n✗ {country_name} failed with error:")
        print(f"   {type(e).__name__}: {e}")
        traceback.print_exc()
        print()
        return False

def main():
    """Main pipeline: run all countries."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = f"results/tsp_pipeline_{timestamp}/"
    os.makedirs(save_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("TSP SOLVER PIPELINE - MULTI-COUNTRY RUNNER")
    print("="*60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output directory: {save_dir}")
    print(f"Countries: {len(COUNTRIES_CONFIG)}\n")
    
    start_time = time.time()
    results = {}
    
    for country_name, config in COUNTRIES_CONFIG.items():
        results[country_name] = process_country(country_name, config, save_dir)
    
    elapsed = time.time() - start_time
    success = sum(1 for v in results.values() if v)
    
    print("\n" + "="*60)
    print("PIPELINE SUMMARY")
    print("="*60)
    print(f"✓ Success: {success}/{len(COUNTRIES_CONFIG)}")
    for country, status in results.items():
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {country}")
    
    print(f"\n⏱️  Total time: {elapsed:.2f}s ({elapsed/60:.2f}m)")
    print(f"📁 Results: {save_dir}\n")

if __name__ == "__main__":
    main()