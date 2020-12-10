from random import choice


class Letter:
    """"
    Cette classe va sera utile pour chaque lettre du mot qui sera choisi. Il aurait été possible de n'utiliser que des
    listes ou des tuples, mais cela aurait rendu la tache plus dure au niveau de l'interface graphique, qui elle,
    utilisera la meme base de classe, mais avec quelques methodes et attributs en plus.
    Et puis, les class, c'est classe !
    """

    def __init__(self, value):
        """"
        Le constructeur de la classe, on initialise l'attribut value, qui sera en fait la lettre sous forme de chaine de
        caractere
        """
        self.value = value
        self.hidden = False

    def toggle(self):
        """"
        Cette methode permet de savoir si la lettre est affichee normalement ou sous forme de "_"
        """
        if not self.hidden:
            self.hidden = True
        else:
            self.hidden = False

    def __repr__(self):
        """"
        Cette methode speciale permet de renvoyer la representation de la lettre en fonction de son etat (hidden or not)
        """
        if not self.hidden:
            return self.value
        else:
            return "_"


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
    Dans ce cas, elle appelle la fonction save_score().
    """
    global letter_list, guessed, times

    if all([not letter.hidden for letter in letter_list]):
        """" Ici, on inverse l'état de chaque lettre pour pouvoir utiliser la focntion all"""
        guessed = True
        print(f"///{word}/// Bravo, vous avez trouvé le mot en {times} coups !")
        save_score()


def save_score():
    """
    La fonction qui permettra de sauvegarder les scores sous forme de fichier texte.
    """
    global word, lives, times

    with open("score.txt", "a") as file:
        file.writelines(f"{word}/{times}\n")


def beautiful_line():
    """"
    Cette fonction n'est pas tres utile, elle rend juste l'affichage en console plus joli.
    """
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")


def endgame():
    """
    A la fin du jeu, cette fonction sera appelée pour proposer à l'utilisateur différentes actions.
    """
    global next, word, play, letter_list, not_in_word, times, lives, guessed

    not_in_word = []
    letter_list = []
    guessed = False
    lives = 8
    print("Engame sur lives")
    times = 0
    next = ""

    while next not in ["o", "n", "h"]:
        beautiful_line()

        next = input("Voulez vous rejouer (o/n)? \n"
                     "Voir l'historique des parties (h)")
        if next == "o":
            word = random_word()
            word_letters(word)
            hidden_word()

        elif next == "n":
            beautiful_line()
            print("Merci d'avoir jouer !")
            play = False

        elif next == "h":
            beautiful_line()
            print("MOT | TENTATIVES")
            with open("score.txt", "r") as scores:
                for score in scores.readlines():
                    history = score.split("/")
                    print(f"{history[0]} | {history[1]}")


not_in_word = []  # Liste des lettres qui ne font pas parties du mot
words_list = []
create_wlist()
letter_list = []
word = random_word()
word_letters(word)
hidden_word()

play = True  # Variable qui définie si on joue encore ou pas
guessed = False  # État du mot ( True => toutes les lettres ont étés trouvées )
lives = 8  # Nombre de tentatives restantes
times = 0  # Nombre de coups
next = ""  # Chaîne de caractère qui vas permettre de sauvegarder le score, recommencer ou quitter
guess = ""

while play:
    print(word)  # Juste pour le debug, j'espère ne pas oulier de supprimer cette ligne
    beautiful_line()
    found = False  # Cette variable permettra de verifier si une lettre à été trouvée ou pas.
    show_word()
    guess = input("\nDonnez une lettre : ")
    guessCheck()

    for letter in letter_list:
        """"
        Ici on va verifier pour chaque lettre du mot si celle entree par l'utilisateur lui correspond, si oui, alors 
        la lettre change de statut et lettre.hidden == False, et la boucle s'arrete, sinon on continue
        """
        if guess == letter.value and letter.hidden:
            found = True
            letter.toggle()
            times += 1  # On met à jour le nombre de tentatives
            break



    if found and not guessed:
        print(f"Bravo ! ({lives} chances restantes)")
        print(f"Lettres essayées : {'//'.join(not_in_word)}")

    elif not found:
        if guess not in not_in_word:
            not_in_word += [guess]  # La lettre ne fait pas parti du mot
        lives -= 1
        print(f"Aïe, '{guess}' n'est pas dans ce mot :/ ({lives} chances restantes)")
        print(f"Lettres essayées : {'//'.join(not_in_word)}")

    if lives == 0:
        print(f"Dommage, vous avez perdu, le mot était : {word}")
        endgame()

    elif guessed:
        endgame()

    beautiful_line()
