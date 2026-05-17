Programmation Orientée Objet

Mathieu RAYNAL
mathieu.raynal@irit.fr
http://www.irit.fr/~Mathieu.Raynal

Programmation Orientée Objet

Notion de classe
Notion d’objet

Que voyez-vous ?

Programmation  et génie logiciel

3

4 rectangles

Nom

R1

R2

R3

R4

X

Y

Longueur

Hauteur

4

4

6

4

9

6

4

8

9

7

2

4

2

9

2

2

Programmation  et génie logiciel

4

Comment implémenter ces rectangles ?

(cid:127) Les décrire

(cid:127) Calculer

– Périmètre
– surface

(cid:127) Tester

– Une intersection entre deux rectangles
– Si un rectangle est inclus dans un autre
– Si deux rectangles sont alignés (haut bas, gauche ou droite)

à Comment faire tout ceci en python ?

Programmation  et génie logiciel

5

En JAVA

(cid:127) Tous les rectangles ont

– les mêmes caractéristiques

(cid:127) X, Y,
(cid:127) longueur, hauteur,
(cid:127) nom,
(cid:127) Couleur

– On peut calculer la même chose pour chacun

(cid:127) Surface
(cid:127) Périmètre

– Et tester les mêmes choses

(cid:127) Intersection
(cid:127) Inclusion
(cid:127) alignement

Programmation  et génie logiciel

6

Définir un type d’objet

(cid:127) Une classe permet de décrire un type d’objet

– Ses caractéristiques : Les attributs
– Ses fonctions : les méthodes

(cid:127) Structure d’une classe en JAVA

public class NomDeLaClasse
{

typeAttribut1 nomAttribut1;
typeAttribut2 nomAttribut2;
…
méthode1()
méthode2()
…

}

Programmation  et génie logiciel

7

Les attributs

(cid:127) Un attribut est une variable affectée à la classe

(cid:127)

Il est défini par
– le type de données qu’il représente

(cid:127) Un type primitif
(cid:127) Une référence à un objet
(cid:127) Une référence à un tableau

– Un nom

(cid:127) Sa déclaration se fait en début de classe

(cid:127) Son initialisation se fait dans le constructeur de la classe

Programmation  et génie logiciel

8

Les méthodes

(cid:127) C’est une fonction liée à la classe

(cid:127) Elle décrit un comportement de la classe sous la forme d’un

ensemble d’instructions

(cid:127) Une méthode est définie par, au minimum

– Un type de retour
– son nom
– Des parenthèses

typeRetour NomDeLaMethode()

Programmation  et génie logiciel

9

Retour d’une méthode

(cid:127) Une méthode sert à effectuer un ensemble d’instructions

(cid:127) A la fin de ces instructions, on peut demander à la méthode

de retourner un résultat

(cid:127) Ce résultat est retourné dans une variable au moyen du mot

clé return

(cid:127) Dans la déclaration de la méthode, il faut définir le type de

variable qui sera retournée
– Si la méthode ne retourne pas de valeur, le type de retour est void

Programmation  et génie logiciel

10

Paramètres d’une méthode

(cid:127) Ce sont des variables extérieures à la classe

(cid:127) Dans la définition de la méthode, les paramètres sont placés

entre les parenthèses, sous la forme
– typeDeLaVariable suivi du nomDeLaVariable
– S’il y a plusieurs paramètres, ils sont séparés par une virgule

typeRetour NomDeLaMethode(type1 param1, type2 param2, …)

(cid:127) Les paramètres sont utilisables dans la méthode grâce à leur

nom

Programmation  et génie logiciel

11

Exemple de méthodes

void ditBonjour(String nom)
{

System.out.println("Bonjour" + nom);

}

int calculPuissance(int a, int b)
{

if(b==0)

return 1;

int puissance = 1;
for(int i=0;i<b;i++)
puissance*=a;

return puissance;

}

Programmation  et génie logiciel

12

Utilisation des membres à l’intérieur de la classe

public class MaClasse
{

int a;
int b;

public int addition()
{

int c = a+b;
return c;

}

public void m(){ int d=addition();}

}

(cid:127) Les attributs et méthodes
d’une classe peuvent être
utilisés dans cette classe par
leur nom

