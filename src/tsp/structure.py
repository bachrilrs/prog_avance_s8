import time
import pandas as pd
import numpy as np

class Ville:
    """Représente une ville avec ses coordonnées."""

    def __init__(self, nom):
        self.nom = nom
        self.__coord_X = None
        self.__coord_Y = None

    @property
    def coord_X(self):
        return self.__coord_X
    
    @property
    def coord_Y(self):
        return self.__coord_Y

    @coord_X.setter
    def coord_X(self, x):
        self.__coord_X = x

    @coord_Y.setter
    def coord_Y(self, y):
        self.__coord_Y = y

    def __str__(self):
        return f'{self.nom} (X: {self.__coord_X}, Y: {self.__coord_Y})'
    
    def eucledian_distance(self, other):
        """Calcule la distance euclidienne vers une autre ville."""
        return np.sqrt((other.coord_X - self.coord_X)**2 + (other.coord_Y - self.coord_Y)**2)

class DistanceGraph:
    """Gère la matrice de distances entre villes."""
    
    def __init__(self, villes):
        self.villes = villes
        self.index = {v.nom: i for i, v in enumerate(villes)}
        self.matrix = self._build_matrix()

    def _build_matrix(self):
        """Construit la matrice de distances."""
        n = len(self.villes)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j] = self.villes[i].eucledian_distance(self.villes[j])
                matrix[j][i] = matrix[i][j]
        return matrix
    
    def get_distance(self, ville1_idx, ville2_idx):
        """Retourne la distance entre deux villes."""
        return self.matrix[ville1_idx, ville2_idx]
    
    def path_distance(self, path):
        """Calcule la distance totale d'un chemin."""
        indices = [self.index[nom] for nom in path]
        rows = indices[:-1]
        cols = indices[1:]
        return np.sum(self.matrix[rows, cols])
    
    def get_dataframe(self):
        """Retourne la matrice sous forme de DataFrame."""
        noms = [v.nom for v in self.villes]
        return pd.DataFrame(self.matrix, index=noms, columns=noms)

class Path:
    """Représente un chemin solution dans le TSP."""

    def __init__(self, path, distance_path, algo_name="Unknown"):
        self.path = path
        self.distance_path = distance_path
        self.point_depart = path[0] if path else None
        self.algo_name = algo_name
        self.temps_execution = 0.0

    def __str__(self):
        """Affichage lisible du chemin."""
        chemin_str = " → ".join(self.path[:3]) + " ... " + " → ".join(self.path[-3:]) \
            if len(self.path) > 6 else " → ".join(self.path)
        return f"{self.algo_name} ({self.point_depart}): {self.distance_path:.2f} | {chemin_str}"
    
    def get_improvement_percent(self, reference_distance):
        """Calcule le % d'amélioration vs une distance de référence."""
        if reference_distance <= 0:
            return 0.0
        return ((reference_distance - self.distance_path) / reference_distance) * 100

