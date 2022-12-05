import csv
import math
import numpy as np
import branca
import folium
import matplotlib.pyplot as plt
from enum import Enum

# Variables

indexes = [1, 3, 8, 14, 15, 16, 17, 18, 19, 20, 25, 26]
liste_departs_04 = ['01', '03', '04', '05', '06', '07', '11', '13', '15', '2A', '2B', '26', '30', '34', '38', '42',
                    '43', '48',
                    '63', '66', '69', '73', '74', '83', '84']

# Index des elements que l'on traitera
""" useful column ids
departement     01
nom             03
code_postal     08

population_2010 14
population_1999 15
population_2012 16

densite_2010    17
surface         18

longitude_deg   19
latitude_deg    20

zmin            25
zmax            26
"""


# Functions

# Partie 1.1 & 1.2
def menu():
    print("Bienvenue !")
    print("Veuillez choisir un département: ")
    departement = str(input("\n -> "))

    # removes errors if you type 3 instead of 03 for instance
    if len(departement) == 1:
        departement = '0' + departement

    print("\nInitilisation des villes du département....")
    sorted_villes_france = extraction_villes_csv('villes_france.csv')
    fichier_ville = extract_villes_NumDepart(sorted_villes_france, departement, "villes_" + departement + ".txt")
    print("Fichier ville créé !")

    print("\nVeuillez choisir la tâche à réaliser: ")
    print("(- Extraire les villes du fichier | 1)")
    print("- Extraire des statistiques sur les villes d'un département | 2")
    print("- Calculer la distance entre deux villes | 3")
    print("- Déterminer le plus court chemin | 4")
    print("- Extraire les villes ayant l'indicatif téléphonique 04 | 5")
    print("- Déterminer le plus court chemin en passant par les plus grandes villes | 6")
    task = 0
    while not 1 <= task <= 6:
        try:
            task = int(input("\n-> "))
        except:
            print("Veuillez entrer une valeur comprise entre 1 et 6.")

    print("Tâche", task, "sélectionnée")

    # Task 1 is useless because ran during init
    if task == 1:
        extraction_villes_csv('villes_france.csv')
    elif task == 5:
        extract_villes_depart_indicatif(sorted_villes_france)
    elif task == 3:
        print("\nEntrez le nom de la ville 1")
        nom_ville1 = str(input("-> "))
        ville1 = rechercheVille(nom_ville1)
        print("\nEntrez le nom de la ville 2")
        nom_ville2 = str(input("-> "))
        ville2 = rechercheVille(nom_ville2)
        secondary_task = 0
        print("\nChoisissez le type de distance à calculer: ")
        print("- Distance euclidienne | 1")
        print("- Distance géodésique | 2")
        print("- Distance géodésique & euclidienne | 3")
        while not 1 <= secondary_task <= 3:
            try:
                secondary_task = int(input("\n-> "))
            except:
                print("Veuillez entrer une valeur comprise entre 1 et 3.")
        if secondary_task == 1:
            print(dist_Euclidienne(ville1, ville2), "kilomètres")
        elif secondary_task == 2:
            print(dist_Geodesique(ville1, ville2), "kilomètres")
        else:
            print("Géodésique:", dist_Geodesique(ville1, ville2), "mètres")
            print("Euclidienne:", dist_Euclidienne(ville1, ville2), "mètres")
    elif task == 2:
        secondary_task = 0
        print("\nVeuillez choisir la tâche secondaire à réaliser: ")
        print("- Les 10 villes avec le PLUS / MOINS d'habitants | 1")
        print("- Afficher une carte exposant les densités des villes | 2")
        print("- Les 10 villes avec le plus FORT / FAIBLE accroissement de leur population entre 1999 & 2012 | 3")
        print("- Afficher une carte exposant les différences d'altitudes des villes | 4")
        print("- Visualiser un histogramme | 5")

        while not 1 <= secondary_task <= 6:
            try:
                secondary_task = int(input("\n-> "))
            except:
                print("Veuillez entrer une valeur comprise entre 1 et 6.")
        if secondary_task == 1:
            Max5Villes_Habitants(fichier_ville.name, "Top5Villes_" + departement + ".txt")
            Min5Villes_Habitants(fichier_ville.name, "Min5Villes_" + departement + ".txt")
            print("Fichiers créés avec succès")
        elif secondary_task == 2:
            villes_max_densite = Max5VillesDens(fichier_ville.name, "Top5VillesDens_" + departement + ".txt")
            villes_min_densite = Min5VillesDens(fichier_ville.name, "Min5VillesDens_" + departement + ".txt")
            liste_villes_densite = villes_min_densite + villes_max_densite
            mapTenVille(liste_villes_densite)
            print("La carte des densités a été enregistrée au format HTML")
        elif secondary_task == 3:
            TopAcc10Villes(fichier_ville.name, "TopAcc10Villes_" + departement + ".txt")
            TopBaisse10Villes(fichier_ville.name, "TopBaisse10Villes_" + departement + ".txt")
            print("Fichiers créés avec succès")
        elif secondary_task == 4:
            villes_max_diff_alt = Max5Alt_Dept(fichier_ville.name, "Top5Alt_" + departement + ".txt")
            villes_min_diff_alt = Min5Alt_Dept(fichier_ville.name, "Min5Alt_" + departement + ".txt")
            liste_alt = villes_min_diff_alt + villes_max_diff_alt
            mapTenAlt(liste_alt)
            print("La carte des différences d'altitudes a été enregistrée au format HTML")
        elif secondary_task == 5:
            traceHistoVille(fichier_ville.name, "histogramme.png")
    elif task == 4:
        print("\nEntrez le nom de la ville 1")
        nom_ville1 = str(input("-> "))
        print("\nEntrez le nom de la ville 2")
        nom_ville2 = str(input("-> "))
        ville1 = rechercheVille(nom_ville1)
        ville2 = rechercheVille(nom_ville2)
        map_crossed_cities(gps_direction(ville1, ville2))
    elif task == 6:
        print("\nEntrez le nom de la ville 1")
        nom_ville1 = str(input("-> "))
        print("\nEntrez le nom de la ville 2")
        nom_ville2 = str(input("-> "))
        ville1 = rechercheVille(nom_ville1)
        ville2 = rechercheVille(nom_ville2)
        map_crossed_cities(gps_direction2(ville1, ville2))


