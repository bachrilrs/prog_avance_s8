#!/usr/bin/env python
"""Module de tri d'une liste d'entiers avec différents algorithmes de tri."""
import random

def generer_liste(nb):
    """Génère une liste de nb éléments aléatoires."""
    return [random.randint(x, x * 10) for x in range(nb)]

def bubble_sort(liste):
    """Tri à bulle."""
    l = liste
    n = len(l)
    for i in range(n):
        for j in range(i, n):
            if l[j] < l[i]:
                l[i], l[j] = l[j], l[i]
    return l

def select_sort(liste):
    """Tri par sélection."""
    n = len(liste)
    minimum = 0
    argmin = 0

    for i in range(n):
        minimum = liste[i]
        argmin = i
        for j in range(i, n):
            if liste[j] < minimum:
                minimum = liste[j]
                argmin = j
        liste[i], liste[argmin] = liste[argmin], liste[i]

    return liste

def insert_sort(liste, start=0, end=None):
    """Tri par insertion."""
    if end is None:
        end = len(liste)
    for i in range(start + 1, end):
        k = liste[i]
        j = i
        while j > start and liste[j - 1] > k:
            liste[j] = liste[j - 1]
            j -= 1
        liste[j] = k
    return liste



def quick_sort(l):
    """Tri rapide."""
    if len(l) <= 1:
        return l

    centre = len(l) // 2
    pivot = l[centre]

    gauche = []
    middle = []
    droite = []

    for el in l:
        if el > pivot:
            droite.append(el)
        elif el == pivot:
            middle.append(el)
        else:
            gauche.append(el)
    return quick_sort(gauche) + middle + quick_sort(droite)

def minrun_length(n):
    """Calcule la longueur minimale d'un run pour Timsort."""
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


def insert_sort_2(liste, start=0, end=None):
    """Tri par insertion pour une portion de la liste."""
    if end is None:
        end = len(liste)

    for i in range(start + 1, end):
        k = liste[i]
        j = i
        while j > start and liste[j - 1] > k:
            liste[j] = liste[j - 1]
            j -= 1
        liste[j] = k


def detect_run(a, start, end):
    """
    Détecte un run naturel à partir de start.
    Si le run est décroissant, on l'inverse pour le rendre croissant.
    Retourne la longueur du run.
    """
    i = start + 1
    if i >= end:
        return 1

    # Run décroissant
    if a[i] < a[start]:
        while i < end and a[i] < a[i - 1]:
            i += 1
        a[start:i] = reversed(a[start:i])
    else:
        # Run croissant
        while i < end and a[i] >= a[i - 1]:
            i += 1

    return i - start


def make_runs(a):
    """
    Découpe a en runs (segments triés).
    Force une taille minimalemin_run via insertion sort si besoin.
    Renvoie la liste de tuples (lo, hi) (hi exclu).
    """
    n = len(a)
    if n <= 1:
        return [(0, n)]

    min_run = minrun_length(n)
    runs = []
    i = 0

    while i < n:
        run_len = detect_run(a, i, n)

        if run_len <min_run:
            force = min(min_run, n - i)
            insert_sort_2(a, i, i + force)
            run_len = force

        runs.append((i, i + run_len))
        i += run_len

    return runs


def fusion_2(l1, l2):
    """
    Fusionne 2 listes triées (l1, l2) et renvoie une nouvelle liste triée.
    """
    i = j = 0
    res = []

    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            res.append(l1[i])
            i += 1
        else:
            res.append(l2[j])
            j += 1

    res.extend(l1[i:])
    res.extend(l2[j:])
    return res


def merge_runs(a, lo, mid, hi):
    """
    Fusionne a[lo:mid] et a[mid:hi] (déjà triés) dans a[lo:hi].
    """
    a[lo:hi] = fusion_2(a[lo:mid], a[mid:hi])


def merge_all_runs(a, runs):
    """
    Fusionne tous les runs jusqu'à n'en garder qu'un.
    """
    while len(runs) > 1:
        new_runs = []
        i = 0

        while i < len(runs):
            if i + 1 == len(runs):
                new_runs.append(runs[i])
                break

            lo1, hi1 = runs[i]
            _, hi2 = runs[i + 1]

            merge_runs(a, lo1, hi1, hi2)
            new_runs.append((lo1, hi2))
            i += 2

        runs = new_runs

    return a


def timsort(a):
    """Tri par Timsort."""
    runs = make_runs(a)
    return merge_all_runs(a, runs)

if __name__ == "__main__":
    l = generer_liste(20)
    print("Liste originale:", l)
    print("Tri à bulle:", bubble_sort(l.copy()))
    print("Tri par sélection:", select_sort(l.copy()))
    print("Tri par insertion:", insert_sort(l.copy()))
    print("Tri rapide:", quick_sort(l.copy()))
    print("Timsort:", timsort(l.copy()))