Présentation du langage JAVA

Java en bref …

(cid:127)

Langage de programmation libre
(cid:127)
(cid:127)

Développé par Sun (1995)
Racheté par Oracle (2009)

(cid:127) Portable « write once, run everywhere »

(cid:127)

Interprété
(cid:127)
(cid:127)

Bytecode
Java Virtual Machine (JVM)

(cid:127) Programmation Orientée Objet

(cid:127) Une bibliothèque de classes : API

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

Java Virtual Machine (JVM)

3

(cid:127) Machine virtuelle

(cid:127) Avantages

(cid:127)

(cid:127)

le compilateur Java génère du byte
code et non de l’assembleur

(cid:127)

(cid:127)

Plus de gestion manuelle de
la mémoire
Indépendance de la
plateforme cible

le byte code est exécuté sur une
machine virtuelle : la JVM

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

Quelques définitions

4

(cid:127)

(cid:127)

(cid:127)

(cid:127)

JVM : Java Virtual Machine
à Machine virtuelle permettant d'interpréter et d'exécuter le bytecode Java.

JRE : Java Runtime Environement
à Kit destiné au client pour pouvoir exécuter un programme Java
à Il contient la JVM et les bibliothèques standards

JDK : Java Development Kit
à Kit destiné au programmeur
à Contient JRE, exemples, compilateur …

API : Application Programming Interface
à Bibliothèque de classes standards

https://docs.oracle.com/javase/8/docs/api/

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

Environnement de développement

Compiler un fichier Java

6

(cid:127)

La compilation de chaque fichier .java génèrera un fichier
d’extension .class

(cid:127) Commande de compilation

javac [options] fichiers_source

(cid:127)

Les options possibles
-classpath path

(cid:127)

path = chemin d’accès aux classes extérieures au projet et nécessaires à la
compilation

-d rep

(cid:127)

spécifie le répertoire dans lequel les fichiers .class seront enregistrés

-deprecation

(cid:127)

Indique les méthodes deprecated et comment les remplacer

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

Exécuter une application Java

7

(cid:127) Commande d’éxecution

java [options] nomdelaclasse [paramètres]

(cid:127)

Les options possibles
-classpath path

(cid:127)

Path = chemin d’accès aux classes nécessaires pour exécuter le projet

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

Documentation

8

(cid:127)

(cid:127)

(cid:127)

Permet de faire des documentations identiques à celle de l’API

Commande

javadoc –d rep fichiers_source

Commentaires pris en compte dans la documentation
/**  */

(cid:127) Mots clés
@see
@author
@version
@param
@return
@throws

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

Création de fichiers JAR

9

(cid:127)

(cid:127)

(cid:127)

JAR = Java ARchive

Regroupe un ensemble de fichiers sous forme d’archive
(cid:127)

Souvent sous forme d’arborescence

Commande

(cid:127) Options

-c : création, avec ou sans contenu
-u : Mise-à-jour

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

De bonnes pratiques

10

(cid:127) Structurer son répertoire de travail

(cid:127)
(cid:127)
(cid:127)
(cid:127)

Un dossier pour les sources (.java)
Un dossier pour les fichiers bytecode (.class)
Un dossier pour les ressources extérieures
Un dossier pour la documentation

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

Syntaxe Java

A savoir …

12

(cid:127) Ce n’est pas un script !

Toutes les instructions sont dans des « fonctions » des classes

(cid:127)
(cid:127) On ne parlera plus de fonction mais de méthode

(cid:127) Toutes les instructions terminent par un point virgule

(cid:127) On utilise les accolades pour délimiter un bloc d’instructions

(cid:127)

Le programme s’exécute à partir de la fonction main de la classe
qui est appelée
(cid:127)

Le programme exécute toutes les instructions de la méthode main

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

La méthode principale : main

13

public static void main(String[] args)
{

…

}

l

i

e
c
g
o

i

(cid:127)

Il peut y en avoir une par classe
(cid:127) Toute classe qui a une méthode main peut être exécutée

(cid:127) Pour les projets comportant plusieurs classes, il est préférable

de faire une classe à part pour la méthode main

(cid:127)

Le tableau args contient les différents éléments, sous forme de
chaines de caractères, passés en argument au moment du
lancement du projet

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

Afficher du texte

