"""
Overview:
This program uses Selenium to render a web page and then uses BeautifulSoup to parse the HTML.
The program displays a form in PySimpleGUI with a calendar to choose the date and a dropdown
menu that contains very many locations and corresponding airports around the world.
The weather data obtained for this date and location, then organized into a table using PySimpleGUI.
"""

import PySimpleGUI as sg
import json
from json import load, loads, dump, dumps
from datetime import datetime
import time                                             # needed for the sleep function

from pathlib import Path
from bs4 import BeautifulSoup                           # used to parse the HTML
from selenium import webdriver                          # used to render the web page
from seleniumwire import webdriver                      
from selenium.webdriver.chrome.service import Service   # Service is only needed for ChromeDriverManager


import functools                                        # used to create a print function that flushes the buffer
flushprint = functools.partial(print, flush=True)       # create a print function that flushes the buffer immediately

from bs4 import BeautifulSoup  
from rich import print

locations = []
Wdata = []

def asyncGetWeather(url):
  """Returns the page source HTML from a URL rendered by ChromeDriver.
  Args:
      url (str): The URL to get the page source HTML from.
  Returns:
      str: The page source HTML from the URL.
  """
  
  #change '/usr/local/bin/chromedriver' to the path of your chromedriver executable
  service = Service(executable_path=Path('C:/Users/asaia/OneDrive/Desktop/chromedriver_win32/chromedriver'))
  # service = Service(executable_path='/usr/local/bin/chromedriver')
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  
  driver = webdriver.Chrome(service=service,options=options)  # run ChromeDriver
  flushprint("Getting page...")
  driver.get(url)                                             # load the web page from the URL
  flushprint("waiting 3 seconds for dynamic data to load...")
  time.sleep(3)                                               # wait for the web page to load
  flushprint("Done ... returning page source HTML")
  render = driver.page_source                                 # get the page source HTML
  driver.quit()                                               # quit ChromeDriver
  return render                                               # return the page source HTML
    


def getLocations():
  with open("airports.json") as f:
    #data = json.loads(f.read())
    data = json.load(f)
    for i in data:
      locations.append(i['city']+ ', Airport (' + i['icao'] + ')')
  
getLocations()

def findData():
  with open('table1.html') as f:
      table = f.read()
      soup = BeautifulSoup(table, 'html.parser')
      
      
      
  # print(soup.prettify())
  # print(soup.text)
  rows = soup.find_all('tr')
  head = soup.find_all('th')
  
  allData = []
  
  keys = []
  for d in head:
      key = d.text.strip().replace(' ','').replace('\n','')
    #   print('key: ' + key)
      keys.append(key)
      
  for row in rows: 
      row = row.find_all('td')
      data = []
      for td in row:
          # print(data.text.strip().replace(' ','').replace('\n',''))
          # print("====================================")
          data.append(td.text.strip().replace(' ','').replace('\n',''))
      dictionary = dict(zip(keys, data))
      allData.append(dictionary)
#   print(allData)
  for dict1 in allData:
    if dict1:
        list = [i for i in dict1.values()]
        Wdata.append(list)
    #   print(dict1.values())
    #   Wdata.append(dict1.values())
  
#   print(Wdata)
  return Wdata

def genUrl(date,code):
  base_url = "https://wunderground.com/history"
  filter = "daily"   
  # build the url to scrape weather from
  url = f"{base_url}/{filter}/{code}/date/{date}"
#   print(url)
  return url

lst = sg.Combo(locations, font=('Arial Bold', 14),  expand_x=True, enable_events=True, key='-COMBO-')  

layout = [
          [sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton("Calendar", close_when_date_chosen=True,  target='-DATE-', location=(0,0), no_titlebar=False,format='%Y-%m-%d' )],
          [sg.Text('DATE: YYYY-MM-DD')],
          [lst],
          [sg.Text('Location')],
          [sg.Text(size=(20, 2), font=('Helvetica', 20), justification='center')],
          [sg.Button('Retrieve Weather Data'), sg.Exit()]
]

window = sg.Window('Calendar', layout)




while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Retrieve Weather Data':
        # layout = [[sg.Text("New Window", key="new")]]
        # window = sg.Window("Second Window", layout, modal=True)
        toprow = ['Time', 'Temperature', 'Dewpoint', 'Humidity','Wind','Wind Speed','Wind Gust', 'Pressure','Precipitation','Condition']
        length = len(values['-COMBO-'].split())
        # print(length)
        toClean = values['-COMBO-'].split()[length-1]
        apCode = toClean.replace('(','').replace(')','')  
        # print(apCode)
        site = genUrl(values['-DATE-'], apCode)
        # get the page source HTML from the URL
        page = asyncGetWeather(site)
        # # Could be a good idea to use the buildWeatherURL function from gui.py
        # url = 'http://www.wunderground.com/history/daily/KCHO/date/2020-12-31'
        # parse the HTML
        soup = BeautifulSoup(page, 'html.parser')
        
        # find the appropriate tag that contains the weather data
        history = soup.find('lib-city-history-observation')
        # print the parsed HTML
        # print(history.prettify())

        with open('table1.html', 'w') as f:
            f.write(history.prettify())

        rows = findData()
        tbl1 = sg.Table(values=rows, headings=toprow,
           auto_size_columns=True,
           display_row_numbers=False,
           justification='center', key='-TABLE-',
           selected_row_colors='red on yellow',
           enable_events=True,
           expand_x=True,
           expand_y=True,
         enable_click_events=True)
        layout = [[tbl1]]
        window = sg.Window(values['-COMBO-'], layout, size=(715, 200), resizable=True)
window.close()
