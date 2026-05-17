Bibliothèques NumPy et Pandas

Mathieu RAYNAL
www.irit.fr/~Mathieu.Raynal
mathieu.raynal@irit.fr

Bibliothèque NumPy

Contexte

(cid:127) NumPy pour Numerical Python : http://www.numpy.org/

– bibliothèque open source
– permet d’effectuer des calculs numériques avec Python.
– gestion facilitée des tableaux de nombres.

(cid:127) Besoin d’importer le package numpy

import numpy as np

Programmation avancée et génie logiciel

3

Création de tableaux

(cid:127) Utilisation de la méthode array

– crochets pour délimiter les listes d’éléments dans les tableaux.

a = np.array([1, 2, 3, 4])

(cid:127) Pour créer un tableau 2D, utilisation d’une liste de listes avec des crochets imbriqués.

– Les listes internes correspondent à des lignes du tableau.

b = np.array([[1, 2, 3], [4, 5, 6]])

Programmation avancée et génie logiciel

4

Méthodes spécifiques pour créer des tableaux

(cid:127) Méthodes d’initialisation
– zeros : tableau rempli de 0
– ones : tableau rempli de un
– full : tableau rempli avec une valeur déterminée

Exemples

tab = np.zeros(3)

tab = np.zeros(3, np.int16)

tab = np.zeros((3,2), np.bool)

tab = np.ones(2, np.bool)

tab = np.full((2, 4), 6.5)

Résultat

[0. 0. 0.]

[0 0 0]

[[False False]
[False False]
[False False]]

[ True True]

[[6.5 6.5 6.5 6.5]
[6.5 6.5 6.5 6.5]]

Programmation avancée et génie logiciel

5

Création de tableaux avec des séquences logiques

(cid:127) Suite de nombre

np.arange(debut, fin, pas)

(cid:127)

Interpolation linéaire entre deux bornes

np.linspace(debut, fin, nb_val, dtype)

Exemples

tab = np.arange(5)

tab = np.arange(4,7)

tab = np.arange(3,20,5)

tab = np.linspace(3,5,4)

Résultat

[0 1 2 3 4]

[4 5 6]

[ 3 8 13 18]

[3. 3.66666667 4.33333333 5. ]

tab = np.linspace(3,5,4,dtype=np.int8)

[3 3 4 5]

Programmation avancée et génie logiciel

6

Génération de tableau avec valeurs aléatoires

(cid:127) Pour des entiers

np.random.randint(borne, size=N)

(cid:127) Pour des réels entre 0 et 1 exclu

np.random.random(dim)

Exemples

Résultat

x = np.random.randint(10)

Entier aléatoire entre 0 et 9

tab = np.random.randint(10, size=3)

Tableau de 3 entiers aléatoires entre 0 et 9

mat = np.random.randint(10, size=(4,2))

Matrice de 4 lignes et 2colonnes d’entiers aléatoires entre 0 et 9

x = np.random.random()

Réel aléatoire entre 0 et 1 exclu

tab = np.random.random(3)

Tableau de 3 réels aléatoires entre 0 et 1 exclu

mat = np.random.random((3,4))

Matrice de 3 lignes et 4 colonnes de réels aléatoires entre 0 et 1 exclu

Programmation avancée et génie logiciel

7

Utilisation de générateur de nombres aléatoires

(cid:127) Classe Random Number Generator (RNG)
– Créer un générateur de nombres aléatoires …

rng = np.random.default_rng ( )

– Ou pseudo aléatoires …

rng = np.random.default_rng (42)

(cid:127) Générer des nombres entiers aléatoires
rng.integers(low=, high=, size=, dtype=, endpoint=)

(cid:127) Générer des nombres réels aléatoires entre 0 et 1 exclu

rng.random(size, dtype=)

(cid:127) Générer des nombres réels aléatoires sur d’autres bornes

rng. uniform(min, max, nb)

Programmation avancée et génie logiciel

8

Opérations sur des tableaux

(cid:127) Modifier la forme du tableau
– Réarranger : np.reshape()
– Transposer : np.transpose()
– Aplatir :

(cid:127) np.flatten() : créer une copie
(cid:127) np.ravel() : modifie juste la vue, mais c’est toujours sur le même tableau

