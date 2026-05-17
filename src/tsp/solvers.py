import numpy as np
import random
import time
import heapq
from tqdm import tqdm
from .structure import DistanceGraph, Path


class BaseSolver:
    """Classe regroupant les différentes heuristiques pour résoudre le TSP"""
    def __init__(self, graph):
        self.graph = graph
        self.villes = graph.villes
        self.matrix_distance = graph.matrix
        self.index_ville = graph.index


class KNN(BaseSolver):
    """K-Nearest Neighbor optimisé."""
    
    def __init__(self, graph):
        super().__init__(graph)
        self.all_paths = {}
    
    def _knn_from_start(self, start_idx):
        """Résout KNN depuis un point de départ spécifique. O(n²)"""
        n = len(self.matrix_distance)
        visited = np.zeros(n, dtype=bool)  #  numpy au lieu de liste
        path = [self.villes[start_idx].nom]
        visited[start_idx] = True
        current = start_idx
        
        # Greedy: aller au plus proche voisin non visité
        for _ in range(n - 1):
            #  Utiliser argmin au lieu de boucle manuelle
            distances = self.matrix_distance[current].copy()
            distances[visited] = np.inf
            nearest = np.argmin(distances)
            
            path.append(self.villes[nearest].nom)
            visited[nearest] = True
            current = nearest
        
        # Fermer le chemin
        path.append(self.villes[start_idx].nom)
        distance = self.graph.path_distance(path)
        
        return Path(path=path, distance_path=distance, algo_name="KNN")
        
    def solve(self, start_idx=None, verbose=False):

        """

        Si start_idx est fourni : calcule KNN depuis cette ville uniquement.

        Sinon : teste plusieurs départs.

        """

        n = len(self.villes)
        if start_idx is not None:
            path = self._knn_from_start(start_idx)
            self.all_paths = {self.villes[start_idx].nom: path}
            return path
        if n <= 50:
            starts = range(n)

        else:
            starts = np.random.choice(n, min(10, n), replace=False)

        self.all_paths = {}
        for i in starts:
            path = self._knn_from_start(i)
            self.all_paths[self.villes[i].nom] = path
            if verbose and i % max(1, n // 5) == 0:
                print(f"  {i + 1}/{n} testés")
        best = min(self.all_paths.values(), key=lambda p: p.distance_path)
        return best


class TwoOpt(BaseSolver):
    """2-OPT optimisé avec delta local."""

    def __init__(self, graph):
        super().__init__(graph)

    def solve(self, path_obj, max_no_improve=50, verbose=False):
        """
        2-OPT avec delta local O(1) au lieu de recalcul O(n).
        Aussi : réduire max_no_improve par défaut.
        """
        best_path = path_obj.path[:]
        best_distance = path_obj.distance_path
        n = len(best_path)
        
        no_improve_count = 0
        iteration = 0
        
        while no_improve_count < max_no_improve:
            iteration += 1
            improved_this_round = False
            
            for i in range(n - 1):
                if improved_this_round:
                    break
                    
                for j in range(i + 2, n):
                    if i == 0 and j == n - 1:
                        continue
                    
                    #  Indices pré-calculés
                    a_idx = self.index_ville[best_path[i]]
                    b_idx = self.index_ville[best_path[i + 1]]
                    c_idx = self.index_ville[best_path[j]]
                    d_idx = self.index_ville[best_path[(j + 1) % n]]
                    
                    #  Delta local O(1)
                    old_dist = self.matrix_distance[a_idx][b_idx] + self.matrix_distance[c_idx][d_idx]
                    new_dist = self.matrix_distance[a_idx][c_idx] + self.matrix_distance[b_idx][d_idx]
                    
                    if new_dist < old_dist - 1e-9:
                        best_distance += (new_dist - old_dist)
                        best_path[i + 1:j + 1] = reversed(best_path[i + 1:j + 1])
                        improved_this_round = True
                        
                        if verbose and iteration % 10 == 0:
                            print(f"  2-OPT it {iteration}: {best_distance:.2f}")
                        break
            
            if not improved_this_round:
                no_improve_count += 1
            else:
                no_improve_count = 0
        
        return Path(path=best_path, distance_path=best_distance, algo_name="2-OPT")


class ThreeOpt(BaseSolver):
    """3-OPT optimisé : early stopping agressif."""

    def __init__(self, graph):
        super().__init__(graph)

    def _find_best_move(self, path, i, j, k):
        """Évalue les 7 reconnexions possibles."""
        A = self.index_ville[path[i - 1]]
        B = self.index_ville[path[i]]
        C = self.index_ville[path[j - 1]]
        D = self.index_ville[path[j]]
        E = self.index_ville[path[k - 1]]
        F = self.index_ville[path[k]]
        
        d = self.matrix_distance
        cur = d[A][B] + d[C][D] + d[E][F]
        
        deltas = [
            d[A][C] + d[B][D] + d[E][F] - cur,
            d[A][B] + d[C][E] + d[D][F] - cur,
            d[A][C] + d[B][E] + d[D][F] - cur,
            d[A][D] + d[E][B] + d[C][F] - cur,
            d[A][E] + d[D][B] + d[C][F] - cur,
            d[A][D] + d[E][C] + d[B][F] - cur,
            d[A][E] + d[D][C] + d[B][F] - cur,
        ]
        
        min_delta = min(deltas)
        best_idx = deltas.index(min_delta)
        return min_delta, best_idx

    def _apply_move(self, path, i, j, k, move_idx):
        """Applique une reconnexion 3-OPT."""
        seg1 = path[:i]
        seg2 = path[i:j]
        seg3 = path[j:k]
        seg4 = path[k:]
        
        moves = [
            seg1 + seg2[::-1] + seg3 + seg4,
            seg1 + seg2 + seg3[::-1] + seg4,
            seg1 + seg2[::-1] + seg3[::-1] + seg4,
            seg1 + seg3 + seg2 + seg4,
            seg1 + seg3[::-1] + seg2 + seg4,
            seg1 + seg3 + seg2[::-1] + seg4,
            seg1 + seg3[::-1] + seg2[::-1] + seg4,
        ]
        return moves[move_idx]

    def solve(self, path_obj, max_iterations=10, timeout=30.0, verbose=False, best_only=False):
        """
        3-OPT optimisé.
        
        Args:
            path_obj: Path objet à améliorer
            max_iterations: Nombre max d'itérations
            timeout: Temps max en secondes
            verbose: Afficher progression
            best_only: Si True, utilisé uniquement dans run_three_opt_best_only
        """
        best_path = path_obj.path[:]
        if best_path[0] != best_path[-1]:
            best_path.append(best_path[0])
        
        n = len(best_path)
        start_time = time.time()
        iteration = 0
        no_improve_count = 0
        
        while iteration < max_iterations and (time.time() - start_time) < timeout:
            iteration += 1
            improved = False
            
            for i in range(1, min(n - 2, n // 2)):
                if improved or no_improve_count > 3:
                    break
                    
                for j in range(i + 1, min(n - 1, i + n // 3)):
                    if improved or no_improve_count > 3:
                        break
                        
                    for k in range(j + 1, min(n, j + n // 3)):
                        min_delta, move_idx = self._find_best_move(best_path, i, j, k)
                        
                        if min_delta < -1e-9:
                            best_path = self._apply_move(best_path, i, j, k, move_idx)
                            improved = True
                            no_improve_count = 0
                            break
            
            if not improved:
                no_improve_count += 1
            
            if no_improve_count >= 2:
                break
        
        if best_path[0] != best_path[-1]:
            best_path.append(best_path[0])
        
        distance = self.graph.path_distance(best_path)
        return Path(path=best_path, distance_path=distance, algo_name="3-OPT")
class AlgoGenetique(BaseSolver):
    """Algorithme génétique optimisé."""
    
    def __init__(self, graph, pop_size=50, generations=50, mutation_rate=0.05):
        super().__init__(graph)
        self.pop_size = pop_size  #  Réduit de 100 à 50
        self.generations = generations  #  Réduit de 100 à 50
        self.mutation_rate = mutation_rate
        self.population = self.generate_initial_population(pop_size)
        self.best_fitness_history = []
    
    def generate_initial_population(self, population_size):
        """Génère une population initiale aléatoire."""
        noms_villes = [ville.nom for ville in self.villes]
        population = []
        
        for _ in range(population_size):
            random_path = noms_villes.copy()
            np.random.shuffle(random_path)
            population.append(random_path)
        
        return population
    
    def select_parents(self, scored_population, nb_parents=2):
        """Sélectionne les meilleurs parents."""
        top_entries = heapq.nsmallest(nb_parents, scored_population, key=lambda x: x[0])
        return [path for score, path in top_entries]
    
    def ordered_crossover(self, parent1, parent2):
        """Crossover ordonné (OX)."""
        n = len(parent1)
        cut1 = random.randint(0, n - 2)
        cut2 = random.randint(cut1 + 1, n - 1)
        
        child = [None] * n
        child[cut1:cut2] = parent1[cut1:cut2]
        
        p2_pool = [city for city in parent2 if city not in child[cut1:cut2]]
        
        idx = 0
        for i in range(n):
            if child[i] is None:
                child[i] = p2_pool[idx]
                idx += 1
        
        return child
    
    def mutation(self, path):
        """Mutation par échange aléatoire."""
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(path)), 2)
            path[i], path[j] = path[j], path[i]
        return path
    
    def solve(self, initial_path=None, verbose=False):
        """Résout TSP avec AG."""
        if initial_path:
            if initial_path[0] == initial_path[-1]:
                initial_path = initial_path[:-1]
            self.population[0] = initial_path[:]
        
        for gen in tqdm(range(self.generations), disable=not verbose):
            scored_population = []
            for chromosome in self.population:
                closed_path = chromosome + [chromosome[0]]
                dist = self.graph.path_distance(closed_path)
                scored_population.append((dist, chromosome))
            
            scored_population.sort(key=lambda x: x[0])
            best_dist = scored_population[0][0]
            self.best_fitness_history.append(best_dist)
            
            if verbose and gen % 10 == 0:
                print(f"  Génération {gen}: {best_dist:.2f}")
            
            new_population = [scored_population[0][1]]
            
            while len(new_population) < self.pop_size:
                parents = self.select_parents(scored_population, nb_parents=2)
                child = self.ordered_crossover(parents[0], parents[1])
                child = self.mutation(child)
                new_population.append(child)
            
            self.population = new_population
        
        final_best = self.population[0]
        final_best_closed = final_best + [final_best[0]]
        final_dist = self.graph.path_distance(final_best_closed)
        
        return Path(path=final_best_closed, distance_path=final_dist, algo_name="AG")
    
class TSPOrchestrator:
    """Classe orchestrant l'exécution de tous les algorithmes sur un même graphe et stockant les résultats."""

    def __init__(self, graph: DistanceGraph):
        self.graph = graph
        self.knn = KNN(graph)
        self.two_opt = TwoOpt(graph)
        self.three_opt = ThreeOpt(graph)

    def solve_all(self, verbose: bool = True):
        """
        Résout TSP: KNN sur tous les départs → 2-OPT et 3-OPT sur chaque résultat.
        
        Returns: avec tous les résultats
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"RÉSOLUTION TSP - {len(self.graph.villes)} villes")
            print(f"{'='*70}")
        
        # --- KNN sur tous les départs ---
        if verbose:
            print(f"\n[1/3] K-Nearest Neighbor (tous les départs)...")
        knn_results = self.knn.solve_all_starts(verbose=verbose)
        
        # --- 2-OPT et 3-OPT sur chaque résultat KNN ---
        if verbose:
            print(f"\n[2/3] 2-OPT (amélioration locale)...")
        two_opt_results = {}
        
        for start_city, knn_path in knn_results.items():
            start_t = time.time()
            path_2opt = self.two_opt.solve(knn_path, verbose=False)
            path_2opt.temps_execution = time.time() - start_t
            two_opt_results[start_city] = path_2opt
            
            if verbose:
                improvement = ((knn_path.distance_path - path_2opt.distance_path) / knn_path.distance_path) * 100
                print(f"  2-OPT depuis {start_city:15s} → {path_2opt.distance_path:.2f} "
                    f"(amélioration: {improvement:.1f}%)")
        
        if verbose:
            print(f"\n[3/3] 3-OPT (amélioration fine)...")
        three_opt_results = {}
        
        for start_city, two_opt_path in two_opt_results.items():
            start_t = time.time()
            path_3opt = self.three_opt.solve(two_opt_path, verbose=False)
            path_3opt.temps_execution = time.time() - start_t
            three_opt_results[start_city] = path_3opt
            
            if verbose:
                improvement = ((two_opt_path.distance_path - path_3opt.distance_path) / two_opt_path.distance_path) * 100
                print(f"  3-OPT depuis {start_city:15s} → {path_3opt.distance_path:.2f} "
                    f"(amélioration: {improvement:.1f}%)")
        

        resultats = {
            'knn': knn_results,
            'two_opt': two_opt_results,
            'three_opt': three_opt_results}
        

        if verbose:
            print("Résolution complète")
        
        return resultats