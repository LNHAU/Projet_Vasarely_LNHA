"""
    Auteur : LNHA
    Date : 8 mars 2019
    Code qui produit un tableau d’art optique représentant un pavage hexagonal, vu d’en haut (par projection
        orthogonale sur les axes x, y (z = 0)), formé avec des losanges de couleurs différentes, déformés par une boule
        qui sort du pavage (ou y rentre).
"""

import turtle
from math import pi, sin, cos, ceil
from deformation import deformation  # trop compliquée pour moi...
import time
import sys


def aucune_deformation(p, c, r):
    """
        Reçoit un point et le renvoie tel quel sans aucune déformation.

        Entrées :
        - un point p donnant les trois coordonnées du point p = (p_x, p_y, p_z) (triple de float),
        - et, pour avoir la même signature que la fonction deformation(p, c, r) importée (pour être compatible
          et interchangeable dans tout appel à la fonction deformation(p, c, r) passée en paramètre d'une autre
          fonction), deux paramètres inutilisés :
            - un point centre donnant les trois coordonnées du centre de la sphère de déformation
                centre = (centre_x, centre_y, centre_z) (triple de int)
            - et le rayon de la sphère de déformation rayon (float).
        Résultat : le point p = (p_x, p_y, p_z) initial sans déformation (triple de float).
    """
    return p


