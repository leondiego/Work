# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 14:57:00 2022

@author: León Diego Rivera Hdz
"""

import os
import re
import time
import locale
import requests
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')

pag_prin = 'https://dermamedina.com/'

r = requests.get(pag_prin)
soup = BeautifulSoup(r.text)
d = soup.find_all("a", attrs= {"class" : "navmenu-link"})
enlaces = []
for i in d:
    enlaces.append(pag_prin + i['href'][1:])

enlaces = [i for i in enlaces if 'pages' not in i]
enlaces = [i for i in enlaces if pag_prin != i]
enlaces = list(set(enlaces))

totales = []
for link in enlaces:
    r = requests.get(link)
    soup = BeautifulSoup(r.text)
    prod_pag = soup.find_all('div', class_ = 'productitem')
    dep = link.split("/")[-1]
    print(f'Departamento {dep}')
    print(f'Se encontraron {len(prod_pag)} productos')
    i = 1
    time.sleep(1)
    for prod in prod_pag:
        href = prod.find_all('a', class_ = 'productitem--image-link')[0]['href']
        r = requests.get(pag_prin + href)
        soup = BeautifulSoup(r.text)
        time.sleep(1.5)
        print(i)
        i += 1
        sku_prod = max(re.findall(r'\d{5,}', soup.find_all('meta', property = 'og:image')[0]['content']), key = len) # 
        nombre_prod = soup.find_all('meta', property = 'og:title')[0]['content']
        precio_prod_orig = float(soup.find_all('span', class_ = 'money')[1].text.strip().split('$')[1][1:].replace(',',''))
        precio_prod_desc = float(soup.find_all('span', class_ = 'money')[2].text.strip().split('$')[1][1:].replace(',',''))
        totales.append([sku_prod, nombre_prod, precio_prod_orig, precio_prod_desc, dep])

final = pd.DataFrame(totales, columns= ['SKU', 'Descripción', 'Precio Original', 'Precio Descuento', 'Departamento'])
final.drop_duplicates('SKU')
final.to_excel(f"Precios Medina {date.today()}.xlsx", index=False)