(cid:127) Combiner des tableaux

– np.concatenate() : met bout à bout 2 tableaux
– np.vstack() : ajouter des lignes à une matrice
– np.hstack() : ajouter des colonnes à une matrice

Programmation avancée et génie logiciel

9

Opérations sur des array

(cid:127) Les opérations s’appliquent élément par élément

(cid:127) NumPy permet de faire des opérations sans boucle Python

à Code beaucoup plus rapide.

a = np.array([1,2,3])
b = np.array([4,5,6])
a + b
Résultat : array([5,7,9])

Autres exemples :
a * b
a ** 2
np.sqrt(a)
np.exp(a)

Programmation avancée et génie logiciel

10

Broadcasting

(cid:127) Permet d’appliquer des opérations entre tableaux de tailles différentes

– NumPy étend automatiquement la dimension.

a = np.array([[1, 2],[3, 4]])
b = np.array([5, 6])
print(a+b)
print(a*b)

Résultat :
[[ 6 8]
[ 8 10]]

[[ 5 12]
[15 24]]

Programmation avancée et génie logiciel

11

Indexation et slicing

(cid:127) Comme avec les listes Python

– mais plus puissant.

a = np.array([10,20,30,40])

a[0]     # 10
a[1:3]   # [20,30]

(cid:127) Pour matrices :

A[0,1]      # élément
A[:,1]      # colonne
A[1,:]      # ligne

(cid:127)

Indexation conditionnelle :

a[a > 20]

à modifier une slice modifie l’array original

Programmation avancée et génie logiciel

12

Fonctions mathématiques

(cid:127) NumPy contient énormément de fonctions optimisées.

– np.sum(a)
– np.mean(a)
– np.max(a)
– np.min(a)
– np.std(a)

(cid:127) Sur les matrices :

– np.sum(A, axis=0)  # par colonnes
– np.sum(A, axis=1)  # par lignes

Programmation avancée et génie logiciel

13

Bibliothèque Pandas

Contexte

(cid:127) Bibliothèque python pour faire de l’analyse de données

(cid:127) Basé sur NumPy

(cid:127) Site de référence :

https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html

(cid:127) Livre de référence : McKinney, Wes. 2012. Python for data analysis: Data wrangling

with Pandas, NumPy, and IPython. " O’Reilly Media, Inc.".

Programmation avancée et génie logiciel

15

L’objet Series

(cid:127) Objet à une dimension

(cid:127) Extension des tableaux unidimensionnels de numpy

import pandas as pd

tab = pd.Series( [1, 2, 3] )

Programmation avancée et génie logiciel

16

L’objet DataFrame

(cid:127) Structure à deux dimensions

(cid:127) Les colonnes peuvent être de types différents

(cid:127) Un DataFrame est composé de :

– Indice de la ligne,
– Nom de la colonne,
– Valeur pour chaque cellule

Programmation avancée et génie logiciel

17

Structure d’un DataFrame

df = pd.DataFrame({A': [1, 4, 7], ‘B': [2, 5, 8], ‘C’: [3, 6, 9]})

df = pd.DataFrame(mat,

columns=["A","B","C"],
index=[str((i+1)*500) for i in range (3)])

(cid:127) df.index : donne les index d’un DataFrame
(cid:127) df.columns : donne les noms de colonnes d’un DataFrame
(cid:127) df.axes : donne les index et les noms de colonnes d’un DataFrame
(cid:127) df.shape : donne le nombre de lignes et colonnes
(cid:127) df.size : donne le nombre de valeurs

Programmation avancée et génie logiciel

18

Importer des données au format CSV

url = "https://... "
df = pd.read_csv(url)

(cid:127) Spécifier le type

df = pd.read_csv("https://...",dtype={« nom_col« :str})

(cid:127) Spécifier l’index

df = pd.read_csv("https://...",index_col=N )

Programmation avancée et génie logiciel

19

Exercice

(cid:127) Charger dans un DataFrame les données issues de :

https://www.data.gouv.fr/api/1/datasets/r/f5df602b-3800-44d7-b2df-fa40a0350325

(cid:127) Définir la première colonne comme index