def controle_nb_valeurs_typees(donnee, nb, type_valeurs=str, invite=None):
    """
        Construit une liste d'un nombre exact de valeurs extraites d'une chaîne de caractères, dans laquelle ces valeurs
            sont séparées d'au moins un espace, une tabulation ou un saut de ligne, d'un certain type (après avoir
            "sauté" les valeurs de type incorrect), et renvoie soit cette liste, soit, si on ne demandait qu'une seule
            valeur, l'unique valeur lue, soit, si aucune invite n'était précisée et qu'aucune valeur n'était correcte,
            une liste vide.
        Attention : cette fonction peut boucler indéfiniment si la chaîne en entrée ne contient pas assez de valeurs
            du bon type séparées d'au moins un espace, une tabulation ou un saut de ligne et qu'on invite
            l'utilisateur à la compléter au clavier!
            A l'inverse, après être parvenu à lire assez de valeurs du bon type séparées d'au moins un espace,
            une tabulation ou un saut de ligne, cette fonction s'arrêtera avec un code erreur si l'utilisateur
            a saisi quelque chose en plus de ces valeurs bien typées sur la dernière ligne (et les suivantes)!

    Entrées :
    - la chaîne de caractères donnee dont il faut extraire la ou les valeurs du type type_valeurs (un str),
    - le nombre nb de valeurs du type type_valeurs à extraire (un int),
    - le type type_valeurs des valeurs à extraire (un nom de type non mis entre quotes, par exemple : int) ;
        si cette entrée est omise, par défaut type_valeurs est égal à str.
    - l'invite invite s'il faut redemander une chaîne donnee supplémentaire pour réussir à extraire nb valeurs du type
        type_valeurs ; si cette entrée est omise, par défaut invite est égal à None.
    Résultat : la liste vide si aucune invite n'était précisée et qu'aucune valeur n'était du type type_valeurs,
        ou bien la valeur lue du type type_valeurs, ou bien, si nb > 1, la liste des nb valeurs lues du type
        type_valeurs.
    """
    res = []

    # on ne prend pas en compte les quotes enveloppantes saisies par l'utilisateur pour la valeur de type_valeurs
    if str(type_valeurs) in ("", ''):
        type_valeurs = str
    elif len(str(type_valeurs)) > 0 and str(type_valeurs)[0] in ('"', "'"):
        type_valeurs = str(type_valeurs)[1:]
    if len(str(type_valeurs)) > 0 and str(type_valeurs)[len(str(type_valeurs)) - 1] in ('"', "'"):
        type_valeurs = str(type_valeurs)[:len(str(type_valeurs)) - 1]

    total = 0
    surplus = []
    while total < nb:
        if donnee not in ('', (), []):  # une ligne vide n'a pas besoin d'être traitée
            if type(donnee) in (tuple, list):
                donnee = str(donnee)

            x = donnee.replace("\\n", "\n")  # remplace les sous-chaînes "\n" saisies "en dur" par l'utilisateur
                                             # par des sauts de lignes

            if type_valeurs != str:
                # on ne prend pas en compte les éventuels délimiteurs, ni les quotes saisis par l'utilisateur
                # lorsque le type attendu n'est pas str, quelque soit leur nombre ou leur mélange
                for delimiter in ['"', "'", '(', ')', '[', ']', '{', '}', ',', ';', ':', '*', '/', '%', '=',
                                  '!', '?', ' - ', ' + ']:
                    x = x.replace(delimiter, " ")

            decoupe = x.strip().split()  # parties de x séparées par un/des espace(s) ou une/des tabulation(s)
                                         # sous forme d'une liste de chaînes de caractères (liste de str)
            for num, elem in enumerate(decoupe):
                if total < nb:
                    if type_valeurs != str:
                        elem = "".join([d for d in elem if d.isdigit() or d in ['-', '+']])
                        if (len(elem) > 0 and (elem[0].isdigit() or (elem[0] in ['-', '+'] and len(elem) > 1
                                                                     and elem[1].isdigit()))
                                and isinstance(eval(elem), type_valeurs)):
                            res.append(eval(elem))  # on stocke une valeur de type type_valeurs, et non pas un str
                            total += 1
                    else:
                        # on ne prend pas en compte les délimiteurs enveloppant une partie de x (en première
                        # et/ou dernière positions) saisis par l'utilisateur lorsque le type attendu est str
                        delimiters = ['(', ')', '[', ']', '{', '}', ',', ';', ':', '( ', ' )', '[ ', ' ]',
                                      '{ ', ' }', ' ,', ' ;', ' :', '/', ' /', '*', ' *', ' -']
                        for delimiter in delimiters:
                            if elem[0:len(delimiter)] == delimiter:
                                elem = elem[len(delimiter):]
                        for delimiter in delimiters:
                            if elem[len(elem) - len(delimiter):] == delimiter:
                                elem = elem[:len(elem) - len(delimiter)]

                        # on ne prend pas en compte les quotes (sous-)enveloppantes
                        # saisies par l'utilisateur lorsque le type attendu est str
                        if elem[0] in ('"', "'"):
                            elem = elem[1:]
                        if elem[len(elem) - 1] in ('"', "'"):
                            elem = elem[:len(elem) - 1]

                        if (isinstance(eval("'" + elem + "'"), type_valeurs)):
                            res.append(elem)  # on stocke une valeur de type str
                            total += 1

                    if total == nb and len(decoupe[num + 1:]) > 0:
                        surplus = decoupe[num + 1:]
                        print("\nCes valeurs : " + str(surplus) + "  sont en trop.")
                        break  # force la sortie du for précédent
        if invite not in (None, '') and total < nb:
            # on continuera à attendre une saisie au clavier tant que donnee ne contiendra pas assez de valeurs
            # du bon type séparées d'au moins un espace, une tabulation, ou saut de ligne!
            donnee = input("Il manque encore " + str(nb - total) + " valeur(s) pour " + invite + " :\n")
        elif total < nb:
            break  # force la sortie du while précédent
        elif len(surplus) > 0:
            exit(-1)  # sortie de la fonction en erreur car je ne parviens pas à "réutiliser" ce surplus
                      # pour un input via un appel ultérieur à la fonction, ou à la fonction lecture_nb_valeurs_typees
    if nb == 1 and len(res) > 0:
        res = res[0]  # l'unique valeur du bon type lue car on ne demandait qu'une seule valeur
    return res


def lecture_nb_valeurs_typees(invite, nb, type_valeurs=str):
    """
        Construit une liste d'un nombre exact de valeurs lues au clavier, séparées d'au moins un espace, une tabulation
            ou un saut de ligne, d'un certain type (après avoir "sauté" les données saisies de type incorrect), et
            renvoie soit cette liste, soit, si on ne demandait qu'une seule valeur, l'unique valeur lue.
        Attention : cette fonction peut boucler indéfiniment si l'utilisateur ne saisit pas assez de valeurs
            du bon type séparées d'au moins un espace, une tabulation ou un saut de ligne!
            A l'inverse, après être parvenu à lire assez de valeurs du bon type séparées d'au moins un espace,
            une tabulation ou un saut de ligne, cette fonction s'arrêtera avec un code erreur si l'utilisateur
            a saisi quelque chose en plus de ces valeurs bien typées sur la dernière ligne (et les suivantes)!

    Entrées :
    - l'invite invite qui explique à l'utilisateur quelle(s) valeur(s) il doit saisir au clavier (un str),
    - le nombre nb de valeurs de même type à lire (un int),
    - le type type_valeurs des valeurs à lire (un nom de type non mis entre quotes, par exemple : int) ;
        si cette entrée est omise, par défaut type_valeurs est égal à str.
    Résultat : la valeur lue du type type_valeurs ou, si nb > 1, la liste des nb valeurs lues du type type_valeurs.
    """
    if invite in (None, ''):
        invite = nb + " valeur(s) de type " + str(type_valeurs)
    x = input("Veuillez donner " + invite + " :\n(Saisissez un retour à la ligne pour mettre fin à la lecture.)\n")
    return controle_nb_valeurs_typees(x, nb, type_valeurs, invite)


