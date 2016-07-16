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
        self.calcList = [self.earnings,self.revenue,self.cash_flow]
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
        
    def compute_5years(self,switch):
        #switch == 0 -> earnings
        #Switch == 1 -> revenue
        #switch == 2 -> cash flow
        calcItem = self.calcList[switch]
        
        #for status attribute, default is green, modify to red if computation conditions are not met
        status_color = Output.green

        #convert string data to float(string contains comma)
        float_data = [float(item.replace(',','')) for item in calcItem.data]

        #first data has nothing before it, no comparison needed, thus color remains black
        calcItem.data_color.append(Output.black)

        #first item neglected, nothing to compare before it
        #last item neglected, since TTM data is not needed
        for ind,item in float_data[1:-1]:
            #resets to green every cycle
            indiv_color = Output.green

            #if value decreases over the year, set data_color to red, status no longer golden
            if item < float_data[ind]:
                indiv_color = Output.red
                status_color = Output.red

            calcItem.data_color.append(indiv_color)

        #set TTM data text to blue just to make it stand out
        calcItem.data_color.append(Output.blue)
        #set status tile color
        calcItem.status = status_color

    def compute_earnings(self):
        #load data
        self.earnings.data = self.in_earnings        

        #pass '0' as parameter to indicate 'earnings'
        self.compute_5years(0)

    def compute_revenue(self):
        #load data
        self.revenue.data = self.in_revenue        

        #pass '1' as parameter to indicate 'revenue'
        self.compute_5years(1)

    def compute_cashFlow(self):
        #load data
        self.cash_flow.data = self.in_cash_flow  

        #pass '2' as parameter to indicate 'cash flow'
        self.compute_5years(2)        

    def compute_grossMargin(self):
        #load data
        self.gross_margin.data.append(self.in_gross_margin)
        #set color. Has to compare to competitor, and this feature is not implemented
        self.gross_margin.status = Output.black
        self.gross_margin.data_color.append(Output.blue)

    def compute_netMargin(self):
        #load data
        self.net_margin.data.append(self.in_net_margin)
        #set color. Has to compare to competitor, and this feature is not implemented
        self.net_margin.status = Output.black
        self.net_margin.data_color.append(Output.blue)

    def compute_LTgrowthRate(self):
        result_gr = self.GR_getMeanGrowthRate()

        #load data
        self.LT_growthRate.data.append(str(result_gr))

        #if Long term growth Rate exceeds 10%, set status to green
        threshold = 10
        self.LT_growthRate.status = Output.red
        if self.LT_growthRate.data > threshold:
            self.LT_growthRate.status = Output.green

        self.LT_growthRate.data_color.append(Output.black)

    def GR_getMeanGrowthRate(self):
        #extract mean and 1 year ago growth rate
        mean_gr = float(self.in_LT_growthRate[1].replace(',',''))
        1yearAgo_gr = float(self.in_LT_growthRate[4].replace(',',''))
        #computation method: take the mean of mean_growth_rate and 1_year_ago_growth_rate
        result_gr = (mean_gr + 1yearAgo_gr) / 2

        return result_gr

    def compute_LTdebt(self):
        #conservative debt: LT_debt < 3 x Net Income
        debt = float(self.in_LT_debt.replace(',',''))
        threshold = 3 * float(self.in_earnings[-1].replace(',',''))

        #load data
        self.LT_debt.data.append(self.in_LT_debt)

        self.LT_debt.status = Output.red
        if debt > threshold:
            self.LT_debt.status = Output.green

        self.LT_debt.data_color.append(Output.black)

    def compute_returnOnEquity(self):
        #extract ROE
        roe = float(self.in_ROE.replace(',',''))

        #load data
        self.ROE.data.append(self.in_ROE)

        #if return on equity exceeds 12%, set status to green
        threshold = 12
        self.ROE.status = Output.red
        if roe > threshold:
            self.ROE.status = Output.green

        self.ROE.data_color.append(Output.black)

    def compute_intrinsicVal(self):
        #formula:
        #get projected cash flow for ten years => cash flow * long term growthRate
        #get discounted values by applying discounted factor to all 10 years of cash flow
        #get present value of company by adding up all the discounted values
        #get rough intrinsic val of one share by dividing present val with outstanding shares
        #get intrinsic val by adding net cash per share((cashEquivalents-totalDebt)/outstanding shares)
        
        outstandingShares = float(self.in_shares_outstanding.replace(',',''))

        #get list of projected cash flow
        pcf_list = self.IV_projectCashFlow()

        #get discount rate
        discount_rate = self.IV_discountRate()

        #get net cash per share
        net_cash_per_share = self.IV_netCashPerShare(outstandingShares)

        #rough present value of company
        present_val = 0

        #get discount value by applying discount rate to each pcf
        #DV = CF * DF(discounted factor)
        for ind, cf in enumerate(pcf,1):
            present_val += (cf * (1 / ((1+discount_rate) ** ind)))

        rough_IV_per_share = present_val / outstandingShares
        intrinsic_val = rough_IV_per_share + net_cash_per_share

        #update data
        self.intrinsic_val.data.append(str(intrinsic_val))
        self.intrinsic_val.status = Output.black
        self.intrinsic_val.data_color.append(Output.blue)


    def IV_netCashPerShare(self,outstandingShares):
        ST_debt = float(self.in_ST_debt.replace(',',''))
        LT_debt = float(self.in_LT_debt.replace(',',''))
        cash_equivalents = float(self.in_cash_equivalents.replace(',',''))

        return_val = (cash_equivalents - (ST_debt + LT_debt)) / outstandingShares
        return return_val

    def IV_projectCashFlow(self):
        cash_flow = float(self.in_cash_flow[-1].replace(',',''))
        growth_rate = self.GR_getMeanGrowthRate()
        #projected cash flow
        pcf = []
        #TTM is the baseline, no calculation needed
        pcf.append(cash_flow)
        #loop for 10 times, and calculate projected cash flow in 10 years
        ind = 0
        for ind < 9:
            #current projected cash flow is
            #previous projected cash flow +
            #previous projected cash flow * growth rate
            pcf.append(pcf[ind] * growth_rate + pcf[ind])
            ind += 1
        return pcf
        
    def IV_discountRate(self):
        #discount rate based on beta value(adam khoo)
        beta = float(self.in_beta.replace(',',''))
        if beta < 0.801:
            discount_rate = 0.05
        elif beta < 0.901:
            discount_rate = 0.055
        elif beta < 0.101:
            discount_rate = 0.06
        elif beta < 0.111:
            discount_rate = 0.068
        elif beta < 0.121:
            discount_rate = 0.07
        elif beta < 0.131:
            discount_rate = 0.079
        elif beta < 0.141:
            discount_rate = 0.08
        elif beta < 0.151:
            discount_rate = 0.089
        else:
            discount_rate = 0.09

        return discount_rate
