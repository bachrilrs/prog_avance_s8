import numpy as np
import random
import time
import heapq
from tqdm import tqdm
from .structure import DistanceGraph, Parcours

class Heuristique:
    """Classe regroupant les différentes heuristiques pour résoudre le TSP"""
    def __init__(self, graph: DistanceGraph):
        self.graph = graph
        self.villes = graph.villes
        self.matrix_distance = graph.matrix
        self.index_ville = graph.index

    def solve(self):
        """Classe solve qui est passé aux classes filles"""
        pass

class KNN(Heuristique):
    """KNN"""
    def __init__(self, graph: DistanceGraph):
        super().__init__(graph)
        self.paths = {}
        self.distances = {}
    
    def _knn_with_matrix(self, start: int) -> None:
        """Résout KNN depuis UN point de départ."""
        n = len(self.matrix_distance)
        visited = [False] * n
        path = [self.villes[start].nom]
        visited[start] = True
        current = start
        
        # Greedy: toujours aller au plus proche voisin non visité
        for _ in range(n - 1):
            nearest = None
            nearest_dist = float('inf')
            
            for j in range(n):
                if not visited[j] and self.matrix_distance[current][j] < nearest_dist:
                    nearest_dist = self.matrix_distance[current][j]
                    nearest = j
            
            if nearest is None:  # Sécurité (ne devrait pas arriver)
                raise ValueError(f"Impossible de trouver le prochain voisin à partir de {current}")
            
            path.append(self.villes[nearest].nom)
            visited[nearest] = True
            current = nearest
        
        path.append(self.villes[start].nom)  # Retour au départ (chemin fermé)
        self.paths[self.villes[start].nom] = path
    
    def knn_multistart(self, num_random_starts: int = 10) -> None:
        """
        KNN amélioré: teste TOUS les points de départ + N points aléatoires.
        Beaucoup plus robuste que KNN greedy seul.
        """
        
        # Teste tous les points de départ
        for i in range(len(self.villes)):
            self._knn_with_matrix(i)
        
        # Teste aussi N points aléatoires (parfois plus performant)
        for _ in range(num_random_starts):
            random_start = random.randint(0, len(self.villes) - 1)
            self._knn_with_matrix(random_start)
        
        # Calcule les distances
        self._compute_distances()

    def compute_all_paths_knn(self, multistart: bool = False, num_random: int = 10) -> None:
        """
        Args:
            multistart: Si True, teste aussi des départs aléatoires
            num_random: Nombre de départs aléatoires à tester
        """
        if multistart:
            self.knn_multistart(num_random_starts=num_random)
        else:
            # Teste tous les points de départ
            for i in range(len(self.villes)):
                self._knn_with_matrix(i)
            
            self._compute_distances()
    
    def get_optimal_path(self) -> Parcours:
        """Retourne le meilleur chemin KNN."""
        if not self.distances:
            raise ValueError("compute_all_paths_knn() d'abord")
        
        start_point = min(self.distances, key=self.distances.get)
        best_path = self.paths[start_point]
        best_distance = self.distances[start_point]
        
        return Parcours(parcours=best_path, distance_path=best_distance)
    
    def solve(self, verbose: bool = False) -> Parcours:
        """Étape 1: KNN amélioré - teste plusieurs stratégies."""
        
        # Version 1: Multi-start (rapide, robuste)
        if len(self.villes) > 200:
            self.compute_all_paths_knn(multistart=True, num_random=20)
        else:
            self.compute_all_paths_knn(multistart=False)
        
        # 1. Call the correctly named method
        # 2. Store the Parcours object instead of trying to unpack it as a tuple
        best_parcours = self.get_optimal_path()
        
        # Keep storing the attributes if your other classes rely on them
        self.start_city_knn = best_parcours.point_depart
        self.best_path_knn = best_parcours.parcours
        self.distance_knn = best_parcours.distance_path
        
        if verbose:
            print(f"[1/3] KNN: {self.distance_knn:.2f} depuis {self.start_city_knn}")
            
        return best_parcours
    
    def _compute_distances(self) -> None:
        """Calcule et stocke la distance de chaque chemin."""
        for ville_start in self.paths.keys():
            path = self.paths[ville_start]
            self.distances[ville_start] = self.graph.path_distance(path)
    
    def get_optimal_path_KNN(self) -> tuple[str, list[str], float]:
        """Retourne le meilleur chemin KNN."""
        if not self.distances:
            raise ValueError("compute_all_paths_knn() d'abord")
        
        start_point = min(self.distances, key=self.distances.get)
        best_path = self.paths[start_point]
        best_distance = self.distances[start_point]
        
        return Parcours(parcours=best_path, distance_path=best_distance)
    
    def print_distance_from_each_city(self) -> None:
        """Affiche les distances pour chaque point de départ (pour diagnostic)."""
        print("\nDimensions KNN par point de départ:")

        for ville in sorted(self.distances.items(), key=lambda x: x[1]):
            print(f"  {ville[0]:20s} -> {ville[1]:10.2f}")

