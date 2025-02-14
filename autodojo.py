#! /user/local/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as soup
from config import passw
import os
import time
import re
from popup import Setup


class Bot:
    def __init__(self):
        self.assignment_name = None
        self.assignment_date = None
        self.dates_chosen = False
        self.driver = webdriver.Chrome(os.path.join(
            os.path.dirname(__file__), "chrome77/chromedriver"))
        self.scores = {}
        self.score_dict = {}
        self.periods = None
        self.date_xpath = None
        print("INITIALIZING.....")
        self.urls = {'Period 0': 'https://berkeley.illuminateed.com/dna/?gradebook_id=8742&page=GradebookScoresheet', 'Period 1': 'https://berkeley.illuminateed.com/dna/?gradebook_id=8632&view=scoresheet&page=GradebookScoresheet',
                     'Period 2': 'https://berkeley.illuminateed.com/dna/?gradebook_id=8670&view=scoresheet&page=GradebookScoresheet', 'Period 3': 'https://berkeley.illuminateed.com/dna/?gradebook_id=8744&view=scoresheet&page=GradebookScoresheet', 'Period 5': 'https://berkeley.illuminateed.com/dna/?gradebook_id=8745&view=scoresheet&page=GradebookScoresheet'}

    def login(self):
        print("LOGGING IN....")
        self.driver.get(
            "https://teach.classdojo.com/#/login?redirect=%2Flaunchpad")
        assert "ClassDojo" in self.driver.title
        if self.check_exists_by_xpath('//*[@id="reactApplication"]/div/div[2]/div/form/div[1]/span/div[1]/div/input') == False:
            username = WebDriverWait(self.driver, 7).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="reactApplication"]/div/div/div[2]/div/form/div[1]/span/div[1]/div/input')))
        else:
            username = WebDriverWait(self.driver, 7).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="reactApplication"]/div/div[2]/div/form/div[1]/span/div[1]/div/input')))

        username.click()
        username.send_keys("joshuapaz@berkeley.net")
        if self.check_exists_by_xpath('//*[@id="reactApplication"]/div/div[2]/div/form/div[2]/div/div/input') == False:
            password = self.driver.find_element_by_xpath(
                '//*[@id="reactApplication"]/div/div/div[2]/div/form/div[2]/div/div/input')
        else:
            password = self.driver.find_element_by_xpath(
                '//*[@id="reactApplication"]/div/div[2]/div/form/div[2]/div/div/input')
        password.click()
        password.send_keys(passw)
        login = self.driver.find_element_by_css_selector("button")
        login.click()
        time.sleep(2)

    def collect_classes(self):
        print("FINDING REPORT....")
        time.sleep(2)
        self.periods = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Period')]")

    def go_to_report(self):
        try:

            options = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="reactApplication"]/div/div/div/div/div/div[2]/div[1]/div/div[5]/div/div[3]/span/div/a/div/div[1]')))
        except:
            options = WebDriverWait(self.driver, 7).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="reactApplication"]/div/div/div/div/div[2]/div[1]/div/div[5]/div/div[3]/span/div/a/div/div[2]/span/span')))

        options.click()
        time.sleep(1)
        try:
            report = self.driver.find_element_by_xpath(
                '//*[@id="reactApplication"]/div/div/div/div/div/div[2]/div[1]/div/div[5]/div/div[3]/span/div/div/div/div/div/ul/li[2]/div/div[1]')
        except:
            report = self.driver.find_element_by_xpath(
                '//*[@id="reactApplication"]/div/div/div/div/div[2]/div[1]/div/div[5]/div/div[3]/span/div/div/div/div/div/ul/li[2]/div/div[1]/span')
        report.click()

    def custom_dates(self):
        time.sleep(1)
        date = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/span/div/a/div/div[1]')
        date.click()
        custom_dates = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/span/div/div/div/div/div/ul/li[8]/div/div[1]')
        time.sleep(1)
        custom_dates.click()
        time.sleep(1)


    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_elements_by_link_text(xpath)
        except NoSuchElementException:
            self.date_xpath = False
        self.date_xpath = True

    def choose_dates(self):
        self.dates_chosen = Setup(
            "Custom Dates", "Choose a custom date range then click continue")

    def get_scores(self):
        print("COLLECTING SCORES....")
        students = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]'))).get_attribute('innerHTML')
        time.sleep(2)
        bs = soup(students, "html.parser")

        spans = bs.findAll('div', {'class': 'css-jpd5x2'})
        for span in spans[1::]:
            result = re.split(r'(\d.*)', span.text)[0:2]
            print(result)
            name = result[0]
            try:
                score = self.convert_score(int(result[1].strip("%")))
            except:
                score = 1
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
        login = Setup("Login", "Login to IlluminateEd then click continue")

    def score_mode(self):
        xpath = '//*[@id="canvas"]/form[1]/table[2]/tbody/tr/td[1]/select'
        menu = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))
        for option in menu.find_elements_by_tag_name('option'):
            if option.text == 'Score':
                option.click()  # select() in earlier versions of webdriver
                break

    def check_names(self, name):
        if name == "Gab Barajas Melendez, Pablo Angel":
            name = "Barajas Melendez, Pablo Angel Gab"
        elif name == "Minh Toldon, Ochosi":
            name = "Toldon, Ochosi M"
        elif name == "Duran Flores, Miguel Angel":
            name = "Duran Flores, Miguel A"
        elif name == "Walton IV, Norman":
            name = "Walton, Norman"
        elif name == "Marie Howard, Jae":
            name = "Howard, Jae Marie"
        elif name == "Olawoye, Feranmi":
            name = "Olawoye, Oluwabukunmi"
        else:
            return name
        return name

    def get_inputs(self):
        name = raw_input("What is the short name? ")
        self.assignment_name = name
        date_input = raw_input("What is the assigned date?(mm/dd/yyyy) ")
        self.assignment_date = date_input

    def create_assignment(self):
        create_xpath =  WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH,("//*[contains(text(), 'Create Assignment')]"))))
        create_xpath.click()
        short_name = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="short_name"]')))
        name = self.assignment_name
        short_name.send_keys(name)
        actions = ActionChains(self.driver) 
        actions.send_keys(Keys.TAB * 3)
        actions.send_keys("Classwork")
        actions.send_keys(Keys.RETURN)
        actions.perform()
        date = self.driver.find_element_by_xpath('//*[@id="assign_date"]')
        date.click()
        date_input = self.assignment_date
        date.send_keys(date_input)
        possible_points = self.driver.find_element_by_xpath('//*[@id="possible_points"]')
        possible_points.click()
        possible_points.send_keys("11")
        possible_score = self.driver.find_element_by_xpath('//*[@id="possible_score"]')
        possible_score.click()
        possible_score.send_keys("4")
        actions = ActionChains(self.driver) 
        actions.send_keys(Keys.TAB * 4)
        actions.send_keys("P0 H")
        actions.send_keys(Keys.RETURN)
        actions.send_keys("P1 H")
        actions.send_keys(Keys.RETURN)
        actions.send_keys("P2 H")
        actions.send_keys(Keys.RETURN)
        actions.send_keys("P5 H")
        actions.send_keys(Keys.RETURN)
        actions.perform()
        save = self.driver.find_element_by_xpath('//*[@id="save"]')
        save.click()

    def insert_scores(self, student, score, assignment_id):
        name = student[0].encode("utf-8") + " " + student[1].encode("utf-8")
        name = self.check_names(name)
        name_cell = self.driver.find_element_by_xpath(
            '//*[text()[contains(., "{}")]]'.format(name))
        parent = name_cell.find_element_by_xpath(
            '..').find_element_by_xpath('..')
        student_id = parent.get_attribute('student_id')
        inp = self.driver.find_element_by_id(
            "score_{}_{}".format(student_id, assignment_id))
        inp.click()
        inp.send_keys(score)



