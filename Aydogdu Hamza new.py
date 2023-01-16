import folium, branca
import matplotlib.pyplot as plt
import math


# -----------------------------------------------------------
# Fonction qui extrait les 12 informations sur chaque ville
# -----------------------------------------------------------

def lire_fichier_csv(nomFich):
    """
    Cette fonction permet de LIRE les données du fichier villes_france.csv
    le fait d'utiliser readlines permet de récupérer une liste dont chaque élément correspond à une ville
    ainsi que toutes les données associées
    :param nomFich: fichier "villes_france.csv"
    :return: une liste "liste_villes" dont chaque élément est une str qui comporte toutes les données d'une ville
    (27 données par ville au total)
    """
    f = open(nomFich, 'r')
    liste_villes = f.readlines()

    print("Fin de l'Extraction des infos du fichier", nomFich)
    f.close()
    return liste_villes


def extract_info_villes(uneListe):
    """
    Fonction qui extrait les 12 informations de la liste[str] extraite du fichier Excel
    :param : uneListe:
    :return: L: une liste dont chaque élément contient les 12 infos de la ville
    la taille de la liste L[] retournée est de 36700 villes
    """
    L = []
    temp = []
    for i in uneListe:
        temp.append(i.split(','))
    print("taille = ", len(temp))

    """
    Il faut faire attention aux Départements de Corse : 2A et 2B
    et également aux département d'Outre-Mer : 971, 972, ...,977
    """
    for i in temp:
        # eval(..) transforme "Annecy" en Annecy, et "18.59" en 18.59 donc une chaîne de caractères sans les "..."
        # ensuite il faut transformer le type str() en int() ou float()
        # Pour tous les départements sauf la Corse 2A et 2B
        # et les territoires d'Outre-Mer : les derniers champs sont à 'NULL'
        if ((eval(i[1]) != '2A') and (eval(i[1]) != '2B')) and i[25] != 'NULL':
            L.append([int(eval(i[1])),  # numéro du Département
                      eval(i[3]),  # Nom de la ville en MAJUSCULE
                      eval(i[8]),  # Code postal
                      int(eval(i[14])),  # population en 2010
                      int(eval(i[15])),  # population en 1999
                      int(eval(i[16])),  # population en 2012
                      float(eval(i[17])),  # densité
                      float(eval(i[18])),  # surface
                      float(eval(i[19])),  # longitude
                      float(eval(i[20])),  # latitude
                      int(eval(i[25])),  # altitude min
                      int(eval(i[26]))])  # altitude max
        elif i[13] == 'NULL':  # pour gérer les départements et territoires d'Outre-Mer : 971, 972, 974, ...
            L.append([int(eval(i[1])),
                      eval(i[3]),
                      eval(i[8]),
                      int(eval(i[14])),
                      int(eval(i[15])),
                      int(eval(i[16])),
                      float(eval(i[17])),
                      float(eval(i[18])),
                      float(eval(i[19])),
                      float(eval(i[20])),
                      "NULL",
                      "NULL"])
        else:
            L.append([eval(i[1]),
                      eval(i[3]),
                      eval(i[8]),
                      int(eval(i[14])),
                      int(eval(i[15])),
                      int(eval(i[16])),
                      float(eval(i[17])),
                      float(eval(i[18])),
                      float(eval(i[19])),
                      float(eval(i[20])),
                      i[25],
                      i[26]])

    return L