class TwoOpt(Heuristique):
    """Implémentation de l'algorithme K-Opt pour améliorer une solution initiale du TSP"""

    def __init__(self, graph: DistanceGraph):
        """ Args:
            graph: Instance de DistanceGraph
        """
        super().__init__(graph)        
    # def distance_route(self, path):
    #     """calculer path d'un chemin"""
    #     total = 0
    #     n = len(path)
        
    #     for i in range(n):
    #         current_city = self.index_ville[path[i]]
    #         next_city = self.index_ville[path[(i + 1) % n]]  # % n pour boucler
    #         total += self.matrix_distance[current_city][next_city]
        
    #     return total 

    def solve(self, path: list[str]) -> tuple[list[str], float]:
        """2-opt local search - assumes CLOSED path (returns to start)"""
        best_path = path[:]
        improved = True
        n = len(best_path)
        
        while improved:
            improved = False
            
            for i in range(n - 1):
                for j in range(i + 2, n):

                    if i == 0 and j == n - 1:
                        continue
                    
                    a_idx = self.index_ville[best_path[i]]
                    b_idx = self.index_ville[best_path[i + 1]]
                    c_idx = self.index_ville[best_path[j]]
                    d_idx = self.index_ville[best_path[(j + 1) % n]]
                    
                    old_distance = (self.matrix_distance[a_idx][b_idx] + self.matrix_distance[c_idx][d_idx])
                    new_distance = (self.matrix_distance[a_idx][c_idx] + self.matrix_distance[b_idx][d_idx])
                    
                    if new_distance < old_distance:
                        best_path[i + 1:j + 1] = best_path[i + 1:j + 1][::-1]
                        improved = True
                        break
                
                if improved:
                    break
        
        total_distance = self.graph.path_distance(best_path)
        return best_path, total_distance
    
    # def compute_all_paths_two_opt(self, KNN_paths = None):
    #     distances = {}
    #     for path in KNN_paths:
    #         path_two_opt , dist = self.solve(path)
    #         distances[path] = dist
        
    #     return distances

