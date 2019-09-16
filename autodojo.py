from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as soup
import os
import time
import re




class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome(os.path.join(os.path.dirname(__file__), "chrome77/chromedriver"))
        self.scores = []
        self.periods = None
        print("INITIALIZING")

    def login(self):
        print("LOGGING IN")
        self.driver.get("https://teach.classdojo.com/#/login?redirect=%2Flaunchpad")
        assert "ClassDojo" in self.driver.title
        username = self.driver.find_element_by_xpath('//*[@id="reactApplication"]/div/div/div[2]/div/form/div[1]/span/div[1]/div/input')
        username.click()
        username.send_keys("joshuapaz@berkeley.net")
        password = self.driver.find_element_by_xpath('//*[@id="reactApplication"]/div/div/div[2]/div/form/div[2]/div/div/input')
        password.click()
        password.send_keys("J@m1169o")
        login = self.driver.find_element_by_xpath('//*[@id="reactApplication"]/div/div/div[2]/div/form/button')
        login.click()
        time.sleep(2)

    def collect_classes(self):
        print("FINDING REPORT")
        time.sleep(2)
        self.periods = self.driver.find_elements_by_xpath("//*[contains(text(), 'Period')]")

        
    def go_to_report(self):
            options = WebDriverWait(self.driver, 7).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="reactApplication"]/div/div/div/div/div/div[2]/div[1]/div/div[5]/div/div[3]/span/div/a/div/div[1]')))
            options.click()
            time.sleep(1)
            report = self.driver.find_element_by_xpath('//*[@id="reactApplication"]/div/div/div/div/div/div[2]/div[1]/div/div[5]/div/div[3]/span/div/div/div/div/div/ul/li[2]/div/div[1]')
            report.click()
            time.sleep(1)
            week = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/span/div/a/div/div[1]')
            week.click()
            last_week = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/span/div/div/div/div/div/ul/li[4]/div/div[1]')
            time.sleep(1)
            last_week.click()
            time.sleep(1)

    def get_scores(self):
        print("COLLECTING SCORES")
        students = WebDriverWait(self.driver, 7).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]'))).get_attribute('innerHTML')
        bs = soup(students, "html.parser")

        spans = bs.findAll('div', {'class': 'css-jpd5x2'})
        for span in spans[1::]:
            result = re.split(r'(\d.*)', span.text)[0:2]
            name = result[0]
            score = int(result[1].strip("%"))
            self.scores.append([name, score])

    def return_to_launchpad(self):
            self.driver.get("https://teach.classdojo.com/#/launchpad")
    
    def get_illuminateed(self):
        self.driver.get("https://berkeley.illuminateed.com/dna/?GradebookSelect")
    
    def login_w_google(self):
        google_login = WebDriverWait(self.driver, 7).until(
                    EC.presence_of_element_located(
                        (By.XPATH,('//*[@id="google-login-button"]'))))
        google_login.click()
    
    def enter_email(self):
        email = WebDriverWait(self.driver, 7).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="identifierId"]')))
        email.click()
        email.send_keys("joshuapaz@berkeley.net")
        next_button = WebDriverWait(self.driver, 7).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="identifierNext"]/span')))
        next_button.click()
    
    def enter_password(self):
        password = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        password.send_keys("J@m1169o")
        next_button = WebDriverWait(self.driver, 7).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="passwordNext"]/span')))
        next_button.click()




if __name__ == '__main__':
    bot = Bot()
    bot.login()
    bot.collect_classes()
    for i in range(len(bot.periods)):
        periods = bot.driver.find_elements_by_xpath("//*[contains(text(), 'Period')]")
        periods[i].click()
        bot.go_to_report()
        bot.get_scores()
        bot.return_to_launchpad()
    for score in bot.scores:
        print(score)

