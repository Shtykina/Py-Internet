"""Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from pprint import pprint

url = 'https://account.mail.ru/login'
chrome_options = Options()
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path='../yandexdriver.exe', options=chrome_options)
driver.implicitly_wait(120)
driver.get(url)
# ---------
elem = driver.find_element(By.NAME, 'username')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
sleep(3)
elem = driver.find_element(By.NAME, 'password')
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)
# ---------
letters_link = set()
while True:
    flag = len(letters_link)
    letters = driver.find_elements(By.CLASS_NAME, "js-letter-list-item")
    for letter in letters:
        link = letter.get_attribute('href')
        if link is not None:
            letters_link.add(link)
    if flag == len(letters_link):
        break
    actions = ActionChains(driver)
    actions.move_to_element(letters[-1])
    actions.perform()
# ---------
email_list = []
for link in letters_link:
    email = {}
    driver.get(link)
    try:
        wait = WebDriverWait(driver, 30)
        button_wait = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__author')))
        email['author_name'] = driver.find_element(By.CLASS_NAME, "letter-contact").text
        email['author_email'] = driver.find_element(By.CLASS_NAME, "letter-contact").get_attribute('title')
        email['letter_date'] = driver.find_element(By.CLASS_NAME, "letter__date").text
        email['letter_subject'] = driver.find_element(By.XPATH, "//h2").text
        email['letter_content'] = driver.find_element(By.CLASS_NAME, "letter-body__body-content").text
        email_list.append(email)
    except:
        continue
# ---------
client = MongoClient('127.0.0.1', 27017)
db = client['emails_db']
emails = db.emails
emails.inbox.insert_many(email_list)

for email in emails.find({}):
    pprint(email)