if __name__ == '__main__':
    bot = Bot()
    bot.login()
    bot.collect_classes()
    for i in range(len(bot.periods)):
        bot.scores = {}
        periods = bot.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Period')]")
        key = periods[i].get_attribute("innerText")[0:8]
        periods[i].click()
        bot.go_to_report()
        if not bot.dates_chosen:
            bot.custom_dates()
            bot.choose_dates()
        time.sleep(1)
        bot.get_scores()
        bot.score_dict[key] = bot.scores
        bot.return_to_launchpad()
    bot.get_illuminateed()
    bot.logged_in()
    for period, url in bot.urls.items():
        bot.driver.get(url)
        if bot.assignment_date == None or bot.assignment_name == None:
            bot.get_inputs()
            bot.create_assignment()
        bot.score_mode()
        image = bot.driver.find_element_by_xpath(
            "//img[contains(@src, '{}')]".format("+".join(bot.assignment_name.split())))
        image_parent = image.find_element_by_xpath('..')
        assignment_id = image_parent.find_element_by_xpath(
            '..').get_attribute('id')[5::]
        print(period)
        count = 0 
        for student, score in bot.score_dict[period].items():
            if len(student.split()) > 3:
                student = " ".join(
                    student.split()[2::]) + ",", " ".join(student.split()[0:2])
            else:
                student = " ".join(
                    student.split()[1::]) + ",", student.split()[0]
            bot.insert_scores(student, str(score), assignment_id)
            if count >= len(bot.score_dict[period].items())-2:
                time.sleep(4)
            else:
                time.sleep(1)
            count += 1
            
            
        print "{} Complete".format(period)
    time.sleep(5000)


'''
When a new assignment is created there is a "data-assignment_id" under context menu 
or "id"=assn_<id> under the table header. The assigment ID is also used for the table
data cells to relate the head to the data.

go to <tr> containing student name, find <input> with assignment_id, enter score
'''
