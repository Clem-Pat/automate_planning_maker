import tkinter as tk
from tkinter import ttk
import numpy as np
import os
from Tkinter_Manager.tkinter_objects import Tkinter_button, Tkinter_label, Tkinter_canvas, Tkinter_checkbox, Tkinter_entry, Tkinter_scale, Tkinter_frame

class Data():
    def __init__(self, copy=None):
        if copy == None:
            self.init_names = ['Alice', 'Clément', 'Tea', 'Tiphaine', 'Matthieu', 'Arthur', 'Guillaume', 'Zéphyr', 'Noé', 'Thibault', 'Bornier', 'Zoé', 'Benjamin', 'Marie', 'Baptiste', 'Romain']
            self.names = ['Alice', 'Clément', 'Tea', 'Tiphaine', 'Matthieu', 'Arthur', 'Guillaume', 'Zéphyr', 'Noé', 'Thibault', 'Bornier', 'Zoé', 'Benjamin', 'Marie', 'Baptiste', 'Romain']
            self.usernames = ['Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio', 'Clement Enstalavista Patrizio']
            self.colors = ["#3FB2C1", "#9A5454", "#7030A0", "#00FF00", "#008000", "#8EA9DB", "#203764", "#305496", "#FF9900", "#FF00FF", "#CCA434", "#00FF9A", "#FFD700", "#C000C0", "#B22222", "#FF0000"]
            self.dispo_filename = 'Data/indispo_dispo.xlsx'
            self.historic_filename = 'Data/historic.xlsx'
            self.nbre_repetition = 5 #nombre de plannings dans l'échantillon à étudier. On ne gardera que le meilleur planning de l'échantillon
            self.soiree = 'none'
            self.workers_per_cren = [[2,2,2,0,2,0,3], [2,2,2,2,2,0,0], [2,2,2,2,2,2,2], [2,2,2,2,2,2,2], [0,0,0,0,0,0,0]]
            self.max_worker_in_cren = self.get_max_worker_in_cren()

        else:
            self.init_names = np.copy(copy.init_names)
            self.names = np.copy(copy.names)
            self.colors = np.copy(copy.colors)
            self.dispo_filename = copy.dispo_filename
            self.historic_filename = copy.historic_filename
            self.nbre_repetition = copy.nbre_repetition
            self.soiree = copy.soiree
            self.workers_per_cren = np.copy(copy.workers_per_cren)
            self.max_worker_in_cren = copy.max_worker_in_cren

    def __str__(self):
        return str(self.workers_per_cren)

    def copy(self):
        return Data(copy=self)

    def get_max_worker_in_cren(self):
        return max([max(self.workers_per_cren[i]) for i in range(len(self.workers_per_cren))])