(cid:127) Affichage simple

System.out.print(“Bonjour”);

(cid:127) Affichage puis retour à la ligne

System.out.println(“Bonjour”);

(cid:127) Exemple « Hello World »

public class HelloWorldTerminal
{

public static void main(String[] args)
{

System.out.println("Hello World");

}

}

14

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

Les variables

15

(cid:127)

(cid:127)

Elles sont de trois types
Types primitifs,
(cid:127)
Références à un tableau,
(cid:127)
Références à un objet.
(cid:127)

Déclaration d’une variable
(cid:127)

Type de la variable suivi du nom de cette variable

int somme;
String nom;

(cid:127)

Affectation d’une valeur à une variable

somme = 0;
Nom = "Roger";

(cid:127)

Elles doivent être initialisées explicitement avant de pouvoir s’en servir.

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

Les types primitifs

(cid:127)

(cid:127)

(cid:127)

Les différents types primitifs :
(cid:127)
(cid:127)
(cid:127)
(cid:127)
(cid:127)
(cid:127)
(cid:127)
(cid:127)

boolean (true,false)
byte (8 bits)
char (16 bits)
short (16 bits)
int (32 bits)
long (64 bits)
float (32 bits)
double (64 bits)

Tous les types numériques sont signés

Il n’existe pas de transtypage implicite

16

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

Les tableaux

(cid:127) Déclaration

(cid:127)

Type d’éléments présents dans le tableau suivi de [], puis du nom du
tableau

int[] tab;

(cid:127) Création

(cid:127)

Il faut commencer par créer un tableau en indiquant le nombre
d’éléments souhaités dans ce tableau

tab = new int[42];

(cid:127)

Il faut initialiser chaque cellule du tableau avant de pouvoir l’utiliser

tab[0] = 0;

17

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

Les tableaux

(cid:127) Taille du tableau connue grâce à length

int taille = tab.length

18

l

i

e
c
g
o

i

(cid:127)

Les éléments du tableau
(cid:127)

Pour un tableau de taille N, les éléments sont stockés de l’indice 0 à
l’indice N-1

(cid:127)

Pour accéder à un élément du tableau

int premierElement = tab[0];
int dernierElement = tab[tab.length-1];

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

(cid:127)

Les différents éléments du tableau sont manipulables comme toute autre
variable

Structure conditionnelle : if … else …

19

(cid:127)

(cid:127)

Les instructions du bloc A seront
exécutées si la condition est vraie

Le bloc else n’est pas obligatoire
Si il est présent, les instructions du
(cid:127)
bloc B seront exécutées si la
condition du if est fausse

(cid:127) Dans tous les cas, les instructions

C sont exécutées

if(condition)
{

instructions du bloc A;

}
else
{

instructions du bloc B;

}
Instructions C;

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

Les conditions

(cid:127) On teste

(cid:127)
(cid:127)

une égalité entre deux éléments avec ==
une inégalité entre deux éléments avec
(cid:127)
(cid:127)
(cid:127)
(cid:127)
(cid:127)

Différent : !=
Supérieur strict : >
Supérieur ou égal : >=
Inférieur strict : <
Inférieur ou égal : <=

(cid:127) Plusieurs conditions peuvent être regroupées par

ET : &&

(cid:127)
(cid:127) OU : ||

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

Structure conditionnelle : switch

21

(cid:127)

(cid:127)

Le programme exécute les
instructions en fonction de la
valeur de la variable

Les différentes valeurs testées
sont définies par case et se
terminent par un break

(cid:127) Pour les cas non traités, il y a

le bloc default

switch(variable)
{

case val1 :

instructions;

break;
…
case valn :

instructions;

break;
default:

instructions;

break;

}

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

Les boucles

for(init compteur ; condition arrêt ; modif cpt)
{

instructions;

}

while(condition d’arrêt)
{

instructions;

}

do
{

instructions;

} while(condition d’arrêt);

22

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

Exercices

1. Afficher les puissances de 2 de 21 à 210

2. Afficher les tables de multiplication de 1 à 9 sous la forme

23

*** Table de 1

1 x 1 = 1

2 x 1 = 2
…

9 x 1 = 9

*** Table de 2

1 x 2 = 2
…

3. Afficher les chaines de caractères passées en argument au

lancement du programme

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