def lecture_données_utilisateur():
    """
        Demande à l’utilisateur ce qu’il désire comme paramètres (couleurs, longueur des segments, …) pour le pavage
            et retourne les valeurs saisies (après filtrage éventuel des valeurs de type incorrect) sous forme de tuple.

        Aucune entrée.
        Résultat : le tuple de tous les paramètres nécessaires (hormis la tortue et la fonction de déformation)
            au pavage (inf_gauche, sup_droit, longueur, col1, col2, col3, centre, r), soit
        - les coordonnées du bord inférieur gauche de la fenêtre de visualisation inf_gauche
            (une seule valeur entière commune à x_inf_gauche et y_inf_gauche) (un int)
        - les coordonnées du bord supérieur droit de la fenêtre de visualisation sup_droit
            (une seule valeur entière commune à x_sup_droit et y_sup_droit) (un int)
        - la longueur d’un segment de pavé (avant déformation) longueur (un int)
        - la couleur des pavés Nord-Est (en haut à droite de chaque hexagone) col1 (un str)
        - la couleur des pavés Ouest (à gauche de chaque hexagone) col2 (un str)
        - la couleur des pavés Sud-Est (en bas à droite de chaque hexagone) col3 (un str)
        - les coordonnées du centre de la sphère déformante centre sous forme de tuple (centre_x, centre_y et centre_z)
            (tuple de trois int)
        - le rayon de la sphère déformante r (un int).
    """
    inf_gauche, sup_droit, longueur, col1, col2, col3, centre, r = (0, 0, 0, '', '', '', (), 0)  # initialisation
    inf_gauche = lecture_nb_valeurs_typees("les coordonnées du bord inférieur gauche de la fenêtre \
de visualisation (une seule valeur entière commune à x_inf_gauche et y_inf_gauche)", 1, int)
    sup_droit = lecture_nb_valeurs_typees("les coordonnées du bord supérieur droit de la fenêtre \
de visualisation (une seule valeur entière commune à x_sup_droit et y_sup_droit)", 1, int)
    longueur = lecture_nb_valeurs_typees("la longueur d’un segment de pavé (avant déformation) \
(une valeur entière)", 1, int)
    col1 = lecture_nb_valeurs_typees("la couleur des pavés Nord-Est \
(en haut à droite de chaque hexagone) (une chaîne de caractères)", 1, str)
    col2 = lecture_nb_valeurs_typees("la couleur des pavés Ouest (à gauche de chaque hexagone) \
(une chaîne de caractères)", 1)
    col3 = lecture_nb_valeurs_typees("la couleur des pavés Sud-Est \
(en bas à droite de chaque hexagone) (une chaîne de caractères)", 1)
    centre = tuple(lecture_nb_valeurs_typees("les coordonnées du centre de la sphère déformante \
(trois entiers séparés chacun par un espace pour centre_x, centre_y et centre_z)", 3, int))
    r = lecture_nb_valeurs_typees("le rayon de la sphère déformante (une valeur entière)", 1, int)
    print("\n")
    return (inf_gauche, sup_droit, longueur, col1, col2, col3, centre, r)


