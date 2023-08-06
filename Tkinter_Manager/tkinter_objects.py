import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import os
import yagmail
from Planning_Manager.planning_manager import The_Planning_Maker, Planning_Filler, Creneau
from Sender_Manager.sender_manager import Message_sender
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

class Tkinter_button(tk.Button):
    '''Créer les boutons de commande'''
    def __init__(self, application, id, caller=None):
        tk.Button.__init__(self, application)
        try:
            self.app = application
            self.jours, self.crens = self.app.jours, self.app.crens
        except:
            self.app = application.master
            self.jours, self.crens = self.app.jours, self.app.crens
        if not(caller) : self.caller = self.app
        else: self.caller = caller
        self.id = id

        if self.app.name == 'main':
            if self.id == 0:
                self.bg, self.fg, self.cursor, self.command, self.state = '#a4deaa', 'black', 'hand2', self.create_planning, 'unclicked'
                self.config(text='Créer le planning', width=20, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold',
                            relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y = 450, 670

            elif self.id == 1:
                self.bg, self.fg, self.cursor, self.command, self.state = 'navy', 'white', 'hand2', self.show_creneaux, 'unclicked'
                self.config(text='Créneaux', width=7, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 10 ',
                            relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y = 700, 410

            elif self.id == 2:
                self.bg, self.fg, self.cursor, self.command, self.state = 'navy', 'white', 'hand2', self.show_resu, 'unclicked'
                self.config(text='Résultats', width=7, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 10 ',
                            relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y, self.right_x = 2000, 670, 700

            if self.id >= 1000:
                self.cursor, self.command = 'hand2', self.choose_file
                img = Image.open("Ressources/folder_icon.png")
                resized_img = img.resize((20, 20), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(resized_img)
                self.config(image=photo, cursor='hand2', bg='light blue', font='Arial 10', relief=tk.RAISED, command=self.command)
                self.image = photo
                self.x, self.y = 680, self.caller.y

        elif self.app.name == 'crens':
            if self.id < 35:
                matrix = np.ndarray(shape=(5,7), buffer=np.array(list(range(35))), dtype=int)
                self.row_cren, self.column_cren = self.id//len(matrix[0]), self.id%len(matrix[0])
                self.row, self.column = self.row_cren + 2, self.column_cren + 1
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
                self.bg, self.disable_bg, self.fg, self.cursor = 'navy', 'grey', 'white', 'hand2'
                self.config(text='2', width=10, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold',
                            relief=tk.RAISED, cursor=self.cursor)
                self.bind('<Button-1>', self.active_cren)
                self.bind('<Button-3>', self.active_cren)
                self.configure_button()
            elif self.id == 35:
                self.row, self.column = 7, 8
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 5, 5
                self.bg, self.disable_bg, self.fg, self.cursor = '#a4deaa', 'grey', 'black', 'hand2'
                self.config(text='Valider', width=7, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold',
                            relief=tk.RAISED, cursor=self.cursor)
                self.bind('<Button-1>', self.valid_crens)

        elif self.app.name == 'resu':
            if self.id == 0:
                self.bg, self.fg, self.cursor, self.command, self.state = '#a4deaa', 'black', 'hand2', self.create_excels, 'unclicked'
                self.config(text='Créer les excels', width=20, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold', relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y = 1200, 550
            elif self.id == 1:
                self.bg, self.fg, self.cursor, self.command, self.state = 'navy', 'white', 'hand2', self.send_mail, 'unclicked'
                self.config(text='Envoyer les messages', width=20, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold', relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y = 1200, 630

        elif isinstance(self.app, Tkinter_canvas):
            self.parent = self.app
            self.app = self.parent.app
            self.max_worker_in_cren = self.parent.max_worker_in_cren
            if self.id < len(self.crens)*self.max_worker_in_cren:
                workers_to_consider = [self.app.main_app.planning.resu_general[i][self.parent.id][k] for i in range(len(self.crens)) for k in range(self.max_worker_in_cren)]
                self.worker = workers_to_consider[self.id]
                self.row, self.column = int(self.id/self.max_worker_in_cren) + 2, self.id%self.max_worker_in_cren + 1
                self.jour, self.cren = self.app.jours[self.parent.id], self.app.crens[self.row-2]
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
                self.bg, self.disable_bg, self.fg, self.cursor = workers_to_consider[self.id].color, 'grey', 'white', 'hand2'
                self.config(text=workers_to_consider[self.id].name, bg=self.bg, fg=self.fg,
                            font='Arial 10', width=7,
                            relief=tk.RAISED, cursor=self.cursor)
                self.bind('<Button-1>', self.select_worker)
                self.bind('<Button-3>', self.select_worker)

    def show_creneaux(self):
        if self.state == 'unclicked': self.state = 'clicked'
        # elif self.state == 'clicked': self.state = 'unclicked'

    def show_resu(self):
        if self.state == 'unclicked': self.state = 'clicked'

    def create_planning(self):
        self.app.planning_maker = The_Planning_Maker(self.app.data)
        self.app.planning = self.app.planning_maker.planning
        self.app.init_planning = Planning_Filler(np.copy(self.app.planning.workers), self.app.planning.init_data, self.app.planning.layer, copy=self.app.planning)
        self.state = 'clicked'
        self.app.buttons[2].x = self.app.buttons[2].right_x
        self.app.buttons[2].place(x=self.app.buttons[2].x, y=self.app.buttons[2].y)
        self.app.buttons[2].flash()

    def create_excels(self):
        self.app.main_app.planning_maker.get_progress_bar()
        self.app.main_app.planning_maker.save_data_in_excel()
        self.app.main_app.planning_maker.update_historic_excel()
        self.app.main_app.planning_maker.kill_progress_bar()
        print('Plannings créés')
        self.app.label_error['text'] = 'Plannings créés'
        self.app.label_error['fg'] = 'navy'
        self.app.label_error.place(x=self.app.label_error.x, y=520)

    def unfocus(*args):
        self = args[0]
        self.app.labels[0].focus()

    def choose_file(self, *args):
        filename = str(askopenfilename())
        x = filename.split('/')
        resu = ''
        for i in range(len(x) - 1, -1, -1):
            newresu = '/' + x[i] + resu
            if len(newresu) > 30: break
            else: resu = newresu
        self.caller.delete(0, tk.END)
        self.caller.insert(0, resu)
        self.caller.enter(value=filename)

    def active_cren(self, *args):
        event = args[0]
        coeff = 1
        if int(event.num) == 1: coeff = 1
        elif int(event.num) == 3: coeff = -1
        self['text'] = str(max(int(self['text']) + coeff*1, 0))
        if self['text'] == '0': self['bg'] = self.disable_bg
        else : self['bg'] = self.bg

    def configure_button(self):
        workers_per_cren = self.app.main_app.data.workers_per_cren
        if workers_per_cren[self.row_cren][self.column_cren] == 0: self['bg'], self['text'] = self.disable_bg, 0
        else: self['bg'], self['text'] = self.bg, str(workers_per_cren[self.row_cren][self.column_cren])

    def valid_crens(self, *args):
        workers_per_cren = np.zeros(len(self.app.buttons)-1)
        for i in range(len(self.app.buttons)-1) :
            workers_per_cren[i] = int(self.app.buttons[i]['text'])
        workers_per_cren_copy = list(np.copy(workers_per_cren))
        resu = []
        for i in range(5):
            resu.append([])
            for j in range(7):
                value = int(workers_per_cren_copy.pop(0))
                resu[-1].append(value)
                if i == 4 and value != 0:
                    self.app.main_app.data.soiree = self.jours[j]
                    self.app.main_app.entrys[2].enter(value=self.jours[j])
        self.app.main_app.data.workers_per_cren = resu
        self.app.order_to_kill = True

    def select_worker(self, *args):
        try: order = args[0].num
        except: order = args[0]
        if self['text'] != 'None' and self['text'] != 'none':
            if int(order) == 1 or int(order) == 1000:
                if self.app.first_worker_selected == None:
                    self['relief'] = tk.SOLID
                    self['borderwidth'] = 4
                    if int(order) == 1 : self.app.after(1, lambda self: self.configure(relief='solid'), self)
                    self.app.first_worker_selected = self
                else :
                    planning = self.app.main_app.planning_maker.planning
                    worker1 = self.app.first_worker_selected.worker
                    worker2 = self.worker
                    cren1, cren2 = Creneau([self.app.first_worker_selected.jour, self.app.first_worker_selected.cren]), Creneau([self.jour, self.cren])
                    success = planning.test_swap(worker1, worker2, cren1, cren2)
                    if all(success):
                        planning.swap_cren(worker1, worker2, cren1, cren2)
                        self.app.first_worker_selected.worker = worker2
                        self.app.first_worker_selected['bg'] = worker2.color
                        self.app.first_worker_selected['text'] = worker2.name
                        self.worker = worker1
                        self['bg'] = worker1.color
                        self['text'] = worker1.name
                        self.app.historic_modifications.append([self.app.first_worker_selected, self])
                        self.app.canvas[1].itemconfig(self.app.canvas[1].text, text=self.app.canvas[1].get_text())
                    else:
                        messages = [f'{worker1.name} has already a cren in {cren2.jour}', f'{worker1.name} is not available on cren {cren2}', f'{worker1.name} had already menage not a long time ago', f'{worker2.name} has already a cren in {cren1.jour}', f'{worker2.name} is not available on cren {cren1}', f'{worker2.name} had already menage not a long time ago']
                        self.app.label_error['text'] = messages[success.index(False)]
                        self.app.label_error['fg'] = 'red'
                        self.app.label_error.place(x=self.app.label_error.x, y=520)

                    self.app.first_worker_selected['borderwidth'] = 2
                    self.app.first_worker_selected['relief'] = tk.RAISED
                    self.app.first_worker_selected['highlightthickness'] = 2
                    self['borderwidth'] = 2
                    self['relief'] = tk.RAISED
                    self.app.first_worker_selected = None

            elif int(order) == 3:
                self.app.first_worker_selected = None
                self['borderwidth'] = 2
                self['relief'] = tk.RAISED

    def send_mail(self):
        receivers, messages = [], []
        workers = self.app.main_app.planning.workers
        for worker in [workers[0]] :
            receivers.append(worker.username)
            root_message = f'Hello {worker.name} !! Voici ton planning pour la semaine.\n\n'
            messages.append(root_message)
            for cren in worker.crens:
                messages[-1] += cren.jour + ' ' + cren.type + '\n'
            if self.app.main_app.data.soiree != 'none':
                messages[-1] += f'Cette semaine la soirée est {self.app.main_app.data.soiree}\n'
        sender = Message_sender(receivers=receivers, messages=messages)
        print('Messages envoyés')

class Tkinter_label(tk.Label):
    def __init__(self, application, id):
        tk.Label.__init__(self, application)
        try:
            self.app = application
            self.jours, self.crens = self.app.jours, self.app.crens
        except:
            self.app = application.master
            self.jours, self.crens = self.app.jours, self.app.crens
        self.id = id
        if self.app.name == 'main':
            if self.id == 0:
                self.config(text='Interface de pilotage du\ncréateur de planning',
                            bg='light blue', fg='navy', width=30, font='Impact 30 bold')
                self.x, self.y = 85, 40
            elif self.id == 1:
                self.config(text="Emplacement du fichier Excel des disponibilités", bg='light blue', fg='navy', font='Arial 11 italic bold')
                self.x, self.y = 390, 250
            elif self.id == 2:
                self.config(text="Emplacement du fichier Excel des historiques", bg='light blue', fg='navy', font='Arial 11 italic bold')
                self.x, self.y = 390, 320
            elif self.id == 3:
                self.config(text="Jour de la soirée", bg='light blue', fg='navy', font='Arial 11 italic bold')
                self.x, self.y = 390, 400
            elif self.id == 4:
                self.config(text="Application créée par l'équipe Foy'z 25", bg='light blue', fg='navy', font='Arial 9 italic')
                self.x, self.y = 290, 750
            elif self.id == 5:
                self.config(text="Taille de l'échantillon de plannings à étudier", bg='light blue', fg='navy', font='Arial 11 italic bold')
                self.x, self.y = 390, 510
        elif self.app.name == 'crens' :
            self.config(bg='light blue')
            if self.id == 0:
                self.config(text='Créateur de planning : Créneaux', fg='navy', font='Impact 28 bold')
                self.row, self.column = 0, 2
                self.columnspan, self.rowspan, self.padx, self.pady = 5, 1, 2, 2
            elif self.id in range(1, 8):
                self.config(text=f'{self.jours[self.id-1]}')
                self.row, self.column = 1, self.id
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
            elif self.id in range(8, 13):
                self.config(text=f'{self.crens[self.id - 8]}')
                self.row, self.column = self.id-8+2, 0
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
        elif self.app.name == 'resu':
            self.config(bg='light blue')
            if self.id == 0:
                self.config(text='Créateur de planning : Résultats', fg='navy', font='Impact 28 bold')
                self.padx, self.pady = 2, 30
            elif self.id == 1000:
                self.config(text='', fg='red', font='Arial 13')
                self.padx, self.pady = 2, 30
                self.x, self.y = 1000, 6000
                self.bind('<Double-Button-1>', self.hide)
        elif isinstance(self.app, Tkinter_canvas):
            self.parent = application
            if self.parent.name == 'planning_canvas':
                if self.id < 2*len(self.crens):
                    """Labels de créneaux"""
                    self.config(text=self.crens[self.id%len(self.crens)])
                    self.row, self.column = self.id+2+(self.id//len(self.crens)), 1
                    self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
                    if self.id == 0: self.pady = (17,0)
                    elif self.id == 5: self.pady = (30,5)
            elif self.parent.name in self.jours:
                self.config(bg='light blue')
                if self.id == 0:
                    self.config(text=self.parent.name)
                    self.row, self.column = 1, 1
                    self.columnspan, self.rowspan, self.padx, self.pady = self.parent.max_worker_in_cren, 1, 2, 2

    def hide(self, *args):
        self.place(x=self.x, y=self.y)

class Tkinter_canvas(tk.Canvas):
    def __init__(self, parent, id):
        tk.Canvas.__init__(self, parent)
        self.id = id

        if not(isinstance(parent, Tkinter_canvas)):
            try:
                name = parent.name
                self.app = parent
            except:
                self.app = parent.master #le parent est la Frame, on veut donc le master du parent
            if self.app.name == 'main':
                if self.id == 0:
                    self.config(bg='white', height=535, width=277, relief='raised')
                    self.x, self.y = 60, 200
                    self.create_text(20, 20, anchor='w', text='Equipe',
                                     font='Arial 11 italic bold', fill='navy')
            elif self.app.name == 'resu':
                if self.id == 0:
                    self.name = 'planning_canvas'
                    self.config(bg='light blue')
                    self.jours, self.crens = self.app.main_app.jours, self.app.main_app.crens
                    self.labels = [Tkinter_label(self, i) for i in range(2*len(self.crens))]
                    self.canvas = [Tkinter_canvas(self, i) for i in range(len(self.jours))]
                    self.objects = [self.labels, self.canvas]
                    self.place_all_objects()
                elif self.id == 1:
                    self.name = 'equilibre_canvas'
                    self.config(bg='light blue', height=400, width=400)
                    resu = self.get_text()
                    self.text = self.create_text(40, 170, anchor='w', text=resu, font='TkFixedFont', fill='navy')
                    self.pady = 20

        elif isinstance(parent, Tkinter_canvas):
            self.parent = parent
            self.app = self.parent.app
            self.config(bg='light blue')
            self.jours, self.crens = self.parent.jours, self.parent.crens
            self.max_worker_in_cren = self.app.main_app.data.get_max_worker_in_cren()
            if self.parent.name == 'planning_canvas':
                """ Canvas des jours """
                self.name = self.jours[self.id]
                self.row, self.column = (self.id//4 * (len(self.crens)+2))+1, (self.max_worker_in_cren*self.id + 2) % (4*self.max_worker_in_cren)
                self.columnspan, self.rowspan, self.padx, self.pady = self.max_worker_in_cren, len(self.crens)+1, 2, 2
                self.labels = [Tkinter_label(self, i) for i in range(1)]
                self.buttons = [Tkinter_button(self, i) for i in range(self.max_worker_in_cren * len(self.crens))]
                self.objects = [self.labels, self.buttons]
                self.place_all_objects()

    def get_text(self):
        if self.app.name == 'resu' and self.id == 1:
            resu = ''
            plan = self.app.main_app.planning
            nbre_occurence_worker = plan.get_occurence_workers()
            sorted_dic = dict(sorted(nbre_occurence_worker.items(), key=lambda x: x[1], reverse=True))
            for worker in sorted_dic:
                resu += str(worker.name).ljust(15) + f' : {sorted_dic[worker]}       : {plan.coeffs_workers[worker]}' + '\n'
            resu += '\n'
            resu += f'Planning équilibré à {max(list(plan.coeffs_workers.values())) - min(list(plan.coeffs_workers.values()))} coefficients près'
            return resu

    def place_all_objects(self):
        for list_objects in self.objects:
            for object in list_objects:
                object.grid(row=object.row, column=object.column, columnspan=object.columnspan,
                                rowspan=object.rowspan, pady=object.pady, padx=object.padx)

class Tkinter_checkbox(tk.Button):
    def __init__(self, app, id):
        tk.Button.__init__(self)
        self.app = app
        self.id = id

        if self.id in range(len(self.app.data.init_names)):
            self.x, self.y = 75, 240 + self.id*30
            self.bg, self.activebg, self.fg, self.cursor, self.state, self.command = '#dea4a5', '#a4deaa','black', 'hand2', 1, self.check
            self.text = self.app.data.names[self.id]
            self.config(text=self.text, bg=self.activebg, fg=self.fg, cursor=self.cursor, relief=tk.RAISED, command=self.command, font='Arial 10', width=30, height=1)

    def check(self):
        if self['bg'] == self.activebg:
            self.config(bg=self.bg)
            self.state = 0
            self.app.data.names.pop(self.app.data.names.index(self.text))
        else:
            self.config(bg=self.activebg)
            self.state = 1
            self.app.data.names.insert(self.id, self.text)

class Tkinter_entry(tk.Entry):
    def __init__(self, application, id):
        tk.Entry.__init__(self, application)
        self.id = id
        self.app = application
        self.config(width=30, font='Arial 12', fg='black')
        if self.id < 2:
            if self.id == 0:
                self.insert(0, self.app.data.dispo_filename)
                self.x, self.y = 390, 280
                self.value, self.default_value = self.app.data.dispo_filename, self.app.data.dispo_filename
            elif self.id == 1:
                self.insert(0, self.app.data.historic_filename)
                self.x, self.y = 390, 350
                self.value, self.default_value = self.app.data.historic_filename, self.app.data.historic_filename
            self.button = Tkinter_button(self.app, 1000 + self.id, caller=self)
            self.button.place(x=self.button.x, y=self.button.y)
        elif self.id == 2:
            self.insert(0, str(self.app.data.soiree))
            self.x, self.y = 390, 430
            self.value, self.default_value = str(self.app.data.soiree), str(self.app.data.soiree)

        self.bind('<Return>', self.enter)
        self.bind('<Button-1>', self.type)
        self.bind_all('<Key>', self.type)


    def type(*args):
        self, event = args[0], args[1]
        if event.char == event.keysym or event.char == '<Button-1>':
            if self['fg'] == 'grey':
                self.delete(0, tk.END)
                self.config(fg='black')
            if self['fg'] == 'green':
                self.config(fg='black')

    def enter(self, event=None, value=None, *args):
        if value == None: #if the user typed manually, the value arg is None so we get what was typed
            self.value = self.get()
        else: #if the user used the button file, the button returns a value in value arg
            self.value = value
        if self.id == 0:
            if self.get() != '' and self.get() != '/':
                self.config(fg='green')
                self.app.data.dispo_filename = self.value
                self.app.labels[0].focus()
            else:
                self.app.data.dispo_filename = self.default_value
                self.insert(0, self.default_value)
                self.config(fg='green')
                self.app.labels[0].focus()
                self.value = self.default_value
            print('dispo_filename =', self.value)
        elif self.id == 1:
            if self.get() != '' and self.get() != '/':
                self.config(fg='green')
                self.app.data.historic_filename = self.value
                print('historic_filename =', self.value)
                self.app.labels[0].focus()
            else:
                self.app.data.historic_filename = self.default_value
                print('historic_filename =', self.default_value)
                self.insert(0, self.default_value)
                self.config(fg='green')
                self.app.labels[0].focus()
                self.value = self.default_value
        elif self.id == 2:
            if self.get() != '' and self.get() != '/':
                self.config(fg='green')
                self.value = self.value.lower()
                self.app.data.soiree = self.value
                for k in range(2, 5):
                    self.app.data.workers_per_cren[k][self.app.jours.index(self.value)] = 3
                print('soiree =', self.value)
                self.delete(0, tk.END)
                self.insert(0, self.value)
                self.app.labels[0].focus()
            else:
                self.app.data.soiree = self.default_value
                print('soiree =', self.default_value)
                if self.default_value != 'none': indice = self.app.jours.index(self.default_value)
                else: indice = None
                for i in range(7):
                    if i != indice:
                        if self.app.data.workers_per_cren[4][i] != 0:
                            self.app.data.workers_per_cren[2][i] = 2
                            self.app.data.workers_per_cren[3][i] = 2
                            self.app.data.workers_per_cren[4][i] = 0
                    else:
                        for k in range(2, 5):
                            self.app.data.workers_per_cren[k][i] = 3
                self.insert(0, self.default_value)
                self.config(fg='grey')
                self.value = self.default_value
                self.app.labels[0].focus()

class Tkinter_scale(tk.Scale):
    def __init__(self, application, id):
        tk.Scale.__init__(self, application)
        self.id = id
        self.app = application

        if self.id == 0:
            self.value = 0
            self.x, self.y = 390, 540
            self.bg, self.fg, self.cursor = 'light blue', 'black', 'hand2'
            self.config(orient='horizontal', to=100, cursor=self.cursor, font='Arial 10',
                        resolution=1, tickinterval=25, length=350, bg=self.bg, fg=self.fg, command=self.get_value)
            self.set(self.app.data.nbre_repetition)

    def get_value(self, value):
        self.value = value
        self.app.data.nbre_repetition = value

class Tkinter_frame(tk.Frame):
    def __init__(self, application, id):
        tk.Frame.__init__(self, application)
        self.id = id
        self.app = application
        self.config(bg='light blue')
        if self.id == 0:
            self.x, self.y = 0, 30
            self.offset, self.frame_x, self.frame_x_init = 0, 0, 0
            # self.bind("<MouseWheel>", self._on_mousewheel)

        if self.id == 1:
            self.x, self.y = 600, 300
            self.config(bg='yellow')
            self.offset, self.frame_y, self.frame_y_init = 0, 0, 0
            self.canva = tk.Canvas(self.app, bg='light blue', height=600)
            resu = ''
            plan = self.app.main_app.planning
            nbre_occurence_worker = plan.get_occurence_workers()
            sorted_dic = dict(sorted(nbre_occurence_worker.items(), key=lambda x: x[1], reverse=True))
            coeffs_workers = plan.get_coeffs_workers()
            for worker in sorted_dic:
                resu += str(worker.name).ljust(15) + f' : {sorted_dic[worker]}       : {plan.coeffs_workers[worker]}' + '\n'
            resu += '\n'
            resu += f'Planning équilibré à {max(list(plan.coeffs_workers.values())) - min(list(plan.coeffs_workers.values()))} coefficients près'

            self.canva.create_text(40, 170, anchor='w', text=resu,
                             font='TkFixedFont', fill='navy')
            self.canva.pack(side=tk.BOTTOM)
            # self.canva.bind("<MouseWheel>", self._on_mousewheel)

            # s = ttk.Scrollbar(self.app, orient=tk.VERTICAL, command=self.canva.yview)
            # s.pack(side=tk.RIGHT, fill='y', expand=False)
            # self.canva.configure(yscrollcommand=s.set)

    def _on_mousewheel(self, event):
        if self.id == 0:
            if self.offset + event.delta / 5 <= self.x:
                self.offset += event.delta / 5
                self.frame_x += event.delta / 5
            else:
                self.offset = 0
                self.frame_x = self.frame_x_init
            self.place(x=self.frame_x, y=self.y)

        elif self.id == 1:
            if self.offset + event.delta/5 <= self.y:
                self.offset += event.delta/5
                self.frame_y += event.delta/5
            else:
                self.offset = 0
                self.frame_y = self.frame_y_init
            self.canva.place(x=self.x, y=self.frame_y)