(cid:127) S’il y a une ambigüité, les
membres d’une classe
peuvent être précédés du
mot this

public int multiplication(int a)
{

int c = this.a*a;
return c;

}

Programmation  et génie logiciel

13

Les instructions

(cid:127) Une instruction = toute opération que l’on peut effectuer

– Déclaration d’une variable ;
– Affectation d’une valeur à une variable ;
– Opération sur une variable ;
– Appel à une méthode

(cid:127) Toute instruction doit terminer par un point virgule

Programmation  et génie logiciel

14

Les blocs d’instructions

(cid:127) Un bloc délimite l’ensemble des instructions qui sont

effectuées pour
– La définition d’une classe
– La définition d’une méthode
– L’utilisation d’une structure de contrôle (if, for, switch, while)

(cid:127)

Il est délimité par des accolades

(cid:127) Un bloc d’instructions peut contenir d’autres blocs

d’instructions

(cid:127) Une variable déclarée dans un bloc est utilisable jusqu’à la fin

de ce bloc

Programmation  et génie logiciel

15

Qu’est-il possible de faire dans chaque bloc ?

(cid:127) Au niveau de la classe

– Seulement des déclarations d’attributs
– Pas d’affectations ou autres instructions

(cid:127) Au niveau méthode ou boucle, il est possible d’avoir :

– déclaration de variable,
– affectation,
– instruction,
– autres boucle

Programmation  et génie logiciel

16

Où positionner les différents éléments ?

(cid:127) Toutes les méthodes doivent se trouver dans le bloc de la

classe

(cid:127) Toutes les instructions et boucles doivent se trouver dans le

bloc d’une méthode, ou d’une autre boucle

(cid:127) Les variables sont :

– Dans le bloc de la classe à Attribut de la classe
(cid:127) Utilisable par toutes les méthodes de la classe

– Dans le bloc d’une méthode à Variable de la méthode

(cid:127) Utilisable seulement par la méthode

Programmation  et génie logiciel

17

Différents blocs possibles dans une classe

(cid:127) Les variables a et s sont

utilisables dans toutes les
méthodes de la classe
à Attributs de la classe

(cid:127) La variable n est déclarée dans

methode1
à Utilisable que dans la méthode 1

(cid:127) La variable i est déclarée dans

le bloc de la boucle for
à Utilisable que dans la boucle for

public class NomDeLaClasse
{

int a;
String s;
…
void methode1()
{

int n = 0;
for(int i=0;i<10;i++)
{

…

}
…

}

int methode2()
{

…

}

}

Programmation  et génie logiciel

18

Exercice 1 - Définir une classe Rectangle

(cid:127) Ses attributs

– 4 nombres décimaux pour

(cid:127) les coordonnées du centre du rectangle (x, y)
(cid:127) la longueur et la hauteur du rectangle
– Une chaîne de caractères pour le nom

dY

dX

(cid:127) Ses méthodes pour

– Calculer sa surface et qui renvoie un nombre décimal
– Calculer son périmètre et qui renvoie un nombre décimal
– Le déplacer de dX et dY, qui sont passés en paramètres
– Afficher ses caractéristiques sous la forme

Le rectangle R1 est positionné en (x, y), a une longueur de L et une hauteur de H

Programmation  et génie logiciel

19

Les constructeurs

(cid:127) Sert à initialiser les attributs d’une classe

(cid:127)

(cid:127)

(cid:127)

Il a exactement le même nom que la classe

Il n’a pas de valeur de retour

Il peut avoir des paramètres
– Les paramètres servent à initialiser les attributs de la classe

Programmation  et génie logiciel

20

La surcharge

(cid:127)

Il est possible d’avoir dans une même classe
– plusieurs constructeurs
– plusieurs méthodes ayant le même nom

(cid:127) Pour les différencier, il faut

– Un nombre de paramètres différent
– Ou au moins un type de paramètre différent

(cid:127) Le type de retour ne suffit pas à distinguer
deux méthodes qui ont le même nom

Programmation  et génie logiciel

21

Pourquoi faire plusieurs constructeurs ?

(cid:127) Un constructeur sert à initialiser les attributs de la classe

(cid:127) Au moment où on utilise le constructeur, on n’a peut-être pas

une valeur à affecter à chaque attribut

