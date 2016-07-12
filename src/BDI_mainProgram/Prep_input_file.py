#!/usr/bin/env python3

# http://financials.morningstar.com/income-statement/is.html?t=SYMBOL&region=USA&culture=en_US | earnings, revenue
# http://financials.morningstar.com/balance-sheet/bs.html?t=SYMBOL&region=USA&culture=en_US    | long/short-term debt, cash & equivalent
# http://financials.morningstar.com/cash-flow/cf.html?t=SYMBOL&region=USA&culture=en_US        | cash flow
# http://financials.morningstar.com/ratios/r.html?t=SYMBOL&region=USA&culture=en_US            | gross margin, net margin, return on equity
# http://www.reuters.com/finance/stocks/financialHighlights?symbol=SYMBOL                      | Long Term growth rate
# http://www.reuters.com/finance/stocks/overview?symbol=SYMBOL                                 | Beta, outstanding shares

import sys,io,time
from datetime import datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from copy import deepcopy
import pandas
import requests

class Render(QWebPage):
  def __init__(self, in_symbols, in_cb):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.MS_is_head = "http://financials.morningstar.com/income-statement/is.html?t="
    self.MS_bs_head = "http://financials.morningstar.com/balance-sheet/bs.html?t="
    self.MS_cf_head = "http://financials.morningstar.com/cash-flow/cf.html?t="
    self.MS_r_head = "http://financials.morningstar.com/ratios/r.html?t="
    self.MS_tail = "&region=USA&culture=en_US"
    self.R_fh_head = "http://www.reuters.com/finance/stocks/financialHighlights?symbol="
    self.R_o_head = "http://www.reuters.com/finance/stocks/overview?symbol="

    self.done = False
    self.symbols = in_symbols
    self.it = iter(self.symbols)
    self.cb = in_cb
    self.count = 1
    self.dh_visited = False
    self.dh_symbol = ''
    self.ms_urls = []
    self.r_urls = []
    self.html_list = []
    self.crawl()
    self.app.exec_()

  def crawl(self):
    if self.ms_urls:
      url = self.ms_urls.pop(0)
      print("Downloading {0}...".format(url))      
      self.mainFrame().load(QUrl(url))
      
    elif self.r_urls:
      while self.r_urls:
        url = self.r_urls.pop(0)
        print("Downloading {0}...".format(url))
        r = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0'})
        self.html_list.append(r.text)
      self.crawl()
      
    else:
      #dumping html to txt files
      if not self.dh_visited:
        self.dh_visited = True
      else:
        print(self.count); self.count += 1
        self.cb(self.dh_symbol,self.html_list)
        self.html_list = []
        
      if not self.done:
        symbol, has_more = next(self.lookahead())
        self.dh_symbol = symbol
        print(symbol);print(has_more)
        self.ms_urls, self.r_urls = self.setup_urls(symbol)
        if not has_more:
          self.done = True
        time.sleep(10)
        self.crawl()
      else:
        #exit main event loop for good
        self.app.quit()

  def setup_urls(self,symbol):
    MS_url1 = self.MS_is_head + symbol + self.MS_tail
    MS_url2 = self.MS_bs_head + symbol + self.MS_tail
    MS_url3 = self.MS_cf_head + symbol + self.MS_tail
    MS_url4 = self.MS_r_head + symbol + self.MS_tail
    R_url1 = self.R_fh_head + symbol
    R_url2 = self.R_o_head + symbol
    MS_url_list = [MS_url1,MS_url2,MS_url3,MS_url4]
    R_url_list = [R_url1,R_url2]
    return MS_url_list,R_url_list

  def lookahead(self):
    last = None
    first = None
    val = True
    first = last = next(self.it)
    it_copy = deepcopy(self.it)
    for last in it_copy:
      pass
    print('first = {0}'.format(first))
    print('last = {0}'.format(last))    
    if first == last:
      val = False
    yield first,val

  def _loadFinished(self, result):
    print("finished loading!")
    frame = self.mainFrame()  
    url = str(frame.url().toString())
    html = frame.toHtml()
    self.html_list.append(html)
    self.crawl()

def dump_html(symbol,html_list):
  path1 = '../../input_files/htmls/' + symbol + '/MS_url1.txt'
  path2 = '../../input_files/htmls/' + symbol + '/MS_url2.txt'
  path3 = '../../input_files/htmls/' + symbol + '/MS_url3.txt'
  path4 = '../../input_files/htmls/' + symbol + '/MS_url4.txt'
  path5 = '../../input_files/htmls/' + symbol + '/R_url1.txt'  
  path6 = '../../input_files/htmls/' + symbol + '/R_url2.txt'
  path_list = [path1,path2,path3,path4,path5,path6]
  for ind, elem in enumerate(path_list):
    with open(elem,"w") as fptr:
      fptr.write(html_list[ind])

csvfile = "../../input_files/constituents-financials.csv"

print(datetime.now())
data = pandas.read_csv(csvfile)
symbols = data.Symbol.tolist()
ms = Render(symbols[406:],in_cb=dump_html)
print("done rendering")
print(datetime.now())
