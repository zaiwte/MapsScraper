from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import PySimpleGUI as sg
import re
import random
"""
driver.execute_script("window.scrollBy(0,document.body.scrollHeight);",)
print(pague.prettify())
element = driver.find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{n}]/div/a')
action = ActionChains(driver)
action.move_to_element(element).perform()
block2 = pague2.find_all('a', attrs={'class': 'hfpxzc'})
print(len(list(block2)))
#element = self.driver.find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{n}]/div/a')
#action = ActionChains(self.driver)
#action.move_to_element(element).click().perform()
#block = pague.find('a', attrs={'class': 'DUwDvf lfPIob'})
"""


class Map:
    def __init__(self):
        # url = "https://www.google.es/maps/search/clinica+dental+madrid+28001/@40.4193747,-3.6982363,16z?entry=ttu"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.patron='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        time.sleep(1)

    def search(self, text):
        try:
            self.driver.get(text)
        except:
            print("error")

    def get_info(self):
        pague = BeautifulSoup(self.driver.page_source, 'html.parser')
        n=3
        for i in pague.find_all('a', attrs={'class': 'hfpxzc'}):
            urls = re.findall(self.patron, str(i))
            self.search(urls[0])
            print("-----------------------------------------------")
            time.sleep(random.randint(3, 7))
        #print(len(list(block)))
        time.sleep(5)

    def close_driver(self):
        self.driver.close()


class MapsScraperGUI:
    def __init__(self):
        self.map = Map()
        self.map.search("https://www.google.com")

    def show(self):
        layout = [
                    [sg.Input(key='-INPUT-'), sg.Button("search", key='-SEARCH-')],
                    [sg.Button("load", key='-LOAD-',auto_size_button=True)]
                 ]

        window = sg.Window('MapsScraper',
                           layout,
                           finalize=True)

        while True:
            event, values = window.read(timeout=100)

            if event == '-SEARCH-':
                self.map.search("https://www.google.es/maps/search/" + values['-INPUT-'].replace(" ", "+"))

            if event == '-LOAD-':
                self.map.get_info()

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

        window.close()
        self.map.close_driver()


if __name__ == '__main__':
    # sg.theme('LightGray2')
    #
    MapsScraperGUI().show()