# ====================================================================
# Compte le Nombre de villes en fonction de l'indicatif téléphonique
# ====================================================================
def appelNombre_Villes_Indicatif(indTel, unelisteInfo):
    """
        Cette fonction permet d'appeler toutes les villes (et les informations qui les concernent)
        de tout les département de la France ayant le même indicatif téléphonique.
    """
    id01 = [[75, 77, 78, 91, 92, 93, 94, 95],
            [14, 18, 22, 27, 28, 29, 35, 36, 37, 41, 44, 45, 49, 50, 53, 56, 61, 72, 76, 85, 974, 976],
            [2, 8, 10, 21, 25, 39, 51, 52, 54, 55, 57, 58, 59, 60, 62, 67, 68, 70, 71, 80, 88, 89, 90],
            [1, 3, 4, 5, 6, 7, 11, 13, 15, "2A", "2B", 26, 30, 34, 38, 42, 43, 48, 63, 66, 69, 73, 74, 83, 84],
            [9, 12, 16, 17, 19, 23, 24, 31, 32, 33, 40, 46, 47, 64, 65, 79, 81, 82, 86, 87, 971, 972, 973, 975, 977,
             978]]
    indicatif = id01[int(indTel) - 1]
    cpt = 0

    for i in range(0, len(unelisteInfo)):
        for j in range(0, len(indicatif)):
            if indicatif[j] == unelisteInfo[i][0]:
                cpt += 1
    print(cpt)


# --------------------------------------------------------
# Fonction extract_villes_depart_indicatif(listeInfo)
# --------------------------------------------------------
def extract_villes_depart_indicatif(listeDept, unelisteInfo):
    """
    Fonction qui extrait l'ensemble des villes pour chaque département,
    en fonction de l'indicatif téléphonique (01 = Île-de-France, 02 = Nord-Ouest, ...

    :param listeDept: qui est la liste des départements ayant cet indicatif
    :param listeInfo: liste des noms de villes
    :return: nbVilles = nombre de villes
    """

    cpt = 0
    nomFichier = "NE03.txt"
    f = open(nomFichier, "w")
    f = open(nomFichier, "a")
    for i in range(0, len(unelisteInfo)):
        for j in range(0, len(listeDept)):
            if listeDept[j] == unelisteInfo[i][0]:
                cpt += 1
                f.write(str(cpt) + " " + str(unelisteInfo[i][1]) + " " + "(" + str(listeDept[j]) + ")" + "\n")
    return cpt


# --------------------------------------------------------
# Procédure qui permet d'appeler la fonction
# qui extrait les informations sur les villes
# ---------------------------------------------------------
def appelExtractionVilles():
    print("Extraction des informations des Villes de France")
    listeVillesFr = lire_fichier_csv("villes_france.csv")
    print("une ligne = ", listeVillesFr[0])

    # la liste info contient les 12 Informations retenues pour la suite du programme
    info = extract_info_villes(listeVillesFr)

    return info


# ==========================================================
# Recherche les infos d'une Ville dans la liste
# ==========================================================
def rechercheVille(name, listeVilles):
    """

    :param name: nom de la ville recherchée doit être en MAJUSCULE
    :param listeVilles: liste de toutes les villes
    :return: listeVilles[i] : la ville recherchée
    """


"""
    A compléter
"""


# --------------------------------------------------------
# Fonction extract_villes_depart_indicatif(listeInfo)
# --------------------------------------------------------
def extract_villes_NumDepart(numDept, listeVilles):
    """
    Fonction qui extrait l'ensemble des villes pour chaque département,
    en fonction du numéro du Département

    :param numDept: numéro du département
    :param listeVilles: liste des noms de villes
    :return: nbVilles = nombre de villes du département
    """
    cpt = 0
    nomFich = "Ville_du_Département " + str(numDept)
    f = open(nomFich, "w")
    for i in range(0, len(listeVilles)):
        if str(numDept) == str(listeVilles[i][0]):
            f.write(str(listeVilles[i]))

            cpt += 1
    f.write("fin")
    return cpt
# ================================================
# Fonctions Utiles pour le Tri Bulle lié à la POPULATION
# ================================================


def MinMax5_villes_Habitants(lstVillesDepart):
    """

    :param numDept:
    :param lstVillesDepart:

        recherche de 5 villes ayant le MOINS d'habitants dans un tableau
        recherche de 5 villes ayant le PLUS d'habitants dans un tableau
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 5 premières valeurs
    """


    f = open("ville5Min_8.txt", "w")
    f2 = open("ville5Max_8.txt", "w")
    echange = 1
    ville_du_département = []
    for i in range(0, len(lstVillesDepart)):
        if lstVillesDepart[i][0] == 8:
            ville_du_département.append(lstVillesDepart[i])
    print(ville_du_département)
    while echange != 0:

        echange = 0

        for i in range(0, len(ville_du_département) - 1):
            i1 = ville_du_département[i][3]
            i2 = ville_du_département[i + 1][3]
            if i1 > i2:
                ville_du_département[i], ville_du_département[i + 1] = ville_du_département[i + 1], ville_du_département[i]
                echange = 1


    for i in range(0, 5):
        f.write(str(ville_du_département[i]) + "\n")
    for i in range(1,6):
        f2.write(str(ville_du_département[-i]) +"\n")




