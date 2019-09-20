#! /user/local/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as soup
from config import passw
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
        self.date_xpath = None
        print("INITIALIZING")
        self.urls = ['https://berkeley.illuminateed.com/dna/?gradebook_id=8742&page=GradebookScoresheet', 'https://berkeley.illuminateed.com/dna/?gradebook_id=8632&view=scoresheet&page=GradebookScoresheet',
                     'https://berkeley.illuminateed.com/dna/?gradebook_id=8670&view=scoresheet&page=GradebookScoresheet', 'https://berkeley.illuminateed.com/dna/?gradebook_id=8744&view=scoresheet&page=GradebookScoresheet', 'https://berkeley.illuminateed.com/dna/?gradebook_id=8745&view=scoresheet&page=GradebookScoresheet']

    def login(self):
        print("LOGGING IN")
        self.driver.get(
            "https://teach.classdojo.com/#/login?redirect=%2Flaunchpad")
        assert "ClassDojo" in self.driver.title
        username = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="reactApplication"]/div/div/div[2]/div/form/div[1]/span/div[1]/div/input')))
        username.click()
        username.send_keys("joshuapaz@berkeley.net")
        password = self.driver.find_element_by_xpath(
            '//*[@id="reactApplication"]/div/div/div[2]/div/form/div[2]/div/div/input')
        password.click()
        password.send_keys(passw)
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
        date = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/span/div/a/div/div[1]')
        date.click()

    def custom_dates(self):
        custom_dates = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/span/div/div/div/div/div/ul/li[8]/div/div[1]')
        time.sleep(1)
        custom_dates.click()
        time.sleep(1)

    def last_week(self):
        last_week = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/span/div/div/div/div/div/ul/li[8]/div/div[1]')
        time.sleep(1)
        last_week.click()
        time.sleep(1)

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_elements_by_link_text(xpath)
        except NoSuchElementException:
            self.date_xpath = False
        self.date_xpath = True

    def choose_dates(self):
        if input(f"Have you chosen the dates for this period?('y'/'n') ").lower() == 'y':
            return
        self.choose_dates()

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

    def logged_in(self):
        if input("Have you logged-in to illuminateEd?('y'/'n') ").lower() == 'y':
            return
        self.logged_in()

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
        password = WebDriverWait(self.driver, 27).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        password.send_keys("J@m1169o")
        next_button = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="passwordNext"]/span')))
        next_button.click()
    
    def score_mode(self):
        xpath = '//*[@id="canvas"]/form[1]/table[2]/tbody/tr/td[1]/select'
        menu = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))
        for option in menu.find_elements_by_tag_name('option'):
            if option.text == 'Score':
                option.click() # select() in earlier versions of webdriver
                break





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
        bot.custom_dates()
        bot.choose_dates()
        bot.get_scores()
        bot.score_dict[key] = bot.scores
        bot.return_to_launchpad()
    for k, v in bot.score_dict.items():
        print(k, v)
    bot.get_illuminateed()
    bot.logged_in()
    for url in bot.urls:
        bot.driver.get(url)
        bot.score_mode()
        time.sleep(2)
    time.sleep(5000)
