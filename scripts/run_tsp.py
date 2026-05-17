#!/usr/bin/env python3
import os
import time
import traceback
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from src.tsp import (
    load_cities,
    Pays,
    export_results_csv,
    export_comparison_csv,
    TSPVisualizer,
)


COUNTRIES_CONFIG = {
    "France10": {
        "csv_file": "data/fr-10.csv",
        "algorithms": ["knn", "2opt", "3opt", "genetic"],
        "config": {
            "2opt": {"max_no_improve": 50},
            "3opt": {"max_iterations": 20, "timeout": 60},
            "genetic": {"pop_size": 20, "generations": 100, "mutation_rate": 0.05},
        },
    },
    "France50": {
        "csv_file": "data/fr-50.csv",
        "algorithms": ["knn", "2opt", "3opt", "genetic"],
        "config": {
            "2opt": {"max_no_improve": 50},
            "3opt": {"max_iterations": 20, "timeout": 300},
            "genetic": {"pop_size": 50, "generations": 300, "mutation_rate": 0.05},
        },
    },
    "France100": {
        "csv_file": "data/fr-100.csv",
        "algorithms": ["knn", "2opt", "3opt", "genetic"],
        "config": {
            "2opt": {"max_no_improve": 50},
            "3opt": {"max_iterations": 20, "timeout": 600},
            "genetic": {"pop_size": 100, "generations": 500, "mutation_rate": 0.05},
        },
    },
    "France650": {
    "csv_file": "data/fr.csv",
    "algorithms": ["knn", "2opt", "3opt", "genetic"],
    "config": {
        "2opt": {"max_no_improve": 10},
        "3opt": {"max_iterations": 5, "timeout": 3600},
        "genetic": {"pop_size": 50, "generations": 100, "mutation_rate": 0.05},
    }
}
}


def run_algorithm(pays, algo, verbose=False, **kwargs):
    algo_map = {
        "knn": pays.run_knn_only,
        "2opt": pays.run_two_opt_only,
        "3opt": pays.run_three_opt_best_only,
        "genetic": pays.run_ga_only,
    }

    if algo not in algo_map:
        raise ValueError(f"Unknown algorithm: {algo}")

    algo_map[algo](verbose=verbose, **kwargs)


def collect_best_results(pays, country_name):
    rows = []

    n_cities = len(pays.graph.villes)

    for algo, path in pays.best_overall.items():
        rows.append({
            "Instance": country_name,
            "Nb villes": n_cities,
            "Algo": algo.upper(),
            "Distance": path.distance_path,
            "Temps (s)": path.temps_execution,
            "Départ": path.point_depart,
        })

    return rows


