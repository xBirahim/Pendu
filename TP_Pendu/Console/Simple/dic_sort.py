# -*- coding: utf-8 -*-

""""
Ce programme peut-être résumé au tri du dictionnaire télechargé sur internet. Il associe à chaque caractére spécial un
caractère plus simple et le remplace par ce dernier dans un nouveau fichier qui lui, sera utilisable.
Papa Birahim Seye, 3 ETI, CPE Lyon
3/12/2020
"""
correspondence = {"à": "a", "á": "a", "ä": "a", "ã": "a", "â": "a",
                  "ì": "i", "í": "i", "ï": "i", "î": "i",
                  "ù": "u", "ú": "u", "ü": "u", "û": "u",
                  "è": "e", "é": "e", "ë": "e", "ê": "e",
                  "œ": "oe"
                  }

new_list = []

with open("french_words.txt", "r", encoding="UTF-8") as file:
    for word in file.readlines():
        if len(word) >= 6 and ("-" not in word) and ("." not in word):
            add_word = ""
            for letter in word:
                if letter in correspondence.keys():
                    add_word += correspondence[letter]
                    continue
                add_word += letter
            new_list += [add_word.rstrip()]
        else:
            continue

with open('words_list.txt', "a", encoding="UTF-8") as new_file:
    new_list = sorted(new_list)
    for word in new_list:
        new_file.writelines(word + "\n")
