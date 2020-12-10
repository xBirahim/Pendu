# -*- coding: utf-8 -*-

""""
Voici la version graphique du programme, le code aurait pu être beaucoup plus simple, mais dans ce cas le programme le
serait aussi. Je voulais une version un peu plus interactive que prévue, c'est pourquoi ma classe et mes objets ont étés
crées comme cela. Le code m'a l'air très lisible et compréhensif. Excusez moi de faire ma to do list ainsi, autrement
PyCharm ne la reconnaît pas.
Je n'ai pas trouvé comment bien utiliser la méthode after de tkinter, ni comment je pouvais séparer mon programme en
plusieurs scripts, parceque plusieurs de mes fonctions utilisent le mot clé global.
Les deux spinboxs à droite du boutton changer le mot sont pour sélectionner le nombre de lettres à cacher (première)
et la longueur du mot à afficher (deuxième). Je n'avais pas d'idée de comment bien les placer, elles devront être dans
une future page de paramètres.

# TODO -----------------
# TODO  -utiliser la méthode after pour ne pas obliger l'utilisateur à appuyer sur le boutton pour changer de mot
# TODO  -mettre un timer
# TODO  -mettre une fontion qui enregistre les scores automatiquement
# TODO  -mettre une fonction qui affiche les scores et l'historique des parties
# TODO  -créer un menu
# TODO  -créer une page de paramètres (modifier la couleur des textes, la difficulté
# TODO  -créer une page de tutoriel (notemment sur l'utilité des bouttons, comment jouer etc)
# TODO  -mieu commenter le code
# TODO ------------------
#
Papa Birahim Seye, 3 ETI, CPE Lyon
Date: 10/12/2020
"""

from tkinter import StringVar, Frame, LEFT, Label, TOP, Entry, END, EXCEPTION, Tk, FLAT, LabelFrame, Button, Spinbox, \
    RIGHT, PhotoImage, BOTTOM
from random import choice
from winsound import PlaySound, SND_ASYNC


class Letter:
    """
    Sur la base de la classe crée pour la version console, on utilisera cette classe, qui en soit est la même, avec
    quelques méthodes et attributs en plus. Notemment, un objet de la classe lettre sera maintenant caractérisé par
    un objet de tkinter pour avoir une dimension graphique.
    """

    def __init__(self, master, character, index):
        """
        Le constructeur de la classe
        :param master:
        :param character:
        :param index:
        """
        self.character = character
        self.index = index
        self.hidden = False

        self.value = StringVar()
        self.value.set(self)
        self.value.trace("w", self.limitTextSize)

        self.frame = Frame(master)
        self.frame.pack(side=LEFT)

        self.position = Label(self.frame,
                              text=str(self.index + 1),
                              fg="green")
        self.position.pack(side=TOP)

        self.widget = Entry(self.frame,
                            width=2,
                            font="Helvetica 50 bold",
                            textvariable=self.value,
                            justify="center"
                            )
        self.widget.pack()
        self.widget.bind("<Return>", func=self.verify)
        self.widget.bind("<FocusIn>", self.fill_in)
        self.widget.bind("<FocusOut>", self.fill_out)

        if not self.hidden:
            self.widget.insert(index=0, string=self.value.get())
        else:
            self.widget.insert(index=0, string="_")

    def __repr__(self):
        if not self.hidden:
            return self.character
        else:
            return "_"

    def toggle(self):
        if not self.hidden:
            self.erase()
            self.widget.insert(index=0, string="_")
            self.hidden = True
            self.position.configure(fg="red")

        else:
            self.hidden = False

    def limitTextSize(self, *args):
        value = self.value.get()
        if len(value) > 1:
            self.value.set(value[:1])

    def verify(self, *args):
        global attempts, score, lives

        if self.value.get() == word[self.index]:
            attempts += 1

            if lives <= 0:
                interaction(filename="found", new_message=f"C'est trouvé, mais vous avez déjà perdu :/")
                lives = 0
                attempts -= 1
                update_ui()
                self.position.configure(fg="green")
            else:
                update_ui()
                interaction(filename="found", new_message=f"{self.index + 1} / Trouvé")
                updater_text.configure(fg="blue")
                self.position.configure(fg="green")
        else:
            attempts += 1
            lives -= 1

            if lives <= 0:
                interaction(filename="void", new_message=f"Dommage, le mot était {word} recommencez")
                lives = 0
                attempts -= 1
                interaction(filename="unfound",
                            new_message=f"Veuillez appuyer sur 'Changer de mot'")
                update_ui()
            else:
                update_ui()
                self.value.set("")
                interaction(filename="unfound", new_message=f"{self.index + 1} / Mauvaise lettre")
                updater_text.configure(fg="red")
                self.position.configure(fg="red")



    def fill_in(self, *args):
        value = self.value.get()
        if value == "_":
            self.value.set("")
        else:
            pass

    def fill_out(self, *args):
        value = self.value.get()
        if value == "":
            self.value.set("_")
        else:
            pass

    def erase(self):
        self.widget.delete(0, END)

    def destroy(self):
        self.widget.destroy()
        self.position.destroy()
        self.frame.destroy()