# Partie 1.3
def extraction_villes_csv(fichier):
    """
    Creates a file of all the cities contained in a .csv file with only useful columns
    :param fichier: .csv file
    :return: list of all the cities in the .csv file with useful columns only
    """
    fichier = open(fichier)
    csvreader = csv.reader(fichier)
    liste_villes = []
    for row in csvreader:
        liste_villes.append(row)
    fichier.close()
    liste_villes = extract_infos_villes(liste_villes, indexes)
    save_list_to_file("sorted_villes_france.txt", liste_villes)
    return liste_villes


# Partie 1.4
def extract_infos_villes(uneListe, index_to_keep):
    """
    Allows to remove specific columns in a list
    :param uneListe: initial list
    :param index_to_keep: list of indexes of columns to keep
    :return: list with columns removed
    """
    city_stats_extracted = []
    for row in uneListe:
        deleted = 0
        for i in range(len(row)):
            if i not in index_to_keep:
                row.pop(i - deleted)
                deleted += 1
        city_stats_extracted.append(row)
    return city_stats_extracted


# Partie 1.5
def extract_villes_depart_indicatif(uneListe):
    """
    Save to a file all the cities using 04 as telephone code
    :param uneListe: list of cities
    :return: number of cities and file
    """
    listVilles04 = []
    f = open("SE04.txt", "w+")
    for ville in uneListe:
        if ville[CityAttribute.DEPARTEMENT.value] in liste_departs_04:
            listVilles04.append(ville)
            f.write(ville[CityAttribute.NAME.value] + " (" + ville[CityAttribute.DEPARTEMENT.value] + ")" + "\n")
    f.close()
    return len(listVilles04), f