def hexagone(t, c, longueur, col1, col2, col3, deformation, centre, rayon):
    """
        Peint, à l'aide des fonctions du module turtle, un hexagone déformé en traçant des lignes droites
            entre son centre et ses extrémités dont les positions sont calculées avec la fonction deformation.

        Schémas des points (avant déformation), des couleurs de l'hexagone et de l'ordre de dessin des pavés :
            F --- G                 . --- .                . --- .
          /  \     \              /c \ col1\             /  \  2  \
         E    c --- A            . o  . --- .           . 3  . --- .
          \  /     /              \l2/ col3/             \  /  1  /
            D --- B                 . --- .                . --- .

        Entrées :
        - la tortue t,
        - le point central c avant déformation où l’hexagone doit être peint,
            c = (c_x, c_y, c_z) donnant la valeur des trois coordonnées (triple de float),
        - la distance (avant déformation) longueur entre le centre de l’hexagone et n’importe lequel de ses coins (int),
            c'est-à-dire la longueur (avant déformation) d’un segment des pavés constituant l’hexagone,
        - les trois couleurs col1, col2, col3, respectivement du pavé Nord-Est (en haut à droite),
            du pavé Ouest (à gauche) et du pavé Sud-Est (en bas à droite) de l’hexagone (trois str),
        - la fonction deformation(p, centre, rayon) qui elle-même reçoit en paramètre :
            - un point p donnant les trois coordonnées du point p = (p_x, p_y, p_z) (triple de float),
            - un point centre donnant les trois coordonnées du centre de la sphère de déformation
                centre = (centre_x, centre_y, centre_z) (triple de int)
            - et le rayon de la sphère de déformation rayon (float),
            et renvoie le point p2 = (p2_x, p2_y, p2_z) après déformation (triple de float),
        - le point centre de la sphère de déformation centre = (centre_x, centre_y, centre_z) (triple de int),
        - et le rayon rayon de la sphère de déformation (float).
        Résultat : None
    """
    t.up()  # tant que la tortue est en mode “up”, son déplacement ne trace rien
    pointc = deformation((c[0], c[1], 0), centre, rayon)  # "deformation" est la fonction passée en paramètre
    # donc, attention, il se peut qu'elle ne réalise aucune déformation si l'argument est en fait "aucune_deformation"
    t.goto(pointc[0], pointc[1])  # la tortue se place au centre c en coordonnées (c_x, c_y, c_z = 0) +/- déformées

    # dessin du pavé Sud-Est (en bas à droite)
    t.color(col3)   # la tortue est de couleur col3 et cette couleur,
    t.down()        # tant que la tortue est “down”, tracera la ligne de ses déplacements
    t.begin_fill()  # et va remplir l’intérieur de ce qui est tracé entre maintenant et le t.end_fill() ultérieur
    pointA = deformation((c[0] + longueur, c[1], 0), centre, rayon) # point A déformé ou non!!! ( = "+/-")
    t.goto(pointA[0], pointA[1])  # la tortue avance horizontalement vers la droite de longueur jusqu'au point A +/-
    pointB = deformation((c[0] + (longueur * cos(pi / 3)), c[1] - (longueur * sin(pi / 3)), 0), centre, rayon)
    t.goto(pointB[0], pointB[1])  # la tortue avance vers le bas de longueur jusqu'au point B +/-
    pointD = deformation((c[0] + (longueur * cos(2 * pi / 3)), c[1] - (longueur * sin(2 * pi / 3)), 0), centre, rayon)
    t.goto(pointD[0], pointD[1])  # la tortue avance horizontalement vers la gauche de longueur jusqu'au point D +/-
    t.goto(pointc[0], pointc[1])  # la tortue remonte de longueur jusqu'au centre c +/-
    t.end_fill()    # la tortue remplit ce qui a été tracé entre le begin_fill précédent et cette instruction

    # dessin du pavé Nord-Est (en haut à droite)
    t.color(col1)   # la tortue est de couleur col1 et cette couleur tracera la ligne de ses déplacements et
    t.begin_fill()  # va remplir l’intérieur de ce qui est tracé entre maintenant et le t.end_fill() ultérieur
    t.goto(pointA[0], pointA[1])  # la tortue avance horizontalement vers la droite de longueur jusqu'au point A +/-
    pointG = deformation((c[0] + (longueur * cos(pi / 3)), c[1] + (longueur * sin(pi / 3)), 0), centre, rayon)
    t.goto(pointG[0], pointG[1])  # la tortue avance vers le haut de longueur jusqu'au point G +/-
    pointF = deformation((c[0] + (longueur * cos(2 * pi / 3)), c[1] + (longueur * sin(2 * pi / 3)), 0), centre, rayon)
    t.goto(pointF[0], pointF[1])  # la tortue avance horizontalement vers la gauche de longueur jusqu'au point F +/-
    t.goto(pointc[0], pointc[1])  # la tortue redescend de longueur jusqu'au centre c +/-
    t.end_fill()    # la tortue remplit ce qui a été tracé entre le begin_fill précédent et cette instruction

    # dessin du pavé Ouest (à gauche)
    t.color(col2)   # la tortue est de couleur col2 et cette couleur tracera la ligne de ses déplacements et
    t.begin_fill()  # va remplir l’intérieur de ce qui est tracé entre maintenant et le t.end_fill() ultérieur
    t.goto(pointD[0], pointD[1])  # la tortue avance vers le bas de longueur jusqu'au point D +/-
    pointE = deformation((c[0] - longueur, c[1], 0), centre, rayon)
    t.goto(pointE[0], pointE[1])  # la tortue remonte vers la gauche (à la même hauteur que c) de longueur jusqu'à E +/-
    t.goto(pointF[0], pointF[1])  # la tortue remonte vers la droite de longueur jusqu'au point F +/-
    t.goto(pointc[0], pointc[1])  # la tortue redescend de longueur jusqu'au centre c +/-
    t.end_fill()    # la tortue remplit ce qui a été tracé entre le begin_fill précédent et cette instruction
    t.up()


