# coding: utf-8
import spacy

def tokeniser (text):
    '''
    Fonction qui prend en entrée une chaine de caractères et ressort une tokenisation du texte (utilise spacy)
    :param text: Une chaine de caractères
    :return: Liste des mots de la chaine de caractères
    '''
    #tokenisation du texte avec spacy (donne un objet créé par spacy)
    nlpFr = spacy.load('fr_core_news_md')
    words = nlpFr(text)
    #on met tous les tokens dans une liste
    listTokens = []
    for word in words :
        listTokens.append(word)
    return listTokens

def chargeChampsLexicaux() :
    '''
    Fonction qui permet de charger un dictionnaire des champs lexicaux desquatres thèmes : art, litterature, cinéma, musique et scène.
    Le dictionnaire se construit de cette façon : {art : {mot :""}, musique : {mot : ""}}
    :return: Retourne une table de hachage avec tous les thèmes en clé et des dictionnaires pour chaque mot composant le thème.
    '''

    champsLexicaux = {} #Contiendra le dictionnaire des champs lexicaux des thèmes
    themes = ["art", "cinema", "litterature", "musique","scenes"] #Liste des thèmes qui nous intéressent pour lesquels nous avons une liste de mots dans des fichiers .txt
    for theme in themes :
        #On enregistre le thème en clé et on enregistrera en valeur un dictionnaire contenant chaque mot associé au thème
        champsLexicaux[theme] = {}
        #On ouvre le fichier contenant les mots
        with open (theme+".txt", "r", encoding ="utf8")as file:
            for word in file.readlines() :
                #On enlève les sauts de lignes
                word = word.split("\n")[0]
                #on ajoute le mot au niveau du thème avec en valeur un blanc
                champsLexicaux[theme][word] = ""
    return champsLexicaux

if __name__ == "__main__":
    text = "Bonjour, il fait pas beau dehors."
    textTokenise = tokeniser(text)
    champsLexicaux = chargeChampsLexicaux()
    print(champsLexicaux)