def create_wlist():
    """"
    Cette fonction permet de créer la liste des mots à partir du fichier words_list.txt"""

    global words_list

    with open("words_list.txt", "r") as file:
        for element in file.readlines():
            words_list += [element.rstrip()]

    return words_list


def word_letters(word_to_guess):
    number = 0
    for ch in word_to_guess:
        letter = Letter(word_frame, ch, number)
        letter_list.append(letter)
        number += 1


def change_word():
    global letter_list, word, attempts, score, lives
    score = 0
    length = int(length_spinbox.get())
    for letter in letter_list:
        letter.destroy()

    letter_list = []

    new_word = choice([words for words in words_list if len(words) == length]).lower()
    word = new_word
    attempts = 0
    lives = 8
    updater_text["text"] = "Trouvez le mot caché !"
    lives_ui["text"] = f"Vie(s) restantes : {str(lives)}"
    hidden_spinbox["to"] = int(length_spinbox.get()) - 1
    update_ui()
    word_letters(new_word)
    hide(new_word)


def hide(hide_word):
    global letter_list

    hidden_letters_number = int(hidden_spinbox.get())
    hidden = []

    for char in range(hidden_letters_number):
        choosen = choice([ch for ch in letter_list if ch not in hidden])
        choosen.toggle()
        hidden.append(choosen)

    return hidden


def interaction(filename="void", new_message="void"):
    try:
        if new_message == "void":
            pass
        else:
            updater_text["text"] = new_message

        if filename == "void":
            pass
        else:
            PlaySound(f"Sounds/{filename}.wav", SND_ASYNC)
    except EXCEPTION:
        pass


def update_ui():
    global lives, attempts, temps

    attempt_ui["text"] = f"Tentatives : {str(attempts)}"
    lives_ui["text"] = f"Vie(s) restantes : {str(lives)}"
    if lives > 0:
        image_ui["image"] = images[f"image{lives}"]
    else:
        image_ui["image"] = images["image0"]


def check_win(*args):
    global end

    win = True

    for letter in letter_list:

        if not letter.hidden:
            continue
        else:
            if letter.value.get() == word[letter.index]:
                continue
            else:
                win = False

    if win:
        interaction(filename="win", new_message="Bravoooooooo !")
        updater_text.configure(fg="green")

    # end = main_window.after(2000, check_win)


def open_settings():
    """"
    Future fonction qui ouvrira la page de paramètres"""
    print("Opening settings...")


words_list = []
words_list = create_wlist()

word = choice(words_list).lower()
letter_list = []
attempts = 0
score = 0
mult = 1
end = int()
lives = 8
temps = 0

main_window = Tk()
main_window.title("Pendu")

images = {
    "image0": PhotoImage(file="Images/bonhomme0.gif"),
    "image1": PhotoImage(file="Images/bonhomme1.gif"),
    "image2": PhotoImage(file="Images/bonhomme2.gif"),
    "image3": PhotoImage(file="Images/bonhomme3.gif"),
    "image4": PhotoImage(file="Images/bonhomme4.gif"),
    "image5": PhotoImage(file="Images/bonhomme5.gif"),
    "image6": PhotoImage(file="Images/bonhomme6.gif"),
    "image7": PhotoImage(file="Images/bonhomme7.gif"),
    "image8": PhotoImage(file="Images/bonhomme8.gif")
}

info_frame = Frame(main_window)
info_frame.pack()

lives_ui = Label(info_frame,
                 font="Helvetica 20 bold",
                 text=f"Vie(s) restantes : {str(lives)}")
lives_ui.pack()

attempt_ui = Label(info_frame,
                   font="Helvetica 20 bold",
                   text=f"Tentatives : {str(attempts)}",
                   relief=FLAT)
attempt_ui.pack()

word_frame = LabelFrame(main_window,
                        font="Helvetica 20 bold",
                        text="Pendu v2.0:",
                        relief=FLAT)
word_frame.pack()

game_frame = Frame(main_window)
game_frame.pack()

updater_text = Label(game_frame,
                     text="Trouvez le mot !",
                     font="Helvetica 20 bold",
                     fg="blue"
                     )
updater_text.pack()

check_win_button = Button(game_frame,
                          text="Verifier ?",
                          width=15,
                          font="Helvetica 20 bold",
                          command=check_win)
check_win_button.pack(side=LEFT)

length_spinbox = Spinbox(game_frame,
                         width=2,
                         from_=10,
                         to=15,
                         font="Helvetica 20 bold"
                         )
length_spinbox.pack(side=RIGHT)

hidden_spinbox = Spinbox(game_frame,
                         width=2,
                         from_=5,
                         to=int(length_spinbox.get()) - 1,
                         font="Helvetica 20 bold"
                         )
hidden_spinbox.pack(side=RIGHT)

change_word_button = Button(game_frame,
                            text="Changer de mot",
                            width=15,
                            font="Helvetica 20 bold",
                            command=change_word)
change_word_button.pack(side=RIGHT)

images_frame = Frame(main_window)
images_frame.pack(side=BOTTOM)

image_ui = Label(images_frame, image=images[f"image{lives}"])
image_ui.pack()

# *-*-*-*
word_letters(word)
hide(word)
main_window.mainloop()
