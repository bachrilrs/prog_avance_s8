Programmation Orientée Objet et Génie Logiciel

TP – Héritage

L’objectif de ce TP est de simuler une maison connectée contenant un ensemble de capteurs

et des dispositifs connectés. Les capteurs émettent leur valeur à chaque fois que celle-ci est

mise à jour. Les dispositifs connectés peuvent « s’abonner » aux capteurs qui les intéressent et

ainsi réagir en fonction des valeurs envoyées.

Voici un exemple que nous mettrons en œuvre dans ce TP :

Les capteurs présents sont des capteurs de luminosité et d’air. Les dispositifs connectés sont

une station météo, les volets roulants.

La  station  météo  affiche  les  valeurs  des  différents  capteurs.  Les  volets  roulants  seront

automatiquement ouverts si la luminosité est trop faible, et inversement seront fermés en cas

de trop forte intensité.

Pour que les capteurs puissent envoyer une information à leurs abonnés, il faut que tous les

abonnés aient une méthode commune à chacun d’eux par laquelle les informations pourraient

transiter.

Une classe permettra de définir cette méthode. Toutes les classes qui souhaiteront s’abonner

à, au moins, un capteur devront alors hériter de cette classe.

1- Créez la classe Abonne qui aura une méthode actualiserEtat qui prendra en paramètre

un objet de type Capteur.

Afin de pouvoir communiquer leur valeur, les capteurs doivent gérer la liste de leurs abonnés.

A chaque mise à jour de leur valeur, cette information sera communiquée à l’ensemble des

abonnées via la méthode actualiserEtat.

2- Créez une classe Capteur qui aura comme attributs un nom pour le capteur, une liste

de diffusion contenant les abonnés. Cette classe doit avoir les méthodes :
·

ajouterAbonne(Abonne a) qui permet d’ajouter un Abonne à la liste de diffusion

·

envoyerNotification() qui transmet à tous les abonnés le nouvel état du capteur

La  classe  Capteur  est  une  classe  générique  qui regroupe  les  informations  et  fonctionnalités

communes à chaque type de capteur. Mais la classe capteur n’est pas un capteur en soi (elle

n’a pas de valeur).

3- Créez les classes CapteurLuminosite et CapteurAir qui héritent de la classe Capteur

et  qui  auront  respectivement  un  attribut  intensité  et  trois  attributs  température,

Programmation Orientée Objet et Génie Logiciel

humidité et CO2 . Pour pouvoir mettre à jour et accéder à ces valeurs, les classes auront

une méthode setData

4- Créez  la  classe StationMeteo  qui  affiche  au  fur  et  à  mesure  dans  la  console  les

informations reçues

5- Créez la classe VoletRoulant qui a un attribut indiquant si les volets sont ouverts ou

non.  En  fonction  des  valeurs  reçues  par  les  capteurs  d’intensité,  si  l’intensité  est

supérieure  à  100  et  que  les  volets  sont  ouverts,  les  volets  seront  alors  fermés.

Inversement, si les  volets sont fermés et que l’intensité est inférieure à 20, les volets

seront  ouverts. Remarque :  L’ouverture  et  la  fermeture  des  volets  seront  simplement

représentées par un message dans la console.

6- Pour

tester

l’ensemble,

créez  des  objets  de

types  CapteurLuminosité,

CapteurTemperature, StationMeteo et VoletRoulant. La station météo sera abonnée à

tous les capteurs. Les volets roulants seront abonnés au capteur de luminosité. Créez

un  petit  menu  pour  pouvoir  allouer  une  nouvelle  valeur  à  un  capteur  d’air  ou  à  un

capteur de luminosité.

Bonus :  Créez  une  classe  AlerteCanicule  qui  doit  pouvoir  recevoir  les  informations  de

température. Si la température est supérieure à 30, un message d’alerte canicule sera affiché

dans la console et les volets seront fermés.


