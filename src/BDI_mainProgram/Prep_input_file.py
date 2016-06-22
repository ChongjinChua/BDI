#!/usr/bin/env python3

# http://financials.morningstar.com/income-statement/is.html?t=SYMBOL&region=USA&culture=en_US | earnings, revenue
# http://financials.morningstar.com/balance-sheet/bs.html?t=SYMBOL&region=USA&culture=en_US    | long/short-term debt, cash & equivalent
# http://financials.morningstar.com/cash-flow/cf.html?t=SYMBOL&region=USA&culture=en_US        | cash flow
# http://financials.morningstar.com/ratios/r.html?t=SYMBOL&region=USA&culture=en_US            | gross margin, net margin, return on equity
# http://www.reuters.com/finance/stocks/financialHighlights?symbol=SYMBOL                      | Long Term growth rate
# http://www.reuters.com/finance/stocks/overview?symbol=SYMBOL                                 | Beta, outstanding shares

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from bs4 import *
import pandas

class Render(QWebPage):
  def __init__(self, urls, cb):
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.urls = urls
    self.html_list = []
    self.cb = cb
    print("crawling...")
    self.crawl()  
    self.app.exec_()  
      
  def crawl(self):  
    if self.urls:  
      url = self.urls.pop(0)  
      print("Downloading {0}".format(url))
      self.mainFrame().load(QUrl(url))
    else:
      print("quiting...")
      self.app.quit()  
        
  def _loadFinished(self, result):
    print("finished loading!")
    frame = self.mainFrame()  
    url = str(frame.url().toString())
    html = frame.toHtml()
    self.html_list.append(html)
    self.cb(url, html)
    self.crawl()  

def scrape(url, html):
    pass # add scraping code here

csvfile = "../../input_files/constituents-financials.csv"
MS_is_head = "http://financials.morningstar.com/income-statement/is.html?t="
MS_bs_head = "http://financials.morningstar.com/balance-sheet/bs.html?t="
MS_cf_head = "http://financials.morningstar.com/cash-flow/cf.html?t="
MS_r_head = "http://financials.morningstar.com/ratios/r.html?t="
MS_tail = "&region=USA&culture=en_US"
R_fh_head = "http://www.reuters.com/finance/stocks/financialHighlights?symbol="
R_o_head = "http://www.reuters.com/finance/stocks/overview?symbol="

data = pandas.read_csv(csvfile)
symbols = data.Symbol.tolist()

url_list = []
for symbol in symbols[0:1]:
    MS_url1 = MS_is_head + symbol + MS_tail
    MS_url2 = MS_bs_head + symbol + MS_tail
    MS_url3 = MS_cf_head + symbol + MS_tail
    MS_url4 = MS_r_head + symbol + MS_tail
    R_url1 = R_fh_head + symbol
    R_url2 = R_o_head + symbol
    url_list = [R_url2]
#[MS_url1,MS_url2,MS_url3,MS_url4,R_url1,R_url2]

    r = Render(url_list,cb=scrape)
    '''
    for item in r.html_list:
      print(item)
      print("-----------------------------------------\n-----------------------------------------")
    '''
