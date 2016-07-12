#!/usr/bin/env python3

from bs4 import *
#BeautifulSoup(r.text,'html.parser'))

class Input():
    def __init__(self):
        self.earnings = []
        self.revenue = []
        self.cash_flow = []
        self.gross_margin = ""
        self.net_margin = ""
        self.LT_growthRate = ""
        self.LT_debt = ""
        self.ST_debt = ""
        self.ROI = ""
        self.beta = ""
        self.shares_outstanding = ""
        self.cash_equivalent = ""

    def get_earnings(self,in_page):
        tag = in_page.find('div',{'id':'data_i80'})
        children = tag.findChildren()
        self.earnings = [child.text for child in children]
        print(self.earnings)

    def get_revenue(self,in_page):
        tag = in_page.find('div',{'id':'data_i1'})
        children = tag.findChildren()
        self.revenue = [child.text for child in children]
        print(self.revenue)
        
    def get_cashFlow(self,in_page):
        tag = in_page.find('div',{'id':'data_tts1'})
        children = tag.findChildren()
        self.cash_flow = [child.text for child in children]
        print(self.cash_flow)

    def get_grossMargin(self,in_page):
        tag = in_page.find('div',{'id':'data_tts1'})
        children = tag.findChildren()
        self.cash_flow = [child.text for child in children]
        print(self.cash_flow)        
