# TSP Traveler Salesman Problem (TSP) utilisant des heuristiques

Ce projet implémente des heuristiques pour résoudre le problème du voyageur de commerce (TSP). Le TSP est un problème d'optimisation combinatoire qui consiste à trouver le chemin le plus court pour visiter un ensemble de villes et revenir à la ville de départ.

## Heuristiques utilisées
- **k-Nearest Neighbor (kNN)** : Cette heuristique commence à une ville de départ et choisit la ville la plus proche non visitée à chaque étape.
- **2-opt** : Cette heuristique améliore une solution initiale en échangeant deux arêtes pour réduire la longueur totale du chemin.
- **3-opt** : Cette heuristique est une extension de 2-opt qui échange trois arêtes pour trouver une solution encore meilleure.
- **Algorithme génétique** : Cette heuristique utilise des concepts de sélection, croisement et mutation pour évoluer une population de solutions vers une solution optimale.

## Installation
1. Clonez le dépôt :

```bash
git clone https://github.com/bachrilrs/prog_avance_s8.git
```

2. Accédez au répertoire du projet :

```bash
cd prog_avance_s8
```

3. Installez les dépendances nécessaires (si applicable) :

```bash
pip install -e .
```

## Utilisation

Pour exécuter le projet, utilisez la commande suivante :

```bash
chmod +x scripts/run_tsp.py
./scripts/run_tsp.py
```