def pavage(t, inf_gauche, sup_droit, longueur, col1, col2, col3, deformation, centre, rayon):
    """
        Peint, à l'aide des fonctions du module turtle, des lignes d'hexagones déformés dont les centres,
            avant déformation, se trouvent dans la fenêtre de visualisation (bords inclus), en réitérant la même
            séquence de couleurs pour tous les pavés. Le premier hexagone de la première ligne en bas à gauche, avant
            déformation, est centré sur le bord inférieur gauche de la fenêtre de visualisation.

        Entrées :
        - la tortue t,
        - les valeurs inf_gauche et sup_droit donnant respectivement le coin inférieur gauche de coordonnées
            (inf_gauche, inf_gauche) et le coin supérieur droit de coordonnées (sup_droit, sup_droit) de la fenêtre
            de visualisation, sachant que l’on représente uniquement les axes x et y, la hauteur du pavage avant
            transformation étant égale à 0 (deux int),
        - la distance (avant déformation) longueur entre le centre d'un hexagone et n’importe lequel de ses coins (int),
            c'est-à-dire la longueur (avant déformation) d’un segment des pavés constituant chaque hexagone,
        - les trois couleurs col1, col2, col3, respectivement du pavé Nord-Est (en haut à droite),
            du pavé Ouest (à gauche) et du pavé Sud-Est (en bas à droite) des hexagones (trois str),
        - la fonction deformation(p, centre, rayon) qui elle-même reçoit en paramètre :
            - un point p donnant les trois coordonnées du point p = (p_x, p_y, p_z) (triple de float),
            - un point centre donnant les trois coordonnées du centre de la sphère de déformation
                centre = (centre_x, centre_y, centre_z) (triple de int)
            - et le rayon de la sphère de déformation rayon (float),
            et renvoie le point p2 = (p2_x, p2_y, p2_z) après déformation (triple de float),
        - le point centre de la sphère de déformation centre = (centre_x, centre_y, centre_z) (triple de int),
        - et le rayon rayon de la sphère de déformation (float).
        Résultat : None
    """
    if (inf_gauche == None) or (sup_droit == None) or (longueur == None) or (col1 == None) or (col2 == None) \
            or (col3 == None) or (centre == None) or (rayon == None) or (inf_gauche == sup_droit)\
            or (longueur == 0) or (col1 == '') or (col2 == '') or (col3 == '') or (centre == ()) or (rayon == 0.):
        # Demande à l’utilisateur les paramètres (couleurs, longueur des segments, …) du pavage qu'il désire
        inf_gauche, sup_droit, longueur, col1, col2, col3, centre, rayon = lecture_données_utilisateur()

    print("Paramètres choisis pour le pavage : ", inf_gauche, sup_droit, longueur, col1, col2, col3, centre, rayon)

    if inf_gauche < sup_droit + 3 * longueur:
        t.clear()  # Efface les dessins du crayon et réinitialise le crayon
        t.setup()  # Réinitialise la taille de la fenêtre de visualisation et centre cette fenêtre à l'écran

        taille_fenetre = sup_droit - inf_gauche  # largeur et hauteur de la fenêtre de visualisation initiale
        p_inf_gauche = deformation((inf_gauche, inf_gauche, 0), centre, rayon)  # coin inférieur gauche +/- déformé
        p_sup_droit = deformation((sup_droit, sup_droit, 0), centre, rayon)     # coin supérieur droit +/- déformé
        reste_largeur_dessin = ceil((3 * longueur) - taille_fenetre % (3 * longueur))
        reste_hauteur_dessin = ceil((longueur * sin(2 * pi / 3)) - taille_fenetre % (longueur * sin(2 * pi / 3)))
        largeur_dessin = taille_fenetre + reste_largeur_dessin
        hauteur_dessin = taille_fenetre + reste_hauteur_dessin
        # Réduit la fenêtre de visualisation à la taille du dessin et centre cette fenêtre à l'écran
        t.setup(width = largeur_dessin,  height = hauteur_dessin, startx = None, starty = None)

        t.hideturtle()  # cache le crayon
        # Place la fenêtre de visualisation au premier plan
        wn = t.Screen()
        rootwindow = wn.getcanvas().winfo_toplevel()
        rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
        rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
        # Redéfinit le système de coordonnées dans la fenêtre de visualisation
        wn.setworldcoordinates(p_inf_gauche[0] - longueur / 3,
                               p_inf_gauche[1] - longueur / sin(2 * pi / 3),
                               p_sup_droit[0] + reste_largeur_dessin,
                               p_sup_droit[1] + reste_hauteur_dessin)

        t.speed(0)  # vitesse de tracé la plus rapide
        t.tracer(25, 5)  # ne réalise une mise à jour du dessin que tous les 25 * 5 ms intervalles

        # dessin sur toute la hauteur de la fenêtre de visualisation de lignes d'hexagones deux par deux
        c_y = inf_gauche  # départ du bord inférieur gauche en ordonnée
        while c_y <= sup_droit:
            # dessin de la première ligne d'hexagones
            c_x = inf_gauche  # départ du bord inférieur gauche en abscisse
            hexagone(t, (c_x, c_y, 0), longueur, col1, col2, col3, deformation, centre, rayon)
            while c_x <= sup_droit:
                c_x += 3 * longueur  # décalage de deux hexagones vers la droite en abscisse
                hexagone(t, (c_x, c_y, 0), longueur, col1, col2, col3, deformation, centre, rayon)

            # dessin de la ligne immédiatement supérieure
            c_x = inf_gauche + 1.5 * longueur         # décalage d'un hexagone vers la droite en abscisse
            c_y = c_y + (longueur * sin(2 * pi / 3))  # et vers le haut en ordonnée
            hexagone(t, (c_x, c_y, 0), longueur, col1, col2, col3, deformation, centre, rayon)
            while c_x <= sup_droit:
                c_x += 3 * longueur
                hexagone(t, (c_x, c_y, 0), longueur, col1, col2, col3, deformation, centre, rayon)
            c_y = c_y + (longueur * sin(2 * pi / 3))  # décalage d'un hexagone vers le haut en ordonnée

        t.update()  # mise à jour du dessin
    else:
        print("Pavage impossible à réaliser dans cette fenêtre de visualisation : du coin inférieur gauche " +
              str((inf_gauche, inf_gauche)) + " au coin supérieur droit " + str((sup_droit, sup_droit)))


