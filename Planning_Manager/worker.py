
class Worker():
    def __init__(self, name, username=None, color="#FF0000", last_time_had_menage = 2.0, historic=[], mefos=[]):
        self.name = name
        self.color = color
        self.username = username
        # self.prefers_menage = prefers_menage
        # self.student_prefered = student_prefered
        self.historic = historic
        self.last_time_had_menage = float(last_time_had_menage) #par défaut son dernier ménage date d'il y a 2 semaines
        self.crens = [] #list of Creneau()
        self.planning = []
        self.is_mefo = self.name in mefos

    def __repr__(self):
        return self.name

    def get_planning(self, i_tot, j_tot, indispos):
        resu = []
        for i in range(i_tot):
            resu.append([])
            for j in range(j_tot):
                resu[-1].append('')
                for cren in self.crens:
                    if cren.i == i and cren.j == j:
                        resu[-1][-1] += 'o'
                if indispos[self.name][i][j] != None:
                    resu[-1][-1] += 'x'
        return resu

    def __lt__(self, other):
        if self.name == 'None' or self.name == 'none': return False
        if other.name == 'None' or other.name == 'none': return True
        return self.name < other.name

    def __le__(self, other):
        if self.name == 'None' or self.name == 'none': return False
        if other.name == 'None' or other.name == 'none': return True
        return self.name <= other.name

    def __gt__(self, other):
        if self.name == 'None' or self.name == 'none': return True
        if other.name == 'None' or other.name == 'none': return False
        return self.name > other.name

    def __ge__(self, other):
        if self.name == 'None' or self.name == 'none': return True
        if other.name == 'None' or other.name == 'none': return False
        return self.name >= other.name