# Partie 2.1
def extract_villes_NumDepart(listeVilles, departement, outputFile):
    """
    Creates a file of all the cities of a specific county
    :param listeVilles: list of cities to sort
    :param departement: county you wish to save
    :param outputFile: name of the output file
    :return: list of cities of the selected county
    """
    listvilles_departement = []
    for ville in listeVilles:
        if ville[CityAttribute.DEPARTEMENT.value] == departement:
            listvilles_departement.append(ville)
    return save_list_to_file(outputFile, listvilles_departement)


# Partie 2.2
def nombre_villes_dept(fichier):
    """
    :param fichier: file containing a list of cities
    :return: number of cities in the file
    """
    fichier = open(fichier)
    nombre_ville = len(fichier.readlines())
    fichier.close()
    return nombre_ville


# ============================
#           ETAPE 2.3
# ============================

def Max5Villes_Habitants(filename, outputFile):
    """
    Creates a file containing top5 sorted cities with greatest number of inhabitants
    :param filename: name of the file containing all the cities of a county
    :param outputFile: name of the output file
    :return: list of top5 sorted cities with greatest number of inhabitants
    """
    fichier = open(filename)
    cities = []
    for line in fichier.readlines():
        l = line.replace("[\'", "")
        l = l.replace("\']", "")
        l = l.replace("\n", "")
        l = l.replace("\", '", "', '")  # remove errors when cities use ' in name
        l = l.replace("', \"", "', '")  # remove errors when cities use ' in name
        cities.append(l.split("\', \'"))
    max_hab_city = bubblesort(cities, CityAttribute.POP_2010.value, 5, reversed=True)

    stats_list = []
    for city in max_hab_city:
        stats = "Nom: "
        stats += city[CityAttribute.NAME.value]
        stats += " - Habitants (2010): "
        stats += city[CityAttribute.POP_2010.value]
        stats += " - Superficie: "
        stats += city[CityAttribute.SURFACE.value]
        stats += " - Densite: "
        stats += city[CityAttribute.DENSITY_2010.value]
        stats_list.append(stats)

    fichier.close()
    return save_list_to_file(outputFile, stats_list)


def Min5Villes_Habitants(filename, outputFile):
    """
    Creates a file containing top5 sorted cities with lowest number of inhabitants
    :param filename: name of the file containing all the cities of a county
    :param outputFile: name of the output file
    :return: list of top5 sorted cities with lowest number of inhabitants
    """
    fichier = open(filename, "r")
    cities = []
    for line in fichier.readlines():
        l = line.replace("[\'", "")
        l = l.replace("\']", "")
        l = l.replace("\n", "")
        l = l.replace("\", '", "', '")  # remove errors when cities use ' in name
        l = l.replace("', \"", "', '")  # remove errors when cities use ' in name
        cities.append(l.split("\', \'"))
    min_hab_city = bubblesort(cities, CityAttribute.POP_2010.value, 5, reversed=False)

    stats_list = []
    for city in min_hab_city:
        stats = "Nom: "
        stats += city[CityAttribute.NAME.value]
        stats += " - Habitants (2010): "
        stats += city[CityAttribute.POP_2010.value]
        stats += " - Superficie: "
        stats += city[CityAttribute.SURFACE.value]
        stats += " - Densite: "
        stats += city[CityAttribute.DENSITY_2010.value]
        stats_list.append(stats)

    fichier.close()
    return save_list_to_file(outputFile, stats_list)


