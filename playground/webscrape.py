#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

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

url = 'http://www.morningstar.com/stocks/xnas/aapl/quote.html'
r = Render(url)
html = r.frame.toHtml()
html = str(html.toAscii())
page = BeautifulSoup(html, 'html.parser')
print(page)
