#!/usr/bin/env python3

import sys
import time
from bs4 import BeautifulSoup
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

###stole this piece of code from https://webscraping.com/blog/Scraping-JavaScript-webpages-with-webkit/
class Render(QWebPage):
    def __init__(self,url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()
###
        
url = 'http://financials.morningstar.com/balance-sheet/bs.html?t=AAPL&region=USA&culture=en_US'
r = Render(url)
html = r.frame.toHtml()
page = BeautifulSoup(html, 'html.parser')
data = page.find('div',{'id':'data_i50'})
print(data)
