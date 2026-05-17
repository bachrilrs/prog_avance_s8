Programmation Orientée Objet et Génie Logiciel
Master1 Bio-Informatique, parcours BBS

TP – Gestion d’une bibliothèque

L’objectif est de réaliser une application permettant la gestion d’une bibliothèque.

Cette application devra gérer à la fois l’ensemble des livres mis à disposition du public ainsi que
les personnes inscrites à la médiathèque et qui peuvent, par conséquent, emprunter des ouvrages.

Chaque ouvrage sera enregistré avec un identifiant unique qui lui sera propre, un titre, un auteur,
un résumé et le type de livre (magazine, roman, BD, etc.), ainsi qu’une indication sur d’éventuelles
restrictions d’emprunt (interdit -10 ans, -12, -16, -18 ; emprunt uniquement le weekend, etc.).

Les différents auteurs seront aussi enregistrés dans l’application pour pouvoir faire une recherche
par artiste. Pour chaque artiste, nous aurons accès à son nom, son prénom, une biographie, la liste
de ses œuvres.

Les  personnes  inscrites  dans  l’application  devront  renseigner  leur  nom,  prénom,  date  de
naissance, numéro de téléphone, adresse postale et adresse de messagerie.

Votre application doit aussi permettre à une personne inscrite d’emprunter et rendre des ouvrages
(à vous de fixer le nombre limite d’ouvrages que peut emprunter en même temps un inscrit). Un
emprunt se fera pour une période donnée (par exemple 15 jours). Une fois cette période passée,
si l’ouvrage est rendu en retard, l’inscrit sera pénalisé d’un jour de pénalité par jour de retard. Par
exemple, si un inscrit rend des ouvrages avec 10 jours de retard, il ne pourra pas emprunter de
nouveaux ouvrages pendant les 10 jours suivant le moment où il a rendu ces ouvrages.

L’objectif est de réaliser les classes de base de votre application.


