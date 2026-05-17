Programmation Orientée Objet et Génie Logiciel

TP – Manipulation de classes et objets en Python

Exercice 1 : La classe Point

Soit la classe Point qui stocke :

·
·

ses coordonnées 3D (x, y, z),
son nom.

Ecrire cette classe, ainsi que son constructeur qui initialise par défaut chaque coordonnée à 0.

Créer la méthode __str__ de manière à afficher le point sous la forme : nom_du_point (x, y, z)

Exercice 2 : La classe Vecteur

Soit la classe Vecteur qui stocke :

·
·

sa direction et son sens en x, y, z
son nom.

Ecrire la classe Vecteur et son constructeur.

Ecrire une méthode de classe pour construire un vecteur à partir de 2 points.

Ecrire la méthode norme qui retourne un réel correspondant à la norme du vecteur.

Rappel : Soit A et B deux points de coordonnées (xA,yA,zA) et (xB,yB,zB). La norme du vecteur AB

est obtenue par :

Ecrire  la  méthode produitVectoriel  qui  prend  en  argument  un  objet  de  type Vecteur  et

retourne un objet de type Vecteur qui est le résultat du calcul du produit vectoriel entre le

vecteur courant et le vecteur passé en argument.

Programmation Orientée Objet et Génie Logiciel

Rappel : Soit u et v respectivement de coordonnées (u1,u2,u3) et (v1,v2,v3). Le produit vectoriel est

obtenu de la manière suivante :

Créer la méthode __str__ de manière à afficher le vecteur sous la forme :

nom_du_vecteur (x, y, z)

Exercice 3 : La classe Triangle

Ecrire une classe Triangle qui stocke les 3 sommets a, b et c de ce triangle. Le constructeur
prendra en paramètres trois objets de type Point représentant les sommets du triangle.

Ecrire la méthode surface qui retourne un double correspondant à la surface du triangle.

La surface sera arrondie à deux décimales après la virgule.


