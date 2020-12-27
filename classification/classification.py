# coding: utf-8
import spacy, os


def tokeniser(text):
    '''
    Fonction qui prend en entrée une chaine de caractères et ressort une tokenisation du texte (utilise spacy)
    :param text: Une chaine de caractères
    :return: Liste des mots de la chaine de caractères
    '''
    # tokenisation du texte avec spacy (donne un objet créé par spacy)
    nlpFr = spacy.load('fr_core_news_md')
    words = nlpFr(text)
    # on met tous les tokens dans une liste
    listTokens = []
    for word in words:
        # normalisation du mot : passage au type string et baisse de la casse
        word = str(word).lower()
        listTokens.append(word)
    return listTokens


def chargeChampsLexicaux():
    '''
    Fonction qui permet de charger un dictionnaire des champs lexicaux des quatres thèmes : art, litterature, cinéma, musique et scène.
    Le dictionnaire se construit de cette façon : {art : {mot :""}, musique : {mot : ""}}
    :return: Retourne une table de hachage avec tous les thèmes en clé et des dictionnaires pour chaque mot composant le thème.
    '''

    champsLexicaux = {}  # Contiendra le dictionnaire des champs lexicaux des thèmes
    themes = ["art", "cinema", "litterature", "musique",
              "scenes"]  # Liste des thèmes qui nous intéressent pour lesquels nous avons une liste de mots dans des fichiers .txt
    for theme in themes:
        # On enregistre le thème en clé et on enregistrera en valeur un dictionnaire contenant chaque mot associé au thème
        champsLexicaux[theme] = {}
        # On ouvre le fichier contenant les mots
        with open(theme + ".txt", "r", encoding="utf8")as file:
            for word in file.readlines():
                # On enlève les sauts de lignes
                word = word.split("\n")[0]
                # on ajoute le mot au niveau du thème avec en valeur un blanc
                champsLexicaux[theme][word] = ""
    return champsLexicaux


def champLexTexte(textTokenise):
    '''
    Fonction qui prend en entrée un texte tokenisé, compare chaque mot avec un dictionnaire contenant les champs lexicaux des thèmes (art, musique, littérature, scene, cinéma)
    quand elle trouve un mot appartenant à un thème elle l'ajoute à un dictionnaire avec le thème en question et le nombre de fois que le mot a été trouvé pour ce thème.
    :param textTokenise: Un texte tokenisé
    :return: Un dictionnaire de la forme {mot : {thème : occurrence}}
    '''
    champLexText = {}  # contiendra le dictionnaire {mot : {thème : occurrence}}

    champsLexicaux = chargeChampsLexicaux()  # charge les cinq thèmes avec leurs champs lexicaux

    # On prend un mot du texte
    for word in textTokenise:
        # On parcourt les mots des thèmes
        for theme in champsLexicaux.keys():
            if word in champsLexicaux[theme].keys():  # Si le mot fait partie du champ lexicale du thème
                if word not in champLexText.keys():  # S'il n'a pas déjà été enregistré dans notre dico du champ lexical du texte
                    # On ajoute le mot avec en valeur un dico avec le thème en clé et 1 en valeur
                    champLexText[word] = {theme: 1}
                else:  # S'il a déjà été enregistré on vérifie que le thème soit le même, si c'est le même on ajoute 1 à la valeur sinon on ajoute le thème en clé et 1 en vaeur
                    if theme not in champLexText[word].keys():
                        champLexText[word][theme] = 1
                    else:
                        champLexText[word][theme] += 1
    return champLexText

def nbMax(dicPourcentages):
    listPourcentages = []  # Permettra de trouver le pourcentage le plus haut

    # Créer le fichier de statistiques
    for pourcentage in dicPourcentages:
        listPourcentages.append(dicPourcentages[pourcentage])

    # Trouver le pourcentage le plus haut
    pourcentageMax = max(listPourcentages)
    return pourcentageMax

