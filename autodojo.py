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
        self.driver = webdriver.Chrome(os.path.join(
            os.path.dirname(__file__), "chrome77/chromedriver"))
        self.scores = {}
        self.score_dict = {}
        self.periods = None
        print("INITIALIZING")

    def login(self):
        print("LOGGING IN")
        self.driver.get(
            "https://teach.classdojo.com/#/login?redirect=%2Flaunchpad")
        assert "ClassDojo" in self.driver.title
        username = self.driver.find_element_by_xpath(
            '//*[@id="reactApplication"]/div/div/div[2]/div/form/div[1]/span/div[1]/div/input')
        username.click()
        username.send_keys("joshuapaz@berkeley.net")
        password = self.driver.find_element_by_xpath(
            '//*[@id="reactApplication"]/div/div/div[2]/div/form/div[2]/div/div/input')
        password.click()
        password.send_keys("J@m1169o")
        login = self.driver.find_element_by_xpath(
            '//*[@id="reactApplication"]/div/div/div[2]/div/form/button')
        login.click()
        time.sleep(2)

    def collect_classes(self):
        print("FINDING REPORT")
        time.sleep(2)
        self.periods = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Period')]")

    def go_to_report(self):
        options = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="reactApplication"]/div/div/div/div/div/div[2]/div[1]/div/div[5]/div/div[3]/span/div/a/div/div[1]')))
        options.click()
        time.sleep(1)
        report = self.driver.find_element_by_xpath(
            '//*[@id="reactApplication"]/div/div/div/div/div/div[2]/div[1]/div/div[5]/div/div[3]/span/div/div/div/div/div/ul/li[2]/div/div[1]')
        report.click()
        time.sleep(1)
        week = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/span/div/a/div/div[1]')
        week.click()
        last_week = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/span/div/div/div/div/div/ul/li[4]/div/div[1]')
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
            score = self.convert_score(int(result[1].strip("%")))
            self.scores[name] = score

    def convert_score(self, score):
        if score >= 90:
            return 4
        elif score >= 80:
            return 3.5
        elif score >= 70:
            return 3
        elif score >= 60:
            return 2.5
        elif score >= 50:
            return 2
        elif score < 50:
            return 1

    def return_to_launchpad(self):
        self.driver.get("https://teach.classdojo.com/#/launchpad")

    def get_illuminateed(self):
        self.driver.get(
            "https://berkeley.illuminateed.com/dna/?GradebookSelect")

    def login_w_google(self):
        google_login = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, ('//*[@id="google-login-button"]'))))
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
        bot.scores = {}
        periods = bot.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Period')]")
        key = periods[i].get_attribute("innerText")[0:9]
        periods[i].click()
        bot.go_to_report()
        bot.get_scores()
        bot.score_dict[key] = bot.scores
        bot.return_to_launchpad()
    for k, v in bot.score_dict.items():
        print(k, v)