à Plusieurs constructeurs pour initialiser les attributs en
fonction de ce que l’on connait

(cid:127) Pour ce que l’on ne connait pas, les attributs doivent être

initialiser avec une valeur par défaut

Programmation  et génie logiciel

22

Exercice 2 - Constructeurs de la classe Rectangle

(cid:127) Ecrire 3 constructeurs

– Un constructeur par défaut (sans argument)

(cid:127) Initialisation des attributs avec des valeurs par défaut

– Un constructeur avec 3 arguments

(cid:127) Deux nombres décimaux qui représentent la longueur et la

hauteur que l’on souhaite donner au rectangle

(cid:127) Une chaine de caractères pour le nom du rectangle
(cid:127) Initialisation de x et y par une valeur par défaut

– Un constructeur avec 5 arguments

(cid:127) 4 nombres décimaux pour les attributs x, y, longueur et hauteur
(cid:127) Une chaine de caractères pour le nom du rectangle

Programmation  et génie logiciel

23

Structure d’une classe

(cid:127) Généralement une classe est structurée de la manière suivante

– Liste des attributs
– Constructeurs
– Méthodes
– Méthode main s’il y en a une

à Tous ces éléments doivent être dans le bloc de la classe

Programmation  et génie logiciel

24

Programmation Orientée Objet

Notion de classe
Notion d’objet

Qu’est ce qu’un objet ?

(cid:127) Un objet est une instance

d’une classe
– Avec une valeur propre pour

chaque attribut

(cid:127) Pour créer un objet, on utilise
un des constructeurs de la
classe correspondante précédé
du mot new

(cid:127) Pour manipuler cet objet, on
déclare une variable dont le
type est le nom de la classe
dont on veut créer un objet

public class Personne
{

String nom, prenom;
public Personne(){…}
public Personne(String nom)
{

this.nom=nom;

}

}

Personne p1;
p1 = new Personne();

Personne p2;
P2 = new Personne(‘’Dupont’’);

Personne p3 = new Personne();

Programmation  et génie logiciel

26

Les références

(cid:127) Ce sont des variables permettant
de stocker la référence à un objet

Circle c

(cid:127) Aucun objet n’est créé lors de la

déclaration

(cid:127)

Il faut faire appel à un des
constructeurs de la classe dont on
souhaite une instance

0x0001

0x0002

0x0003

0x0004
0x0004

0x0005

0x0006

0x0007

0x0008

0x0009

Circle c;
c = new Circle();

// Déclaration d’un objet : la variable se nomme c
// Création de l’objet associé à la référence c

Programmation  et génie logiciel

27

Utiliser les membres d’un objet

(cid:127) Quand un objet est créé, cet objet peut utiliser les attributs et

les méthodes de la classe dont il est une instance … si la
visibilité de ses membres le permet.

public class Personne
{

String nom, prenom;
public Personne(){…}
public Personne(String nom)
{

this.nom=nom;

}
public void afficheNom()
{

System.out.println(nom);

}

}

Personne p = new Personne();
p.nom = ‘’Durant’’;
p.prenom= ‘’Jean Paul’’;
p.afficheNom();

Programmation  et génie logiciel

28

Exercice 3 – Créer les objets Rectangle

(cid:127) Dans la méthode main, créer 4 rectangles avec les

caractéristiques suivantes :

Nom

R1

R2

R3

X

Y

Longueur

Hauteur

4

4

6

4

8

7

4

4

3

4

4

2

(cid:127) Afficher les différents rectangles

Programmation  et génie logiciel

29

Exercice 4 – Quelques ajouts de méthodes

(cid:127) Dans la classe Rectangle, ajoutez les méthodes :

– contientRectangle
– estContenuDansRectangle

(cid:127) Ces 2 méthodes renverront un booléen et prendront en

paramètre un objet Rectangle

Programmation  et génie logiciel

30

Conventions

(cid:127) Une seule classe par fichier. Même nom que la classe

(cid:127) Noms des classes et interfaces commencent par une majuscule

(cid:127) Noms des attributs commencent par une minuscule

(cid:127) Noms des packages en minuscule

(cid:127) Variables static final et valeurs d’une énumération en majuscule

(cid:127) Tout doit être dans une classe

(cid:127)

La méthode main dans une classe Main

Programmation  et génie logiciel

31