def Max5VillesDens(filename, outputFile):
    """
    Creates a file containing the top5 cities with greatest density
    :param filename: name of the file containing all the cities in a county
    :param outputFile: output file name
    :return: sorted list a cities with greatest density
    """
    cities = put_file_in_list(filename)
    villes_max_densite = bubblesort(cities, CityAttribute.DENSITY_2010.value, 5, reversed=True)

    stats_list = []
    for city in villes_max_densite:
        stats = "Nom: "
        stats += city[CityAttribute.NAME.value]
        stats += " - Habitants (2010): "
        stats += city[CityAttribute.POP_2010.value]
        stats += " - Densite (2010): "
        stats += city[CityAttribute.DENSITY_2010.value]
        stats += " - Superficie: "
        stats += city[CityAttribute.SURFACE.value]
        stats_list.append(stats)

    save_list_to_file(outputFile, stats_list)
    return villes_max_densite


def Min5VillesDens(filename, outputFile):
    """
    Creates a file containing the top5 cities with lowest density
    :param filename: name of the file containing all the cities in a county
    :param outputFile: output file name
    :return: sorted list a cities with lowest density
    """
    cities = put_file_in_list(filename)
    villes_min_densite = bubblesort(cities, CityAttribute.DENSITY_2010.value, 5, reversed=False)

    stats_list = []
    for city in villes_min_densite:
        stats = "Nom: "
        stats += city[CityAttribute.NAME.value]
        stats += " - Habitants (2010): "
        stats += city[CityAttribute.POP_2010.value]
        stats += " - Densite (2010): "
        stats += city[CityAttribute.DENSITY_2010.value]
        stats += " - Superficie: "
        stats += city[CityAttribute.SURFACE.value]
        stats_list.append(stats)

    save_list_to_file(outputFile, stats_list)
    return villes_min_densite


def mapTenVille(liste_villes_densite):
    """
    Draws a map of cities with greatest and lowest densities
    :param liste_villes_densite: list of top 5 cities with greatest density + list of top 5 cities with lowest density
    :return: none
    """
    liste_densite = []
    for city in liste_villes_densite:
        liste_densite.append(int(city[CityAttribute.DENSITY_2010.value]))

    coords = (
        liste_villes_densite[0][CityAttribute.LAT_DEG.value], liste_villes_densite[0][CityAttribute.LONG_DEG.value])
    map_dens = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(liste_densite), vmax=max(liste_densite))
    map_dens.add_child(cm)

    for city in liste_villes_densite:
        folium.CircleMarker(
            location=(float(city[CityAttribute.LAT_DEG.value]), float(city[CityAttribute.LONG_DEG.value])),
            radius=int(city[CityAttribute.DENSITY_2010.value]) / 400 + 5,
            color=cm(int(city[CityAttribute.DENSITY_2010.value])),
            fill=True,
            fill_color=cm(int(city[CityAttribute.DENSITY_2010.value])),
            fill_opacity=0.6,
        ).add_to(map_dens)
    map_dens.save(outfile='mapTenVille.html')


def TopAcc10Villes(fichier, outputFile):
    """
    List of top10 cities with greatest increase of its inhabitants between 2010 and 1999
    :param filename: name of the file of containing cities of a county
    :param outputFile: output file name
    :return: list of cities sorted
    """
    cities = put_file_in_list(fichier)
    villes_max_accroiss = bubblesort_compare(cities, CityAttribute.POP_2012.value, CityAttribute.POP_1999.value, 10,
                                             reversed=True)

    stats_list = []
    for city in villes_max_accroiss:
        stats = "Nom: "
        stats += city[CityAttribute.NAME.value]
        stats += " - Habitants (2012): "
        stats += city[CityAttribute.POP_2012.value]
        stats += " - Habitants (1999): "
        stats += city[CityAttribute.POP_1999.value]
        stats += " - Accroissement: "
        stats += str(int(city[CityAttribute.POP_2012.value]) - int(city[CityAttribute.POP_1999.value]))
        stats_list.append(stats)

    save_list_to_file(outputFile, stats_list)
    return villes_max_accroiss


