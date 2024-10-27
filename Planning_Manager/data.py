import pandas as pd
import os
from Planning_Manager import worker
import random

from Excel_Manager.excel_manager import Excel_Reader, Excel_Creator, Excel_Modifier


class Data():
    """Ceci est l'objet regroupant les données par défaut. Chaque donnée peut être modifiée en utilisant l'application."""

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        
        df = pd.read_excel("Data/team_data.xlsx")
    
        # Skip the first row if it contains the column titles
        self.init_names = df.iloc[0:, 0].tolist()  # Column 1 (index 0) for names
        self.names = df.iloc[0:, 0].tolist()  # Column 1 (index 0) for names
        random.shuffle(self.names)
        self.usernames = df.iloc[0:, 1].tolist()  # Column 2 (index 1) for surnames
        self.admin = [item for item in df.iloc[0:, 2].tolist() if isinstance(item, str)]  # Column 2 (index 1) for admin
        self.mefos = [item for item in df.iloc[0:, 3].tolist() if isinstance(item, str)]  # Column 2 (index 1) for mefo
        self.colors = ["#3FB2C1", "#9A5454", "#7030A0", "#00FF00", "#008000", "#8EA9DB", "#203764", "#305496",
                       "#FF9900", "#FF00FF", "#CCA434", "#00FF9A", "#FFD700", "#C000C0", "#B22222", "#FF0000"]
        self.dispo_filename = f"{path[:-16]}/Data/indispo_dispo.xlsx"
        self.historic_filename = f"{path[:-16]}/Data/historic.xlsx"
        self.nbre_repetition = 5  # nombre de plannings dans l'échantillon à étudier. On ne gardera que le meilleur planning de l'échantillon
        self.soirees = ['none']
        self.soirees_mefo = ['none']
        self.workers_per_cren = [[2, 2, 2, 0, 2, 0, 3], [2, 2, 2, 2, 2, 0, 0], [2, 2, 2, 2, 2, 2, 2],
                                 [2, 2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0]]
        self.max_worker_in_cren = self.get_max_worker_in_cren()

        self.availabilities = Excel_Reader(self.names, self.dispo_filename, type='indispo').data_of_names
        self.historic_ = Excel_Reader(self.names, self.historic_filename, type='historic').data_of_names
        self.historic = [list(self.historic_.values())[i][0] for i in range(len(self.names))]
        self.last_time_had_menage = [float(list(self.historic_.values())[i][1]) for i in range(len(self.names))]
        self.workers = [worker.Worker(self.init_names[i], username=self.usernames[i], color=self.colors[i], last_time_had_menage=self.last_time_had_menage[i], historic=self.historic[i], mefos=self.mefos) for i in range(len(self.names))]
        print(self.admin)
        print(self.init_names)

    def __str__(self):
        return str(self.workers_per_cren)

    def get_max_worker_in_cren(self):
        return max([max(self.workers_per_cren[i]) for i in range(len(self.workers_per_cren))])

    def sort_as_default(self, workers):
        resu = []
        for i in range(len(self.init_names)):
            for w in range(len(workers)):
                if workers[w].name == self.init_names[i]: resu.append(workers[w])
        return resu

    def sort_by_cren_then_coeff(self, workers, planning):
        plan = planning
        resu = {}
        for w in range(len(workers)):
            resu[workers[w]] = [len(workers[w].crens), plan.coeffs_workers[workers[w]]]
        resu2 = dict(sorted(resu.items(), key=lambda x: x[1], reverse=True))
        return resu2

