import tkinter as tk
from tkinter import ttk
import os
from Tkinter_Manager.tkinter_objects import Tkinter_button, Tkinter_label, Tkinter_canvas, Tkinter_checkbox, Tkinter_entry, Tkinter_scale, Tkinter_frame

class Data():
    def __init__(self):
        self.init_names = ['Alice', 'Clément', 'Tea', 'Tiphaine', 'Matthieu', 'Arthur', 'Guillaume', 'Zéphyr', 'Noé', 'Thibault', 'Bornier', 'Zoé', 'Benjamin', 'Marie', 'Baptiste', 'Romain']
        self.names = ['Alice', 'Clément', 'Tea', 'Tiphaine', 'Matthieu', 'Arthur', 'Guillaume', 'Zéphyr', 'Noé', 'Thibault', 'Bornier', 'Zoé', 'Benjamin', 'Marie', 'Baptiste', 'Romain']
        self.colors = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00", "#008000", "#00FFFF", "#0000FF", "#4B0082", "#800080", "#FF00FF", "#FF00CC", "#00FF9A", "#FFD700", "#C000C0", "#B22222", "#FF0000"]
        self.dispo_filename = 'data/indispo_dispo.xlsx'
        self.historic_filename = 'data/historic.xlsx'
        self.nbre_repetition = 1 #nombre de plannings dans l'échantillon à étudier. On ne gardera que le meilleur planning de l'échantillon
        self.soiree = 'none'
        self.workers_per_cren = [[2,2,2,2,2,0,3], [2,2,2,2,2,0,0], [2,2,2,2,2,2,2], [2,2,2,2,2,2,2], [0,0,0,0,0,0,0]]
        self.max_worker_in_cren = self.get_max_worker_in_cren()

    def __str__(self):
        return str(self.workers_per_cren)

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
            self.title("Interface de pilotage du créateur de planning")
            self.buttons = [Tkinter_button(self, i) for i in range(3)]
            self.labels = [Tkinter_label(self, i) for i in range(5)]
            self.scales = [Tkinter_scale(self, i) for i in range(1)]
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
            self.x, self.y = 0, 150
            self.length, self.height = 1600, 800
            self.title("Créateur de planning > Résultats")
            max_worker_in_cren = self.main_app.data.get_max_worker_in_cren()
            self.frames = [Tkinter_frame(self, i) for i in range(2)]
            self.buttons = [Tkinter_button(self.frames[0], i) for i in range(35*max_worker_in_cren)]
            self.labels = [Tkinter_label(self.frames[0], i) for i in range(13)]
            self.objects = [self.buttons, self.labels]
            self.order_to_kill = False
            self.offset = 0
            self.frame_x, self.frame_x_init = 0, 0
            # ttk.Scrollbar(self, orient='vertical', command=self.yview).pack(side=tk.RIGHT, fill='x', expand=False)
            # self.frames[0].bind("<MouseWheel>", self._on_mousewheel)
            self.frames[0].pack(side=tk.TOP, expand=True)
            self.frames[1].pack(side=tk.BOTTOM)

        self.destroyed = False
        self.configure(bg='light blue')
        self.path = os.path.dirname(os.path.abspath(__file__))
        try: self.iconphoto(True, tk.PhotoImage(file=f'{self.path[:-16]}/ressources/foyz1.png'))
        except : pass

        self.geometry(f'{self.length}x{self.height}+{self.x}+{self.y}')
        self.resizable(width=True, height=True)
        self.bind('<Escape>', self.kill)
        self.bind('<Double-Button-1>', self.get_mouse_position)
        self.protocol('WM_DELETE_WINDOW', self.kill)

        self.place_all_objects()

    def __str__(self):
        return 'Interface graphique pour commander le planning maker'

    def refresh(*args):
        self = args[0]
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
                if self.name == 'main' or (isinstance(object, Tkinter_frame) and self.name == 'resu'):
                    object.place(x=object.x, y=object.y)
                else:
                    max_worker_in_cren = self.main_app.data.get_max_worker_in_cren()
                    if self.name == 'crens' or (self.name == 'resu' and object.id != len(self.crens)*len(self.jours)*max_worker_in_cren):
                        object.grid(row=object.row, column=object.column, columnspan=object.columnspan, rowspan=object.rowspan, pady=object.pady, padx=object.padx)
                    elif self.name == 'resu' and object.id == len(self.crens)*len(self.jours)*max_worker_in_cren:
                        object.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)


    def get_mouse_position(*args):
        print(args[1].x, args[1].y)

    def _on_mousewheel(self, event, *args):
        # self.frames[0].yview_scroll(int(-1 * (event.delta / 120)), "units")
        if self.offset + event.delta/5 <= 0:
            self.offset += event.delta/5
            self.frame_x += event.delta/5
        else:
            self.offset = 0
            self.frame_x = self.frame_x_init
        self.frames[0].place(x=self.frame_x, y=0)