def plot_global_distance_barplot(df, save_path):
    plt.figure(figsize=(12, 7))

    pivot = df.pivot_table(
        index="Nb villes",
        columns="Algo",
        values="Distance",
        aggfunc="min"
    )

    pivot.plot(kind="bar", figsize=(12, 7))

    plt.title("Comparaison des distances par algorithme")
    plt.xlabel("Nombre de villes")
    plt.ylabel("Distance totale")
    plt.xticks(rotation=0)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def plot_global_time_barplot(df, save_path):
    plt.figure(figsize=(12, 7))

    pivot = df.pivot_table(
        index="Nb villes",
        columns="Algo",
        values="Temps (s)",
        aggfunc="min"
    )

    pivot.plot(kind="bar", figsize=(12, 7), logy=True)

    plt.title("Comparaison des temps d'exécution par algorithme")
    plt.xlabel("Nombre de villes")
    plt.ylabel("Temps d'exécution (s) - échelle log")
    plt.xticks(rotation=0)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def plot_quality_time_scatter(df, save_path):
    plt.figure(figsize=(10, 7))

    for algo in df["Algo"].unique():
        sub = df[df["Algo"] == algo]
        plt.scatter(sub["Temps (s)"], sub["Distance"], label=algo, s=120)

        for _, row in sub.iterrows():
            plt.text(
                row["Temps (s)"],
                row["Distance"],
                f" {int(row['Nb villes'])}",
                fontsize=9
            )

    plt.xscale("log")
    plt.title("Compromis distance / temps")
    plt.xlabel("Temps d'exécution (s) - échelle log")
    plt.ylabel("Distance totale")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def process_country(country_name, config, save_dir):
    country_save_dir = os.path.join(save_dir, country_name)
    os.makedirs(country_save_dir, exist_ok=True)

    print(f"\n{'=' * 60}")
    print(f"PROCESSING: {country_name}")
    print(f"{'=' * 60}")

    try:
        print(f"[1/5] Loading cities from {config['csv_file']}...")
        villes = load_cities(config["csv_file"])
        pays = Pays(country_name, villes=villes)

        print(f"✓ {len(villes)} cities loaded")

        print(f"\n[2/5] Running algorithms: {', '.join(config['algorithms'])}")

        for idx, algo in enumerate(config["algorithms"], 1):
            algo_config = config.get("config", {}).get(algo, {})

            print(f"  [{idx}/{len(config['algorithms'])}] Running {algo.upper()}...")
            run_algorithm(pays, algo, verbose=False, **algo_config)

            export_results_csv(
                pays,
                os.path.join(country_save_dir, f"{country_name}_{algo}")
            )

            if algo != "knn":
                export_comparison_csv(
                    pays,
                    os.path.join(country_save_dir, f"{country_name}_{algo}")
                )

        print("\n[3/5] Generating local visualizations...")

        viz = TSPVisualizer(pays.graph, country_name=country_name)
        meilleur = pays.meilleur_global()

        viz.plot_path(
            meilleur,
            save_path=os.path.join(country_save_dir, f"{country_name}_best_path.png")
        )

        viz.plot_comparison(
            pays.best_overall,
            save_path=os.path.join(country_save_dir, f"{country_name}_comparison_paths.png")
        )

        viz.plot_distances_comparison(
            pays.best_overall,
            save_path=os.path.join(country_save_dir, f"{country_name}_distances.png")
        )

        # Correction importante
        viz.plot_all_results(
            pays.best_overall,
            save_dir=country_save_dir
        )

        print("\n[4/5] Saving summary...")
        df = pays.to_results_dataframe()
        summary_path = os.path.join(country_save_dir, f"{country_name}_summary.csv")
        df.to_csv(summary_path, index=False)

        print(f"✓ Summary saved: {summary_path}")

        print("\n[5/5] Done")
        return True, collect_best_results(pays, country_name)

    except Exception as e:
        print(f"\n✗ {country_name} failed")
        print(f"{type(e).__name__}: {e}")
        traceback.print_exc()
        return False, []


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = f"results/tsp_pipeline_{timestamp}"
    os.makedirs(save_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("TSP SOLVER PIPELINE")
    print("=" * 60)
    print(f"Output directory: {save_dir}")

    start_time = time.time()
    all_best_rows = []
    status = {}

    for country_name, config in COUNTRIES_CONFIG.items():
        ok, rows = process_country(country_name, config, save_dir)
        status[country_name] = ok
        all_best_rows.extend(rows)

    print("\nGenerating global comparison figures...")

    global_df = pd.DataFrame(all_best_rows)
    global_csv = os.path.join(save_dir, "global_best_results.csv")
    global_df.to_csv(global_csv, index=False)

    plot_global_distance_barplot(
        global_df,
        os.path.join(save_dir, "global_distance_barplot.png")
    )

    plot_global_time_barplot(
        global_df,
        os.path.join(save_dir, "global_time_barplot.png")
    )

    plot_quality_time_scatter(
        global_df,
        os.path.join(save_dir, "global_quality_time_scatter.png")
    )

    elapsed = time.time() - start_time

    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)

    for country, ok in status.items():
        print(f"{'✓' if ok else '✗'} {country}")

    print(f"\nTotal time: {elapsed:.2f}s")
    print(f"Results: {save_dir}")


if __name__ == "__main__":
    main()