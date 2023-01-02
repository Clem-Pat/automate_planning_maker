import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from excel_manager import Excel_Manager
import matplotlib.pyplot as plt
# import pyautogui

class Tkinter_frame(ttk.Frame):
    ''' Advanced zoom of the image '''
    def __init__(self, mainframe):
        ''' Initialize the main Frame '''
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('Visualisation de la consommation de la BSPP')
        width= self.master.winfo_screenwidth()
        height= self.master.winfo_screenheight()
        self.master.geometry("%dx%d" % (width, height))
        self.data = Excel_Manager()
        # Create canvas and put image on it
        self.init_scroll_bars()
        self.init_canvas()
        self.image = Image.open('resources/carte_bspp.png')  # open image
        self.width, self.height = self.image.size
        self.imscale = 1.0  # scale for the canvaas image
        self.delta = 1.3  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
        # Plot some optional random rectangles for the test purposes
        self.draw_buttons()
        self.show_image()
        self.master.bind('<x>', self.kill)
        self.master.bind('<Button-1>', self.get_mouse_position)

    def init_scroll_bars(self):
        # Vertical and horizontal scrollbars for canvas
        self.vbar = AutoScrollbar(self.master, orient='vertical')
        self.hbar = AutoScrollbar(self.master, orient='horizontal')
        self.vbar.grid(row=0, column=1, sticky='ns')
        self.hbar.grid(row=1, column=0, sticky='we')
        self.vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        self.hbar.configure(command=self.scroll_x)

    def init_canvas(self):
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale        *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()

    def show_image(self, event=None):
        ''' Show image on the Canvas '''
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.canvas.configure(bg='light blue', scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def kill(self, *args):
        self.master.destroy()

    def draw_buttons(self):
        # self.buttons = [Tkinter_button(self.master, id) for id in range(3)]
        for i in range(3):
            x, y = position[i][0], position[i][1]
            caserne_color = self.data.get_caserne_color(casernes[i])
            self.canvas.create_rectangle(x, y, x+60, y+10, fill=caserne_color, activefill='black', tags=casernes[i])
            self.canvas.tag_bind(casernes[i], '<Button-1>', lambda event, a=casernes[i]: self.click_on_caserne(a))

    def click_on_caserne(self, *args):
        caserne_name = args[0]
        # children_app = tk.Tk()
        # children_app.title('Visualisation de la consommation de ' + caserne_name)
        # children_app.configure(bg='light blue')
        # children_app.geometry(f'800x800+20+20')
        # children_app.resizable(width=False, height=False)
        # children_app.mainloop()
        X = [2020+i for i in range(self.data.n_years)]
        Y = [self.data.data_by_caserne[caserne_name][2020+i] for i in range(self.data.n_years)]
        print(X, Y)
        plt.plot(X,Y)
        plt.ylabel('Consommation')
        plt.title('Consommation de ' + caserne_name)
        plt.show()

    def get_mouse_position(self, *args):
        # print(pyautogui.position())
        pass

class Tkinter_button(tk.Button):
    def __init__(self, application, id):
        tk.Button.__init__(self, application)
        self.app = application
        self.id = id
        self.name = casernes[self.id]
        self.bg = 'light grey'
        self.cursor = 'hand2'
        self.config(text=self.name, width=3, height=1, bg=self.bg, fg='black', font='Arial 8 bold', relief=tk.RAISED, cursor=self.cursor, command=self.click)
        self.x, self.y = position[self.id][0], position[self.id][1]
        self.bind('<Return>', self.click)
        self.place(x=self.x, y=self.y)

    def click(self, *args):
        print(self.name)
