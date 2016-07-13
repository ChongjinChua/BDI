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
        self.LT_growthRate = []
        self.LT_debt = ""
        self.ST_debt = ""
        self.ROE = ""
        self.beta = ""
        self.shares_outstanding = ""
        self.cash_equivalents = ""

    def get_earnings(self,in_page):
        tag = in_page.find('div',{'id':'data_i80'})
        children = tag.findChildren()
        #earnings for five years
        self.earnings = [child.text for child in children]
        print('earnings = {0}'.format(self.earnings))

    def get_revenue(self,in_page):
        tag = in_page.find('div',{'id':'data_i1'})
        children = tag.findChildren()
        #revenue for five years
        self.revenue = [child.text for child in children]
        print('revenue = {0}'.format(self.revenue))
        
    def get_cashFlow(self,in_page):
        tag = in_page.find('div',{'id':'data_tts1'})
        children = tag.findChildren()
        #cash flow for five years
        self.cash_flow = [child.text for child in children]
        print('cash flow = {0}'.format(self.cash_flow))

    def get_grossMargin(self,in_page):
        tag = in_page.find('th',{'id':'i14'})
        siblings = tag.find_next_siblings('td')
        #only the gross margin for TTM
        self.gross_margin = siblings[-1].text
        print('gross margin = {0}'.format(self.gross_margin))

    def get_netMargin(self,in_page):
        tag = in_page.find('th',{'id':'i22'})
        siblings = tag.find_next_siblings('td')
        #only the gross margin for TTM
        self.net_margin = siblings[-1].text
        print('net margin = {0}'.format(self.net_margin))

    def get_LTgrowthRate(self,in_page):
        tag = in_page.find(text='LT Growth Rate (%)').__dict__
        #'tag' is now a dictionary, where key 'parent' contains actual html tag. Have to do so cause find() only returns text, where html tag is desired
        siblings = tag['parent'].find_next_siblings('td')
        #no. of estimates,mean,high,low,1 year ago
        self.LT_growthRate = [sibling.text for sibling in siblings]
        print('LT growth rate = {0}'.format(self.LT_growthRate))

    def get_LTdebt(self,in_page):
        tag = in_page.find('div',{'id':'data_i50'})
        children = tag.findChildren()
        #only the LT debt for most recent year
        self.LT_debt = children[-1].text
        print('LT debt = {0}'.format(self.LT_debt))

    def get_returnOnEquity(self,in_page):
        tag = in_page.find('th',{'id':'i26'})
        siblings = tag.find_next_siblings('td')
        #only the return on Equity for TTM
        self.ROE = siblings[-1].text
        print('return on equity = {0}'.format(self.ROE))

    def get_beta(self,in_page):
        tag = in_page.find(text='Beta:').__dict__
        #similar situation as LT_growthRate
        sibling = tag['parent'].find_next_sibling('td')
        #only a single value, situated in the 'strong' tag
        self.beta = sibling.strong.text
        print('Beta = {0}'.format(self.beta))

    def get_sharesOutstanding(self,in_page):
        tag = in_page.find(text='Shares Outstanding(Mil.):').__dict__
        #similar situation as beta
        sibling = tag['parent'].find_next_sibling('td')
        #only a single value, situated in the 'strong' tag
        self.shares_outstanding = sibling.strong.text
        print('shares outstanding = {0}'.format(self.shares_outstanding))

    def get_cashEquivalents(self,in_page):
        tag = in_page.find('div',{'id':'data_i1'})
        children = tag.findChildren()
        #only the cash equivalents for most recent year
        self.cash_equivalents = children[-1].text
        print('cash & equivalents = {0}'.format(self.cash_equivalents))

    def get_ST_debt(self,in_page):
        tag = in_page.find('div',{'id':'data_i41'})
        children = tag.findChildren()
        #only the ST debt for most recent year
        self.ST_debt = children[-1].text
        print('ST debt = {0}'.format(self.ST_debt))
