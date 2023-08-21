from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import PySimpleGUI as sg
import re
import random
import threading
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
        #url = "https://www.google.es/maps/search/clinica+dental+madrid+28001/@40.4193747,-3.6982363,16z?entry=ttu"
        self.patron = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    def open_driver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        except:
            print("error open driver")
    def search(self, text):
        try:
            self.driver.get(text)
        except:
            print('error search')

    def list_urls(self):
        pague = BeautifulSoup(self.driver.page_source, 'html.parser')
        block = pague.find_all('a', attrs={'class': 'hfpxzc'})
        return block
        #self.search(urls[0])
        #print(urls[0])
        #time.sleep(random.randint(3, 7))

        #time.sleep(5)

    def close_driver(self):
        try:
            self.driver.close()
        except:
            print('error close driver')


class MapsScraperGUI:
    def __init__(self):
        self.map = Map()
        self.map.open_driver()
        self.values = [['', '', '', '', '', '']]
        self.headings = ['nombre', 'reviews', 'estrellas', 'ubicacion', 'telefono', 'web']

    def show(self):
        layout = [
                    [sg.Input(key='-INPUT-'), sg.Button("buscar", key='-SEARCH-'), sg.Button("abrir navegador", key='-OPENDRIVER-')],
                    [sg.Text('resultados:'), sg.Input(size=(8,0), key='-RESULTS-')],
                    [sg.Table(values=self.values,
                                headings=self.headings,
                                auto_size_columns=False,
                                justification='left',
                                def_col_width=12,
                                num_rows=12,
                                key='-TABLA_INI-',
                                font=['20'],
                                vertical_scroll_only=False)],
                    [sg.ProgressBar(max_value=100,orientation='h',expand_x=True, key='-PBAR-', size=(20,15))],
                    [sg.Button("cargar", key='-LOAD-', size=(20,0))]
                 ]

        window = sg.Window('MapsScraper',
                           layout,
                           finalize=True)

        while True:
            event, values = window.read(timeout=100)

            if event == '-SEARCH-':
                self.map.search("https://www.google.es/maps/search/" + values['-INPUT-'].replace(" ", "+"))
                window.bring_to_front()

            if event == '-OPENDRIVER-':
                self.map.open_driver()
                window.bring_to_front()

            if event == '-LOAD-':
                window['-LOAD-'].update(disabled=True)
                infoMap = self.map.list_urls()
                lenInfoMap = len(infoMap)
                window['-RESULTS-'].update(str(lenInfoMap))
                n=0
                for i in infoMap:
                    n+=1
                    urls = re.findall(self.map.patron, str(i))
                    print(urls)
                    window['-PBAR-'].update(current_count=round(n*(100/lenInfoMap)))
                    print(f"current count: {round(n*(100/lenInfoMap))}")

                window['-LOAD-'].update(disabled=False)

            if event in (sg.WIN_CLOSED, 'Exit'):
                self.map.close_driver()
                break

        window.close()



if __name__ == '__main__':
    # sg.theme('LightGray2')
    #
    MapsScraperGUI().show()
