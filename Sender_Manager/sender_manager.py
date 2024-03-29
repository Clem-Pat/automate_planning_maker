import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


class Message_sender:
    def __init__(self,username='foyz.planning@gmx.com', pw='Cc130100'):
        self.username = username
        self.pw = pw
        self.stopped = False
        self.get_progress_bar()
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.messenger.com/")
        time.sleep(2)
        loop = 0
        while loop < 1:
            loop += 1
            self.refresh_progress_bar(10/100)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.find_element("xpath", '/html/body/div[2]/div[2]/div/div/div/div/div[4]/button[2]').click()  #cliquer sur accepter cookies
            if self.stopped : break
            time.sleep(2)
            if self.stopped : break
            self.refresh_progress_bar(20/100)
            self.driver.find_element("xpath", '// *[@id="email"]').send_keys(self.username)
            self.driver.find_element("xpath", '//*[@id="pass"]').send_keys(self.pw)
            if self.stopped : break
            self.driver.find_element("xpath", '/html/body/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[7]/div[1]/div/div[2]/div[1]/div/form/div/div[1]/button').click()  #cliquer sur accepter cookies
            self.refresh_progress_bar(30/100)
            if self.stopped : break
            time.sleep(4)
            if self.stopped: break
            try:
                self.driver.find_element("xpath", '/html/body/div/div/div/div[1]/div/a').click()  #cliquer sur accepter vérification
                time.sleep(4)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.driver.find_element("xpath", '/html/body/div[3]/div[2]/div/div/div/div/div[4]/button[2]').click()  # cliquer sur accepter cookies
                if self.stopped: break
            except: pass

    def get_progress_bar(self):
        self.progress_bar_app = tk.Tk()
        self.progress_bar_app.overrideredirect(True)
        self.progress_bar_app.attributes('-topmost', True)
        self.progress_bar_app.geometry(f'400x200+600+350')
        self.progress_bar_app.configure(bg='navy')
        self.progress_bar = ttk.Progressbar(self.progress_bar_app, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.label = tk.Label(self.progress_bar_app, text='0%', bg='navy', fg='white', font='Arial 17 bold')
        self.label2 = tk.Label(self.progress_bar_app, text='Ne rien toucher, envoi automatique', bg='navy', fg='white', font='Arial 15')
        self.cancel_button = tk.Button(self.progress_bar_app, text='Annuler', bg='red', fg='black', command=self.cancel)
        self.progress_bar.pack(pady=(30,0))
        self.label.pack(pady=(30,0))
        self.label2.pack()
        self.cancel_button.pack(pady=(20,0))
        self.progress_bar_app.update()

    def refresh_progress_bar(self, i):
        # sys.stdout.write('\r' + f"{int(i * 100 / self.total_attempt)}%")
        self.progress_bar['value'] = int(i * 100)
        self.label['text'] = f"{int(i * 100)}%"
        self.progress_bar_app.update_idletasks()
        self.progress_bar_app.update()

    def kill_progress_bar(self):
        try : self.progress_bar_app.destroy()
        except : pass

    def kill_driver(self):
        try: self.driver.quit()
        except: pass

    def get_user_to_send_message_to(self, user):
        try: self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(user)  # entrer le nom de l'interlocuteur
        except: self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/label/input').send_keys(user)
        time.sleep(3)
        try:
            self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
            Keys.ARROW_DOWN)
            self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
            Keys.RETURN)  # selectionner l'interlocuteur
        except :
            self.driver.find_element("xpath",
                                     '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/label/input').send_keys(
            Keys.ARROW_DOWN)
            self.driver.find_element("xpath",
                                     '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/label/input').send_keys(
                Keys.ARROW_DOWN)
            self.driver.find_element("xpath",
                                     '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/label/input').send_keys(
                Keys.RETURN)  # selectionner l'interlocuteur
        time.sleep(3)

    def send_message(self, user, message):
        # self.driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/a/svg/path[1]').click()  #cliquer sur accepter vérification
        ####
        # self.driver.find_element("xpath",
        #                          '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div').click()  # cliquer sur nv message
        # time.sleep(2)
        # self.driver.find_element("xpath",
        #                          '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
        #     user)  # cliquer sur accepter vérification
        # time.sleep(3)
        # self.driver.find_element("xpath",
        #                          '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
        #     Keys.ARROW_DOWN)
        # self.driver.find_element("xpath",
        #                          '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
        #     Keys.RETURN)  # selectionner l'interlocuteur
        ####
        try:
            self.get_user_to_send_message_to(user)
            time.sleep(3)
            try:
                self.driver.find_element("xpath",
                                         '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div/div/div[1]/p').send_keys(
                    message)  # entrer le message
            except :
                self.driver.find_element("xpath",
                                         '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]/p').send_keys(
                    message)  # entrer le message

            time.sleep(3)
        except :
            print(f'message à {user} non envoyé')

    def send_gif(self, user, key_word_gif):
        time.sleep(3)
        # self.driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/a/svg/path[1]').click()  #cliquer sur accepter vérification
        try: self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div').click()  # cliquer sur nv message
        except : pass
        time.sleep(2)
        try: self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(user)  # entrer le nom de l'interlocuteur
        except: self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/label/input').send_keys(user)
        time.sleep(3)
        try:
            self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
            Keys.ARROW_DOWN)
            self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
            Keys.RETURN)  # selectionner l'interlocuteur
        except :
            self.driver.find_element("xpath",
                                     '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/label/input').send_keys(
            Keys.ARROW_DOWN)
            self.driver.find_element("xpath",
                                     '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/label/input').send_keys(
                Keys.ARROW_DOWN)
            self.driver.find_element("xpath",
                                     '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/label/input').send_keys(
                Keys.RETURN)  # selectionner l'interlocuteur

        time.sleep(3)
        try:
            self.driver.find_element("xpath",
                             '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[3]/span/div/div').click()  # cliquer sur nv gif
        except :
            self.driver.find_element("xpath",
                                     '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/span/div').click()  # cliquer sur nv gif
        time.sleep(1)
        self.driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div/label/input').send_keys(key_word_gif) #taper le nom du gif
        time.sleep(1)
        self.driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div[1]/img').click()

    def cancel(self):
        self.cancel_button['text'] = 'Arrêt en cours'
        self.stopped = True

if __name__ == '__main__':
    Bot = Message_sender()
    for name in ['Benjamin Langle']:
        Bot.send_message(name, 'Je suis un robot stylé enculé\n')
        Bot.send_gif(name, 'simpson')
    # # names = ['Alice Guyot', 'Clement Patrizio', 'Tea Toscan', 'Tiphaine Cal', 'Matthieu Drilhon',
    #                   'Arthur Lanaspèze', 'Guillaume Kerjouan', 'Zéphyr Dentzer', 'Noé Parker', 'Thibault Edouard',
    #                   'Romain Rnrb', 'Zoé Laurent Iranmehr', 'Benjamin Langle', 'Marie Kintzinger', 'Baptiste Savarit',
    #                   'Romain Dupuis']
    # for name in names:
    #     Bot.send_message(name, 'Ceci est un message test\n')
