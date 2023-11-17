import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
#Étape 1 Fonction - Retourne dictionnaire
def function1(text):
    mots = text.lower().split()
    occurrences = {}
    for mot in mots:
        if mot in occurrences:
            occurrences[mot] += 1
        else:
            occurrences[mot] = 1
    occurrences_trie = sorted(occurrences.items(), key=lambda item: item[1], reverse=True)
    return occurrences_trie

texte = "La nature est pleine de beauté. Les arbres, les fleurs, les rivières et les montagnes offrent une diversité incroyable. La beauté de la nature est source d'inspiration pour de nombreux artistes. Admirer un coucher de soleil ou écouter le chant des oiseaux procure un sentiment de paix et d'harmonie avec l'environnement."

resultat1 = function1(texte)

#Étape 2 Fonction - Structure de données privées des mots de la liste parasite
def filtrer_mots_parasites(donnée_text, mots_parasites):
    mots_filtrés = {}
    for mot, occurrences in donnée_text:
        if mot not in mots_parasites:
            mots_filtrés[mot] = occurrences
    return mots_filtrés
mots_parasites = ["de", "pour", "mais", "le", "la", "les", "est","et", "un","une"]

resultat2 = filtrer_mots_parasites(resultat1, mots_parasites)

#Étape 3 Fonction - Récupèration des mots parasites dans un fichier parasite.csv
def recuperer_mots_parasites_from_csv(parasite_file_path):
    mots_parasites = []
    with open(parasite_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            mots_parasites.extend(row)
    return mots_parasites

parasite_file_path = "parasite.csv"
mots_parasites_du_texte = recuperer_mots_parasites_from_csv(parasite_file_path)

# Étape 4: Teste code
#** Étape 1: Obtenez les occurrences des mots
resultat1 = function1(texte)
print("Étape 1 - Occurrences des mots:")
print(resultat1)

#** Étape 2: Filtrez les mots parasites
resultat2 = filtrer_mots_parasites(resultat1, mots_parasites)
print("\nÉtape 3 - Mots filtrés:")
print(resultat2)

#** Étape 3: Récupérez les mots parasites à partir d'un fichier CSV
parasite_file_path = "parasite.csv"
resultat3 = recuperer_mots_parasites_from_csv(parasite_file_path)
print("\nÉtape 3 - fichier .csv:")
print(resultat3)

#Étape 5 Fonction - Texte sans les balises html
def retirer_balises_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    texte_sans_balises = soup.get_text(separator=' ', strip=True)
    return texte_sans_balises

# Testez la fonction avec une chaîne de caractères HTML
html_text_a_tester = """
<html>
    <head>
        <title>Page HTML de tester</title>
    </head>
    <body>
        <p>Ceci est un <b>exemple</b> de texte <a href="#">HTML</a>.</p>
        <p>Une autre ligne de texte.</p>
    </body>
</html>
"""

resultat5 = retirer_balises_html(html_text_a_tester)
print("Étape 5 - Texte sans balises HTML:")
print(resultat5)

#Étape 6 Fonction - Liste des valeurs associées aux balises
def extraire_valeurs_attribut(html_text, balise, attribut):
    valeurs = []

    # Utiliser BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html_text, 'html.parser')

    # Trouver toutes les balises correspondantes
    balises = soup.find_all(balise)

    # Extraire les valeurs de l'attribut spécifié
    for balise in balises:
        valeur = balise.get(attribut)
        if valeur:
            valeurs.append(valeur)

    return valeurs

# Testez la fonction avec une chaîne de caractères HTML
html_text_a_tester = """
<div>
<p>Voici une liste de liens : </p>
    <a href="lien1">Lien 1</a>
    <a href="lien2">Lien 2</a>
    <a href="lien3">Lien 3</a>
  <img src="image1.jpg" alt="Description image 1">
</div>
"""

balise_a_chercher = 'a'
attribut_a_extraire = 'href'

valeurs_attribut = extraire_valeurs_attribut(html_text_a_tester, balise_a_chercher, attribut_a_extraire)

print("Étape 6 - Valeurs associées aux balises:")
print(valeurs_attribut)

#Étape 7 Fonction - Récupération de toutes les valeurs des attributs alt des balises img
balise_a_chercher = 'img'
attribut_a_extraire = 'alt'

valeurs_attribut = extraire_valeurs_attribut(html_text_a_tester, balise_a_chercher, attribut_a_extraire)

print("Étape 7 - Valeurs associées aux balises img:")
print(valeurs_attribut)

#Étape 8 Fonction - Extraire le nom de domaine
def extraire_nom_domaine(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

# Testez la fonction avec une URL
url_a_tester = "https://www.leboncoin.fr/offre/voitures/2444688350"
nom_domaine = extraire_nom_domaine(url_a_tester)

print("Étape 8 - Nom de domaine extrait de l'URL:")
print(nom_domaine)

#Étape 9 Fonction - Listes des urls qui font partie du domaine et ceux qui n’en font pas partie
def trier_urls_par_domaine(nom_domaine, liste_urls):
    urls_du_domaine = []
    urls_pas_du_domaine = []
    for url in liste_urls:
        parsed_url = urlparse(url)
        domaine_url = parsed_url.netloc
        if domaine_url == nom_domaine:
            urls_du_domaine.append(url)
        else:
            urls_pas_du_domaine.append(url)
    return urls_du_domaine, urls_pas_du_domaine

# Teste de la fonction avec un nom de domaine et une liste d'URLs
nom_domaine_a_tester = "www.example.com"
urls_a_tester = [
    "https://www.example.com/page1",
    "https://www.example.com/page2",
    "https://www.example2.com/page3",
    "https://www.example.com/page4",
]

urls_du_domaine, urls_pas_du_domaine = trier_urls_par_domaine(nom_domaine_a_tester, urls_a_tester)

print("Étape 9 - URLs faisant partie du domaine:")
print(urls_du_domaine)

print("\nURLs ne faisant pas partie du domaine:")
print(urls_pas_du_domaine)

#Étape 10 - Texte HTML de la page
def recuperer_texte_html_depuis_url(url):
    reponse = requests.get(url)
    texte_html = reponse.text
    return texte_html

# Teste de la fonction avec une URL
url_a_tester = "https://www.jeuxvideo.com/tous-les-jeux/"
texte_html = recuperer_texte_html_depuis_url(url_a_tester)

if texte_html:
    print("Étape 10 - Texte HTML de la page:")
    print(texte_html[:500])

# Fonction pour auditer une page
def auditer_page(url, mots_parasites_file):
    texte_html = recuperer_texte_html_depuis_url(url)

    if texte_html:
        balises_img_alt = extraire_valeurs_attribut(texte_html, 'img', 'alt')
        presence_balises_alt = len(balises_img_alt) > 0
        print("\nPrésence de balises alt avant suppression des balises HTML:", presence_balises_alt)

        texte_sans_balises = retirer_balises_html(texte_html)

        mots_parasites = recuperer_mots_parasites_from_csv(mots_parasites_file)

        occurrences_mots = function1(texte_sans_balises)
        print("\nMots clés avec les 3 premières valeurs d'occurrences:")
        print(occurrences_mots[:3])

        occurrences_mots_filtres = filtrer_mots_parasites(occurrences_mots, mots_parasites)
        print("\nMots clés filtrés:")
        print(occurrences_mots_filtres)

        liens = extraire_valeurs_attribut(texte_html, 'a', 'href')
        print("\nNombre de liens sortants:", len(liens))



url_a_analyser = input("Veuillez entrer l'URL de la page à analyser : ")

mots_parasites_file = "parasite.csv"
auditer_page(url_a_analyser, mots_parasites_file)



