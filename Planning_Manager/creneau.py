class Creneau():
    def __init__(self, name, soirees=['none'], soiree_mefo='none'):
        """ représente un créneau
            name = ['lundi', '12h15-13h']       'm1'
            name = [1, 2] => mardi 17h30-20h30  's1'
            name = 'lundi 12h15-13h'

            pour mefo : name = 'mercredi mefo'
        """
        self.crens, self.jours = ['12h15-13h', '13h-13h30', '17h30-20h30', '20h30-23h', '23h-00h'], ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
        if isinstance(name, list) or isinstance(name, tuple):
            if isinstance(name[0], int):
                self.j, self.i = name[0], name[1]
                self.jour, self.cren = self.jours[self.j], self.crens[self.i]
            elif isinstance(name[0], str):
                self.jour, self.cren = name[0], name[1]
                self.j, self.i = self.jours.index(self.jour), self.crens.index(self.cren)
        elif isinstance(name, str):
            if 'mefo' in name:
                if any(jour in name for jour in self.jours): #Si name = 'mercredi mefo'
                    self.jour, self.cren = name.split(' ')[0], 'mefo'
                    self.j, self.i = self.jours.index(self.jour), -1
                else: #Si name = 'mefo'
                    self.jour, self.cren = soiree_mefo, 'mefo'
                    self.j, self.i = self.jours.index(self.jour), -1
            else:
                self.jour, self.cren = name.split(' ')[0], name.split(' ')[1]
                self.j, self.i = self.jours.index(self.jour), self.crens.index(self.cren)

        if self.i == 0 and self.j != 6: self.type, self.coeff, self.exact_time, self.color = 'm1', 0.5, '12h15-13h', '#fbbc04'
        elif self.i == 1 :
            if self.j == 3: self.type, self.coeff, self.exact_time, self.color = 'm', 0.5, '12h15-13h30', '#cc0000' #le jeudi le midi s'appelle m
            else: self.type, self.coeff, self.exact_time, self.color = 'm2', 0.5, '13h-13h30', '#ff6d01'
        elif self.i == 2: self.type, self.coeff, self.exact_time, self.color = 's1', 1, '17h30-20h30', '#46bdc6'
        elif self.i == 3:
            if self.jours[self.j] in soirees : self.type, self.coeff, self.exact_time, self.color = 's2', 1, '20h30-22h30', '#9900ff'
            else : self.type, self.coeff, self.exact_time, self.color = 's2', 2, '20h30-23h + ménage', '#34a853'
        elif self.i == 4: self.type, self.coeff, self.exact_time, self.color = 's3', 2, '22h30-00h + ménage', '#ff00ff'
        elif self.i == 0 and self.j == 6 : self.type, self.coeff, self.exact_time, self.color = 'menage', 2, 'Ménage', '#b4a7d6'
        elif self.i == -1 : self.type, self.coeff, self.exact_time, self.color = 'mefo', 2, 'Mefo', '#FFFF00'
        else: self.type, self.coeff, self.exact_time = 'unknown', 0, 'unknown'
        self.text = self.type.upper() + ' ' + self.exact_time

    def __str__(self):
        return self.jour + ' ' + self.cren

    def __repr__(self):
        return self.jour + ' ' + self.cren

    def __eq__(self, cren2):
        return self.j == cren2.j and self.i == cren2.i

    def __lt__(self, other):
        if self.j < other.j: return True
        elif self.j == other.j: return self.i < other.i
        else: return False

    def __le__(self, other):
        if self.j <= other.j: return True
        elif self.j == other.j: return self.i <= other.i
        else: return False

    def __gt__(self, other):
        if self.j > other.j: return True
        elif self.j == other.j: return self.i > other.i
        else: return False

    def __ge__(self, other):
        if self.j >= other.j: return True
        elif self.j == other.j: return self.i >= other.i
        else: return False
