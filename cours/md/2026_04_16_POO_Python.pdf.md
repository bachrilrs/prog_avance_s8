1

l

i

e
c
g
o

i

Base de la POO en Python

Mathieu RAYNAL
mathieu.raynal@irit.fr
http://www.irit.fr/~Mathieu.Raynal

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Déclarer une classe

(cid:127) Déclarer une classe

class MaClasse:

"Description de ma classe …"

…

2

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Constructeur

(cid:127) Constructeur

def __init__(self [,params]):

…

3

l

i

e
c
g
o

i

(cid:127)

Il ne peut y avoir qu’un seul constructeur dans la classe
Possibilité de mettre des valeurs par défaut aux paramètres
(cid:127)

def __init__(self, x=0, y=0):

…

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Méthode de classe

4

(cid:127) Pour « simuler » d’autres constructeurs

@classmethod
def nom_de_la_methode(cls[, params]):

return cls(…)

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Attributs et méthodes d’une classe

5

(cid:127) Attribut (variable d’instance)

(cid:127) Généralement déclaré et initialisé dans le constructeur

self.monAttribut = saValeur

(cid:127)

Les méthodes se déclarent comme les fonctions
(cid:127) Obligatoirement un premier paramètre nommé self

def maMethode(self [,params]):

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Objet : Création d’une instance d’une classe

6

class Point:

"Définition d'un point en 2D"

def __init__(self, x=0, y=0):

self.x = x
self.y = y

@classmethod
def creer_point(cls, y):

return cls(0, y)

def deplacer(self, dx, dy):

self.x += dx
self.y += dy

p = Point(1, 2)
p2 = Point()
p3 = Point.creer_point(4)

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Utilisation d’un membre depuis un objet

7

(cid:127) Membre = attribut ou méthode

p.x = 5
p2.déplacer(3, 4)

(cid:127) Afficher la description d’un objet

print(p. __doc__)

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Les méthodes __str__ et __repr__

8

(cid:127) Pour afficher la représentation d’un objet, il faut définir une des

méthodes suivantes

def __str__(self):

(cid:127) Ou

def __repr__(self):

(cid:127) Ces méthodes doivent retourner la chaine de caractères que

l’on souhaite afficher

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Les énumérations

(cid:127) Déclaration d’une énumération

from enum import Enum, auto

class Color(Enum):
RED = auto()
GREEN = auto()
BLUE = auto()

(cid:127) Utilisation d’une énumération

c = Color.BLUE
if c == Color.BLUE:

print('OK')

(cid:127) Parcours des valeurs d’une énumération

for c in Color:

print(f"{c.name} a pour valeur {c.value}")

9

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Match / case

10

day = "Monday"

# Match the day to predefined patterns
match day:

case "Saturday" | "Sunday":

print(f"{day} is a weekend.")

case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":

print(f"{day} is a weekday.")

case _:

print("That's not a valid day of the week.")

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Surcharge d’opérateur

11

Opérateurs mathématiques

Opérateurs de comparaison

Méthode

__add__

__sub__

__mul__

__truediv__

__mod__

__power__

Opérateur

Méthode

Opérateur

+

-

*

/

%

**

__eq__

__ne__

__gt__

__ge__

__lt__

__le__

==

!=

>

>=

<

<=

def __add__(self, p):

return Point(self.x+p.x, self.y+p.y)

p1 = Point(3,2)
p2 = Point(4,5)
p = p1 + p2

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Exercice

12

(cid:127) Dans la classe Vecteur réalisée précédemment en TP

(cid:127)
(cid:127)
(cid:127)

Ajouter les surcharges d’opérateurs de + et –
Remplacer produit_vectoriel par la surcharge d’opérateurs *
Créer les surcharges d’opérateurs pour tester les égalités et inégalités
entre 2 vecteurs

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Visibilité des membres

13

(cid:127)

Les membres peuvent être
(cid:127)

publics
(cid:127)

Accès possible depuis une instance de la classe

l

i

e
c
g
o

i

(cid:127)

(cid:127)

protégés : nom débute par _
(cid:127)

Accès qu’à l’intérieur de la classe ou depuis une classe fille

