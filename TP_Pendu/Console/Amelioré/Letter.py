class Letter:
    def __init__(self, value):
        self.value = value
        self.hidden = False

    def toggle(self):
        if self.hidden == False:
            self.hidden = True
        else:
            self.hidden = False

    def __repr__(self):
        if self.hidden == False:
            return self.value
        else:
            return "_"
