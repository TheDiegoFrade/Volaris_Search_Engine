from urllib.request import urlopen as uReq
import requests
from bs4 import BeautifulSoup as sopa
from bs4 import Comment
import lxml
from selenium import webdriver

from _csv import writer as writer
from _csv import QUOTE_ALL as QUOTE
from requests import get as get
import pandas as pd
from datetime import timedelta, date

##['ACA','AGU','BJX','CLQ','CUL','CUN','CUU','HMO','JFK','LAP','LAS','LAX','LMM','MDW','MEX','MID','MKE','MLM','MTY','MXL','OAX','PBC','PDX','PHX','PVR','SAL','SEA','SJD','SJO','SMF','TGZ','TIJ','TPQ','VSA']

list_airports = ['JFK'] #Aeropuertos disponibles volaris


start_date = date(2018, 7, 18)
end_date = date(2018, 9, 28) #Se incluye el día anterior en la lista

if int((end_date-start_date).days) >= 5:
    list_mult = [x*5 for x in range(int(((end_date-start_date)/5).days))]
else:
    list_mult = [0]


 #lista de multiplos de 5 type = int
print(list_mult)

def daterange(start_date, end_date):
        for num in list_mult:
            yield start_date + timedelta(num)

print(range(int((end_date-start_date).days)))

#hay dos fechas
date_list_2018 = []

for single_date in daterange(start_date, end_date):
        dates_by_day = str(single_date.strftime("%m-%d-%Y"))
        date_list_2018.append(dates_by_day)
print(date_list_2018)

#Se imprimen las dos fechas

half_links = []
links_2018 = []
for dest in list_airports:
    for d in date_list_2018:
        C = 'https://www.volaris.com/Flight/Select'
        A = '?o1=MEX&d1=' + dest + '&dd1=' + d + '&s=true&cc=MXN' #Aeropuerto origen es Ciudad de México
        CA = C + A
        links_2018.append(CA)
        half_links.append((A))


list_by_dest_by_day = []
print(links_2018)
for y in links_2018:

    url_to_scrape = y
    r = requests.get(url_to_scrape)
    soup = sopa(r.text, 'html.parser')
    inside_a = soup.findAll('li', attrs={'role':'presentation'})
    inside_a_text = [e.get_text for e in inside_a]
    list_by_dest_by_day.append(inside_a_text)
print(list_by_dest_by_day)






csvfile = "/Users/datascience/list_flights_volaris.csv"

#Assuming res is a flat list
with open(csvfile, "w", newline='') as output:
    writer = writer(output, lineterminator='\r\n')
    for val in list_by_dest_by_day:
        writer.writerow([val])