from random import choice
from Letter import Letter
import pendu_terminal_v1

words_list = pendu_terminal_v1.words_list
letter_list = pendu_terminal_v1.letter_list

play = True #Variable qui définie si on joue encore ou pas
guessed = False #État du mot ( True => toutes les lettres ont étés trouvées )
lives = 8 #Nombre de tentatives restantes
times = 0 #Nombre de coups


def word_letters(word):
    """"
    Cette fonction permet de separer les differentes lettres d'un mot qu'elle va ajouter a la liste letter_list
    """
    for ch in word:
        letter = Letter(ch)
        letter_list.append(letter)


def hidden_word():
    """"
    Cette fonction cache toutes les lettres du mot qui ne sont pas similaires a la premiere
    """
    global letter_list
    hidden = []

    for char in [le for le in letter_list if le.value != letter_list[0].value]:
        char.toggle()
        hidden.append(char)


def create_wlist():
    """
    Cette fonction cree une liste de mots dans laquelle notre mot a deviner se trouve.
    """
    global words_list
    with open("words_list.txt", "r") as file:
        for element in file.readlines():
            words_list += [element.rstrip()]


def random_word():
    """
    Cette fonction simple choisi un mot au hasard dans la liste de mots creee grace a create_wlist().
    """
    global words_list
    return choice(words_list)


def show_word():
    """"
    Cette fonction permet tout simplement de 'print' le mot, car il est separer en plusieurs objets de la classe
    Letter, il faut alors les aligner d'ou le * end="" *
    """
    for x in letter_list:
        print(x, end="")


def guessCheck():
    """"
    La fonction vérifie que l'ensemble des lettres qui composent le mot ne sont plus à l'état caché.
    Dans ce cas, elle arrête la partie et affiche un message de victoire.
    """
    global letter_list, guessed, play, times

    if all([not letter.hidden for letter in letter_list]):
        """" Ici, on inverse l'état de chaque lettre pour pouvoir utiliser la focntion all"""
        guessed = True
        print(f"///{word}/// Bravo, vous avez trouvé le mot en {times} coups !")
        play = False


def beautiful_line():
    """"
    Cette fonction n'est pas tres utile, elle rend juste l'affichage du code plus joli.
    """
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")