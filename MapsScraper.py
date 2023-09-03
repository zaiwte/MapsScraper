from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import PySimpleGUI as sg
import random
import pandas as pd
import re

class Map:
    def __init__(self):
        self.patron = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.patronPhone = '^\s*[+]\d*[ |-]*\d*[ |-]*\d*[ |-]*\d*[ |-]*\d*[ |-]*$'

    def save(self, name, heads, values):
        now = datetime.now()
        dict_data = {}
        column = 0

        for h in heads:
            dict_data[h] = [v[column] for v in values]
            column += 1

        print(dict_data)

        list_data = pd.DataFrame(dict_data)

        list_data.to_excel(f'{name}_{now.year}-{now.month}-{now.day}-{now.hour}{now.second}.xlsx')
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

    def scraping(self, url, heading='todo'):
        info = ['', '', '', '', '', '']
        info_heading = ['', '']
        d_pague={}
        self.search(url)
        pague = BeautifulSoup(self.driver.page_source, 'html.parser')

        list_find = [
            ['nombre', 'h1', 'DUwDvf lfPIob', 'A'],
            ['reviews', 'button', 'HHrUdb fontTitleSmall rqjGif', 'A'],
            ['estrellas', 'div', 'fontDisplayLarge', 'A'],
            ['ubicacion', 'button', 'CsEnBe','C'],
            ['telefono', 'a', 'lcr4fd S9kvJb','B'],
            ['web', 'a', 'CsEnBe', 'A']
        ]
        for i in list_find:
            try:
                if i[3] == 'A':
                    d_pague[i[0]] = pague.find(i[1], attrs={'class': i[2]}).text

                elif i[3] == 'B':
                    d_pague[i[0]] = pague.find(i[1], attrs={'class': i[2], 'data-value': 'Llamar al número de teléfono'})['href']

                elif i[3] == 'C':
                    d_pague[i[0]] = pague.find(i[1], attrs={'class': i[2]})['aria-label']
            except:
                d_pague[i[0]] = 'nada'
                print("error scraping")

        if heading == 'todos':
            info = [
                d_pague['nombre'],
                d_pague['reviews'],
                d_pague['estrellas'],
                d_pague['ubicacion'],
                d_pague['telefono'],
                d_pague['web']
            ]
        else:
            info = [
                d_pague['nombre'],
                d_pague[heading]
            ]

        return info

    def list_webs(self):
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
        self.headings_table = ['nombre', 'reviews', 'estrellas', 'ubicacion', 'telefono', 'web']
        self.headings = {
            'todos': {'nombre': 'todos', 'key': '-TABLA_todos-'},
            'reviews': {'nombre': 'reviews', 'key': '-TABLA_reviews-'},
            'estrellas': {'nombre': 'estrellas', 'key': '-TABLA_estrellas-'},
            'ubicacion': {'nombre': 'ubicacion', 'key': '-TABLA_ubicacion-'},
            'telefono': {'nombre': 'telefono', 'key': '-TABLA_telefono-'},
            'web': {'nombre': 'web', 'key': '-TABLA_web-'}
        }

    def tabs(self, name):
        return [[sg.Table(values=[['', '']],
                                headings=['nombres', name],
                                auto_size_columns=False,
                                justification='left',
                                def_col_width=26,
                                num_rows=12,
                                key=f'-TABLA_{name}-',
                                font=['20'],
                                vertical_scroll_only=False)], [sg.Button(f'guardar {name}', key=f'-G_{name}-')]]
    def show(self):

        tab_all = [[sg.Table(values=self.values,
                                headings=self.headings_table,
                                auto_size_columns=False,
                                justification='left',
                                def_col_width=12,
                                num_rows=12,
                                key='-TABLA_todos-',
                                font=['20'],
                                vertical_scroll_only=False)], [sg.Button('guardar todo', key='-G_todo-')]]

        tab_reviews = self.tabs('reviews')
        tab_estrellas = self.tabs('estrellas')
        tab_ubicacion = self.tabs('ubicacion')
        tab_telefono = self.tabs('telefono')
        tab_web = self.tabs('web')
        list_heading = ['todos', 'reviews', 'estrellas', 'ubicacion', 'telefono', 'web']
        layout = [
                    [sg.Input(key='-INPUT-'), sg.Button("buscar", key='-SEARCH-'), sg.Button("abrir navegador", key='-OPENDRIVER-')],
                    [sg.Text('resultados:'), sg.Input(size=(8,0), key='-RESULTS-'), sg.Listbox(list_heading, default_values=['todos'], key='-LBX-')],
                    [sg.TabGroup([[
                            sg.Tab('todos', tab_all),
                            sg.Tab('reviews', tab_reviews),
                            sg.Tab('estrellas', tab_estrellas),
                            sg.Tab('ubicacion', tab_ubicacion),
                            sg.Tab('telefono', tab_telefono),
                            sg.Tab('web', tab_web)

                    ]])],
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

                heading_select=values['-LBX-'][0]
                for k in ['-OPENDRIVER-', '-SEARCH-', '-LOAD-', '-G_todo-', '-G_reviews-', '-G_estrellas-', '-G_ubicacion-', '-G_telefono-', '-G_web-']:
                    window[k].update(disabled=True)

                infoMap = self.map.list_webs()
                lenInfoMap = len(infoMap)
                window['-RESULTS-'].update(str(lenInfoMap))
                load=0
                list_urls = []

                for i in infoMap:
                    load += 1
                    urls = re.findall(self.map.patron, str(i))

                    list_urls.append(self.map.scraping(urls[0], self.headings[heading_select]['nombre']))
                    window[self.headings[heading_select]['key']].update(values=list_urls)

                    window['-PBAR-'].update(current_count=round(load * (100 / lenInfoMap)))

                load = 0
                window['-PBAR-'].update(current_count=0)

                for k in ['-OPENDRIVER-', '-SEARCH-', '-LOAD-', '-G_todo-', '-G_reviews-', '-G_estrellas-', '-G_ubicacion-', '-G_telefono-', '-G_web-']:
                    window[k].update(disabled=False)

            if event == '-G_todo-':
                window['-G_todo-'].update(disabled=True)
                self.map.save('todos',self.headings_table, window[self.headings['todos']['key']].get())
                window['-G_todo-'].update(disabled=False)

            if event == '-G_reviews-':
                window['-G_reviews-'].update(disabled=True)
                self.map.save('reviews',[self.headings_table[0],self.headings_table[1]], window[self.headings['reviews']['key']].get())
                window['-G_reviews-'].update(disabled=False)

            if event == '-G_estrellas-':
                window['-G_estrellas-'].update(disabled=True)
                self.map.save('estrellas',[self.headings_table[0],self.headings_table[2]], window[self.headings['estrellas']['key']].get())
                window['-G_reviews-'].update(disabled=False)

            if event == '-G_ubicacion-':
                window['-G_ubicacion-'].update(disabled=True)
                self.map.save('ubicacion',[self.headings_table[0],self.headings_table[3]], window[self.headings['ubicacion']['key']].get())
                window['-G_ubicacion-'].update(disabled=False)

            if event == '-G_telefono-':
                window['-G_telefono-'].update(disabled=True)
                self.map.save('telefono',[self.headings_table[0],self.headings_table[4]], window[self.headings['telefono']['key']].get())
                window['-G_telefono-'].update(disabled=False)

            if event == '-G_web-':
                window['-G_web-'].update(disabled=True)
                self.map.save('web',[self.headings_table[0],self.headings_table[5]], window[self.headings['web']['key']].get())
                window['-G_web-'].update(disabled=False)

            if event in (sg.WIN_CLOSED, 'Exit'):
                self.map.close_driver()
                break

        window.close()



if __name__ == '__main__':
    # sg.theme('LightGray2')
    #
    MapsScraperGUI().show()