def TopBaisse10Villes(filename, outputFile):
    """
    List of top10 cities with lowest increase of its inhabitants between 2010 and 1999
    :param filename: name of the file of containing cities of a county
    :param outputFile: output file name
    :return: list of cities sorted
    """
    cities = put_file_in_list(filename)
    villes_min_accroiss = bubblesort_compare(cities, CityAttribute.POP_2012.value, CityAttribute.POP_1999.value, 10,
                                             reversed=False)

    stats_list = []
    for city in villes_min_accroiss:
        stats = "Nom: "
        stats += city[CityAttribute.NAME.value]
        stats += " - Habitants (2012): "
        stats += city[CityAttribute.POP_2012.value]
        stats += " - Habitants (1999): "
        stats += city[CityAttribute.POP_1999.value]
        stats += " - Accroissement: "
        stats += str(int(city[CityAttribute.POP_2012.value]) - int(city[CityAttribute.POP_1999.value]))
        stats_list.append(stats)

    save_list_to_file(outputFile, stats_list)
    return villes_min_accroiss


# ============================
#           ETAPE 3
# ============================

def traceHistoVille(fichier, outputFile):
    """
    Draws a histogram of the number of cities according to the number of inhabitants
    :param fichier: name of the file containing all the cities of a county
    :param outputFile: name of the outputfile
    :return: returns a list of cities with limited parameters (name of the city and number of inhabitants in 2010)
    """
    villes = put_file_in_list(fichier)
    liste_habitants_ville = []

    for city in villes:
        liste_habitants_ville.append(int(city[CityAttribute.POP_2010.value]))
    moyenne = sum(liste_habitants_ville) / len(liste_habitants_ville)
    list_ecart_moyenne = []

    for hab in liste_habitants_ville:
        list_ecart_moyenne.append(abs(hab - moyenne) ** 2)
    ecart_type = math.sqrt(sum(list_ecart_moyenne) / len(list_ecart_moyenne))

    print("Ecart-type:", ecart_type)
    plt.hist(liste_habitants_ville, 100, histtype='bar')
    plt.ylabel('Nombre de villes')
    plt.xlabel('Habitants')
    plt.title("Nombre d'habitants par villes")
    plt.show()
    # indexes to keep
    index_to_keep = [CityAttribute.NAME.value, CityAttribute.POP_2010.value]
    return save_list_to_file(outputFile, extract_infos_villes(villes, index_to_keep))


def Max5Alt_Dept(fichier, outputFile):
    """
    Save top5 cities with greatest height difference
    :param fichier: file containing all the cities of a county (.txt)
    :param outputFile: name of the outputfile
    :return: returns the output file
    """
    cities = put_file_in_list(fichier)
    villes_max_diff_alt = bubblesort_compare(cities, CityAttribute.ZMAX.value, CityAttribute.ZMIN.value, 5,
                                             reversed=True)

    # Extract only useful stats
    stats_list = []
    for city in villes_max_diff_alt:
        stats = "Nom: "
        stats += city[CityAttribute.NAME.value]
        stats += " - Différence: "
        stats += str(int(city[CityAttribute.ZMAX.value]) - int(city[CityAttribute.ZMIN.value]))
        stats_list.append(stats)

    save_list_to_file(outputFile, stats_list)
    return villes_max_diff_alt


def Min5Alt_Dept(fichier, outputFile):
    """
    Save top5 cities with lowest height difference
    :param fichier: file containing all the cities of a county (.txt)
    :param outputFile: name of the outputfile
    :return: returns the output file
    """
    cities = put_file_in_list(fichier)
    villes_min_diff_alt = bubblesort_compare(cities, CityAttribute.ZMAX.value, CityAttribute.ZMIN.value, 5,
                                             reversed=False)

    # Extract only useful stats
    stats_list = []
    for city in villes_min_diff_alt:
        stats = "Nom: "
        stats += city[CityAttribute.NAME.value]
        stats += " - Différence: "
        stats += str(int(city[CityAttribute.ZMAX.value]) - int(city[CityAttribute.ZMIN.value]))
        stats_list.append(stats)

    save_list_to_file(outputFile, stats_list)
    return villes_min_diff_alt


