Programmation Orientée Objet et Génie Logiciel

TP – Manipulation d’objets

L’objectif de ce TP est de créer une application permettant de gérer les bulletins de notes d’une

classe.

Chaque  classe  devra  contenir  ces  méthodes __init__  pour  permettre  la  création  d’une

instance de la classe et __str__ pour afficher l’état de l’objet.

Exercice 1 – Enumération NomMatiere

Créer une énumération NomMatiere qui contient les valeurs MATHS, FRANÇAIS, ANGLAIS

Exercice 2 – Classe Controle

Créez une classe nommée Controle qui aura comme attributs deux réels pour représenter la

note obtenue et le coefficient associé à ce contrôle.

Exercice 3 – Classe Matière

Créez une classe nommée Matiere qui aura une liste dans laquelle on stockera les différentes

notes obtenues aux contrôles pour cette matière.

Créez les méthodes :

·

·

ajouterNote qui ajoute une note (passée en paramètre) au tableau des notes ;

calculerMoyenne  qui,  à  partir  du  tableau  de  notes,  calcule  la  moyenne  de  cette

matière et la retourne ;

Exercice 4 – Classe Eleve

Créez une classe nommée Eleve qui aura comme attributs :

· Deux chaines de caractères pour représenter le nom et le prénom de l’élève,
· Un dictionnaire permettant de gérer les différentes matières.

Créez la méthode ajouterNote qui ajoute une note dans la matière souhaitée. La note, son

coefficient et le nom de la matière seront donnés en paramètres ;

Exercice 5 – Classe Classe

Créez  une  classe  nommée Classe qui  aura  comme  attribut  un  dictionnaire  permettant

d’enregistrer  tous  les  élèves.  Pour  cela,  les  élèves  seront  ajoutés  à  la  liste  grâce  à  une  clé

composée de leur nom suivi de leur prénom.

Programmation Orientée Objet et Génie Logiciel

Exercice 6 – Menu pour gérer les notes d’une classe

Créez un menu dans lequel il sera possible de :

· Ajouter un élève
· Afficher la liste des élèves
· Ajouter une note dans une matière donnée à un élève
· Afficher le bulletin d’un élève : c’est-à-dire sa moyenne générale, ainsi que la moyenne

pour chaque matière

·

Pour une matière choisie, afficher la moyenne de chaque élève dans cette matière.