class ThreeOpt(Heuristique):
    """3 opt"""

    def __init__(self, graph: DistanceGraph):
        super().__init__(graph)

    def _find_best_three_opt_move(self, best_path: list[str], i: int, j: int, k: int) -> tuple[float, int]:
        A = self.index_ville[best_path[i - 1]]
        B = self.index_ville[best_path[i]]
        C = self.index_ville[best_path[j - 1]]
        D = self.index_ville[best_path[j]]
        E = self.index_ville[best_path[k - 1]]
        F = self.index_ville[best_path[k]]
        
        d = self.matrix_distance
        cur = d[A][B] + d[C][D] + d[E][F]
        
        # Les 7 reconnexions possibles
        d1 = d[A][C] + d[B][D] + d[E][F] - cur  # Inverse segment 2
        d2 = d[A][B] + d[C][E] + d[D][F] - cur  # Inverse segment 3
        d3 = d[A][C] + d[B][E] + d[D][F] - cur  # Inverse segments 2 et 3
        d4 = d[A][D] + d[E][B] + d[C][F] - cur  # Échange segments 2 et 3
        d5 = d[A][E] + d[D][B] + d[C][F] - cur  # Segment 3 inversé, puis segment 2
        d6 = d[A][D] + d[E][C] + d[B][F] - cur  # Segment 3 normal, segment 2 inversé
        d7 = d[A][E] + d[D][C] + d[B][F] - cur  # Segments 2 et 3 inversés
        
        deltas = [d1, d2, d3, d4, d5, d6, d7]
        min_delta = min(deltas)
        best_idx = deltas.index(min_delta)
        
        return min_delta, best_idx

    def _apply_three_opt_move(self, best_path: list[str], i: int, j: int, k: int, idx: int) -> list[str]:

        seg1 = best_path[:i]
        seg2 = best_path[i:j]
        seg3 = best_path[j:k]
        seg4 = best_path[k:]
        
        if idx == 0:  # Inverse segment 2
            return seg1 + seg2[::-1] + seg3 + seg4
        elif idx == 1:  # Inverse segment 3
            return seg1 + seg2 + seg3[::-1] + seg4
        elif idx == 2:  # Inverse segments 2 et 3
            return seg1 + seg2[::-1] + seg3[::-1] + seg4
        elif idx == 3:  # Échange segments 2 et 3
            return seg1 + seg3 + seg2 + seg4
        elif idx == 4:  # Segment 3 inversé, puis segment 2
            return seg1 + seg3[::-1] + seg2 + seg4
        elif idx == 5:  # Segment 3 normal, segment 2 inversé
            return seg1 + seg3 + seg2[::-1] + seg4
        elif idx == 6:  # Segments 2 et 3 inversés
            return seg1 + seg3[::-1] + seg2[::-1] + seg4
        
        return best_path    

    def solve(self, path: list[str], max_iterations: int = 50, 
              timeout: float = 60.0) -> tuple[list[str], float]:
        """
        Implémentation 3-opt optimisée avec timeout et limite d'itérations.
        
        Args:
            path: Chemin ouvert
            max_iterations: Nombre maximum de passes
            timeout: Temps max en secondes
        
        Returns:
            (chemin amélioré, distance totale)
        """
        
        best_path = path[:]
        if best_path[0] != best_path[-1]:
            best_path.append(best_path[0])
        
        n = len(best_path)
        start_time = time.time()
        iteration = 0
        improved = True
        
        while improved and iteration < max_iterations:
            iteration += 1
            improved = False
            
            if time.time() - start_time > timeout:
                break
            
            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    for k in range(j + 1, n):
                        
                        # Évalue les 7 reconnexions possibles
                        min_delta, best_idx = self._find_best_three_opt_move(
                            best_path, i, j, k
                        )
                        
                        if min_delta < -1e-5:
                            # Applique la meilleure reconnexion
                            best_path = self._apply_three_opt_move(
                                best_path, i, j, k, best_idx
                            )
                            improved = True
                            break
                    
                    if improved:
                        break
                
                if improved:
                    break
        
        # Retourne le chemin ouvert
        open_path = best_path[:-1]
        total_distance = self.graph.path_distance(open_path)
        
        return open_path, total_distance

    def three_opt_implemented(self, path: list[str]) -> tuple[list[str], float]:
            """
            Implémentation 3-opt optimisée (First Improvement) et corrigée.
            """
            best_path = path[:]
            if best_path[0] != best_path[-1]:
                best_path.append(best_path[0]) # on crée un chemin fermé si ce n'est pas déjà le cas
                
            n = len(best_path)
            improved = True

            while improved:
                improved = False
                
                for i in range(1, n - 2):
                    for j in range(i + 1, n - 1):
                        for k in range(j + 1, n):
                            

                            # TODO factoriser cette partie pour éviter les répétitions avec la 2-opt et rendre le code plus clair


                            # Indices des 6 villes aux frontières des 3 arêtes coupées
                            A, B = self.index_ville[best_path[i-1]], self.index_ville[best_path[i]]
                            C, D = self.index_ville[best_path[j-1]], self.index_ville[best_path[j]]
                            E, F = self.index_ville[best_path[k-1]], self.index_ville[best_path[k]]

                            d = self.matrix_distance
                            cur = d[A][B] + d[C][D] + d[E][F]

                            # Les 7 reconnexions possibles (avec les Deltas exacts correspondants)

                            # 1: 2-opt (inverse segment 2)
                            d1 = d[A][C] + d[B][D] + d[E][F] - cur # -cur car on enlève les 3 arêtes d'origine et on ajoute les 3 nouvelles 
                            # calcule juste le Delta de la reconnexion, pas besoin de recalculer la distance totale à chaque fois ! Evaluation locale très rapide O(1) grâce à la matrice de distances pré-calculée.
                            # C'est la clé pour que le 3-opt soit rapide même sur des instances plus grandes.

                            # 2: 2-opt (inverse segment 3)
                            d2 = d[A][B] + d[C][E] + d[D][F] - cur 
                            # 3: 2-opt (inverse segment 2 et 3)
                            d3 = d[A][C] + d[B][E] + d[D][F] - cur
                            # 4: 3-opt pur (échange segment 2 et 3)
                            d4 = d[A][D] + d[E][B] + d[C][F] - cur
                            # 5: 3-opt pur (segment 3 inversé, puis segment 2)
                            d5 = d[A][E] + d[D][B] + d[C][F] - cur
                            # 6: 3-opt pur (segment 3 normal, segment 2 inversé)
                            d6 = d[A][D] + d[E][C] + d[B][F] - cur
                            # 7: 3-opt pur (segment 3 inversé, segment 2 inversé)
                            d7 = d[A][E] + d[D][C] + d[B][F] - cur

                            deltas = [d1, d2, d3, d4, d5, d6, d7]

                            min_delta = min(deltas) # On cherche la meilleure reconnexion possible parmi les 7, et on applique la première qui améliore (First Improvement)
                                                        # TODO factoriser cette partie pour éviter les répétitions avec la 2-opt et rendre le code plus clair

                            if min_delta < -1e-5:
                                idx = deltas.index(min_delta)
                                
                                seg1 = best_path[:i]
                                seg2 = best_path[i:j]
                                seg3 = best_path[j:k]
                                seg4 = best_path[k:]
                                
                                # On applique EXACTEMENT la reconstruction qui correspond au Delta gagnant
                                if idx == 0: 
                                    best_path = seg1 + seg2[::-1] + seg3 + seg4
                                elif idx == 1:
                                    best_path = seg1 + seg2 + seg3[::-1] + seg4
                                elif idx == 2:
                                    best_path = seg1 + seg2[::-1] + seg3[::-1] + seg4
                                elif idx == 3:
                                    best_path = seg1 + seg3 + seg2 + seg4
                                elif idx == 4:
                                    best_path = seg1 + seg3[::-1] + seg2 + seg4
                                elif idx == 5:
                                    best_path = seg1 + seg3 + seg2[::-1] + seg4
                                elif idx == 6: 
                                    best_path = seg1 + seg3[::-1] + seg2[::-1] + seg4
                                
                                improved = True
                                break # On sort de la boucle k (First Improvement)
                        if improved: 
                            break # On sort de la boucle j
                    if improved: 
                        break # On sort de la boucle i et on relance le While

            # Retourne le chemin ouvert
            open_path = best_path[:-1]
            total_distance = self.distance_route(open_path)
            
            return open_path, total_distance

