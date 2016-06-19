#!/usr/bin/env python3

#from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver import Firefox

browser = Firefox()
browser.get('http://www.morningstar.com/stocks/xnas/aapl/quote.html')
iframe = browser.switch_to_frame('mainFrame')
b.switch_to_frame(iframe)
print(b.page_source)
