import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from unidecode import unidecode


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

    def is_the_user_right(self, user):
        """Verifie qu'on parle au bon utilisateur avant d'envoyer le message"""
        #Récupère le titre de l'utilisateur 
        text = self.driver.find_element("xpath",
                                     "/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div/a/div[2]/div/div[1]/h1/span/span/span").text
        #Compare le titre de l'utilisateur avec la commande "user"
        user_enterred = unidecode(text).lower()
        user_targeted = unidecode(user).lower()
        user_targeted_list = user_targeted.split()
        #Renvoie True s'il estime parler à la bonne personne
        return True if sum(1 for word in user_targeted_list if word in user_enterred) == len(user_targeted_list) else False

    def send_message(self, user, message):
        self.get_user_to_send_message_to(user)
        time.sleep(3)
        user_is_the_right_user = self.is_the_user_right(user)
        max_iter = 0
        while not user_is_the_right_user and max_iter < 5:
            max_iter += 1
            self.get_user_to_send_message_to(user)
            user_is_the_right_user = self.is_the_user_right(user)
            time.sleep(1)
        if user_is_the_right_user:
            try:
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
                print(f'message à {user} non envoyé, une erreur est survenue')
        else:
            print(f'Impossible de trouver {user} dans les contacts')

    def send_gif(self, user, key_word_gif):
        self.get_user_to_send_message_to(user)
        time.sleep(3)
        user_is_the_right_user = self.is_the_user_right(user)
        max_iter = 0
        while not user_is_the_right_user and max_iter < 5:
            max_iter += 1
            self.get_user_to_send_message_to(user)
            user_is_the_right_user = self.is_the_user_right(user)
            time.sleep(1)
        if user_is_the_right_user:
            try:
                self.driver.find_element("xpath",
                                '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[3]/span/div/div').click()  # cliquer sur nv gif
            except :
                self.driver.find_element("xpath",
                                        '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/span/div').click()  # cliquer sur nv gif
            time.sleep(2)
            self.driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/label/input').send_keys(key_word_gif) #taper le nom du gif
            time.sleep(1)
            self.driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div[1]/img').click()
        else:
            print(f"Impossible de trouver {user} dans les contacts")

    def cancel(self):
        self.cancel_button['text'] = 'Arrêt en cours'
        self.stopped = True

if __name__ == '__main__':
    Bot = Message_sender()
    i = 0
    for name in ['Clement Patrizio', 'Clement Patrizio', 'Clement Patrizio', 'Clement Patrizio']:
        i += 1
        Bot.send_message(name, f"{i/4}\n")
        Bot.refresh_progress_bar(0.7*(i/4)+0.3)
    # names = ['Alice Guyot', 'Clement Patrizio', 'Tea Toscan', 'Tiphaine Cal', 'Matthieu Drilhon',
    #                   'Arthur Lanaspèze', 'Guillaume Kerjouan', 'Zéphyr Dentzer', 'Noé Parker', 'Thibault Edouard',
    #                   'Romain Rnrb', 'Zoé Laurent Iranmehr', 'Benjamin Langle', 'Marie Kintzinger', 'Baptiste Savarit',
    #                   'Romain Dupuis']
    # for name in names:
    #     Bot.send_message(name, "Hello, c'est encore une campagne de test, ne prends pas en compte ce que je vais dire aujourd'hui. Pardon pour les notifications inutiles...\n")