class Pays:
    """Orchestre l'analyse complète du problème TSP."""

    def __init__(self, nom, villes=None):
        """
        Args:
            nom: Nom du pays/instance
            villes: Liste de Ville chargées depuis load_cities()
        """
        self.nom = nom
        self.graph = DistanceGraph(villes)
        
        from .solvers import KNN, TwoOpt, ThreeOpt, AlgoGenetique
        from .visualizer import TSPVisualizer
        
        # Initialisation des solveurs
        self.knn_solver = KNN(self.graph)
        self.two_opt_solver = TwoOpt(self.graph)
        self.three_opt_solver = ThreeOpt(self.graph)
        self.ga_solver = AlgoGenetique(self.graph)
        self.visualizer = TSPVisualizer(self.graph)

        # Stockage des résultats : {algo: {nom_ville: Path}}
        self.results = {
            'knn': {},
            'two_opt': {},
            'three_opt': {},
            'ag': {}
        }
        
        # Meilleur par algo
        self.best_overall = {}

    def __str__(self):
        """Représentation textuelle du pays."""
        if not self.best_overall:
            return f'{self.nom}: {len(self.graph.villes)} villes (non résolu)'
        best_dist = min(p.distance_path for p in self.best_overall.values())
        return f'{self.nom}: {len(self.graph.villes)} villes - Distance finale: {best_dist:.2f}'
    
    def meilleur_par_algo(self, algo):
        """Retourne le meilleur chemin pour un algorithme."""
        if algo not in self.best_overall:
            raise ValueError(f"Algorithme '{algo}' non trouvé. Disponibles: {list(self.best_overall.keys())}")
        return self.best_overall[algo]
    
    def meilleur_global(self):
        """Retourne le meilleur chemin parmi tous les algos."""
        if not self.best_overall:
            raise ValueError("Aucun résultat. Appelez run_all_algos_multi_depart() d'abord")
        return min(self.best_overall.values(), key=lambda p: p.distance_path)

    def _run_algo(self, algo_name, solver, input_results_key, output_results_key, 
              verbose=True, **solver_kwargs):
        """
        Méthode générique pour exécuter n'importe quel algo.
        
        Args:
            algo_name: Nom de l'algo pour affichage ("KNN", "2-OPT", etc)
            solver: L'objet solver (knn_solver, two_opt_solver, etc)
            input_results_key: Clé des résultats d'entrée (ex: 'knn', None si nouveau)
            output_results_key: Clé des résultats de sortie (ex: 'two_opt')
            verbose: Afficher progression
            **solver_kwargs: Arguments supplémentaires pour solver.solve() # sert a faire passer max_iterations, timeout, etc
        """
        

        # Vérifier que les entrées existent
        if input_results_key and not self.results[input_results_key]:
            print(f"{input_results_key.upper()} manquant pour {algo_name}. Exécutez d'abord {input_results_key.upper()}.")
            self._run_algo(input_results_key, getattr(self, f'{input_results_key}_solver'),
                        None, input_results_key, verbose=False)
        
        self.results[output_results_key] = {}
        
        if verbose:
            kwargs_str = ", ".join(f"{k}={v}" for k, v in solver_kwargs.items())

            print(f"{algo_name} - {self.nom} ({kwargs_str})")

        
        # Déterminer la source de données
        input_dict = self.results[input_results_key] if input_results_key else None
        
        # Exécuter algo
        if algo_name == "KNN":
            # KNN est spécial : boucle sur les départs
            for idx, ville in enumerate(self.graph.villes):
                start_t = time.time()
                path = solver.solve(start_idx=idx)
                path.temps_execution = time.time() - start_t
                self.results[output_results_key][ville.nom] = path
                if verbose and idx % max(1, len(self.graph.villes) // 5) == 0:
                    print(f"  {idx+1}/{len(self.graph.villes)} villes traitées...")
        else:
            # 2-OPT, 3-OPT, AG : boucle sur résultats précédents
            for key, path_input in input_dict.items():
                start_t = time.time()
                path = solver.solve(path_input, **solver_kwargs) 
                path.temps_execution = time.time() - start_t
                self.results[output_results_key][key] = path
                
                if verbose:
                    improvement = ((path_input.distance_path - path.distance_path) / 
                                path_input.distance_path) * 100
                    print(f"  {key:15s} → {path.distance_path:.2f} ({improvement:+.1f}%)")
        
        self._compute_best_overall()
        if verbose:
            self._print_resume()

    def run_knn_only(self, verbose=True):
        """Exécute KNN uniquement."""
        self._run_algo("KNN", self.knn_solver, None, 'knn', verbose=verbose)

    def run_two_opt_only(self, verbose=True, max_no_improve=100):
        """Exécute 2-OPT sur KNN existant."""
        self._run_algo("2-OPT", self.two_opt_solver, 'knn', 'two_opt', verbose=verbose, max_no_improve=max_no_improve)

    def run_three_opt_only(self, verbose=True, max_iterations=50, timeout=60.0):
        """Exécute 3-OPT sur 2-OPT existant."""
        self._run_algo("3-OPT", self.three_opt_solver, 'two_opt', 'three_opt',  verbose=verbose, max_iterations=max_iterations, timeout=timeout)

    def run_three_opt_best_only(self, verbose=True, max_iterations=10, timeout=60.0):
        """
        Exécute 3-OPT UNIQUEMENT sur le meilleur chemin 2-OPT.
        
        Beaucoup plus rapide que sur tous les chemins.
        """
        if not self.results['two_opt']:
            print("2-OPT manquant. Exécutez d'abord 2-OPT.")
            self.run_two_opt_only(verbose=False)
        
        self.results['three_opt'] = {}
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"3-OPT (meilleur 2-OPT uniquement) - {self.nom}")
            print(f"{'='*70}\n")
        
        #Récupérer le meilleur 2-OPT
        best_2opt_path = min(
            self.results['two_opt'].values(), key=lambda p: p.distance_path)
        best_start = best_2opt_path.point_depart
        
        if verbose:
            print(f"Amélioration du meilleur 2-OPT depuis {best_start}: {best_2opt_path.distance_path:.2f}")
        
        #Appliquer 3-OPT uniquement sur le meilleur
        start_t = time.time()
        path_3opt = self.three_opt_solver.solve(
            best_2opt_path, 
            verbose=verbose,
            max_iterations=max_iterations, 
            timeout=timeout
        )
        path_3opt.temps_execution = time.time() - start_t
        
        #Stocker UNIQUEMENT ce résultat
        self.results['three_opt'][best_start] = path_3opt
        
        if verbose:
            improvement = ((best_2opt_path.distance_path - path_3opt.distance_path) / 
                        best_2opt_path.distance_path) * 100
            print(f"  {best_start:15s} → {path_3opt.distance_path:.2f} ({improvement:+.1f}%)")
        
        self._compute_best_overall()
        if verbose:
            self._print_resume()

    def run_ga_only(self, verbose=True, pop_size=100, generations=100, mutation_rate=0.05):
        """Exécute AG sur KNN existant."""
        from .solvers import AlgoGenetique
        ga = AlgoGenetique(self.graph, pop_size=pop_size, 
                        generations=generations, mutation_rate=mutation_rate)
        
        self.results['ag'] = {}
        
        if verbose:
            print(f"AG - {self.nom} (pop={pop_size}, gen={generations})")
        
        # Récupérer le meilleur KNN
        best_knn = min(self.results['knn'].values(), key=lambda p: p.distance_path)
        
        start_t = time.time()
        path_ag = ga.solve(initial_path=best_knn.path[:-1], verbose=verbose)
        path_ag.temps_execution = time.time() - start_t
        self.results['ag'] = {"AG": path_ag}
        
        if verbose:
            print(f"  AG → {path_ag.distance_path:.2f} (Temps: {path_ag.temps_execution:.2f}s)")
        
        self._compute_best_overall()
        if verbose:
            self._print_resume()

    def run_all_algos_multi_depart(self, verbose=True, run_knn=True, run_2opt=True, 
                                run_3opt=True, run_ga=True, **kwargs):
        """
        Lance les algos en cascade selon paramètres.
        
        Args:
            run_knn, run_2opt, run_3opt, run_ga: Boolean pour chaque algo
            **kwargs: Paramètres spécifiques (max_iterations, pop_size, etc)
        """
        if run_knn:
            self.run_knn_only(verbose=verbose)
        
        if run_2opt:
            self.run_two_opt_only(verbose=verbose, 
                                max_no_improve=kwargs.get('max_no_improve', 100))
        
        if run_3opt:
            self.run_three_opt_only(verbose=verbose, 
                                max_iterations=kwargs.get('max_iterations', 50),
                                timeout=kwargs.get('timeout', 60.0))
        
        if run_ga:
            self.run_ga_only(verbose=verbose,
                            pop_size=kwargs.get('pop_size', 100),
                            generations=kwargs.get('generations', 100),
                            mutation_rate=kwargs.get('mutation_rate', 0.05))

    def _compute_best_overall(self):
        """Calcule et stocke le meilleur chemin par algorithme."""
        self.best_overall = {}
        for algo in self.results:
            if self.results[algo]:
                dists = {v: p.distance_path for v, p in self.results[algo].items()}
                best_start = min(dists, key=dists.get)
                self.best_overall[algo] = self.results[algo][best_start]

    def _print_resume(self):
        """Affiche le résumé des résultats."""

        print("RÉSUMÉ DES RÉSULTATS")

        for algo, path in self.best_overall.items():
            print(f"{algo.upper():6s} → {path.distance_path:.2f} (temps: {path.temps_execution:.4f}s)")

    def to_results_dataframe(self):
        """Retourne un DataFrame synthétique sur tous les résultats."""
        lignes = []
        for algo, dict_res in self.results.items():
            for start, path_obj in dict_res.items():
                chemin = path_obj.path
                chemin_str = (" → ".join(chemin[:3]) + " ... " + " → ".join(chemin[-3:])
                             if len(chemin) > 7 else " → ".join(chemin))
                lignes.append({
                    'Algo': algo.upper(),
                    'Départ': start,
                    'Distance': round(path_obj.distance_path, 2),
                    'Temps (s)': round(path_obj.temps_execution, 4),
                    'Aperçu': chemin_str
                })
        
        df = pd.DataFrame(lignes)
        return df.sort_values(['Algo', 'Distance'])

    def get_matrix_with_labels(self):
        """Retourne la matrice de distances avec labels."""
        return self.graph.get_dataframe()