# We're not using the enum here since the city columns were filtered
def mapTenAlt(diff_alt):
    """
    Draws a map of cities with the greatest and lowest height differences
    :param diff_alt: list of top5 cities with greatest height difference + top5 cities with lowest height difference
    :return: none
    """
    liste_alt = []
    for city in diff_alt:
        liste_alt.append(int(city[CityAttribute.ZMAX.value]) - int(city[CityAttribute.ZMIN.value]))

    coords = (float(diff_alt[0][CityAttribute.LAT_DEG.value]), float(diff_alt[0][CityAttribute.LONG_DEG.value]))
    map_alt = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(liste_alt),
                                        vmax=max(liste_alt))
    map_alt.add_child(cm)

    for city in diff_alt:
        diff = int(city[CityAttribute.ZMAX.value]) - int(city[CityAttribute.ZMIN.value])
        folium.CircleMarker(
            location=(float(city[CityAttribute.LAT_DEG.value]), float(city[CityAttribute.LONG_DEG.value])),
            radius=(int(city[CityAttribute.ZMAX.value]) - int(city[CityAttribute.ZMIN.value])) / 400 + 5,
            color=cm(diff),
            fill=True,
            fill_color=cm(diff),
            fill_opacity=0.6,
        ).add_to(map_alt)
    map_alt.save(outfile='mapTenAlt.html')


# ============================
#           ETAPE 4
# ============================
# Source : https://www.mathworks.com/matlabcentral/answers/519457-how-to-calculate-the-euclidean-distance-beetwen-all-points-of-latitude-longitude-pairs

# B2 = calais - toulouse (en metres)
def dist_Euclidienne(ville1, ville2):
    """
    Allows to calculate euclidian distance between two cities, with gps coordinates
    :param ville1: city1 as a list
    :param ville2: city2 as a list
    :return: distance in meters
    """
    long1 = float(ville1[CityAttribute.LONG_DEG.value]) * math.pi / 180
    long2 = float(ville2[CityAttribute.LONG_DEG.value]) * math.pi / 180
    lat1 = float(ville1[CityAttribute.LAT_DEG.value]) * math.pi / 180
    lat2 = float(ville2[CityAttribute.LAT_DEG.value]) * math.pi / 180

    deltaLat = lat2 - lat1;
    deltaLong = long2 - long1

    x = deltaLong * math.cos((lat1 + lat2) / 2);
    y = deltaLat;

    return 6371000 * math.sqrt(x * x + y * y)  # 6371000 = earth radius


