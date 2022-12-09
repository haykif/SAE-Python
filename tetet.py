def appelExtractionVilles():
    print("Extraction des informations des Villes de France")
    listeVillesFr = lire_fichier_csv("villes_france.csv")
    print("une ligne = ",listeVillesFr[0])

def lire_fichier_csv(nomFich):
    """
    Cette fonction permet de LIRE les données du fichier villes_france.csv
    le fait d'utiliser readlines permet de récupérer une liste dont chaque élément correspond à une ville
    ainsi que toutes les données associées
    :param nomFich: fichier "villes_france.csv"
    :return: une liste "liste_villes" dont chaque élément est une str qui comporte toutes les données d'une ville
    (27 données par ville au total)
    """
    fich = open(nomFich,'r')
    liste_villes = fich.readlines()

    print("Fin de l'Extraction des infos du fichier",nomFich)
    fich.close()
    return liste_villes
    
l01 = ["75","77","78","91","92","93","94","95"]
l02 = ["14","18","22","27","28","29","35","36","37","41","44","45","49","50","53","56","61","72","76","85","974","976"]
l03 = ["02","08","10","21","25","39","51","52","54","55","57","58","59","60","62","67","68","70","71","80","88","89","90"]
l04 = ["01","03","04","05","06","07","11","13","15","2A","2B","26","30","34","38","42","43","48","63","66","69","73","74","83","84"]
l05 = ["09","12","16","17","19","23","24","31","32","33","40","46","47","64","65","79","81","82","86","87","971","972","973","975","977","978"] 
    
indTel = l01 + l02 + l03 + l04 + l05
print(indTel)
elt = indTel[31]
print(indTel.count(elt))