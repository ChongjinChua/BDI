#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

print("hi")
r = requests.get('http://financials.morningstar.com/ratios/r.html?t=AAPL&region=USA&culture=en_US',headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0'})

html = r.text
page = BeautifulSoup(html,'html.parser')
#data = page.find('tr',{'class':'gr_table_row4'})
print(page)
