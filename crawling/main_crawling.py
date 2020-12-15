# coding: utf-8

from bs4 import BeautifulSoup
import requests

def contenuHTML(url) :
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

def crawl_lemonde(url, nomClasse) :
    """
    Fonction qui récupère les liens présents dans les balises a d'une page html et enregistre dans un fichier texte le contenu de chacune des page (titre, auteur, date, contenu)
    :param url: url de la page Web à crawler
    :param nomClasse : Nom de la classe dont on veut récupérer les liens
    :return: Ne retourne rien
    """
    #Récupérer le contenu html de l'url pasré
    soup = contenuHTML(url)
    #on trouve toutes les balises a
    liens = soup.find_all("a",{'class':nomClasse})

    # Pour chaque lien on extrait titre, auteur, date, contenu
    for lien in liens :
        #Récupérer les liens des a
        lien = lien.get("href")

        #Parser le contenu du lien
        soup_liens = contenuHTML(lien)

        #Trouver le titre
        titre = (soup_liens.find("h1", {'class': 'article__title'})).string
        print(titre)
        #Trouver l'auteur
        balises_auteur = soup_liens.find("a", {'class': 'article__author-link'})
        #Traiter les cas où l'auteur n'est pas mentionné
        if balises_auteur == None :
            auteur = "Auteur inconnu"
        else :
            auteur = balises_auteur.string

        #Trouver la date
        date = (soup_liens.find("p", {'class': 'meta__publisher'})).string

        #Trouver le corps du document
        balises_contenu = soup_liens.find_all("p", {'class': 'article__paragraph'})
        contenu=""
        for paragraphe in balises_contenu:
            ###ATTENTION LE PROBLEME PEUT ETRE DU FAIT QU'IL Y A D AUTRESBALISES DANS LES PARAGRAPHES !!!!
            test = paragraphe.string
            print(test)
        print(contenu)

    #on récupère la page


if __name__ == "__main__" :
    crawl_lemonde("https://www.lemonde.fr/culture/", 'teaser__link')