# Programme principal appelé si l'on exécute directement ce script en ligne de commande depuis un terminal,
# ou encore via PyCharm (cf. ci-après), ou bien si l'on fait appel à projetVasarely.main() dans un autre script
def main():
    """
        Code qui produit tout d'abord un tableau d’art optique représentant un pavage hexagonal, vu d’en haut
            (par projection orthogonale sur les axes x, y (z = 0)), formé avec des losanges de couleurs différentes,
             puis un second tableau représentant ce même pavage déformé par une boule qui en sort (ou y rentre),
             et qui sauvegarde ces dessins dans des fichiers postscript (de suffixe eps).

        Aucune entrée.
        Résultat : None
    """
    if len(sys.argv) == 11:
        # si l'on exécute directement ce script en ligne de commande depuis un terminal avec dix arguments
        # (séparés par des espaces) "python projetVasarely.py v1 ... v10", on récupère les arguments de la commande pour
        # initialiser les valeurs de tous les paramètres inf_gauche, sup_droit, longueur, col1, col2, col3, centre, r
        # (où centre = (centre_x, centre_y, centre_z)) après contrôle de leurs type et nombre
        # sys.argv inclut le nom du programme "projetVasarely.py" en position 0
        inf_gauche, sup_droit, longueur, col1, col2, col3, centre, r = (
            controle_nb_valeurs_typees(sys.argv[1], 1, int, "les coordonnées du bord inférieur gauche de la fenêtre de \
visualisation (une seule valeur entière commune à x_inf_gauche et y_inf_gauche)"),
            controle_nb_valeurs_typees(sys.argv[2], 1, int, "les coordonnées du bord supérieur droit de la fenêtre de \
visualisation (une seule valeur entière commune à x_sup_droit et y_sup_droit)"),
            controle_nb_valeurs_typees(sys.argv[3], 1, int, "la longueur d’un segment de pavé (avant déformation) \
(une valeur entière)"),
            controle_nb_valeurs_typees(sys.argv[4], 1, invite="la couleur des pavés Nord-Est (en haut à droite de \
chaque hexagone) (une chaîne de caractères)"),
            controle_nb_valeurs_typees(sys.argv[5], 1, invite="la couleur des pavés Ouest (à gauche de chaque hexagone)\
 (une chaîne de caractères)"),
            controle_nb_valeurs_typees(sys.argv[6], 1, invite="la couleur des pavés Sud-Est (en bas à droite de chaque\
 hexagone) (une chaîne de caractères)"),
            controle_nb_valeurs_typees((sys.argv[7], sys.argv[8], sys.argv[9]), 3, int, "les coordonnées du centre de \
la sphère déformante (trois entiers séparés chacun par un espace pour centre_x, centre_y et centre_z)"),
            controle_nb_valeurs_typees(sys.argv[10], 1, int, "le rayon de la sphère déformante (une valeur entière)"))
    else:
        # si l'on exécute directement ce script via PyCharm, ou bien si l'on fait appel à projetVasarely.main() dans
        # un autre script où l'on a importé turtle, deformation et projetVasarely, et préalablement défini les valeurs
        # de tous les paramètres (inf_gauche, sup_droit, longueur, col1, col2, col3, centre, r), il n'est
        # pas nécessaire de redemander ces valeurs à l'utilisateur
        if 'rayon' in globals():
            r = eval('rayon')  # j'ai remarqué dans les exemples de résultats que rayon était parfois utilisé pour r
        if 'inf_gauche' in globals() and 'sup_droit' in globals() and 'longueur' in globals() and 'col1' in globals()\
                and 'col2' in globals() and 'col3' in globals() and 'centre' in globals() and 'r' in globals():
            inf_gauche, sup_droit, longueur, col1, col2, col3, centre, r = (eval('inf_gauche'), eval('sup_droit'),
                                                                            eval('longueur'), eval('col1'),
                                                                            eval('col2'), eval('col3'),
                                                                            eval('centre'), eval('r'))
        else:
            # Demande à l’utilisateur les paramètres (couleurs, longueur des segments, …) du pavage qu'il désire
            inf_gauche, sup_droit, longueur, col1, col2, col3, centre, r = lecture_données_utilisateur()

    # Dessine un premier pavage sans déformation et le sauvegarde dans le fichier postscript "pavage_initial.eps"
    turtle.title("Pavage Vasarely initial")
    pavage(turtle, inf_gauche, sup_droit, longueur, col1, col2, col3, aucune_deformation, centre, r)
    turtle.getcanvas().postscript(file="pavage_initial.eps")
    # Efface ce dessin, puis dessine un second pavage avec déformation et le sauvegarde
    # dans le fichier "pavage_deforme.eps"
    time.sleep(1)  # attend 1 seconde
    turtle.title("Pavage Vasarely après déformation")
    pavage(turtle, inf_gauche, sup_droit, longueur, col1, col2, col3, deformation, centre, r)
    turtle.getcanvas().postscript(file="pavage_deforme.eps")
    turtle.done()  # attend que l'utilisateur ferme la fenêtre


if __name__ == "__main__":
    # si l'on exécute directement ce script via PyCharm, ou bien en ligne de commande depuis un terminal
    main()


# Si l'on appelle directement projetVasarely.pavage(turtle, inf_gauche, sup_droit, longueur, col1, col2, col3,
# deformation, centre, r) dans un script où l'on a importé turtle, deformation et projetVasarely, et préalablement
# défini les valeurs de tous les paramètres (inf_gauche, sup_droit, longueur, col1, col2, col3, centre, r), il n'est
# pas nécessaire de redemander ces valeurs à l'utilisateur