def dist_Geodesique(ville1, ville2):
    """
    Allow to calculate distance between two distance, with gps cooordinates
    :param ville1: city1 as a list
    :param ville2: city2 as a list
    :return: distance in meters
    """
    long1 = float(ville1[CityAttribute.LONG_DEG.value]) * math.pi / 180
    long2 = float(ville2[CityAttribute.LONG_DEG.value]) * math.pi / 180
    lat1 = float(ville1[CityAttribute.LAT_DEG.value]) * math.pi / 180
    lat2 = float(ville2[CityAttribute.LAT_DEG.value]) * math.pi / 180

    deltaLat = lat2 - lat1
    deltaLong = long2 - long1

    a = math.sin(deltaLat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(deltaLong / 2) ** 2;
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return 6371000 * c


# ============================
#           ETAPE 5
# ============================

# Le principe de cet algorithme repose sur une boucle qui
# cherche la ville la plus proche de la ville de destination
# dans un rayon de x kilomètres autour de la ville de départ.

# Et ainsi de suite jusqu'à ce que la ville de départ se trouve être la ville de destination.
def gps_direction(ville1, ville2):
    """
    Searches all the cities crossed to travel from city1 to city2
    :param ville1: starting city
    :param ville2: target city
    :return: list of crossed cities
    """
    print("Calcul en cours...")
    crossed_cities = []
    closest_from_city2 = ville1
    # On défini la ville la plus proche de ville2 étant ville1, car c'est la seule que l'on connait pour le moment

    # Tant que la ville la plus proche de la ville cible n'est pas elle même, le programme continue (on est pas arrivé à destination)
    while closest_from_city2 != ville2:
        closest_cities_from_city1 = []
        # Cette liste contient toutes les villes dans un rayon de X mètres autour de la dernière ville trouvée.

        # Ici, on calcul la distance de toutes les villes de france à la ville en cours.
        for c in csv_cities:
            distance = math.inf
            if closest_from_city2 != c:
                distance = dist_Geodesique(c, closest_from_city2)
            # Un rayon de 10 kilomètres est recommandé. Cependant, plus celui-ci est petit,
            # plus le nombre de villes trouvées sera grand, plus le programme sera long.
            if distance < 10000:
                # On ajoute la ville seulement si elle est assez proche
                closest_cities_from_city1.append(c)

        # Cette partie du programme consiste à sélectionner la ville dans la liste de celles autour de notre ville en cours.
        # Le programme sélectionne la ville la plus proche de la ville cible, le but étant que la ville soit à la fois proche de notre dernière ville trouvée,
        # et à la fois que l'on se rapproche de notre destination.
        closest_from_city2 = closest_cities_from_city1[0]
        city_distance = dist_Geodesique(closest_cities_from_city1[0], ville2)
        for v in closest_cities_from_city1:
            distance = dist_Geodesique(v, ville2)
            if distance < city_distance:
                city_distance = distance
                closest_from_city2 = v
        crossed_cities.append(closest_from_city2)
    return crossed_cities


def gps_direction2(ville1, ville2):
    """
    Searches all the cities crossed to travel from city1 to city2
    Picking the cities with the greatest number of inhabitants in a 40km range.
    :param ville1: starting city
    :param ville2: target city
    :return: list of crossed cities
    """
    print("Calcul en cours...")
    crossed_cities = []
    closest_from_city2 = ville1

    while closest_from_city2 != ville2:
        closest_cities_from_city1 = []

        for c in csv_cities:
            if c in crossed_cities: continue;
            distance = math.inf
            if closest_from_city2 != c:
                distance = dist_Geodesique(c, closest_from_city2)
            if distance < 40000:
                closest_cities_from_city1.append(c)

        closest_cities_from_city1 = bubblesort(closest_cities_from_city1, CityAttribute.POP_2010.value,
                                               len(closest_cities_from_city1), reversed=True)
        closest_from_city2 = closest_cities_from_city1[0]
        city_distance = dist_Geodesique(closest_cities_from_city1[0], ville2)
        for v in closest_cities_from_city1:
            distance = dist_Geodesique(v, ville2)
            if distance < city_distance:
                city_distance = distance
                closest_from_city2 = v
        print(closest_from_city2)
        crossed_cities.append(closest_from_city2)
    return crossed_cities


def map_crossed_cities(villes_traversees):
    """
    Draws a map marking all the cities in a list
    :param villes_traversees: list of cities to be mapped
    :return: none
    """
    coords = (46.227638, 2.213749)
    map_cc = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=7)
    points = []
    for city in villes_traversees:
        points.append((float(city[CityAttribute.LAT_DEG.value]), float(city[CityAttribute.LONG_DEG.value])))
        folium.CircleMarker(
            location=(float(city[CityAttribute.LAT_DEG.value]), float(city[CityAttribute.LONG_DEG.value])),
            radius=8,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
        ).add_to(map_cc)
    folium.PolyLine(points).add_to(map_cc)
    map_cc.save(outfile='map_crossed_cities.html')
    print("La carte a été créée.")


