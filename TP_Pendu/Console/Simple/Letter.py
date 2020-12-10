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
