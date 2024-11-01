import random
import numpy as np
import sys
import os
import tkinter as tk
from tkinter import ttk
from Planning_Manager.creneau import Creneau
from Planning_Manager.worker import Worker

from Excel_Manager.excel_manager import Excel_Reader, Excel_Creator, Excel_Modifier

class Planning_Filler():
    def __init__(self, workers, data, layer, must_shuffle=True, resu_general=None, workers_latest_menage=[], availabilities={}, last_time_had_most_crens={}, copy=None):
        self.data, self.layer = data, layer
        self.must_shuffle = must_shuffle
        self.workers = workers
        self.names = [worker.name for worker in workers] #the order of ames and workers must be the same
        self.availabilities = availabilities
        self.last_time_had_most_crens = last_time_had_most_crens
        self.workers_latest_menage = workers_latest_menage
        self.workers_to_visit = np.copy(self.workers) #a copy of workers that we can sort in any way
        self.crens, self.jours = ['12h15-13h', '13h-13h30', '17h30-20h30', '20h30-23h', '23h-00h'], ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
        self.soirees = self.data.soirees
        self.soirees_mefo = self.data.soirees_mefo
        self.occurences_workers = {worker: 0 for worker in self.workers}
        if copy != None:
            self.resu_general = copy.resu_general
        else:
            if resu_general != None :
                self.resu_general = resu_general #will be a list of list of workers
                self.fill_another_worker_on_party_and_menage_cren = True
            else :
                self.resu_general = [[[] for j in range(len(self.jours))] for i in range(len(self.crens))]
                self.fill_another_worker_on_party_and_menage_cren = False
                #self.fill_mefos()
            self.none_worker = Worker('None', color = "#C0C0C0")
            self.fill_planning()
            self.equalizing()
            # if resu_general != None :
            self.equalizing_coeffs()

    def __str__(self):
        colwidth = 15
        resu = '\n'
        nbre_occurence_worker = {}
        for i, row in enumerate(self.resu_general):
            outrow = ''
            for j, item in enumerate(row):
                self.resu_general[i][j].sort()
                for k in range(len(self.resu_general[i][j])) :
                    if k == 0: outrow += str(self.resu_general[i][j][k].name).ljust(colwidth)
                    else:
                        if str(self.resu_general[i][j][k].name) != 'None': outrow += str(' & ' + str(self.resu_general[i][j][k].name)).ljust(colwidth)
                        else: outrow += str(' ').ljust(colwidth)
                    if self.resu_general[i][j][k].name != 'None':
                        try:
                            nbre_occurence_worker[self.resu_general[i][j][k]] += 1
                        except:
                            nbre_occurence_worker[self.resu_general[i][j][k]] = 1
            resu += outrow + '\n'
        resu += '\n'
        # sorted_dic = dict(sorted(nbre_occurence_worker.items(), key=lambda x: x[1], reverse=True))
        self.coeffs_workers = self.get_coeffs_workers()
        resu1 = {}
        for w in range(len(self.workers)):
            resu1[self.workers[w]] = [len(self.workers[w].crens), self.coeffs_workers[self.workers[w]]]
        sorted_dic = dict(sorted(resu1.items(), key=lambda x: x[1], reverse=True))
        for worker in list(sorted_dic.keys()):
            resu += str(worker.name).ljust(colwidth) + f' : {sorted_dic[worker][0]}       : {sorted_dic[worker][1]}' + '\n'
        resu += '\n'
        resu += f'Planning équilibré à {max(list(self.coeffs_workers.values())) - min(list(self.coeffs_workers.values()))} coefficients près'
        resu += '\n'
        return resu

    def get_occurence_workers(self):
        """Find the number of crens a worker has"""
        resu = {}
        for i in range(len(self.crens)):
            for j in range(len(self.jours)):
                for k in range(len(self.resu_general[i][j])):
                    if self.resu_general[i][j][k].name != 'None':
                        try:
                            resu[self.resu_general[i][j][k]] += 1
                        except:
                            resu[self.resu_general[i][j][k]] = 1
        return resu

    def get_workers_most_working(self):
        """returns the worker who has the most crens"""
        return dict(sorted(self.occurences_workers.items(), key=lambda x: x[1]))

    def get_coeffs_workers(self):
        """returns the coeffs of all workers"""
        return dict(sorted({worker : worker.historic for worker in self.workers}.items(), key=lambda x : x[1]))

    def take_out_cren_from_worker(self, worker, cren, nbre_of_modifications=0):
        """we delete a cren from the worker's planning"""
        j, i = cren.j, cren.i
        for k in range(len(self.resu_general[i][j])):
            if self.resu_general[i][j][k] == worker:
                self.resu_general[i][j].pop(k)
                # print('self.resu_general got worker taken away')
                break
        for c in range(len(worker.crens)):
            if worker.crens[c] == cren and worker.crens[c] == cren:
                worker.crens.pop(c)
                worker.historic -= cren.coeff
                self.occurences_workers[worker] -= 1
                nbre_of_modifications += 1
                # print('worker got cren taken away')
                break
        return nbre_of_modifications

    def fill_mefos(self):
        if self.soirees_mefo != ['none']:
            for worker in self.workers:
                if worker.is_mefo :
                    for soiree in self.soirees_mefo:
                        print('---------', worker.name)
                        #if worker.name == 'Noé': self.resu_general[2][2].append(worker)
                        #if worker.name == 'Thibault': self.resu_general[3][2].append(worker)
                        cren = Creneau("mefo", self.soirees, soiree_mefo=soiree)
                        worker.crens.append(cren)
                        self.occurences_workers[worker] += 1
                        worker.historic += cren.coeff
                print(worker.crens)

    def fill_planning(self):
        if self.layer == 1 :
            for k in range(len(self.workers_latest_menage)):
                self.fill_planning_case(0, 6, worker=self.workers[self.names.index(self.workers_latest_menage[k])], test_1_verified=True, test_2_verified=True, test_3_verified=True, test_4_verified=True)

        for i in range(len(self.crens)):
            for j in range(len(self.jours)):
                # print("self.layer, i, j, workers_per_cren[i][j]", self.crens[i], self.jours[j], self.layer, i, j, self.data.workers_per_cren[i][j])
                if self.layer <= self.data.workers_per_cren[i][j]:
                    self.fill_planning_case(i, j)
                else:
                    self.resu_general[i][j].append(self.none_worker)
                self.sorted_workers_dic = self.get_workers_most_working()
                self.sorted_workers = list(self.sorted_workers_dic.keys())

    def test_1(self, worker_to_affect, i, j):
        """name has already a job in the day ?"""
        for cren in worker_to_affect.crens:
            if cren.j == j:
                # print(worker_to_affect.name, "can't take cren", self.jours[j], self.crens[i], "has already a job on", cren)
                return False
        return True  # on a regardé chaque créneau

    def test_2(self, worker_to_affect, i, j):
        """the name is available at this time ?"""
        # print("test_2 : ", worker_to_affect.name)
        # print(self.availabilities[worker_to_affect.name][i][j])
        return self.availabilities[worker_to_affect.name][i][j] == None

    def test_3(self, worker_to_affect, i, j):
        """last time the worker had menage was a long time ago"""
        # print('test_3 :',worker_to_affect.name, self.jours[j], self.crens[i], worker_to_affect.last_time_had_menage)
        if (j == 6 and i == 0):
            return worker_to_affect in self.workers_latest_menage
        else:
            return True

    def test_4(self, worker_to_affect, i, j, except_j=None):
        """name has already menage the day before or the day after ?"""
        if ((i == 3 and self.jours[j] not in self.soirees) or i == 4) or (j == 6 and i == 0): #On parle d'un ménage
            for cren in worker_to_affect.crens:
                if ((cren.i == 3 and self.jours[cren.j] not in self.soirees) or cren.i == 4) or (cren.j == 6 and cren.i == 0): #le worker a un menage
                    if cren.j != except_j: #On fait le test pour tous les créneaux de worker sauf le créneau au jour except_j
                        if cren.j == j-1 or cren.j == j+1: #Le créneau ménage en question est la veille ou le lendemain du créneau à tester
                            return False
        return True

    def test_5(self, worker_to_affect, i, j, printed=False):
        """si on parle d'un créneau du soir lors du mefo et que le worker est un mefo, il ne peut pas prendre le créneau"""
        return not(self.jours[j] in self.soirees_mefo and worker_to_affect.is_mefo)

    def test_swap(self, worker1, worker2, cren1, cren2):
        if cren1.j == cren2.j:
            test1_verified1, test1_verified2 = True, True
        else:
            test1_verified1 = self.test_1(worker1, cren2.i, cren2.j)
            test1_verified2 = self.test_1(worker2, cren1.i, cren1.j)
        if cren1.j == cren2.j-1 or cren1.j == cren2.j+1 :
            test4_verified1 = self.test_4(worker1, cren2.i, cren2.j, except_j=cren1.j)
            test4_verified2 = self.test_4(worker2, cren1.i, cren1.j, except_j=cren2.j)
        else:
            test4_verified1 = self.test_4(worker1, cren2.i, cren2.j)
            test4_verified2 = self.test_4(worker2, cren1.i, cren1.j)

        test2_verified1 = self.test_2(worker1, cren2.i, cren2.j)
        test2_verified2 = self.test_2(worker2, cren1.i, cren1.j)
        test3_verified1 = self.test_3(worker1, cren2.i, cren2.j)
        test3_verified2 = self.test_3(worker2, cren1.i, cren1.j)
        test5_verified1 = self.test_5(worker1, cren2.i, cren2.j)
        test5_verified2 = self.test_5(worker2, cren1.i, cren1.j)
        if test1_verified1 and test2_verified1 and test3_verified1 and test4_verified1 and test5_verified1:
            if test1_verified2 and test2_verified2 and test3_verified2 and test4_verified2 and test5_verified2:
                return [True]
        return [test1_verified1, test1_verified2, test2_verified1, test2_verified2, test3_verified1, test3_verified2, test4_verified1, test4_verified2, test5_verified1, test5_verified2]

    def fill_planning_case(self, i, j, worker=None, affect_cren_to_worker=True, test_1_verified=False, test_2_verified=False, test_3_verified=False, test_4_verified=False, test_5_verified=False):
        """
        We can specify a worker to know if the cren would fit the worker. If it does, we can choose if the function does the affectation itself or not.
        Plus, by specifying in args that test_1_verified is True, it makes all the tests but the test_1. Usefull if we want to swap crens from same day."""

        list_of_workers_in_priority = self.find_prority_worker()
        if worker == None :  #If we are not trying to fill in the date with a particular worker, we find one that fits the conditions
            n_workers = -1
            while not(test_1_verified) or not(test_2_verified) or not(test_3_verified) or not(test_4_verified) or not(test_5_verified):
                n_workers += 1
                if n_workers >= len(list_of_workers_in_priority):
                    # print(self.jours[j], self.crens[i], 'No worker fits the conditions !!')
                    return False
                else:
                    worker_to_affect = list_of_workers_in_priority[n_workers]
                    test_1_verified = self.test_1(worker_to_affect, i, j)
                    test_2_verified = self.test_2(worker_to_affect, i, j)
                    test_3_verified = self.test_3(worker_to_affect, i, j)
                    test_4_verified = self.test_4(worker_to_affect, i, j)
                    test_5_verified = self.test_5(worker_to_affect, i, j)
            if affect_cren_to_worker:
                self.resu_general[i][j].append(worker_to_affect)
                creneau = Creneau([j, i], self.soirees)
                worker_to_affect.crens.append(creneau)
                self.occurences_workers[worker_to_affect] += 1
                worker_to_affect.historic += creneau.coeff
            return True

        else: #We are trying to check if the worker fits the conditions to work at the specific date
            worker_to_affect = worker
            if not(test_1_verified) : test_1_verified = self.test_1(worker_to_affect, i, j)
            if not(test_2_verified) : test_2_verified = self.test_2(worker_to_affect, i, j)
            if not(test_3_verified) : test_3_verified = self.test_3(worker_to_affect, i, j)
            if not(test_4_verified) : test_4_verified = self.test_4(worker_to_affect, i, j)
            if not(test_5_verified) : test_5_verified = self.test_5(worker_to_affect, i, j)
            if test_1_verified and test_2_verified and test_3_verified and test_4_verified and test_5_verified:
                if affect_cren_to_worker: #the user wants th function to do the affectation itself
                    self.resu_general[i][j].append(worker_to_affect)
                    creneau = Creneau([j, i], self.soirees)
                    worker_to_affect.crens.append(creneau)
                    self.occurences_workers[worker_to_affect] += 1
                    worker_to_affect.historic += creneau.coeff
                return True
            else:
                # print(f'the worker {worker_to_affect} does not verify the conditions for {self.jours[j]} {self.crens[i]} ({test_1_verified}, {test_2_verified}, {test_3_verified}, {test_4_verified})')
                pass

    def find_prority_worker(self):
        self.sorted_workers_dic = self.get_workers_most_working()
        self.sorted_workers = list(self.sorted_workers_dic.keys())
        i = self.sorted_workers_dic[self.sorted_workers[0]]
        resu = []
        L = []
        for worker in self.sorted_workers:
            if self.occurences_workers[worker] == i:
                L.append(worker)
            else:
                i += 1
                random.shuffle(L)
                for j in L: resu.append(j)
                L = [worker]
        for j in L: resu.append(j)
        return resu

    def swap_cren(self, worker, worker2, cren1, cren2):
        self.fill_planning_case(cren1.i, cren1.j, worker2, test_1_verified=True, test_2_verified=True, test_3_verified=True, test_4_verified=True)
        self.fill_planning_case(cren2.i, cren2.j, worker, test_1_verified=True, test_2_verified=True, test_3_verified=True, test_4_verified=True)
        self.take_out_cren_from_worker(worker, cren1)
        self.take_out_cren_from_worker(worker2, cren2)
        self.coeffs_workers = self.get_coeffs_workers()
        
    def equalizing(self):
        def equalizing_process(workers2_to_consider, worker):
            for worker2 in workers2_to_consider:
                nbre_of_modifications = 0
                worker_crens = np.copy(worker.crens)
                for cren in worker_crens:
                    j, i = cren.j, cren.i
                    succeed = self.fill_planning_case(i, j, worker2)
                    if succeed: nbre_of_modifications = self.take_out_cren_from_worker(worker, cren, nbre_of_modifications)
                    if nbre_of_modifications == 1: return True

        self.occurences_workers = self.get_occurence_workers()
        self.sorted_workers_dic = self.get_workers_most_working()
        for worker in self.sorted_workers_dic.keys():
            workers2_to_consider = []
            for worker2 in self.sorted_workers_dic.keys():
                if self.sorted_workers_dic[worker] - self.sorted_workers_dic[worker2] == 2:
                    workers2_to_consider.append(worker2)
            random.shuffle(workers2_to_consider)
            equalizing_process(workers2_to_consider, worker)

        self.sorted_workers_dic = self.get_workers_most_working()
        self.sorted_workers = list(self.sorted_workers_dic.keys())

        if self.fill_another_worker_on_party_and_menage_cren:
            values = sorted(list(set(self.sorted_workers_dic.values())), reverse=True)
            occurence_biggest_ammount_crens = list(self.sorted_workers_dic.values()).count(values[0])
            last_time_had_most_crens_to_consider = [list(self.last_time_had_most_crens.keys())[k] for k in
                                                    range(occurence_biggest_ammount_crens)]
            sorted_workers_to_consider = np.copy([self.sorted_workers[-k] for k in range(len(self.sorted_workers))])
            for worker_name in last_time_had_most_crens_to_consider:
                for worker in self.workers :
                    if worker.name == worker_name : break
                if len(worker.crens) < values[0]:
                    for worker2 in sorted_workers_to_consider:
                        if worker2.name not in last_time_had_most_crens_to_consider:
                            # print(worker, len(worker.crens), worker2, len(worker2.crens))
                            if len(worker.crens) < len(worker2.crens):
                                worker2_crens = np.copy(worker2.crens)
                                for cren in worker2_crens:
                                    succeed = self.fill_planning_case(cren.i, cren.j, worker)
                                    if succeed:
                                        self.take_out_cren_from_worker(worker2, cren, 0)
                                        break
                                if succeed:
                                    # print(succeed, ':', worker, len(worker.crens), worker2, len(worker2.crens), cren)
                                    break

        self.sorted_workers_dic = self.get_workers_most_working()
        self.sorted_workers = list(self.sorted_workers_dic.keys())

    def equalizing_coeffs(self):

        def equalizing_process(worker, worker2):
            # print('\nequalizing between', worker.name, 'and', worker2.name, self.coeffs_workers[worker], self.coeffs_workers[worker2])
            # print(f'{worker.name} : {worker.crens}\n{worker2.name} : {worker2.crens}')
            if abs(self.coeffs_workers[worker] - self.coeffs_workers[worker2]) >= 1:
                crens1 = [[cren, cren.coeff] for cren in worker.crens]
                crens2 = [[cren, cren.coeff] for cren in worker2.crens]
                sorted_crens1 = [sorted(crens1, key=lambda x: x[1], reverse=False)[k][0] for k in range(len(worker.crens))]
                sorted_crens2 = [sorted(crens2, key=lambda x: x[1], reverse=True)[k][0] for k in range(len(worker2.crens))]
                for cren1 in sorted_crens1:
                    j1, i1 = cren1.j, cren1.i
                    worker2_can_take_cren = self.fill_planning_case(i1, j1, worker2, affect_cren_to_worker=False)
                    if worker2_can_take_cren:
                        for cren2 in sorted_crens2:
                            # print(f'{cren1}.coeff : {cren1.coeff}   ||   {cren2}.coeff : {cren2.coeff}')
                            if cren2.coeff > cren1.coeff:
                                if abs(self.coeffs_workers[worker]-self.coeffs_workers[worker2]) > abs((self.coeffs_workers[worker]-cren1.coeff+cren2.coeff) - (self.coeffs_workers[worker2]-cren2.coeff+cren1.coeff)) :
                                    j2, i2 = cren2.j, cren2.i
                                    worker1_can_take_cren = self.fill_planning_case(i2, j2, worker, affect_cren_to_worker=False)
                                    if worker1_can_take_cren:
                                        self.swap_cren(worker, worker2, cren1, cren2)
                                        return True
                #         print(f'{worker.name} cannot take any cren from {worker2.name}')
                    else:
                        jours_sorted_crens2 = [cren.j for cren in sorted_crens2]
                        if j1 in jours_sorted_crens2:
                            worker2_can_take_cren = self.fill_planning_case(i1, j1, worker2, affect_cren_to_worker=False, test_1_verified=True)
                            if worker2_can_take_cren:
                                cren2 = sorted_crens2[jours_sorted_crens2.index(j1)]
                                # print(f'SWAP {cren1}.coeff : {cren1.coeff}   ||   {cren2}.coeff : {cren2.coeff}')
                                if cren2.coeff > cren1.coeff:
                                    if abs(self.coeffs_workers[worker] - self.coeffs_workers[worker2]) > abs((self.coeffs_workers[worker] - cren1.coeff + cren2.coeff) - (self.coeffs_workers[worker2] - cren2.coeff + cren1.coeff)):
                                        j2, i2 = cren2.j, cren2.i
                                        worker1_can_take_cren = self.fill_planning_case(i2, j2, worker, affect_cren_to_worker=False, test_1_verified=True)
                                        if worker1_can_take_cren:
                                            self.swap_cren(worker, worker2, cren1, cren2)
                                            return True
                # print(f'{worker2.name} cannot take any cren from {worker.name}')
            return False

        self.coeffs_workers = self.get_coeffs_workers()
        nbre_loop1 = 0
        while max(list(self.coeffs_workers.values())) - min(list(self.coeffs_workers.values())) >= 1 and nbre_loop1 < 10:
            nbre_loop1 += 1
            for i in range(len(self.coeffs_workers)//2):
                worker, worker2 = list(self.coeffs_workers.keys())[i], list(self.coeffs_workers.keys())[-(i+1)]
                # print(f"working on {worker} and {worker2} ({self.coeffs_workers[worker]}, {self.coeffs_workers[worker2]})")
                succeed = equalizing_process(worker, worker2)
                if i == 0 and not(succeed): #We cheat a bit, if the first worker and the last one could not match, we try the second first with the last one and the second last with the first one
                    worker, worker2 = list(self.coeffs_workers.keys())[i], list(self.coeffs_workers.keys())[-(i + 2)]
                    equalizing_process(worker, worker2)
                    worker, worker2 = list(self.coeffs_workers.keys())[i+1], list(self.coeffs_workers.keys())[-(i + 1)]
                    equalizing_process(worker, worker2)
                self.coeffs_workers = self.get_coeffs_workers()

class The_Planning_Maker():
    def __init__(self, data):
        self.data = data
        self.names = self.data.names
        self.historic_filename = self.data.historic_filename
        self.dispo_filename = self.data.dispo_filename
        self.soirees = self.data.soirees
        self.total_attempt = int(self.data.nbre_repetition)
        self.availabilities = Excel_Reader(self.names, self.dispo_filename, type='indispo').data_of_names
        historic_ = Excel_Reader(self.names, self.historic_filename, type='historic').data_of_names
        self.historic = [list(historic_.values())[i][0] for i in range(len(self.names))]
        self.dic_last_time_had_menage_not_sorted = {list(historic_.keys())[i] : list(historic_.values())[i][1] for i in range(len(historic_))}
        self.dic_last_time_had_menage = dict(sorted(self.dic_last_time_had_menage_not_sorted.items(), key=lambda x:x[1], reverse=True))
        self.last_time_had_menage = [float(list(historic_.values())[i][1]) for i in range(len(self.names))]
        self.last_time_had_most_crens_not_sorted = {list(historic_.keys())[i] : list(historic_.values())[i][2] for i in range(len(historic_))}
        self.last_time_had_most_crens = dict(sorted(self.last_time_had_most_crens_not_sorted.items(), key=lambda x:x[1], reverse=True))
        self.workers_latest_menage = self.get_workers_latest_menage()
        self.get_progress_bar()
        self.planning = self.find_best_planning()
        self.kill_progress_bar()

    def __str__(self):
        return str(self.planning)

    def get_progress_bar(self):
        self.progress_bar_app = tk.Tk()
        self.progress_bar_app.overrideredirect(True)
        self.progress_bar_app.attributes('-topmost', True)
        self.progress_bar_app.geometry(f'400x170+600+350')
        self.progress_bar_app.configure(bg='navy')
        self.progress_bar = ttk.Progressbar(self.progress_bar_app, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.label = tk.Label(self.progress_bar_app, text='0%', bg='navy', fg='white', font='Arial 17 bold')
        self.progress_bar.pack(pady=30)
        self.label.pack(pady=30)
        self.progress_bar_app.update()

    def refresh_progress_bar(self, i):
        # sys.stdout.write('\r' + f"{int(i * 100 / self.total_attempt)}%")
        self.progress_bar['value'] = int(i * 100)
        self.label['text'] = f"{int(i * 100)}%"
        self.progress_bar_app.update_idletasks()
        self.progress_bar_app.update()

    def kill_progress_bar(self):
        self.progress_bar_app.destroy()

    def get_workers_latest_menage(self):
        resu = []
        for k in range(len(list(self.dic_last_time_had_menage))):
            name_worker_to_affect = list(self.dic_last_time_had_menage)[k]
            if self.availabilities[name_worker_to_affect][0][6] == None:
                resu.append(name_worker_to_affect)
            if len(resu) == self.data.workers_per_cren[0][6]: break
        return resu

    def find_best_planning(self):
        workers = [Worker(self.names[i], username=self.data.usernames[i], color=self.data.colors[i], last_time_had_menage=self.last_time_had_menage[i], historic=self.historic[i], mefos=self.data.mefos) for i in range(len(self.names))]
        self.max_worker_in_cren = max([max(self.data.workers_per_cren[i]) for i in range(len(self.data.workers_per_cren))])
        # On crée un premier planning qu'on enregistre. Planning kept sera le meilleur planning que l'on gardera à chaque itération
        planning_kept = Planning_Filler(workers, self.data, 1, availabilities=self.availabilities, workers_latest_menage=self.workers_latest_menage, last_time_had_most_crens=self.last_time_had_most_crens)
        for j in range(self.max_worker_in_cren-1):
            planning_kept = Planning_Filler(planning_kept.sorted_workers, self.data, j+2, availabilities=self.availabilities, resu_general=planning_kept.resu_general, workers_latest_menage=self.workers_latest_menage, last_time_had_most_crens=self.last_time_had_most_crens)

        for i in range(self.total_attempt):
            self.refresh_progress_bar(i/self.total_attempt)
            workers = [Worker(self.names[i], username=self.data.usernames[i], color=self.data.colors[i], last_time_had_menage=self.last_time_had_menage[i], historic=self.historic[i], mefos=self.data.mefos) for i in
                       range(len(self.names))]
            planning = Planning_Filler(np.copy(workers), self.data, 1, availabilities=self.availabilities, workers_latest_menage=self.workers_latest_menage, last_time_had_most_crens=self.last_time_had_most_crens)
            for j in range(self.max_worker_in_cren - 1):
                planning = Planning_Filler(planning.sorted_workers, self.data, j+2, availabilities=self.availabilities, resu_general=planning.resu_general, workers_latest_menage=self.workers_latest_menage, last_time_had_most_crens=self.last_time_had_most_crens)
            if max(list(planning.coeffs_workers.values())) - min(list(planning.coeffs_workers.values())) <= max(
                list(planning_kept.coeffs_workers.values())) - min(
                list(planning_kept.coeffs_workers.values())): #Si le nouveau planning est meilleur que celui gardé, on garde le meilleur
                planning_kept = planning
        sys.stdout.write('\r')
        self.refresh_progress_bar(99 / 100)
        print(planning_kept)
        return planning_kept

    def save_data_in_excel(self, filename=None):
        self.excel_creator = Excel_Creator(self.planning.jours, self.planning.crens, filename=filename)
        self.excel_creator.create_planning('General_planning', self.planning.resu_general)
        workers_planning = []
        for worker in self.planning.workers:
            worker.planning = worker.get_planning(len(self.planning.crens), len(self.planning.jours), self.planning.availabilities)
            workers_planning.append(worker.planning)
        self.excel_creator.create_planning('Planning_for_each_worker', workers_planning, workers=self.planning.workers, caller=self)
        self.excel_creator.create_planning('Publishable_planning', workers_planning, workers=self.planning.workers, caller=self)

    def update_historic_excel(self):
        excel = Excel_Modifier(self.historic_filename)
        nbre_crens_per_worker = sorted(list(set(self.planning.sorted_workers_dic.values())), reverse=True)
        for i in range(len(self.names)):
            try: self.refresh_progress_bar((i+len(self.names))/(len(self.planning.workers)+len(self.names)))
            except: pass
            for worker in self.planning.workers:
                if worker.name == self.names[i]: break
            value = self.planning.coeffs_workers[worker]
            excel.modify_case(f'B{i+2}', value)
            excel.modify_case(f'C{i+2}', float(excel.get_value(f'C{i+2}'))+1)
            for cren in worker.crens:
                if cren.type == 'menage':
                    excel.modify_case(f'C{i+2}', 0)
                    break
            if len(worker.crens) == nbre_crens_per_worker[0]:
                excel.modify_case(f'D{i+2}', 0)
            else:
                excel.modify_case(f'D{i+2}', float(excel.get_value(f'D{i+2}'))+1)

