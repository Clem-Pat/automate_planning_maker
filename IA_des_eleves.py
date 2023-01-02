import numpy as np
import random
from excel_manager import Excel_Reader, Excel_Creator
import time
import os

class IA_des_eleves():
    """docstring for IA_des_eleves."""

    def __init__(self, names, group_number):
        self.names, self.group_number = names, group_number
        self.nbre_creneau_par_nom = [[0, self.names[i]] for i in range(len(self.names))]
        self.plannings = {name : [['' for j in range(7)] for k in range(9)] for name in self.names}
        self.planning_general = [['' for j in range(7)] for k in range(9)]
        self.planning_hours = [[['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'][i]+['08h', '10h', '12h', '14h', '16h', '18h', '20h', '22h', '00h'][j] for i in range(7)] for j in range(9)]
        self.nbre_creneaux_par_jour = len(self.planning_hours)
        self.excel = Excel_Creator()


        for name in self.names:
            print(name)
            self.complete_random_planning(name)
        self.verify_planning()

        for name in self.names:
            self.excel.create_excel(name, self.plannings[name])

        self.excel.create_excel(f'Général{self.group_number}', self.planning_general)

    def __repr__(self):
        creneaux, creneaux_vides = '', ''
        for i in range(len(self.nbre_creneau_par_nom)):
            creneaux += f'\n {self.nbre_creneau_par_nom[i][1]} : {self.nbre_creneau_par_nom[i][0]} créneaux'
        for i in range(len(self.planning_general)):
            for j in range(len(self.planning_general[0])):
                if self.planning_general[i][j] == '':
                    creneaux_vides += f'\n{str(self.planning_hours[i][j])[:-3]} {str(self.planning_hours[i][j])[-3:]}'
        if creneaux_vides != '': creneaux_vides  = f"\n\ncreneaux sans Foy'z man/woman : " + creneaux_vides
        return str(np.array(self.planning_general)) + '\n' + creneaux + creneaux_vides + '\n\n\n'

    def tri_rapide_names(self, g, d):
        def partition(g, d):
            pivot = self.nbre_creneau_par_nom[g]
            i = g+1
            j = d
            while i <= j:
                while i < len(self.nbre_creneau_par_nom) and self.nbre_creneau_par_nom[i][0] <= pivot[0]:
                    i += 1
                while self.nbre_creneau_par_nom[j][0] > pivot[0]:
                    j -= 1
                if i < j:
                    self.nbre_creneau_par_nom[i], self.nbre_creneau_par_nom[j] = self.nbre_creneau_par_nom[j], self.nbre_creneau_par_nom[i]
                    self.names[i], self.names[j] = self.names[j], self.names[i]
                    i += 1
                    j -= 1
            self.nbre_creneau_par_nom[g], self.nbre_creneau_par_nom[j] = self.nbre_creneau_par_nom[j], self.nbre_creneau_par_nom[g]
            self.names[g], self.names[j] = self.names[j], self.names[g]
            return j

        if g<d:
            j = partition(g, d)
            self.tri_rapide_names(g, j-1)
            self.tri_rapide_names(j+1, d)

    def give_creneau_to_name(self, name, j, k):
        self.plannings[name][j][k], self.planning_general[j][k] = 'x', name
        self.nbre_creneau_par_nom[self.names.index(name)][0] += 1

    def get_indispo_dispo(self, name=None):
        excel = Excel_Reader(self.names)
        return excel.indispo_dispo[name]

    def ask_if_free(self, name, j, k, indispo_dispo):
        if self.plannings[name][j][k] == '' and indispo_dispo[j][k] == None:
            self.give_creneau_to_name(name, j, k)
            return True
        else:
            return False

    def ask_if_free_until_death(self, name, j, k, indispo_dispo):
        if self.ask_if_free(name, j, k, indispo_dispo): return True
        else :
            nbre_test = 0
            last_parachute = 0
            while not self.ask_if_free(name, j, k, indispo_dispo):
                last_parachute += 1
                if last_parachute > 1000: break
                if nbre_test == len(self.names)+1: return False
                nbre_test += 1
                name, j, k, indispo_dispo = self.names[self.names.index(name)-1], j, k, self.get_indispo_dispo(self.names[self.names.index(name)-1])
        if last_parachute > 1000: os.system('python IA_des_eleves.py')
        return True

    def complete_random_planning(self, name):
        planning = self.plannings[name]
        indispo_dispo = self.get_indispo_dispo(name)
        count, breaker = 0, 0
        total_nbre_creneaux = ((self.nbre_creneaux_par_jour-1)*7//len(self.names))-1
        while count != total_nbre_creneaux:
            j = random.randint(0,self.nbre_creneaux_par_jour-1)
            k = random.randint(0,6)
            if self.planning_general[j][k] == '':
                if planning[j][k] == '':
                    if indispo_dispo[j][k] == None:
                        count += 1
                        self.give_creneau_to_name(name, j, k)
                    else:
                        planning[j][k] = '-'
                        self.ask_if_free_until_death(self.names[self.names.index(name)-1], j, k, indispo_dispo)

    def verify_planning(self):
        self.tri_rapide_names(0, len(self.nbre_creneau_par_nom)-1)
        for j in range(self.nbre_creneaux_par_jour):
            for k in range(7):
                i = 0
                breaker = False
                self.tri_rapide_names(0, len(self.nbre_creneau_par_nom)-1)
                while self.planning_general[j][k] == '' and not breaker:
                    name = self.nbre_creneau_par_nom[i][1]
                    planning = self.plannings[name]
                    indispo_dispo = self.get_indispo_dispo(name)
                    if planning[j][k] == '':
                        if indispo_dispo[j][k] == None:
                            self.give_creneau_to_name(name, j, k)
                            i = 0
                        else:
                            planning[j][k] = '-'
                            if i+1 < len(self.names): i += 1
                            else: breaker = True
                    else:
                        if i+1 < len(self.names): i += 1
                        else: breaker = True


class Planning_compiler():
    def __init__(self, names, bots):
        self.names, self.bots = names, bots
        self.planning_general = self.compile_everyone(self.bots)
        self.excel = Excel_Creator()
        self.excel.create_excel(f'Général_final', self.planning_general)

    def __repr__(self):
        return str(np.array(self.planning_general))

    def compile_everyone(self, bots):
        if len(bots) == 1: return bots[0].planning_general
        elif len(bots) == 2: return self.compile(bots[0].planning_general, bots[1].planning_general)
        else:
            planning_compiled = self.compile(bots[0].planning_general, bots[1].planning_general)
            for i in range(2, len(bots)):
                planning_compiled = self.compile(planning_compiled, bots[i].planning_general)
            return planning_compiled

    def compile(self, A, B):
        """FUUUUSION"""
        C = [[0 for j in range(len(A[0]))] for i in range(len(A))]
        for i in range(len(A)):
            for j in range(len(A[0])):
                if A[i][j] == '': C[i][j] = B[i][j]
                if B[i][j] == '': C[i][j] = A[i][j]
                if A[i][j] != '' and B[i][j] != '': C[i][j] = A[i][j] + ' + ' + B[i][j]
        return C


if __name__ == '__main__':
    names = ['Nathalie', 'André', 'Fred', 'Patrice', 'Jackie', 'Violette', 'Jean', 'Mathilde', 'Hugues']
    bots = []
    for i in range(len(names)//3):
        print(names[3*i:3*(i+1)])
        bot = IA_des_eleves(names[3*i:3*(i+1)], i)
        bots.append(bot)
        print(repr(bot))
    final_planning = Planning_compiler(names, bots)
    print(repr(final_planning))

"""
    Faire un anti indispo : des créneaux que le F man/woman veut absolument occuper ('x' et '+')
    Eviter les horaires qui se suivent
    Eviter les trous de une seule heure
    Ajouter les coefficients
    Faire un Cupidon (deux F veulent être ensemnble le plus possible)
    Faire un Diable  (deux F veulent être ensemble le moins possible)
"""