# -------------------------------------------------------------------------
# Procédure qui permet d'afficher sur une carte OpenStreetMap
# les 10 villes (5 ayant la population MAX, et 5 ayant la population MIN)
# -------------------------------------------------------------------------
def mapTenVilles(maxPopul, minPopul):
    """

    :param maxPop: fichier contenant les 5 villes de forte densité
    :param minPop: fichier contenant les 5 villes de faible densité
    :return:
    """
    Min = open(minPopul,'r')
    Max = open(maxPopul,'r')
    listeMin = []
    listMax = []
    for i in range (0,5):
        listeMin.append(Min.readlines()[i].split(','))
        listMax.append(Max.readlines()[i].split(','))



    """
        A compléter
    """


def MinMax10Accroissement(lstVillesDepart):
    """
    :param lstVillesDepart:

        recherche de 10 villes ayant la plus FORTE BAISSE de sa population entre 1999 et 2012
        recherche de 10 villes ayant le plus FORT ACCROISSEMENT de sa population entre 1999 et 2012
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 10 premières valeurs et 10 dernières valeurs
    """


"""
    A compléter
"""


def MinMax5Alt_Dept(lstVillesDepart):
    """
    :param lstVillesDepart:

        recherche de 5 villes ayant la plus FAIBLE différence d'altitude dans un tableau
        recherche de 5 villes ayant la plus FORTE différence d'altitude dans un tableau
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 5 premières valeurs
        Numéro du département = lstVillesDepart[0][0]
    """


"""
    A compléter
"""


# -------------------------------------------------------------------------
# Procédure qui permet d'afficher sur une carte OpenStreetMap
# les 10 villes (5 ayant la différence d'ALTITUDE MAX
# et 5 ayant la différence d'ALTITUDE MIN)
# -------------------------------------------------------------------------
def mapTenAlt(maxAlt, minAlt):
    """

    :param maxAlt: fichier contenant les 5 villes de forte différence d'altitude
    :param minAlt: fichier contenant les 5 villes de faible différence d'altitude
    :return:
    """

    """
        A compléter
    """


# ===================================================================
# Construction de l'HISTOGRAMME
# ===================================================================
def traceHistoVilles(lstVillesDepart):
    """
        A compléter
    """


# ====================================================================
# Distance EUCLIDIENNE entre 2 villes (en km)
# ====================================================================
def dist_Euclidienne(ville1, ville2):
    # Méthode par le calcul de Pythagore
    """
        A compléter
    """


# ====================================================================
# Distance GEODESIQUE (surface de la terre) entre 2 villes (en km)
# Formule de Haversine
# ====================================================================
def dist_GEOdesique(ville1, ville2):
    # calcul par la méthode HAVERSINE
    """
        A compléter
    """


# ===============================================================
# ETAPE 5 : Parcours Ville1 ==> Ville2
# ===============================================================

# =================================================================
# Recherche un ensemble de villes distante de R km dans une liste
# =================================================================
def ensembleVilles(name, rayon, listeVilles):
    """

    :param name: centre = ville avec les 12 infos
    :param rayon: distance de la ville retenue
    :param listeVilles: liste de toutes les villes
    :return: listeVilles[i] : la ville recherchée
    """

    """
        A compléter
    """


# ===================================================================
# ETAPE 5 : Plus court chemin entre les 2 Villes vil1 et vil2
# ===================================================================
def parcoursVilles(vil1, vil2, listeRef, rayon):
    """
        A compléter
    """