privés : nom débute par __
(cid:127)

Accès qu’à l’intérieur de la classe

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Les getters (accesseurs) et setters (mutateur)

14

(cid:127) Dans les deux cas, le nom de la méthode est le nom de

l’attribut à modifier
(cid:127)

Pour l’accesseur, faire précéder la méthode de @property

@property
def x(self):

return self.__x

(cid:127)

Pour le mutateur, faire précéder la méthode de @nomAttribut.setter

@x.setter
def x(self, x):
self.__x = x

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Exercice

15

(cid:127) Dans la classe Vecteur

(cid:127) Mettre les attributs x, y, z en privé

(cid:127) Modifier la méthode norme() pour que celle-ci
ne renvoie plus le résultat mais le stocke dans
un attribut norme lui-même privé

(cid:127)

Ajouter les accesseurs et les mutateurs pour
x, y et z de telle sorte à mettre à jour la norme
à chaque modification

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Héritage

16

(cid:127) Une classe qui hérite d’une autre aura (a minima)

Les mêmes attributs
Les mêmes méthodes

(cid:127)
(cid:127)
à Il n’est pas nécessaire de les définir dans la classe. Elle en hérite
automatiquement

(cid:127) Elle peut avoir des attributs et/ou méthodes supplémentaires qui

lui seront propre

(cid:127) Une classe peut redéfinir une méthode déjà présente dans la

classe dont elle hérite à on parle de masquage

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Héritage

17

(cid:127) Déclaration de la classe dont on hérite

class MaClasse(ClasseMere):

…

(cid:127) Utilisation de méthodes de la classe mère

super().laMethodeClasseMere()

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Exemple d’héritage

class Point2D:
def __init__(self, nom, x, y):
self.nom = nom
self.x = x
self.y = y

def get_nom(self):
return self.nom

def deplacer(self, x, y):
self.x += x
self.y += y

def distance(self, other):
return ((self.x - other.x) ** 2

+ (self.y - other.y) ** 2) ** 0.5

def __str__(self):
return f"({self.x}, {self.y})"

class Point3D(Point2D):
def __init__(self, nom, x, y, z):
super().__init__(nom, x, y)
self.z = z

def deplacer(self, x, y, z):
super().deplacer(x, y)
self.z += z

def distance(self, other):
return ((self.x - other.x) ** 2
+ (self.y - other.y) ** 2
+ (self.z - other.z) ** 2) ** 0.5

def __str__(self):
return f"({self.x}, {self.y}, {self.z})"

18

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Exemple d’héritage

class Mutation:

def appliquer(self, adn):

pass

19

class Substitution(Mutation):
def appliquer(self, adn):

pos = random.randint(0, len(adn.sequence) - 1)
base = random.choice("ATCG")
seq = list(adn.sequence)
seq[pos] = base
adn.sequence = "".join(seq)

class Insertion(Mutation):
def appliquer(self, adn):

pos = random.randint(0, len(adn.sequence))
base = random.choice("ATCG")
adn.sequence = adn.sequence[:pos] + base + adn.sequence[pos:]

class Deletion(Mutation):
def appliquer(self, adn):

if len(adn.sequence) > 1:

pos = random.randint(0, len(adn.sequence) - 1)
adn.sequence = adn.sequence[:pos] + adn.sequence[pos+1:]

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P

Exemple d’héritage (suite)

class Cellule:

def __init__(self, adn):

self.adn = adn
self.fitness = self.evaluer_fitness()

def evaluer_fitness(self):

# Exemple : plus il y a de "A", plus c'est adapté
return self.adn.sequence.count("A")

def muter(self, mutation):

mutation.appliquer(self.adn)
self.fitness = self.evaluer_fitness()

def mutation(self, taux):

mutations = [Substitution(), Insertion(), Deletion()]
for cellule in self.cellules:

if random.random() < taux:

mutation = random.choice(mutations)
cellule.muter(mutation)

20

l

i

e
c
g
o

i

l

i

e
n
é
g
t
e
e
é
c
n
a
v
a
n
o
i
t
a
m
m
a
r
g
o
r
P


