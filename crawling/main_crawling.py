# coding: utf-8

from bs4 import BeautifulSoup
import requests, os

def contenuHTML(url):
    """
    Fonction qui utilise requests pour récupérer une page, mettre son contenu dans une variable et faire une soup à l'aide de BeautifulSoup (on parse le contenu html).
    :param url: l'url de la page à parser
    :return: retourne le contenu de la page html parsé (objet de type BeautifulSoup)
    """
    # On récupère la page
    requete = requests.get(url)

    # on met son contenu dans une variable
    page = requete.content

    # On donne ce contenu à Beautiful soup pour le parser
    soup = BeautifulSoup(page)

    return soup


def crawl_lemonde(url, nomClasse):
    """
    Fonction qui récupère les liens présents dans les balises <a> d'une page html et enregistre dans un fichier texte le contenu de chacune des pages (titre, auteur, date, contenu) dans un dossier "Corpus"
    :param url: url de la page Web à crawler
    :param nomClasse : Nom de la classe (html) dont on veut récupérer les liens
    :return: Ne retourne rien
    """
    # Récupérer le contenu html de l'url passé
    soup = contenuHTML(url)
    # on trouve toutes les balises a
    liens = soup.find_all("a", {'class': nomClasse})

    #Création du dossier dans lequel on enregistrera les fichiers .txt
    try:
        os.mkdir('../Corpus')
    except:
        print("Le dossier existe déjà.")
    # Pour chaque lien on extrait titre, auteur, date, contenu et on l'enregistre dans un fichier texte dans le dossier "Corpus"
    for i in range (1,21): #Pour notre exercice on va extraire le contenu des 20 premiers liens
        #On sélectionne un lien dans la liste des liens de la page
        lien = liens[i]

        # Récupérer les liens des a
        lien = lien.get("href")

        # Parser le contenu du lien
        soup_liens = contenuHTML(lien)

        # Trouver le titre
        titre = (soup_liens.find("h1", {'class': 'article__title'})).string

        # Trouver l'auteur
        balises_auteur = soup_liens.find("a", {'class': 'article__author-link'})
        # Traiter les cas où l'auteur n'est pas mentionné
        if balises_auteur == None:
            auteur = "Auteur inconnu"
        else:
            auteur = balises_auteur.get_text().strip()

        # Trouver la date
        date = (soup_liens.find("p", {'class': 'meta__publisher'})).string
        #Dans les cas où la balise ne porte pas le même nom de classe (le monde semble avoir deux façons d'appeler les classes de date)
        if date == None :
            date = (soup_liens.find("span", {'class': 'meta__date'})).string

        # Trouver le corps du document (composé de plusieurs balises <p>)
        balises_contenu = soup_liens.find_all("p", {'class': 'article__paragraph'})
        contenu = ""
        for paragraphe in balises_contenu:
            # Extraire le texte des balises <p>
            paragraphe = paragraphe.get_text()
            # Enregistrer chaque paragraphe dans une seule variable
            contenu += "\n" + paragraphe

        #Créer le nom du fichier à partir de i (qui s'incrémente à chaque lien)
        fileName = "text" +str(i)
        i+=1

        #Ouvrir le nouveau fichier à l'aide du nom de fichier et enregistrer les informations extraites dans le fichier
        with open("../Corpus/" + fileName + ".txt", 'w', encoding="utf8") as text:
            text.write(titre + "\n" + auteur + "\n" + date + "\n" + contenu)


if __name__ == "__main__":
    crawl_lemonde("https://www.lemonde.fr/culture/", 'teaser__link')