class Tkinter_window(tk.Tk):
    def __init__(self, name_of_application, main_app=None):
        tk.Tk.__init__(self)
        self.name = name_of_application
        self.main_app = main_app
        self.crens, self.jours = ['12h15-13h', '13h-13h30', '17h30-20h30', '20h30-23h', '23h-00h'], ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
        if self.name == 'main':
            self.data = Data()
            self.x, self.y = 470, 0
            self.length, self.height = 800, 800
            self.title("Créateur de planning")
            self.buttons = [Tkinter_button(self, i) for i in range(3)]
            self.labels = [Tkinter_label(self, i) for i in range(5)]
            self.scales = [Tkinter_scale(self, i) for i in range(0)]
            self.canvas = [Tkinter_canvas(self, i) for i in range(1)]
            self.checkbox = [Tkinter_checkbox(self, i) for i in range(len(self.data.init_names))]
            self.entrys = [Tkinter_entry(self, i) for i in range(3)]
            self.objects = [self.buttons, self.labels, self.canvas, self.checkbox, self.entrys, self.scales]

        elif self.name == 'crens':
            self.x, self.y = 0, 150
            self.length, self.height = 910, 440
            self.title("Créateur de planning > créneaux à remplir")
            self.buttons = [Tkinter_button(self, i) for i in range(36)]
            self.labels = [Tkinter_label(self, i) for i in range(13)]
            self.objects = [self.buttons, self.labels]
            self.order_to_kill = False

        elif self.name == 'resu':
            self.x, self.y = 0, 50
            self.length, self.height = 1600, 700
            self.title("Créateur de planning > Résultats")
            self.frame = tk.Frame(self, height=self.height, width=self.length, bg='light blue')
            self.first_worker_selected = None
            self.label_error = Tkinter_label(self, 1000)
            self.canvas = [Tkinter_canvas(self.frame, i) for i in range(2)]
            self.buttons = [Tkinter_button(self, i) for i in range(2)]
            self.labels = [Tkinter_label(self.frame, i) for i in range(1)]
            self.objects = [self.labels, self.canvas, self.buttons]
            self.order_to_kill = False
            self.offset, self.frame_y, self.frame_y_init = 0, 0, 0
            self.historic_modifications = []
            self.bind("<MouseWheel>", self._on_mousewheel)
            self.bind('<Control_L>z', self.ctrl_z)
            self.frame.place(x=300, y=0)

        self.destroyed = False
        self.configure(bg='light blue')
        self.path = os.path.dirname(os.path.abspath(__file__))
        try: self.iconphoto(True, tk.PhotoImage(file=f'{self.path[:-16]}/Ressources/foyz1.png'))
        except: pass
        self.geometry(f'{self.length}x{self.height}+{self.x}+{self.y}')
        self.resizable(width=True, height=True)
        self.bind('<Double-Button-3>', self.get_mouse_position)
        self.bind('<Escape>', self.echap)
        self.protocol('WM_DELETE_WINDOW', self.kill)

        self.place_all_objects()

    def __str__(self):
        return 'Interface graphique pour commander le planning maker'

    def refresh(*args):
        self = args[0]
        if self.name != 'main':
            if self.main_app.destroyed : self.kill()
        if self.name == 'crens':
            if self.order_to_kill:
                self.kill()
        self.update()

    def kill(*args):
        self = args[0]
        self.destroyed = True
        self.destroy()

    def place_all_objects(self):
        for list_objects in self.objects:
            for object in list_objects:
                if self.name == 'main' or (self.name == 'resu' and isinstance(object, Tkinter_button)):
                    object.place(x=object.x, y=object.y)
                elif self.name == 'crens' :
                    object.grid(row=object.row, column=object.column, columnspan=object.columnspan, rowspan=object.rowspan, pady=object.pady, padx=object.padx)
                elif self.name == 'resu' and not(isinstance(object, Tkinter_button)):
                    try: object.pack(pady=object.pady)
                    except: object.pack()
        if self.name == 'resu':
            self.label_error.place(x=self.label_error.x, y=self.label_error.y)

    def get_mouse_position(*args):
        print(args[1].x, args[1].y)

    def _on_mousewheel(self, event, *args):
        # self.frames[0].yview_scroll(int(-1 * (event.delta / 120)), "units")
        if self.offset + event.delta/5 <= 0:
            self.offset += event.delta/5
            self.frame_y += event.delta/5
        else:
            self.offset = 0
            self.frame_y = self.frame_y_init
        self.frame.place(x=300, y=self.frame_y)

    def ctrl_z(self, *args):
        if len(self.historic_modifications) > 0:
            self.historic_modifications[-1][1].select_worker(1000)
            self.historic_modifications[-1][0].select_worker(1000)
            self.historic_modifications.pop(-1)
            self.historic_modifications.pop(-1)
            self.canvas[1].itemconfig(self.canvas[1].text, text=self.canvas[1].get_text())
        else:
            self.label_error['text'] = 'Vous êtes revenu au planning initial'
            self.label_error['fg'] = 'navy'
            self.label_error.place(x=self.label_error.x, y=520)

    def echap(self, *args):
        if self.name == 'resu':
            if self.first_worker_selected != None:
                self.first_worker_selected.select_worker(1)
            else:
                self.kill()
        else:
            self.kill()
