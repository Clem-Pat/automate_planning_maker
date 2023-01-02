# import panda
import csv
import os, os.path
import pandas as pd
import openpyxl
import string

"""
L_data = [['Lundi8h', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', 'Mardi12h', '', '', '', 'Samedi12', ''], ['', '', '', '', '', '', ''], ['', '', 'Mercredi16h', '', '', '', ''], ['', '', 'Mercredi18h', 'x', '', '', ''], ['', '', '', '', '', 'Samedi20h', ''], ['', '', '', '', '', '', ''], ['Lundi00h', '', 'Mercredi00h', '', '', '', '']]
"""

class Excel_Reader():
    def __init__(self, names):
        self.names = names
        self.indispo_dispo = {}
        for name in self.names:
            self.indispo_dispo[name] = self.extract_indispo_dispo(name)

    def extract_indispo_dispo(self, name):
        indispo_dispo = []
        workBook = openpyxl.load_workbook(filename=f'data/indispo_dispo.xlsx')
        sheet = workBook[name]
        alph = list(string.ascii_lowercase)
        res = [[sheet[str(alph[i])+str(j)].value for i in range(1,8)] for j in range(3, 12)]
        return res

class Excel_Creator():
    def __init__(self):
        pass

    def data_from_list_to_dict(self,L_data):
        """translates the list of data to dictionnary (useful for excel creation)"""
        taille = len(L_data)
        return {"":['8h-10h', '10h-12h', '12h-14h', '14h-16h', '16h-18h', '18h-20h', '20h-22h', '22h-00h', '00h-02h'], "Lundi": [L_data[i][0] for i in range(taille)], "Mardi": [L_data[i][1] for i in range(taille)], "Mercredi": [L_data[i][2] for i in range(taille)], "Jeudi":  [L_data[i][3] for i in range(taille)], "Vendredi": [L_data[i][4] for i in range(taille)],  "Samedi": [L_data[i][5] for i in range(taille)], "Dimanche": [L_data[i][6] for i in range(taille)]}


    def create_excel(self, name, L_data):
        """crée le fichier excel"""
        self.name = name
        self.L_data = L_data
        self.data_dic = self.data_from_list_to_dict(self.L_data)
        if 'Général' in self.name: self.path = str(os.path.dirname(os.path.abspath(__file__))) + '/data'
        else: self.path = str(os.path.dirname(os.path.abspath(__file__))) + '/data/F_men_women'

        data_frame = pd.DataFrame(self.data_dic)
        writer = pd.ExcelWriter(f'{self.path}/{self.name}.xlsx')
        data_frame.to_excel(writer, index=False)
        writer.save()
        # read_file = pd.read_excel(f'{self.path}/{self.name}.xlsx')
        # read_file.to_csv(f'{self.path}/{self.name}.csv', index=False, header=True)


if __name__ == '__main__':
    print('main')
    names = ['Nathalie', 'André', 'Fred']
    indispo_dispo_excel = Excel_Reader(names)
    excel = Excel_Creator()
    excel.create_excel('Nathalie', indispo_dispo_excel.indispo_dispo['Nathalie'])