(cid:127) Définir que chaque colonne de code contient une chaine de caractère

Programmation avancée et génie logiciel

20

Extraire des lignes

(cid:127) head()

– Extrait les 5 premières lignes du tableau

(cid:127)

tail()
– Extrait les 5 dernières lignes du tableau

(cid:127) sample()

– Extrait aléatoirement une ligne du tableau

(cid:127) Possibilité de spécifier le nombre de lignes souhaité

Programmation avancée et génie logiciel

21

Indexation

(cid:127) Utilisation d’index plus explicites que l’utilisation de l’indice de position

à Utilisation des noms de colonnes

(cid:127) Renommer les colonnes

df = df.rename(columns={"ancien_nom": "nouveau_nom"})

df.columns = ["col1", "col2", "col3"]

(cid:127) Nettoyer les noms de colonnes

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")

Programmation avancée et génie logiciel

22

Accéder à une colonne

(cid:127) dataframe.variable

– Noms de colonnes sans espace ou caractères spéciaux

(cid:127) dataframe['variable’]

– Retour sous la forme de Series

(cid:127) dataframe[['variable’]]

– Retour sous forme de DataFrame
à A éviter pour une variable seule

Programmation avancée et génie logiciel

23

Accéder à plusieurs colonnes

(cid:127) dataframe[['variable1', 'variable2’]]

(cid:127) Privilégier l’utilisation de loc[]

– dataframe.loc[:, ['variable1', 'variable2’]]
à équivalent à SELECT variable1, variable2 FROM dataframe

Programmation avancée et génie logiciel

24

Exercice

(cid:127) Créer un DataFrame à partir des colonnes

– code_insee
– nom_sans_accent
– reg_nom
– dep_code
– academie_nom
– type_commune_unite_urbaine
– Population
– superficie_hectare
– altitude_moyenne
– latitude_centre
– longitude_centre
– niveau_equipements_services

(cid:127) Afficher 10 lignes de ce nouveau tableau

Programmation avancée et génie logiciel

25

Accéder à des lignes

(cid:127) df.loc[]

– Méthode recommandée
– Fonctionne avec les labels des colonnes
– Condition sur les valeurs souhaitées pour une colonne

df.loc[df['superficie_hectare']>5000]

– Possibilité de combiner plusieurs conditions avec & et |

df.loc[(df['dep_code']==31.0) | (df['dep_code']==32.0)]

(cid:127) df.iloc[]

– Utilise les indices.

df.iloc[5000]

Programmation avancée et génie logiciel

26

Quelques fonctions bien pratiques …

(cid:127) df[‘col’].min()
(cid:127) df[‘col’].max()
(cid:127) df[‘col’].mean()
(cid:127) df[‘col’].median()
(cid:127) df[‘col’].std()
(cid:127) df.sort_values(by=“col", ascending=True)
(cid:127) df[‘col'].unique() : extrait un tableau avec les différentes valeurs
(cid:127) df[‘col'].nunique() : donne le nombre de valeurs différentes

Programmation avancée et génie logiciel

27

Fonction groupby

(cid:127) Regroupe les valeurs identiques d’une colonne en sous tableau

– Pas exploitable directement

df.groupby(‘col’)
df.groupby([‘col1’, ‘col2’])

(cid:127) Opérations de regroupement

– Agrégation : min() ; max() : mean() ; median() ; std() ; size()
– Fonction agg() pour pouvoir agréger plusieurs colonnes

print(grouped.agg({

'points': 'sum’,
'assists': 'mean’
}))

Programmation avancée et génie logiciel

28

Exercice

(cid:127) Quelle est la population de la France ?

(cid:127) Quelles sont les villes de plus de 100 000 habitants ?

(cid:127) Quelles sont les 3 régions avec le plus de villes de 10 000 habitants ?
– Afficher le nom des régions et le nombre de villes de plus de 10 000 habitants

Programmation avancée et génie logiciel

29

Ajouter des colonnes

(cid:127) Ajout de colonnes

df[« nom_col"] = …

Programmation avancée et génie logiciel

30

Exercice

(cid:127) Quelle est la ville la plus proche du centre de la France Métropolitaine ?

Programmation avancée et génie logiciel

31