def trouveClasse(champLexText):
    '''
    Fonction qui prend en entrée le champ lexical d'un texte et en donne le thème et une liste des pourcentages d'appartenance à chaque thème
    :param champLexText: un dictionnaire du champ lexical du texte
    :return: retourne le thème du texte et un dictionnaire des pourcentages d'appartenance à chaque catégorie
    '''
    nbMots = 0.1  # Nombre de mots appartenant à tous les thèmes confondus pour calculer le pourcentage
    cinema = 0
    art = 0
    litterature = 0
    scenes = 0
    musique = 0
    # Compter le nombre de mot appartenant à chaque thème
    for word in champLexText.keys():
        for theme in champLexText[word].keys():
            if theme == "cinema":
                cinema += champLexText[word][theme]
                nbMots += champLexText[word][theme]
            elif theme == "art":
                art += champLexText[word][theme]
                nbMots += champLexText[word][theme]
            elif theme == "litterature":
                litterature += champLexText[word][theme]
                nbMots += champLexText[word][theme]
            elif theme == "scenes":
                scenes += champLexText[word][theme]
                nbMots += champLexText[word][theme]
            elif theme == "musique":
                musique += champLexText[word][theme]
                nbMots += champLexText[word][theme]

    # Enregister la proportion de mot pour chaque catégories
    pourcentages = {"Cinéma": cinema / nbMots , "Art":art / nbMots , "Scènes" : scenes / nbMots, "Musique":musique / nbMots ,  "Littérature": litterature/nbMots}


    # Trouver le pourcentage le plus haut
    pourcentageMax = nbMax(pourcentages)

    #Trouver à quel thème correspond le pourcentage le plus hauts
    for key in pourcentages.keys():
        if pourcentages[key] == pourcentageMax :
            categorie = key

    return categorie, pourcentages



def openFiletoClass (chemin):
    """
    Fonction qui ouvre un fichier, en extrait le titre (première ligne) et le reste du fichier
    :param chemin: chemin où se trouve le texte
    :return: retourne le titre (string) et le reste du fichier (string)
    """
    with open(chemin, "r", encoding="utf-8") as f :
        contenu = f.readlines()
        titre = contenu[0]
        reste = "".join(contenu)
    return titre, reste

def classeText(chemin) :
    '''
    Fonction principale qui prend en entrée un texte, l'ouvre, le tokenise, en extrait le champ lexical pour le titre et le corps du texte, pondère le titre,
    crée un fichier de statistiques avec le pourcentage d'appartenance du texte à chaque thème et classe le ficheir dans un dossier correspondant à son thème
    :param chemin: chemin du texte à analyser
    :return: Ne retourne rien
    '''
    # Ouvrir le texte
    newChemin ="../Corpus/"+chemin
    contenu = openFiletoClass(newChemin)
    titre = contenu[0]
    text = contenu[1]

    # Tokeniser le text et le titre
    textTokenise = tokeniser(text)
    titreTokenise = tokeniser(titre)

    # Enregistrer dans un dictionnaire le champ lexical du texte et du titre
    champLexText = champLexTexte(textTokenise)
    champLexTitre =  champLexTexte(titreTokenise)

    #Trouver la catégorie d'appartenance du titre
    catTitre = trouveClasse(champLexTitre)
    catTitre = catTitre[0]

    #Trouver la catégorie d'appartenance du texte
    catTexte = trouveClasse(champLexText)
    #categorieTexte = catTexte[0]
    pourcentages = catTexte[1]

    #Donner un pour plus important à la catégorie du titre (25% de plus) (modification du dico pourcentage)
    pourcentages[catTitre]=+0.15

    #Recalcule le pourcentage le plus, donc on trouve la nouvelle catégorie du texte
    pourcentageMax = nbMax(pourcentages)

    # Trouver à quel thème correspond le pourcentage le plus haut
    for key in pourcentages.keys():
        if pourcentages[key] == pourcentageMax:
            catTexte = key

    # Créer le dossier dans lequel on enregistrera les stats et les textes classés
    try:
        os.mkdir('ClassificationCorpus')
    except:
        print("Le dossier existe déjà. Les fichiers seront enregistrés dedans.")

    #Ouvrir le fichier de stats et y enregistrer les informations de pourcentage d'appartenance à un thème
    with open("ClassificationCorpus/stats.txt", "a", encoding="utf-8") as statfile:
        statfile.write("Pourcentages d'appartenance aux thèmes pour le fichier "+chemin+": \n")
        for pourcentage in pourcentages :
            statfile.write(pourcentage + " : " + format(pourcentages[pourcentage], '.2%') + "\n")
        statfile.write("\n")

    # Créer le fichier thème auquel appartient le texte ou y enregister le texte si le gichier existe déjà
    try:
        os.mkdir("ClassificationCorpus/" + catTexte)
        with open("ClassificationCorpus/" + catTexte+ "/"+chemin, "w", encoding="utf-8") as file:
            file.write(text)
    except:
        with open("ClassificationCorpus/" + catTexte + "/"+chemin, "w", encoding="utf-8") as file:
            file.write(text)

if __name__ == "__main__":
    chemins = os.listdir("../Corpus")
    for chemin in chemins:
        classeText(chemin)