# ----------------------------------------------------------------------------------
# On sauvegarde le trajet dans un fichier html pour l'afficher dans un navigateur
# ----------------------------------------------------------------------------------
def map_trajet(villes_traversees):
    """
        A compléter
    """


# ===============================================================
# AFFICHE MENU
# ===============================================================

def afficheMENU():
    print("\n================ MENU ==================")
    print("taper 1: Nombre de villes en fonction de l'indicatif téléphonique")
    print("taper 2: Extraire des Statistiques des Villes d’un département")
    print("taper 3: Distance Euclidienne et Géodésique entre 2 villes")
    print("taper 4: Plus court chemin entre 2 villes")
    print("F: pour finir")


def afficheSOUS_MENU(unDepartement):
    print("\n================ SOUS MENU : STATISTIQUES du Département ", unDepartement, "==================")
    print("taper 1: Lister les 5 Villes ayant le plus/le moins d'habitants")
    print("taper 2: Afficher les 10 Villes en fonction de la DENSITE sur une carte")
    print("taper 3: Lister les 10 Villes ayant le plus fort/faible taux d'accroissement")
    print("taper 4: HISTOGRAMME des villes par habitants")
    print("taper 5: Lister les 5 Villes ayant la différence d'altitude max/min")
    print("taper 6: Afficher les 10 Villes en fonction de l'ALTITUDE sur une carte")
    print("Q: pour Quitter le sous-menu")


# =============================================================================================
# Programme principal
# Appel de la procédure afficheMENU()
# =============================================================================================
fini = False
while fini == False:
    afficheMENU()
    choix = input("votre choix: ")
    listeInfo = appelExtractionVilles()

    nombre = extract_villes_NumDepart(8, listeInfo)
    print("il y a ", nombre, "ville")
    MinMax5_villes_Habitants(listeInfo)
    if choix == '1':
        # Pour débuter il faut extraire des informations du fichier CSV1

        # =====================================
        id = input("\nEntrez l'indicatif téléphonique: ")

        res = appelNombre_Villes_Indicatif(id, listeInfo)
        listedepartement = [2, 8, 10, 21, 25, 39, 51, 52, 54, 55, 57, 58, 59, 60, 62, 67, 68, 70, 71, 80, 88, 89, 90]
        extract_villes_depart_indicatif(listedepartement, listeInfo)
    elif choix == '2':
        print("\n**** Nombre de Villes par Département *****")
        print("A compléter")
        # =====================================
        finiBis = False
        while finiBis == False:
            # ==> Changer le numéro du Département <==
            afficheSOUS_MENU(74)
            choixBis = input("votre choix: ")
            if choixBis == '1':
                print("\nappel de la stat1 : Min/Max Habitants : 5 villes\n")

            elif choixBis == '2':
                print("\nappel de la stat2: Afficher les 10 villes (DENSITE) sur la carte\n")
                """
                    A compléter
                """
            elif choixBis == '3':
                print("\nappel de la stat3: ACCROISSEMENT/BAISSE population entre 1999 et 2012\n")
                """
                    A compléter
                """
            elif choixBis == '4':
                print("\nappel de la stat4 : HISTOGRAMME du nombre des Villes par habitants\n")
                """
                    A compléter
                """
            elif choixBis == '5':
                print("\nappel de la stat5 : ALTITUDE Min/Max : 5 villes\n")
                """
                    A compléter
                """
            elif choixBis == '6':
                print("\nappel de la stat6: Afficher les 10 villes (ALTITUDE) sur la carte\n")
                """
                    A compléter
                """
            else:
                finiBis = True
    elif choix == '3':
        print("\nDistance Euclidienne entre 2 villes")
        """
            A compléter
        """

        print("\nDistance Géodésique entre 2 villes")
        """
            A compléter
        """
    elif choix == '4':
        print("\nPLus court chemine entre 2 villes")
        """
            A compléter
        """
        print("*** Traitement terminé, Map réalisée ****")
    elif choix == '5':
        print("\nAppel de la fonction4\n")
    elif choix == 'F':
        fini = True

print("Fin du programme")
