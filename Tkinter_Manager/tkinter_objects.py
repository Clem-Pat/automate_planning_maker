import tkinter as tk
from tkinter import messagebox
import numpy as np
import os
import subprocess, sys
from Planning_Manager.planning_manager import The_Planning_Maker, Creneau
from Sender_Manager.sender_manager import Message_sender
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import ImageTk, Image
import ctypes

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
        if not (caller):
            self.caller = self.app
        else:
            self.caller = caller
        self.id = id

        if self.app.name == 'main':
            if self.id == 0:
                self.bg, self.fg, self.cursor, self.command, self.state = '#a4deaa', 'black', 'hand2', self.create_planning, 'unclicked'
                self.config(text='Créer le planning', width=20, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold',
                            relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y = 450, 665

            elif self.id == 1:
                self.bg, self.fg, self.cursor, self.command, self.state = 'navy', 'white', 'hand2', self.show_creneaux, 'unclicked'
                self.config(text='Créneaux', width=7, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 10',
                            relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y = 700, 405

            elif self.id == 2:
                self.bg, self.fg, self.cursor, self.command, self.state = 'navy', 'white', 'hand2', self.show_resu, 'unclicked'
                self.config(text='Résultats', width=7, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 10',
                            relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y, self.right_x = 2000, 665, 700

            elif self.id == 3:
                self.bg, self.fg, self.cursor, self.command, self.state = 'navy', 'white', 'hand2', self.import_planning, 'unclicked'
                self.config(text='Importer planning', width=13, height=1, bg=self.bg, fg=self.fg,
                            font='Arial 8',
                            relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y, self.right_x = 710, 275, 700

            elif self.id == 4:
                self.bg, self.fg, self.cursor, self.command, self.state = 'light blue', 'black', 'hand2', self.info_help, 'unclicked'
                try:
                    path = os.path.dirname(os.path.abspath(__file__))
                    img = Image.open(f"{path[:-16]}/Ressources/question_button.png")
                    resized_img = img.resize((20, 20), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(resized_img)
                    self.config(image=photo, cursor=self.cursor, bg=self.bg, font='Arial 11', relief=tk.RAISED,
                                command=self.command)
                    self.image = photo
                except Exception as e:
                    self.config(text='Aide', width=13, height=1, bg=self.bg, fg=self.fg,
                                font='Arial 11',
                                relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y, self.right_x = 15, 15, 700

            if self.id >= 1000:
                self.cursor, self.command = 'hand2', self.choose_file
                path = os.path.dirname(os.path.abspath(__file__))
                img = Image.open(f"{path[:-16]}/Ressources/folder_icon.png")
                resized_img = img.resize((20, 20), Image.LANCZOS)
                photo = ImageTk.PhotoImage(resized_img)
                self.config(image=photo, cursor='hand2', bg='light blue', font='Arial 11', relief=tk.RAISED,
                            command=self.command)
                self.image = photo
                self.x, self.y = 680, self.caller.y

        elif self.app.name == 'crens':
            if self.id < 35:
                matrix = np.ndarray(shape=(5, 7), buffer=np.array(list(range(35))), dtype=int)
                self.row_cren, self.column_cren = self.id // len(matrix[0]), self.id % len(matrix[0])
                self.row, self.column = self.row_cren + 2, self.column_cren + 1
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
                self.bg, self.disable_bg, self.fg, self.cursor = 'navy', '#C0C0C0', 'white', 'hand2'
                self.config(text='2', width=10, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold',
                            relief=tk.RAISED, cursor=self.cursor)
                self.bind('<Button-1>', self.active_cren)
                self.bind('<Button-2>', self.active_cren)
                self.bind('<Button-3>', self.active_cren)
                self.configure_button()
            elif self.id == 35:
                self.row, self.column = 7, 8
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 5, 5
                self.bg, self.disable_bg, self.fg, self.cursor = '#a4deaa', 'grey', 'black', 'hand2'
                self.config(text='Valider', width=7, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold',
                            relief=tk.RAISED, cursor=self.cursor)
                self.old_resu = self.app.main_app.data.workers_per_cren
                self.bind('<Button-1>', self.valid_crens)

        elif self.app.name == 'resu':
            if sys.platform == 'darwin':
                offset_x = 100
            else:
                offset_x = 0
            if self.id == 0:
                self.bg, self.fg, self.cursor, self.command, self.state = '#a4deaa', 'black', 'hand2', self.create_excels, 'unclicked'
                self.config(text='Créer les excels', width=20, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold', relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y = 1150 - offset_x, 600
                self.button = Tkinter_button(self.app, 1000 + self.id, caller=self)
                self.button.place(x=self.button.x, y=self.button.y)
            elif self.id == 1:
                self.bg, self.fg, self.cursor, self.state = 'navy', 'white', 'hand2', 'unclicked'
                self.config(text='Envoyer les messages', width=20, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold', relief=tk.RAISED, cursor=self.cursor)
                self.x, self.y = 1150 - offset_x, 670
                self.allow_key_order = False
                self.bind('<Button-1>', self.send_mail)
                self.bind('<Button-2>', self.show_menu)
                self.bind('<Button-3>', self.show_menu)
                self.bind('<Enter>', self.set_allow_key_order)

            elif self.id >= 1000:
                self.cursor, self.command = 'hand2', self.choose_directory
                path = os.path.dirname(os.path.abspath(__file__))
                img = Image.open(f"{path[:-16]}/Ressources/folder_icon2.png")
                resized_img = img.resize((20, 20), Image.LANCZOS)
                photo = ImageTk.PhotoImage(resized_img)
                try:
                    self.config(image=photo)
                except:
                    self.config(text="Choisir\nl'emplacement", fg='navy')
                self.config(cursor='hand2', bg='light blue', font='Arial 11 bold', relief=tk.RAISED,
                            command=self.command)
                self.image = photo
                self.caller.resu_filename = None
                self.x, self.y = self.caller.x + 200, self.caller.y

        elif self.app.name == 'choose_receivers':
            if self.id == 0:
                self.bg, self.fg, self.cursor, self.state = '#a4deaa', 'black', 'hand2', 'unclicked'
                self.config(text='Valider', width=20, height=2, bg=self.bg, fg=self.fg,
                            font='Arial 11 bold', relief=tk.RAISED, cursor=self.cursor, command=self.app.kill)
                self.x, self.y = 450, 500

        elif isinstance(self.app, Tkinter_canvas):
            self.parent = self.app
            self.app = self.parent.app
            self.max_worker_in_cren = self.app.main_app.data.get_max_worker_in_cren()
            if self.id < len(self.crens) * self.max_worker_in_cren:
                workers_to_consider = [self.app.main_app.planning.resu_general[i][self.parent.id][k] for i in
                                       range(len(self.app.main_app.planning.resu_general)) for k in range(len(self.app.main_app.planning.resu_general[0][self.parent.id]))]
                self.worker = workers_to_consider[self.id]
                self.row, self.column = int(
                    self.id / self.max_worker_in_cren) + 2, self.id % self.max_worker_in_cren + 1
                self.jour, self.cren = self.app.jours[self.parent.id], self.app.crens[self.row - 2]
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
                self.bg, self.disable_bg, self.fg, self.cursor = workers_to_consider[
                    self.id].color, 'grey', 'white', 'hand2'
                self.config(text=workers_to_consider[self.id].name, bg=self.bg, fg=self.fg,
                            font='Arial 10', width=7,
                            relief=tk.RAISED, cursor=self.cursor)
                self.bind('<Button-1>', self.select_worker)
                self.bind('<Button-2>', self.select_worker)
                self.bind('<Button-3>', self.select_worker)

        if sys.platform == 'darwin':
            try:
                self.fg = self.bg
                self.config(fg=self.fg)
            except:
                pass
    
    def info_help(self):
        messagebox.showinfo("Besoin d'aide ?",
                                    "Pour une question sur l'utilisation du site ou la maintenance du code, n'hésite vraiment pas à me contacter par mail (clement.patrizio@gmail.com) ou à m'envoyer un message sur Messenger. \nCa me fera vraiment plaisir de t'aider. \n\nBises foyzeuses, \nClément VP 25")
            
    def show_creneaux(self):
        self.app.open_window.cren = True

    def show_resu(self):
        self.app.open_window.resu = True

    def show_choose_receivers(self, *args):
        self['relief'], self['bg'], self['fg'] = tk.RAISED, self.bg, self.fg
        self.app.main_app.open_window.choose_receivers = True

    def show_menu(self, *args):
        text_admins = 'Personne' if len(self.app.main_app.data.admin) == 0 else ', '.join(
            self.app.main_app.data.admin) if len(
            self.app.main_app.data.admin) <= 1 else f"{', '.join(self.app.main_app.data.admin[:-1])} et {self.app.main_app.data.admin[-1]}"
        m = tk.Menu(self.app, tearoff=0)
        m.add_command(label="Choisir à qui envoyer les messages", command=self.show_choose_receivers)
        m.add_separator()
        m.add_command(label=f"Mode démo (envoi à {text_admins})", command=lambda: self.send_mail(3))
        try:
            m.tk_popup(args[0].x_root, args[0].y_root)
        finally:
            m.grab_release()

    def choose_file(self, *args):
        filename = str(askopenfilename())
        x = filename.split('/')
        resu = ''
        for i in range(len(x) - 1, -1, -1):
            newresu = '/' + x[i] + resu
            if len(newresu) > 30:
                break
            else:
                resu = newresu
        self.caller.delete(0, tk.END)
        self.caller.insert(0, resu)
        self.caller.enter(value=filename)

    def import_planning(self):
        print('import plannning')

    def create_planning(self):
        self.app.planning_maker = The_Planning_Maker(self.app.data)
        self.app.planning = self.app.planning_maker.planning
        self.state = 'clicked'
        self.app.buttons[2].x = self.app.buttons[2].right_x
        self.app.buttons[2].place(x=self.app.buttons[2].x, y=self.app.buttons[2].y)
        self.app.buttons[2].flash()

    def valid_crens(self, *args):
        workers_per_cren = np.zeros(len(self.app.buttons) - 1)
        for i in range(len(self.app.buttons) - 1):
            workers_per_cren[i] = int(self.app.buttons[i]['text'])
        workers_per_cren_copy = list(np.copy(workers_per_cren))
        resu = []
        self.app.main_app.data.soirees = []
        for i in range(5):
            resu.append([])
            for j in range(7):
                value = int(workers_per_cren_copy.pop(0))
                resu[-1].append(value)
                if i == 4 and value != 0:
                    self.app.main_app.data.soirees.append(self.jours[j])
        resu2 = ''
        for i in range(len(self.app.main_app.data.soirees)):
            if i == 0:
                resu2 += f'{self.app.main_app.data.soirees[i]}'
            else:
                resu2 += f' - {self.app.main_app.data.soirees[i]}'
        if resu2 == '': resu2 = 'none'
        self.app.main_app.entrys[2].enter(value=resu2)
        if resu != self.old_resu: self.app.main_app.buttons[2].place(x=9000, y=self.app.main_app.buttons[2].y)
        self.old_resu = resu  # Ne sert qu'à masquer le bouton 'résultats' si un changement a été fait
        self.app.main_app.data.workers_per_cren = resu
        self.app.order_to_kill = True

    def unfocus(*args):
        self = args[0]
        self.app.labels[0].focus()

    def active_cren(self, *args):
        event = args[0]
        coeff = 1
        if int(event.num) == 1:
            coeff = 1
        elif int(event.num) == 2 or int(event.num) == 3:
            coeff = -1
        self['text'] = str(max(int(self['text']) + coeff * 1, 0))
        if self['text'] == '0':
            self['bg'] = self.disable_bg
            if sys.platform == 'darwin': self['fg'] = self.disable_bg
        else:
            self['bg'] = self.bg
            if sys.platform == 'darwin': self['fg'] = self.bg

    def configure_button(self):
        workers_per_cren = self.app.main_app.data.workers_per_cren
        if workers_per_cren[self.row_cren][self.column_cren] == 0:
            self['bg'], self['text'] = self.disable_bg, 0
            if sys.platform == 'darwin': self['fg'] = self.disable_bg
        else:
            self['bg'], self['text'] = self.bg, str(workers_per_cren[self.row_cren][self.column_cren])
            if sys.platform == 'darwin': self['fg'] = self.bg

    def select_worker(self, *args):
        try:
            order = args[0].num
        except:
            order = args[0]
        self.app.label_error.hide()
        if self['text'] != 'None' and self['text'] != 'none':
            if int(order) == 1 or int(order) == 1000:
                if self.app.first_worker_selected == None:
                    self['relief'] = tk.SOLID
                    self['borderwidth'] = 4
                    if int(order) == 1: self.app.after(1, lambda self: self.configure(relief='solid'), self)
                    self.app.first_worker_selected = self
                else:
                    planning = self.app.main_app.planning_maker.planning
                    worker1 = self.app.first_worker_selected.worker
                    worker2 = self.worker
                    cren1, cren2 = Creneau(
                        [self.app.first_worker_selected.jour, self.app.first_worker_selected.cren]), Creneau(
                        [self.jour, self.cren])
                    success = planning.test_swap(worker1, worker2, cren1, cren2)
                    print('')
                    print(worker1.name, worker1.crens, worker1.is_mefo)
                    planning.test_5(worker1, cren2.i, cren2.j, printed=True)
                    print(worker2.name, worker2.crens, worker2.is_mefo)
                    planning.test_5(worker2, cren1.i, cren1.j, printed=True)
                    print(success)
                    print('')
                    if all(success): #################################
                        planning.swap_cren(worker1, worker2, cren1, cren2)
                        self.app.first_worker_selected.worker = worker2
                        self.app.first_worker_selected['bg'] = worker2.color
                        if sys.platform == 'darwin': self.app.first_worker_selected['fg'] = worker2.color
                        self.app.first_worker_selected['text'] = worker2.name
                        self.worker = worker1
                        self['bg'] = worker1.color
                        if sys.platform == 'darwin': self['fg'] = worker1.color
                        self['text'] = worker1.name
                        self.app.historic_modifications.append([self.app.first_worker_selected, self])
                        self.app.canvas[1].itemconfig(self.app.canvas[1].text, text=self.app.canvas[1].get_text())
                    else:
                        messages = [f'{worker1.name} has already a cren on {cren2.jour}',
                                    f'{worker2.name} has already a cren on {cren1.jour}',
                                    f'{worker1.name} is not available on cren {cren2}',
                                    f'{worker2.name} is not available on cren {cren1}',
                                    f'{worker1.name} had already menage not a long time ago',
                                    f'{worker2.name} had already menage not a long time ago',
                                    f'{worker1.name} has already a cleaning the day before or the day after',
                                    f'{worker2.name} has already a cleaning the day before or the day after', 
                                    f"{worker1.name} is a mefo, they can't have cren on a mefo day", 
                                    f"{worker2.name} is a mefo, they can't have cren on a mefo day"]
                        self.app.label_error.worker1, self.app.label_error.worker2, self.app.label_error.cren1, self.app.label_error.cren2 = self.app.first_worker_selected, self, cren1, cren2  
                        false_indexes = [index for index, value in enumerate(success) if not value]
                        text_ = "\n".join(messages[index] for index in false_indexes)
                        self.app.label_error.show(text_, fg='red', cursor='arrow',
                                                  file_to_open=None)

                    self.app.first_worker_selected['borderwidth'] = 2
                    self.app.first_worker_selected['relief'] = tk.RAISED
                    self.app.first_worker_selected['highlightthickness'] = 2
                    self['borderwidth'] = 2
                    self['relief'] = tk.RAISED
                    self.app.first_worker_selected = None

            elif int(order) == 2 or int(order) == 3:
                self.app.first_worker_selected['borderwidth'] = 2
                self.app.first_worker_selected['relief'] = tk.RAISED
                self.app.first_worker_selected = None
                self['borderwidth'] = 2
                self['relief'] = tk.RAISED

    def create_excels(self):
        self.app.label_error.hide()
        self.app.main_app.planning_maker.get_progress_bar()
        self.app.main_app.planning_maker.save_data_in_excel(filename=self.resu_filename)
        self.app.main_app.planning_maker.update_historic_excel()
        self.app.main_app.planning_maker.kill_progress_bar()
        print(f'Plannings créés dans {self.app.main_app.planning_maker.excel_creator.filename}')
        x = self.app.main_app.planning_maker.excel_creator.filename.split('/')
        resu = ''
        for i in range(len(x) - 1, -1, -1):
            newresu = '/' + x[i] + resu
            if len(newresu) > 40:
                break
            else:
                resu = newresu
        self.app.label_error.show(f'Plannings créés dans {resu}', cursor='hand2',
                                  file_to_open=self.app.main_app.planning_maker.excel_creator.filename)

    def choose_directory(self, *args):
        self.app.label_error.hide()
        resu = str(askdirectory())
        if resu != '' and resu != ' ': self.caller.resu_filename = resu
        self.app.attributes('-topmost', True)
        self.app.attributes('-topmost', False)

    def ask_send_mail(self, *args):
        self.app.parent_app.buttons[1].send_mail(args[0])

    def send_mail(self, *args):
        try:
            order = args[0].num
        except:
            order = args[0]
        self.app.label_error.hide()
        if int(order) == 1:
            workers = self.app.main_app.planning.workers
            mode = ''
        elif int(order) == 2 or int(order) == 3:
            text_admins = 'Personne' if len(self.app.main_app.data.admin) == 0 else ', '.join(
                self.app.main_app.data.admin) if len(
                self.app.main_app.data.admin) <= 1 else f"{', '.join(self.app.main_app.data.admin[:-1])} et {self.app.main_app.data.admin[-1]}"
            mode = ' - mode démo '
            if text_admins != 'Personne': mode += f'(envoi à {text_admins} seulement)'
            workers = []
            for worker in self.app.main_app.planning.workers:
                if worker.name in self.app.main_app.data.admin:
                    workers.append(worker)
        self['relief'], self['bg'], self['fg'] = tk.SUNKEN, 'grey80', 'black'
        receivers, messages = [], []
        for worker in workers:
            if worker.username in self.app.main_app.data.usernames:
                receivers.append(worker.username)
                root_message = f'Hello {worker.name} !! Voici ton planning pour la semaine.\n\n'
                messages.append(root_message)
                worker.crens.sort()
                for cren in worker.crens:
                    messages[-1] += cren.jour + ' ' + cren.type + '\n\n'
                if self.app.main_app.data.soirees != ['none']:
                    messages[-1] += f'Cette semaine la soirée est'
                    for i in range(len(self.app.main_app.data.soirees)):
                        if i == 0: messages[-1] += f' {self.app.main_app.data.soirees[i]}'
                        if i > 0 and i < len(self.app.main_app.data.soirees) - 1: messages[
                            -1] += f', {self.app.main_app.data.soirees[i]}'
                        if i > 0 and i == len(self.app.main_app.data.soirees) - 1: messages[
                            -1] += f' et {self.app.main_app.data.soirees[i]}'
                    messages[-1] += '\n\n'
        if receivers != []:
            print(receivers)
            self.app.label_error.show('Envoi automatique en cours' + mode, fg='black')
            sender = Message_sender()
            workers_aware = []
            for i in range(len(receivers)):
                if sender.stopped: break
                sender.refresh_progress_bar(0.7*(i/len(receivers))+0.3)
                sender.send_message(receivers[i], messages[i])
                workers_aware.append(workers[i])
            sender.kill_progress_bar()
            sender.kill_driver()
            if sender.stopped:
                message = 'Envois annulés. Voir la console'
                if workers_aware == []:
                    print("Envois annulés. Aucun utilisateur n'a reçu de message")
                else:
                    print(f'Envois annulés. Seuls {workers_aware} ont reçu un message')
            else:
                message = 'Messages envoyés'
                print(f'Messages envoyés à {workers_aware}')
            self['relief'], self['bg'], self['fg'] = tk.RAISED, self.bg, self.fg
            self.app.label_error.show(message)
        else:
            message = mode + "Aucune personne n'est à prévenir par message"
            self.app.label_error.show(message)

    def set_allow_key_order(self, *args):
        self.allow_key_order = True


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
                self.x, self.y = 85, 35
            elif self.id == 1:
                self.config(text="Emplacement du fichier Excel des disponibilités", bg='light blue', fg='navy',
                            font='Arial 11 italic bold')
                self.x, self.y = 390, 245
            elif self.id == 2:
                self.config(text="Emplacement du fichier Excel des historiques", bg='light blue', fg='navy',
                            font='Arial 11 italic bold')
                self.x, self.y = 390, 315
            elif self.id == 3:
                self.config(text="Jour de la soirée", bg='light blue', fg='navy', font='Arial 11 italic bold')
                self.x, self.y = 390, 395
            elif self.id == 4:
                self.config(text="Jour du Mefo", bg='light blue', fg='navy', font='Arial 11 italic bold')
                self.x, self.y = 390, 465
            elif self.id == 5:
                self.config(text="Application créée par l'équipe Foy'z 25 - Version 1.4", bg='light blue', fg='navy',
                            font='Arial 9 italic')
                self.x, self.y = 290, 745
            elif self.id == 6:
                self.config(text="Taille de l'échantillon de plannings à étudier", bg='light blue', fg='navy',
                            font='Arial 11 italic bold')
                self.x, self.y = 390, 505
        elif self.app.name == 'crens':
            self.config(bg='light blue')
            if self.id == 0:
                self.config(text='Créateur de planning : Créneaux', fg='navy', font='Impact 28 bold')
                self.row, self.column = 0, 2
                self.columnspan, self.rowspan, self.padx, self.pady = 5, 1, 2, 2
            elif self.id in range(1, 8):
                self.config(text=f'{self.jours[self.id - 1]}')
                self.row, self.column = 1, self.id
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
            elif self.id in range(8, 13):
                self.config(text=f'{self.crens[self.id - 8]}')
                self.row, self.column = self.id - 8 + 2, 0
                self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
            elif self.id == 13:
                self.config(text='Choisissez le nombre de personnes par créneau (clic gauche +1, clic droit -1)',
                            fg='navy', font='Arial 11')
                self.row, self.column = 7, 2
                self.columnspan, self.rowspan, self.padx, self.pady = 5, 1, 2, 2
        elif self.app.name == 'resu':
            self.config(bg='light blue')
            if self.id == 0:
                self.config(text='Créateur de planning : Résultats', fg='navy', font='Impact 28 bold')
                self.padx, self.pady = 2, 30
            elif self.id == 1000:
                self.config(text='error_label', fg='red', font='Arial 13')
                self.padx, self.pady = 2, 30
                self.x, self.y = 1000, 6000
                self.worker1, self.worker2, self.cren1, self.cren2 = None, None, None, None
                self.bind('<Double-Button-1>', self.hide)
                self.bind('<Button-2>', self.click_label_error)
                self.bind('<Button-3>', self.click_label_error)
                self.bind('<Enter>', lambda e: self.config(cursor='hand2'))
                self.bind('<Leave>', lambda e: self.config(cursor=''))
            elif self.id == 1001:
                noms_mefos = ', '.join(self.app.main_app.data.mefos) if len(self.app.main_app.data.mefos) <= 1 else ', '.join(self.app.main_app.data.mefos[:-1]) + f' et {self.app.main_app.data.mefos[-1]}' if len(self.app.main_app.data.mefos) > 1 else ''
                jour_mefo  = ', '.join(self.app.main_app.data.soirees_mefo) if len(self.app.main_app.data.soirees_mefo) <= 1 else ', '.join(self.app.main_app.data.soirees_mefo[:-1]) + f' et {self.app.main_app.data.soirees_mefo[-1]}' if len(self.app.main_app.data.soirees_mefo) > 1 else '' 
                self.config(text=f'{noms_mefos} ont un créneau Mefo le {jour_mefo}', fg='navy', font='Arial 13')
                self.padx, self.pady = 2, 30
                self.x, self.y = 100, 520
                self.bind('<Double-Button-1>', self.hide)
        elif self.app.name == 'choose_receivers':
            self.config(bg='light blue')
            if self.id == 0:
                self.config(text='Créateur de planning : Envoyer les messages', fg='navy', font='Impact 28 bold')
                self.x, self.y = 15, 20
        elif isinstance(self.app, Tkinter_canvas):
            self.parent = application
            self.config(bg='light blue')
            if self.parent.name == 'planning_canvas':
                if self.id < 2 * len(self.crens):
                    """Labels de créneaux"""
                    self.config(text=self.crens[self.id % len(self.crens)])
                    self.row, self.column = self.id + 2 + (self.id // len(self.crens)), 1
                    self.columnspan, self.rowspan, self.padx, self.pady = 1, 1, 2, 2
                    if self.id == 0:
                        self.pady = (17, 0)
                    elif self.id == 5:
                        self.pady = (30, 5)
            elif self.parent.name in self.jours:
                if self.id == 0:
                    if self.parent.name in self.app.app.main_app.data.soirees: self.config(text=f"{self.parent.name} (soirée)")
                    elif self.parent.name in self.app.app.main_app.data.soirees_mefo: self.config(text=f"{self.parent.name} (mefo)")
                    else: self.config(text=self.parent.name)
                    self.row, self.column = 1, 1
                    self.columnspan, self.rowspan, self.padx, self.pady = self.parent.max_worker_in_cren, 1, 2, 2

    def hide(self, *args):
        self.worker1, self.worker2, self.cren1, self.cren2 = None, None, None, None
        self.place(x=self.x, y=self.y)

    def show(self, text, fg='navy', cursor='arrow', file_to_open=None):
        self['text'] = text
        self['fg'] = fg
        self['cursor'] = cursor
        self.place(x=self.x, y=520)
        if file_to_open != None:
            self.file_path_to_open = file_to_open
            self['fg'] = 'blue'
            self['font'] = 'Arial 13 underline'
            self.bind('<Button-1>', self.open_file)
        else:
            self['font'] = 'Arial 13'
            self.unbind('<Button-1>')

    def click_label_error(self, *args):
        m = tk.Menu(self.app, tearoff=0)
        m.add_command(label="Hide", command=self.hide)
        if (self['bg'] == 'red' or self['fg'] == 'red') and (self.worker1 != None):
            m.add_separator()
            m.add_command(label=f"Force", command=self.force)
        try:
            m.tk_popup(args[0].x_root, args[0].y_root)
        finally:
            m.grab_release()

    def force(self, *args):
        print("force swapping")
        planning = self.app.main_app.planning_maker.planning
        worker1, worker2, cren1, cren2 = self.worker1.worker, self.worker2.worker, self.cren1, self.cren2
        planning.swap_cren(worker1, worker2, cren1, cren2)
        self.worker1.worker = worker2
        self.worker1['bg'] = worker2.color
        if sys.platform == 'darwin': self.worker1['fg'] = worker2.color
        self.worker1['text'] = worker2.name
        self.worker2.worker = worker1
        self.worker2['bg'] = worker1.color
        if sys.platform == 'darwin': self.worker2['fg'] = worker1.color
        self.worker2['text'] = worker1.name
        self.app.historic_modifications.append([self.worker1, self.worker2])
        self.app.canvas[1].itemconfig(self.app.canvas[1].text, text=self.app.canvas[1].get_text())
        self.worker1, self.worker2, self.cren1, self.cren2 = None, None, None, None
        self.hide()
        
    def open_file(self, *args):
        path = os.path.realpath(self.file_path_to_open)
        try:
            os.startfile(path, show_cmd=3)
        except:
            opener = "open" if sys.platform == 'darwin' else 'xdg-open'
            subprocess.call([opener, path])


class Tkinter_canvas(tk.Canvas):
    def __init__(self, parent, id):
        tk.Canvas.__init__(self, parent)
        self.id = id

        if not (isinstance(parent, Tkinter_canvas)):
            try:
                name = parent.name
                self.app = parent
            except:
                self.app = parent.master  # le parent est la Frame, on veut donc le master du parent
            if self.app.name == 'main' or self.app.name == 'choose_receivers':
                if self.id == 0:
                    self.config(bg='white', height=535, width=277, relief='raised')
                    if self.app.name == 'main':
                        self.x, self.y, title = 60, 195, 'Equipe'
                    elif self.app.name == 'choose_receivers':
                        self.x, self.y, title = 60, 105, 'Envoyer à...'
                    self.create_text(20, 20, anchor='w', text=title,
                                     font='Arial 11 italic bold', fill='navy')
            elif self.app.name == 'resu':
                if self.id == 0:
                    self.name = 'planning_canvas'
                    self.config(bg='light blue')
                    self.jours, self.crens = self.app.main_app.jours, self.app.main_app.crens
                    self.labels = [Tkinter_label(self, i) for i in range(2 * len(self.crens))]
                    self.canvas = [Tkinter_canvas(self, i) for i in range(len(self.jours))]
                    self.objects = [self.labels, self.canvas]
                    self.place_all_objects()
                elif self.id == 1:
                    self.name = 'equilibre_canvas'
                    self.config(bg='light blue', height=400, width=420)
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
                """ Canvas pour un jour """
                self.name = self.jours[self.id]
                self.row, self.column = (self.id // 4 * (len(self.crens) + 2)) + 1, (
                            self.id + self.max_worker_in_cren * self.id) % (4 + self.max_worker_in_cren * 4) + 2
                self.columnspan, self.rowspan, self.padx, self.pady = self.max_worker_in_cren, len(self.crens) + 1, 2, 2
                self.labels = [Tkinter_label(self, i) for i in range(1)]
                self.buttons = [Tkinter_button(self, i) for i in range(self.max_worker_in_cren * len(self.crens))]
                self.objects = [self.labels, self.buttons]
                self.place_all_objects()

    def get_text(self):
        if self.app.name == 'resu' and self.id == 1:
            resu = ''
            plan = self.app.main_app.planning
            workers = self.app.main_app.data.sort_by_cren_then_coeff(plan.workers, plan)
            resu += str('Nom').ljust(15) + str('Nbre cren').ljust(15) + 'Coefficients' + '\n'
            resu += '-------------------------------------------' + '\n'
            for worker in list(workers.keys()):
                resu += str(worker.name).ljust(15) + str(f'{workers[worker][0]}').ljust(
                    15) + f'{workers[worker][1]}' + '\n'
            resu += '\n'
            resu += f'Planning équilibré à {max(list(plan.coeffs_workers.values())) - min(list(plan.coeffs_workers.values()))} coefficients près'
            return resu

    def place_all_objects(self):
        for list_objects in self.objects:
            for object in list_objects:
                object.grid(row=object.row, column=object.column, columnspan=object.columnspan,
                            rowspan=object.rowspan, pady=object.pady, padx=object.padx)


class Tkinter_checkbox(tk.Button):
    def __init__(self, application, id):
        tk.Button.__init__(self, application)
        self.id = id
        try:
            self.app = application
            self.jours, self.crens = self.app.jours, self.app.crens
        except:
            self.app = application.master
            self.jours, self.crens = self.app.jours, self.app.crens

        if hasattr(self.app, "data"):
            self.main_app = self.app
        else:
            self.main_app = self.app.main_app

        if self.id in range(len(self.main_app.data.init_names)):
            if self.app.name == 'main':
                self.x, self.y = 75, 240 + self.id * 30
            elif self.app.name == 'choose_receivers':
                self.x, self.y = 75, 150 + self.id * 30
            if sys.platform == 'darwin': self.fg, self.activefg = self.bg, self.activebg
            self.name = self.main_app.data.init_names[self.id]
            self.username = self.main_app.data.usernames[self.id]
            text_to_show = self.name
            if self.name in self.main_app.data.admin: text_to_show = text_to_show + ' [admin]'
            if self.name in self.main_app.data.mefos: text_to_show = text_to_show + ' [mefo]'
            self.bg, self.activebg, self.fg, self.activefg, self.cursor, self.state = '#dea4a5', '#a4deaa', 'black', 'black', 'hand2', 1
            if self.name not in self.main_app.data.names:
                self["state"] = "disabled"
                self.activebg = '#dea4a5'
            self.config(text=text_to_show, bg=self.activebg, fg=self.activefg, cursor=self.cursor, relief=tk.RAISED,
                        font='Arial 10', width=30, height=1)

        self.bind('<Button-1>', self.check)
        self.bind('<Button-2>', self.define_status)
        self.bind('<Button-3>', self.define_status)

    def define_status(self, *args):
        m = tk.Menu(self.app, tearoff=0)
        m.add_command(label="Admin", command=self.define_as_admin)
        m.add_separator()
        m.add_command(label=f"Mefo", command=self.define_as_mefo)
        try:
            m.tk_popup(args[0].x_root, args[0].y_root)
        finally:
            m.grab_release()

    def define_as_admin(self):
        if '[admin]' in self['text']:
            self['text'] = self['text'].replace(' [admin]', '')
            if self.app.name != 'main': self.main_app.checkbox[self.id]['text'] = self.main_app.checkbox[self.id].name  # modifier l'étiquette du main aussi
            self.main_app.data.admin.pop(self.main_app.data.admin.index(self.name))
        else:
            self['text'] = self['text'] + ' [admin]'
            if self.app.name != 'main': self.main_app.checkbox[self.id]['text'] = self.main_app.checkbox[self.id].name + ' [admin]'  # modifier l'étiquette du main aussi
            self.main_app.data.admin.append(self.name)

    def define_as_mefo(self):
        if '[mefo]' in self['text']:
            self['text'] = self['text'].replace(' [mefo]', '')
            self.main_app.data.mefos.pop(self.main_app.data.mefos.index(self.name))
        else:
            self['text'] = self['text'] + ' [mefo]'
            self.main_app.data.mefos.append(self.name)

    def check(self, *args):
        if self['state'] != 'disabled':
            if self['bg'] == self.activebg:
                self.config(bg=self.bg, fg=self.fg)
                self.state = 0
                if self.app.name == 'main':
                    self.main_app.data.names.pop(self.main_app.data.names.index(self.name))
                elif self.app.name == 'choose_receivers':
                    self.main_app.data.usernames.pop(self.main_app.data.usernames.index(self.username))
            else:
                self.config(bg=self.activebg, fg=self.activefg)
                self.state = 1
                if self.app.name == 'main':
                    self.main_app.data.names.insert(self.id, self.name)
                elif self.app.name == 'choose_receivers':
                    self.main_app.data.usernames.insert(self.id, self.username)


class Tkinter_entry(tk.Entry):
    def __init__(self, application, id):
        tk.Entry.__init__(self, application)
        self.id = id
        try:
            self.app = application
            self.jours, self.crens = self.app.jours, self.app.crens
        except:
            self.app = application.master
            self.jours, self.crens = self.app.jours, self.app.crens
        self.config(width=30, font='Arial 12', fg='black')
        if self.id < 2:
            if self.id == 0:
                self.insert(0, self.app.data.dispo_filename)
                self.x, self.y = 390, 275
                self.value, self.default_value = self.app.data.dispo_filename, self.app.data.dispo_filename
            elif self.id == 1:
                self.insert(0, self.app.data.historic_filename)
                self.x, self.y = 390, 345
                self.value, self.default_value = self.app.data.historic_filename, self.app.data.historic_filename
            self.button = Tkinter_button(self.app.frame, 1000 + self.id, caller=self)
            self.button.place(x=self.button.x, y=self.button.y)
        elif self.id >= 2:
            if self.id == 2:
                self.x, self.y = 390, 425
                soirees = self.app.data.soirees
            elif self.id == 3:
                self.x, self.y = 390, 495
                soirees = self.app.data.soirees_mefo
            resu = ''
            for i in range(len(soirees)):
                if i == 0:
                    resu += f'{soirees[i]}'
                else:
                    resu += f' - {soirees[i]}'
            self.insert(0, resu)
            self.value, self.default_value = soirees, soirees
            
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
        if value == None:  # if the user typed manually, the value arg is None so we get what was typed
            self.value = self.get()
        else:  # if the user used the button file, the button returns a value in value arg
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
        elif self.id >= 2:
            if self.get() != '' and self.get() != '/':
                self.config(fg='green')
                self.value = self.value.lower()
                self.value = self.value.replace('et ', '')
                self.value = self.value.replace(' et', '')
                if '-' in str(self.value):
                    values = self.value.replace(' ', '').split('-')
                elif ',' in str(self.value):
                    values = self.value.replace(' ', '').split(',')
                elif '/' in str(self.value):
                    values = self.value.replace(' ', '').split('/')
                elif '_' in str(self.value):
                    values = self.value.replace(' ', '').split('_')
                elif '+' in str(self.value):
                    values = self.value.replace(' ', '').split('+')
                else:
                    values = self.value.split(' ')
                if self.id == 2:
                    self.app.data.soirees = values
                    for i in range(len(self.app.jours)):
                        if self.app.jours[i] not in self.app.data.soirees:
                            if self.app.data.workers_per_cren[4][i] != 0:
                                self.app.data.workers_per_cren[2][i] = 2
                                self.app.data.workers_per_cren[3][i] = 2
                                self.app.data.workers_per_cren[4][i] = 0
                        else:
                            for k in range(2, 5):
                                self.app.data.workers_per_cren[k][i] = 3
                    soirees = self.app.data.soirees
                elif self.id == 3:
                    self.app.data.soirees_mefo = values
                    soirees = self.app.data.soirees_mefo
                resu = ''
                for i in range(len(soirees)):
                    if i == 0:
                        resu += f'{soirees[i]}'
                    else:
                        resu += f' - {soirees[i]}'
                self.delete(0, tk.END)
                self.insert(0, resu)
                self.app.labels[0].focus()
            else:
                if self.id == 2: self.app.data.soirees = self.default_value
                elif self.id == 3: self.app.data.soirees_mefo = self.default_value
                if self.default_value != ['none']:
                    indices = []
                    for day in self.default_value:
                        indices.append(self.app.jours.index(day))
                else:
                    indices = [None]
                if self.id == 2:
                    for i in range(7):
                        if i not in indices:
                            if self.app.data.workers_per_cren[4][i] != 0:
                                self.app.data.workers_per_cren[2][i] = 2
                                self.app.data.workers_per_cren[3][i] = 2
                                self.app.data.workers_per_cren[4][i] = 0
                        else:
                            for k in range(2, 5):
                                self.app.data.workers_per_cren[k][i] = 3
                resu = ''
                for i in range(len(self.default_value)):
                    if i == 0:
                        resu += f'{self.default_value[i]}'
                    else:
                        resu += f' - {self.default_value[i]}'
                self.insert(0, resu)
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
            self.x, self.y = 390, 535
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
        if self.app.name == 'main':
            if self.id == 0:
                self.height, self.width = self.app.height, self.app.length
                self.bg = 'blue'
                self.config(bg='light blue', width=self.width, height=self.height)
                self.x, self.y = 0, 0
                self.place(x=self.x, y=self.y)
        elif self.app.name == 'resu':
            if self.id == 0:
                self.height, self.width = self.app.height, self.app.length
                max_worker_in_cren = self.app.main_app.data.get_max_worker_in_cren()
                if sys.platform == 'darwin':
                    offset = 150
                else:
                    offset = 0
                if max_worker_in_cren == 1:
                    self.x, self.y = 500 - offset, 0
                elif max_worker_in_cren == 2:
                    self.x, self.y = 400 - offset, 0
                elif max_worker_in_cren == 3:
                    self.x, self.y = 300 - offset, 0
                elif max_worker_in_cren == 4:
                    self.x, self.y = 150 - offset, 0
                elif max_worker_in_cren == 5:
                    self.x, self.y = 10, 0
                else:
                    self.x, self.y = 0, 0
                self.place(x=self.x, y=self.y)


class Tkinter_menu(tk.Menu):
    def __init__(self, application, id):
        tk.Menu.__init__(self, application, background='light blue')
        self.id = id
        self.app = application
        if self.app.name == 'main':
            if self.id == 0:
                helpmenu = tk.Menu(self, tearoff=0)
                helpmenu.add_command(label="Enlever une personne du programme car indispo toute la semaine",
                                     command=lambda: self.help('get_rid_of_worker'))
                helpmenu.add_command(label="Choisir l'emplacement des fichiers 'indispos' et 'historic'",
                                     command=lambda: self.help('choose_filepath'))
                helpmenu.add_command(label="Choisir rapidement une soirée", command=lambda: self.help('choose_soiree'))
                helpmenu.add_command(label="Choisir le nombre de personnes par créneau",
                                     command=lambda: self.help('choose_nbre_workers_per_cren'))
                self.add_cascade(label="Aide", menu=helpmenu)
                self.app.config(menu=self)
        if self.app.name == 'resu':
            if self.id == 0:
                helpmenu = tk.Menu(self, tearoff=0)
                helpmenu.add_command(label="Echanger deux personnes", command=lambda: self.help('swap_workers'))
                helpmenu.add_command(label="Créer les fichiers Excel Output", command=lambda: self.help('create_excel'))
                helpmenu.add_command(label="Envoyer les plannings par message",
                                     command=lambda: self.help('send_message'))
                helpmenu.add_command(label="Choisir les interlocuteurs par message",
                                     command=lambda: self.help('choose_receivers'))
                helpmenu.add_separator()
                helpmenu.add_command(label="Tips", command=lambda: self.help('tips'))
                self.add_cascade(label="Aide", menu=helpmenu)
                self.app.config(menu=self)

    def help(self, order):
        if self.app.name == 'main':
            if order == 'get_rid_of_worker':
                messagebox.showinfo('Enlever une personne',
                                    'Vous pouvez cliquer sur le nom à supprimer dans la fenêtre "Equipe". Cela le désactive pour l\'algorithme')
            elif order == 'choose_filepath':
                messagebox.showinfo('choisir l\'emplacement des fichiers input',
                                    'Vous pouvez écrire l\'emplacement manuellement et cliquer sur Entrée ou choisir l\'emplacement avec l\'icône document')
            elif order == 'choose_soiree':
                messagebox.showinfo('choisir la soirée',
                                    "Vous pouvez écrire les jours de soirée séparés d'un tiret, d'un '+', d'un '/' ou d'un espace puis cliquer sur Entrée. Cela mettra automatiquement 3 personnes aux créneaux du soir.")
            elif order == 'choose_nbre_workers_per_cren':
                messagebox.showinfo('Choisir le nombre de personnes par créneau',
                                    "Par défaut le nombre de personnes par créneau est 2 mais il est possible de choisir en cliquant sur le bouton 'Créneaux'")

        elif self.app.name == 'resu':
            if order == 'swap_workers':
                messagebox.showinfo('Echanger deux personnes',
                                    "Cliquer sur une personne puis une autre. Si l'échange est impossible un message d'erreur rouge apparaîtra. \n\nPour annuler la sélection, faites un clic droit sur la personne déjà sélectionnée. \n\nPour annuler le dernier échange, faites ctrl+Z. \n\nPour revenir au planning initial, faites ctrl+Z jusqu'à ce que le message d'erreur bleu apparaisse. \n\nNotez que la fenêtre d'équilibre sous le planning s'actualise en temps réel")
            if order == 'create_excel':
                messagebox.showinfo('Créer les Excels',
                                    "Si vous cliquez sur le bouton 'Créer les Excels', cela va créer trois fichiers Excel output avec des formats jugés utiles. L'emplacement est par défaut l'emplacement du dossier Data dans l'arborescence de cette application. Mais vous pouvez choisir un autre emplacement en cliquant sur le bouton \"Choisir l'emplacement\"")
            if order == 'send_message':
                text_admins = 'Personne' if len(self.app.main_app.data.admin) == 0 else ', '.join(self.app.main_app.data.admin) if len(self.app.main_app.data.admin) <= 1 else f"{', '.join(self.app.main_app.data.admin[:-1])} et {self.app.main_app.data.admin[-1]}"
                messagebox.showinfo('Envoyer les messages',
                                    f"Pour envoyer les plannings de chacun par messenger, cliquez sur le bouton 'envoyer par message'et ne touchez à rien. Vous pouvez annuler à tout moment en cliquant sur annuler. \n\nVous pouvez faire clic droit puis 'Envoyer qu'à l'admin' pour passer en mode démo et n'envoyer les messages qu'aux admins (ici : {text_admins}) \n\n[Raccourci : 'd' comme démo lorsque la souris est au dessus du bouton]")
            if order == 'choose_receivers':
                messagebox.showinfo('Choisir les interlocuteurs',
                                    f"Pour choisir à qui envoyer les messages, il suffit de faire clic droit sur 'Envoyer les messages' puis 'Choisir à qui envoyer'. On peut changer qui l'admin, en rajouter, en enlever, ajouter des personnes à contacter, en enlever, etc. \n\n[Raccourci : 'p' comme paramètre lorsque la souris est au dessus du bouton]")
            if order == 'tips':
                messagebox.showinfo('Tips',
                                    f"Pour faire dispaître un message d'erreur, vous pouvez double-cliquer dessus. \n\nPour aller à l'emplacement des fichiers Excels Output, vous pouvez cliquer sur le message d'info bleu. \n\nPour annuler le dernier échange : ctrl+Z \n\nPour tuer la fenêtre : Esc \n\nPour choisir les interlocuteurs : 'p' quand la souris est au dessus du bouton 'Envoyer les messages' \n\nPour envoyer en mode démo : 'd' quand la souris est au dessus du bouton 'Envoyer les messages'")
            self.app.attributes('-topmost', True)
            self.app.attributes('-topmost', False)
