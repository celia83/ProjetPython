# coding: utf-8
import spacy,os


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
    Fonction qui permet de charger un dictionnaire des champs lexicaux desquatres thèmes : art, litterature, cinéma, musique et scène.
    Le dictionnaire se construit de cette façon : {art : {mot :""}, musique : {mot : ""}}
    :return: Retourne une table de hachage avec tous les thèmes en clé et des dictionnaires pour chaque mot composant le thème.
    '''

    champsLexicaux = {}  # Contiendra le dictionnaire des champs lexicaux des thèmes
    themes = ["art", "cinema", "litterature", "musique", "scenes"]  # Liste des thèmes qui nous intéressent pour lesquels nous avons une liste de mots dans des fichiers .txt
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
    champLexText = {} #contiendra le dictionnaire {mot : {thème : occurrence}}
    champsLexicaux = chargeChampsLexicaux() #charge les cinq thèmes avec leurs champs lexicaux
    #On prend un mot du texte
    for word in textTokenise:
        #On parcourt les mots des thèmes
        for theme in champsLexicaux.keys():
            if word in champsLexicaux[theme].keys():  # Si le mot fait partie du champ lexicale du thème
                if word not in champLexText.keys(): # S'il n'a pas déjà été enregistré dans notre dico du champ lexical du texte
                    # On ajoute le mot avec en valeur un dico avec le thème en clé et 1 en valeur
                    champLexText[word] = {theme: 1}
                else:  # S'il a déjà été enregistré on vérifie que le thème soit le même, si c'est le même on ajoute 1 à la valeur sinon on ajoute le thème en clé et 1 en vaeur
                    if theme not in champLexText[word].keys():
                        champLexText[word][theme] = 1
                    else:
                        champLexText[word][theme] += 1
    return champLexText

def classeText(champLexText, text) :
    '''
    Crée un dossier avec les fichiers classés et un fichier .txt qui donne un récapitulatif de la classification (pourcentage d'appartenance à chaque thème
    :param champLexText:
    :return: ne retourne rien
    '''
    try:
        os.mkdir('ClassificationCorpus')
    except:
        print("Le dossier existe déjà.")
    nbMots = 0
    cinema = 0
    art = 0
    litterature =0
    scenes = 0
    musique = 0
    for word in champLexText.keys():
        for theme in champLexText[word].keys() :
            if theme == "cinema" :
                cinema += champLexText[word][theme]
                nbMots += champLexText[word][theme]
            elif theme == "art" :
                art += champLexText[word][theme]
                nbMots += champLexText[word][theme]
            elif  theme == "litterature":
                litterature += champLexText[word][theme]
                nbMots += champLexText[word][theme]
            elif  theme == "scenes" :
                scenes += champLexText[word][theme]
                nbMots += champLexText[word][theme]
            elif theme == "musique":
                musique += champLexText[word][theme]
                nbMots += champLexText[word][theme]

    pourcentages = { cinema/nbMots: "Cinéma", art/nbMots :"Art" ,litterature/nbMots : "Littérature", scenes/nbMots : "Scènes",musique/nbMots:"Musique"}
    listPourcentages = []

    with open ("ClassificationCorpus/stats.txt", "a", encoding="utf-8") as statfile :
        statfile.write("Pourcentages d'appartenance aux thèmes : \n")
        for pourcentage in pourcentages :
            listPourcentages.append(pourcentage)
            statfile.write( pourcentages[pourcentage]+ " : " + format(pourcentage,'.2%') + "\n")

    pourcentageMax = max(listPourcentages)
    print(pourcentages[pourcentageMax])

    try:
        os.mkdir("ClassificationCorpus/"+pourcentages[pourcentageMax])
        with open("ClassificationCorpus/"+pourcentages[pourcentageMax]+"/text.txt", "w", encoding="utf-8") as file:
            file.write(text)
    except:
        with open("ClassificationCorpus/"+pourcentages[pourcentageMax]+"/text.txt", "w", encoding="utf-8") as file:
            file.write(text)

if __name__ == "__main__":
    text = "J'ai vu un film aujourd'hui avec un super comédien et un casting génial. Le comédien jouait un peintre."
    textTokenise = tokeniser(text)
    champLexText = champLexTexte(textTokenise)
    classeText(champLexText, text)