# ============================
#       USEFUL FUNCTIONS
# ============================

# City name in caps lock (column 3)
def rechercheVille(cityName):
    """
    Search for a specific city in a list
    :param cityName: name of the city
    :return: returns the city
    """
    for city in csv_cities:  # cvs_cities contains all the cities
        if city[CityAttribute.NAME.value] == cityName:
            return city


def put_file_in_list(filename):
    """
    Creates a list from a file
    :param filename: name of .txt file to put in a python list
    :return: list of cities found in the input file
    """
    fichier = open(filename, "r")
    cities = []
    for line in fichier.readlines():
        l = line.replace("[\'", "")
        l = l.replace("\']", "")
        l = l.replace("\n", "")
        l = l.replace("\", '", "', '")  # remove errors when cities use ' in name
        l = l.replace("', \"", "', '")  # remove errors when cities use ' in name
        cities.append(l.split("\', \'"))
    fichier.close()
    return cities


def save_list_to_file(fileName, list):
    """
    Creates a file from a list
    :param fileName: name of the file to create
    :param list: python list to save into a file
    :return: returns the file
    """
    f = open(fileName, "w+")
    for row in list:
        f.write(str(row) + "\n")
    f.close()
    return f


def bubblesort(liste, column, top, reversed=False):
    """
    Sorts top X elements of a list depending on a specific column value
    :param liste: list to sort
    :param column: index of the column you want to sort by
    :param top: number of elements you want to return
    :param reversed: reversed returns elements starting from the greater ones
    :return: returns top X sorted elements
    """
    if reversed:
        for x in range(len(liste) - 1, 0, -1):
            for y in range(x):
                if int(liste[y][column]) < int(liste[y + 1][column]):
                    liste[y], liste[y + 1] = liste[y + 1], liste[y]

    else:
        for x in range(len(liste) - 1, 0, -1):
            for y in range(x):
                if int(liste[y][column]) > int(liste[y + 1][column]):
                    liste[y], liste[y + 1] = liste[y + 1], liste[y]
    top_liste = []

    for i in range(top):
        top_liste.append(liste[i])
    return top_liste


# Bubble sort compare is basically the same as before, but allows to sort with the difference between two columns
def bubblesort_compare(liste, column1, column2, top, reversed=False):
    """
    Allows to sort elements with the difference between column1 and column2
    :param liste: list to be sorted (column1 - column2)
    :param column1: index of column 1
    :param column2: index of column 2
    :param top: number of elements you want to sort return
    :param reversed: reversed returns elements starting from the greater ones
    :return: return top X sorted elements
    """
    if reversed:
        for x in range(len(liste) - 1, 0, -1):
            for y in range(x):
                if int(liste[y][column1]) - int(liste[y][column2]) < int(liste[y + 1][column1]) - int(
                        liste[y + 1][column2]):
                    liste[y], liste[y + 1] = liste[y + 1], liste[y]
    else:
        for x in range(len(liste) - 1, 0, -1):
            for y in range(x):
                if int(liste[y][column1]) - int(liste[y][column2]) > int(liste[y + 1][column1]) - int(
                        liste[y + 1][column2]):
                    liste[y], liste[y + 1] = liste[y + 1], liste[y]
    top_liste = []

    for i in range(top):
        top_liste.append(liste[i])
    return top_liste


# ============================

# ===============================
#               CLASS
# ===============================

# Enum class to name column indexes
class CityAttribute(Enum):
    DEPARTEMENT = 0
    NAME = 1
    ZIP_CODE = 2

    POP_2010 = 3
    POP_1999 = 4
    POP_2012 = 5

    DENSITY_2010 = 6
    SURFACE = 7

    LONG_DEG = 8
    LAT_DEG = 9

    ZMIN = 10
    ZMAX = 11


# =============================

# Run (main)

if __name__ == '__main__':
    print("Initialisation...")
    csv_cities = extraction_villes_csv('villes_france.csv')
    menu()
