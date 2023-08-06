from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


class Message_sender:
    def __init__(self,username='foyz.planning@gmx.com', pw='Cc130100', receivers=[], messages=[]):
        self.username = username
        self.pw = pw

        self.driver = webdriver.Chrome()
        self.driver.get("https://www.messenger.com/")
        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element("xpath", '/html/body/div[2]/div[2]/div/div/div/div/div[4]/button[2]').click()  #cliquer sur accepter cookies
        time.sleep(2)
        self.driver.find_element("xpath", '// *[@id="email"]').send_keys(self.username)
        self.driver.find_element("xpath", '//*[@id="pass"]').send_keys(self.pw)
        self.driver.find_element("xpath", '/html/body/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[7]/div[1]/div/div[2]/div[1]/div/form/div/div[1]/button').click()  #cliquer sur accepter cookies
        time.sleep(4)
        try:
            self.driver.find_element("xpath", '/html/body/div/div/div/div[1]/div/a').click()  #cliquer sur accepter vérification
            time.sleep(4)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.find_element("xpath", '/html/body/div[3]/div[2]/div/div/div/div/div[4]/button[2]').click()  # cliquer sur accepter cookies
        except:
            pass
        for i in range(len(receivers)):
            try:
                self.send_message(receivers[i], messages[i])
            except:
                pass

    def send_message(self, user, message):
        time.sleep(4)
        # self.driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/a/svg/path[1]').click()  #cliquer sur accepter vérification
        self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div/div[2]/div').click()  # cliquer sur nv message
        time.sleep(2)
        self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
            user)  # cliquer sur accepter vérification
        time.sleep(1)
        self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
            Keys.ARROW_DOWN)
        self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input').send_keys(
            Keys.RETURN)  # selectionner l'interlocuteur
        time.sleep(1)
        self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div/div/div[1]/p').send_keys(
            message)  # entrer le message
        time.sleep(0.5)
        self.driver.find_element("xpath",
                                 '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div/div/div[1]/p').send_keys(
            Keys.RETURN)  # entrer le message
        time.sleep(8)

if __name__ == '__main__':
    Bot = Message_sender()