class AlgoGenetique(Heuristique):
    """Implémentation d'un algorithme génétique pour résoudre le TSP"""
    
    def __init__(self, graph: DistanceGraph,  pop_size = 100, generations = 500, mutation_rate = 0.05):
        super().__init__(graph)

        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self.generate_initial_population(population_size=pop_size)

    def generate_initial_population(self, population_size: int = 100) -> list[list[str]]:   
        """Generer des paths aléatoires"""
        
    
        noms_villes = [ville.nom for ville in self.villes]
        liste_paths = []
        
        for _ in range(population_size):
            random_path = noms_villes.copy()
            
            # 3. Shuffle the copy in-place (do not assign the result to a variable)
            np.random.shuffle(random_path)
            
            liste_paths.append(random_path)
            
        return liste_paths
    
    def select_parents(self,scored_population, nb_parents=3):
        """selectionenr les meilleurs"""

        top_entries = heapq.nsmallest(nb_parents, scored_population, key=lambda x: x[0])
    
        # On récupère juste les chemins (le deuxième élément du tuple)
        best_parents = [path for score, path in top_entries]
        return best_parents
    
    
    
    def compute_fitness(self, path: list[str]) -> float:
        """Calculer la fitness d'un path (inverse de la distance totale)"""
        return 1 / self.graph.path_distance(path)
    
    def mutation(self, path: list[str]) -> list[str]:
        """Appliquer une mutation (échange de deux villes) avec une certaine probabilité"""
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(path)), 2)
            path[i], path[j] = path[j], path[i]
        return path
    
    def _get_crossover_section(self, path_length: int) -> tuple[int, int]:
        """Générer deux points de coupe pour le crossover"""
        cut1 = random.randint(0, path_length - 2)
        cut2 = random.randint(cut1 + 1, path_length - 1)
        return cut1, cut2

    def ordered_crossover(self, parent1: list[str], parent2: list[str]) -> list[str]:
        """Crossover ordonné (OX) pour le TSP"""
        cut1, cut2 = self._get_crossover_section(len(parent1))
        
        child = [None] * len(parent1)
        child[cut1:cut2] = parent1[cut1:cut2]
        
        p2_pool = parent2.copy()
        
        for ville in child[cut1:cut2]:
            if ville in p2_pool:
                p2_pool.remove(ville)
        # prendre villes du parent 2 dans l'ordre, sautant celle deja presentes.

        if len(p2_pool) != child.count(None):
            raise ValueError("Mismatch between remaining cities and empty slots in child")

        p2 = [v for v in parent2 if v not in child]
        for i in range(len(child)):
            if child[i] is None:
                child[i] = p2.pop(0)
        return child
    
    # def _evolve(self):
    #     """Effectuer une génération complète: sélection, crossover, mutation"""
    #     chromosomes = self.population

    #     new_population = []

    #     while len(new_population) < len(chromosomes):
    #         parent_1, parent_2 = self.select_parents(2)
    #         child = self.ordered_crossover(parent_1,parent_2)
    #         child = self.mutation(child)
    #         new_population.append(child)

        
    #     self.population = new_population

    #     best_path = min(self.population, key=lambda p: self.graph.path_distance(p))
    #     best_distance = self.graph.path_distance(best_path)
    #     return Parcours(parcours=best_path, distance_path=best_distance)
    
    # def solve(self,initial_path: list[str] = None) -> Parcours:
    #     """evolve through generations"""
    #     for _ in range(self.generations):
    #         self._evolve()

    def solve(self, initial_path: list[str] = None) -> Parcours:
        if initial_path:
            
            if initial_path[0] == initial_path[-1]:
                initial_path = initial_path[:-1]
            self.population[0] = initial_path[:]

        for gen in tqdm(range(self.generations), desc="Algorithme Génétique - Évolution"):
            
            scored_population = []
            for chromo in self.population:
                dist = self.graph.path_distance(chromo + [chromo[0]])
                scored_population.append((dist, chromo))

            scored_population.sort(key=lambda x: x[0])
            best_chromo = scored_population[0][1]
            min_dist = scored_population[0][0]

            new_population = [best_chromo] 

            while len(new_population) < self.pop_size:

                parents = self.select_parents(scored_population, 2)
                p1, p2 = parents[0], parents[1]
                
                child = self.ordered_crossover(p1, p2)
                child = self.mutation(child)
                
                new_population.append(child)

            self.population = new_population

        final_best = self.population[0] # Le premier est le meilleur grâce au tri
        final_dist = self.graph.path_distance(final_best + [final_best[0]])
        return Parcours(parcours=final_best + [final_best[0]], distance_path=final_dist)

