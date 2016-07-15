#!/usr/bin/env python3

from bs4 import *
#BeautifulSoup(r.text,'html.parser'))

class Input:
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

    def get_STdebt(self,in_page):
        tag = in_page.find('div',{'id':'data_i41'})
        children = tag.findChildren()
        #only the ST debt for most recent year
        self.ST_debt = children[-1].text
        print('ST debt = {0}'.format(self.ST_debt))

class Output_attr:
    def __init__(self):
        #status indicator,
        #0 = red, 1 = green, 2 = black
        self.status = 0
        #actual data to be written to output file
        self.data = []
        #text color of each
        self.data_color = []        

class Output:
    red = 0
    green = 1
    blue = 2
    black = 3
    
    def __init__(self):
        self.earnings = Output_attr()
        self.revenue = Output_attr()
        self.cash_flow = Output_attr()
        self.gross_margin = Output_attr()
        self.net_margin = Output_attr()
        self.LT_growthRate = Output_attr()
        self.LT_debt = Output_attr()
        self.ROE = Output_attr()
        self.intrinsic_val = Output_attr()

    def load_inputs(self,BDI_input):
        self.in_earnings = BDI_input.earnings
        self.in_revenue = BDI_input.revenue
        self.in_cash_flow = BDI_input.cash_flow
        self.in_gross_margin = BDI_input.gross_margin
        self.in_net_margin = BDI_input.net_margin
        self.in_LT_growthRate = BDI_input.LT_growthRate
        self.in_LT_debt = BDI_input.LT_debt
        self.in_ST_debt = BDI_input.ST_debt
        self.in_ROE = BDI_input.ROE
        self.in_beta = BDI_input.beta
        self.in_shares_outstanding = BDI_input.shares_outstanding
        self.in_cash_equivalents = BDI_input.cash_equivalents
        
    def compute_earnings(self):
        #for status attribute, default is green, modify to red if computation conditions are not met
        status_golden = Output.green

        #load data
        self.earnings.data = self.in_earnings

        #convert string data to float(string contains comma)
        float_data = [float(item.replace(',','')) for item in self.earnings.data]

        #first data has nothing before it, no comparison needed, thus color remains black
        self.earnings.data_color.append(Output.black)

        #first item neglected, nothing to compare before it
        #last item neglected, since TTM data is not needed
        for ind,item in float_data[1:-1]:
            #resets to green every cycle
            indiv_color = Output.green

            #if value decreases over the year, set data_color to red, status no longer golden
            if item < float_data[ind]:
                indiv_color = Output.red
                status_golden = Output.red

            self.earnings.data_color.append(indiv_color)

        self.earnings.status = status_golden
