import random

def creer_liste_vide():
    """Créer une liste vide."""
    return None

def creer_liste(t,q):
    """Créer une liste avec tête t et queue q."""
    return t,q

def tete(liste):
    """Retourne la tête de la liste."""
    return liste[0]

def queue(liste):
    """Retourne la queue de la liste."""
    return liste[1]

def est_vide(liste):
    """Vérifie si la liste est vide."""
    return liste==None

def longueur(liste):
    """Retourne la longueur de la liste."""
    if est_vide(liste):
        return 0
    else:
        return 1 + longueur(queue(liste))

def substituer_premiere_occurence(liste, x, y):
    """Substitue la première occurrence de x par y dans la liste."""
    if est_vide(liste):
        return creer_liste_vide()
    elif tete(liste) == x:
        return creer_liste(y, queue(liste))
    else:
        return creer_liste(tete(liste), substituer_premiere_occurence(queue(liste), x, y))

def generer_liste_chaine(n):
    """Génère une liste chaînée de n éléments aléatoires."""
    return creer_liste_vide() if n == 0 else creer_liste(random.randint(1,1000), generer_liste_chaine(n-1))

def concatener(liste1, liste2):
    """Concatène deux listes."""
    if est_vide(liste1): # cas d'arret
        return liste2
    else:
        return creer_liste(tete(liste1), concatener(queue(liste1), liste2)) # concatener le reste de liste1 avec liste2 et ajouter tete(liste1) au debut

def quick_sort_liste_chainees(liste):
    """quick sort pour les listes chainées"""
    if est_vide(liste) or est_vide(queue(liste)):
        return liste

    pivot = tete(liste) # choisir le pivot comme le premier élément de la liste
    reste = queue(liste)

    inf,sup = partition(reste,pivot) # partitionner le reste de la liste en deux listes: inf et sup

    return concatener(
        quick_sort_liste_chainees(inf),
        creer_liste(pivot,
        quick_sort_liste_chainees(sup))) # trier les deux listes inf et sup récursivement et concatener les résultats avec le pivot au milieu

def partition(liste,pivot):
    """partitionne la liste en deux listes: inf et sup"""
    inf = creer_liste_vide()
    sup = creer_liste_vide()


    while not est_vide(liste): # tant que liste pas vide
        if tete(liste) < pivot: # mettre tete devant inf
            inf = creer_liste(tete(liste),inf)
        else:
            sup = creer_liste(tete(liste),sup)  # mettre tete devant inf
        liste = queue(liste) # mettre a jour liste retirer tete pour pas avoir de RecusrionError (retirer tete en garder le reste de la liste)
    return inf,sup



