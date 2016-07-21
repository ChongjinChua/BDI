#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import *
import sys

class Input:
    def __init__(self):
        self.ind = 0
        self.symbol = ""
        self.name = ""
        self.sector = ""        
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

    def get_rowId(self,in_page,string_ls):
        #determine row id of a particular html string using it's text string. Will not fail when data in html pages have different order
        for string in string_ls:
            try:
                #accessing _dict_ of Nonetype will break the code
                tag_dict = in_page.find(text=string).__dict__
                break
            except Exception:
                pass
        tag = tag_dict['parent']
        row_id = tag.get('id')
        if row_id is None:
            row_id = tag.parent.get('id')
            row_id = row_id.replace('label','data')

        return row_id

    def get_earnings(self,in_page):
        try:
            row_id = self.get_rowId(in_page,['Net income'])
            tag = in_page.find('div',{'id':row_id})
            children = tag.findChildren()
            #earnings for five years
            self.earnings = [child.text for child in children]
        except:
            print('get_earnings:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.earnings = ['get_earnings '] #catch any sorts of error

        #print('earnings = {0}'.format(self.earnings))

    def get_revenue(self,in_page):
        try:
            row_id = self.get_rowId(in_page,['Revenue','Total revenues'])
            tag = in_page.find('div',{'id':row_id})
            children = tag.findChildren()
            #revenue for five years
            self.revenue = [child.text for child in children]
        except:
            print('get_revenue:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.revenue = ['get_revenue '] #catch any sorts of error
        #print('revenue = {0}'.format(self.revenue))
        
    def get_cashFlow(self,in_page):
        try:
            row_id = self.get_rowId(in_page,['Operating cash flow','Net cash provided by o...'])
            tag = in_page.find('div',{'id':row_id})
            children = tag.findChildren()
            #cash flow for five years
            self.cash_flow = [child.text for child in children]
        except:
            print('get_cashFlow:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.cash_flow = ['get_cashFlow '] #catch any sorts of error

        #print('cash flow = {0}'.format(self.cash_flow))

    def get_grossMargin(self,in_page):
        try:
            row_id = self.get_rowId(in_page,['Gross Margin %'])
            tag = in_page.find('th',{'id':row_id})
            siblings = tag.find_next_siblings('td')
            #only the gross margin for TTM
            self.gross_margin = siblings[-1].text
        except:
            print('get_grossMargin:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.gross_margin = ['get_grossMargin '] #catch any sorts of error
            
        #print('gross margin = {0}'.format(self.gross_margin))

    def get_netMargin(self,in_page):
        try:
            row_id = self.get_rowId(in_page,['Net Margin %'])
            tag = in_page.find('th',{'id':row_id})
            siblings = tag.find_next_siblings('td')
            #only the gross margin for TTM
            self.net_margin = siblings[-1].text
        except:
            print('get_netMargin:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.net_margin = ['get_netMargin '] #catch any sorts of error
            
        #print('net margin = {0}'.format(self.net_margin))

    def get_LTgrowthRate(self,in_page):
        try:
            tag = in_page.find(text='LT Growth Rate (%)').__dict__
            #'tag' is now a dictionary, where key 'parent' contains actual html tag. Have to do so cause find() only returns text, where html tag is desired
            siblings = tag['parent'].find_next_siblings('td')
            #no. of estimates,mean,high,low,1 year ago
            self.LT_growthRate = [sibling.text for sibling in siblings]
        except:
            print('get_LTgrowthRate:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.LT_growthRate = ['get_LTgrowthRate '] #catch any sorts of error

        #print('LT growth rate = {0}'.format(self.LT_growthRate))

    def get_LTdebt(self,in_page):
        try:
            row_id = self.get_rowId(in_page,['Long-term debt'])
            tag = in_page.find('div',{'id':row_id})
            children = tag.findChildren()
            #only the LT debt for most recent year
            self.LT_debt = children[-1].text
        except:
            print('get_LTdebt:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.LT_debt = ['get_LTdebt '] #catch any sorts of error
            
        #print('LT debt = {0}'.format(self.LT_debt))

    def get_returnOnEquity(self,in_page):
        try:
            row_id = self.get_rowId(in_page,['Return on Equity %'])
            tag = in_page.find('th',{'id':row_id})
            siblings = tag.find_next_siblings('td')
            #only the return on Equity for TTM
            self.ROE = siblings[-1].text
        except:
            print('get_returnOnEquity:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.ROE = ['get_returnOnEquity '] #catch any sorts of error

        #print('return on equity = {0}'.format(self.ROE))

    def get_beta(self,in_page):
        try:
            tag = in_page.find(text='Beta:').__dict__
            #similar situation as LT_growthRate
            sibling = tag['parent'].find_next_sibling('td')
            #only a single value, situated in the 'strong' tag
            self.beta = sibling.strong.text
        except:
            print('get_beta:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.beta = ['get_beta '] #catch any sorts of error

        #print('Beta = {0}'.format(self.beta))

    def get_sharesOutstanding(self,in_page):
        try:
            tag = in_page.find(text='Shares Outstanding(Mil.):').__dict__
            #similar situation as beta
            sibling = tag['parent'].find_next_sibling('td')
            #only a single value, situated in the 'strong' tag
            self.shares_outstanding = sibling.strong.text
        except:
            print('get_sharesOutstanding:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.shares_outstanding = ['get_sharesOutstanding '] #catch any sorts of error

        #print('shares outstanding = {0}'.format(self.shares_outstanding))

    def get_cashEquivalents(self,in_page):
        try:
            row_id = self.get_rowId(in_page,['Cash and cash equivale...'])
            tag = in_page.find('div',{'id':row_id})
            children = tag.findChildren()
            #only the cash equivalents for most recent year
            self.cash_equivalents = children[-1].text
        except:
            print('get_cashEquivalents:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.cash_equivalents = ['get_cashEquivalents '] #catch any sorts of error

        #print('cash & equivalents = {0}'.format(self.cash_equivalents))

    def get_STdebt(self,in_page):
        try:
            row_id = self.get_rowId(in_page,['Short-term debt'])
            tag = in_page.find('div',{'id':row_id})
            children = tag.findChildren()
            #only the ST debt for most recent year
            self.ST_debt = children[-1].text
        except:
            print('get_STdebt:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.ST_debt = ['get_STdebt '] #catch any sorts of error

        #print('ST debt = {0}'.format(self.ST_debt))

class Output_attr:
    def __init__(self):
        #status indicator,
        #0xFF0000 = red, 0x00FF00 = green, 0x0000FF = blue, 0x000000 = black
        self.status = 0xFF0000
        self.status_data = ''
        #actual data to be written to output file
        self.data = []
        #text color of each
        self.data_color = []        

class Output:
    red = 0xFF0000
    green = 0x00FF00
    blue = 0x0000FF
    black = 0x000000
    
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
        
    def convert_S2F(self,item):
        #handles conversion of string with (num) to -ve float values
        val = 1.0
        if item[0] == '(':
            val = -1.0
        val *= float(item.replace(',','').replace(')','').replace('(',''))
        return val

    def compute_5years(self,switch):
        #switch == 0 -> earnings
        #Switch == 1 -> revenue
        #switch == 2 -> cash flow
        calcItem = self.calcList[switch]

        try:
            #convert string data to float(string contains comma)
            float_data = [self.convert_S2F(item) for item in calcItem.data]

            #for status attribute, default is green, modify to red if computation conditions are not met
            status_color = Output.green
            status_data = 'Green'

            #first data has nothing before it, no comparison needed, thus color remains black
            calcItem.data_color.append(Output.black)

            #first item neglected, nothing to compare before it
            #last item neglected, since TTM data is not needed
            for ind,item in enumerate(float_data[1:-1]):
                #resets to green every cycle
                indiv_color = Output.green

                #if value decreases over the year, set data_color to red, status no longer golden
                if item < float_data[ind]:
                    indiv_color = Output.red
                    status_color = Output.red
                    status_data = 'Red'
                calcItem.data_color.append(indiv_color)

            #set TTM data text to blue just to make it stand out
            calcItem.data_color.append(Output.blue)
            #set status tile and text color
            calcItem.status = status_color
            calcItem.status_data = status_data
        except:
            #catch error
            print('compute_function:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            calcItem.data = ['compute function','','','','','']
            calcItem.data_color = [Output.red,Output.red,Output.red,Output.red,Output.red,Output.red]
            calcItem.status = Output.red
            calcItem.status_data = 'Red'

    def print_output(self,string):
        if string == 'earnings':
            print(self.earnings.status);print(self.earnings.status_data)
            print(self.earnings.data);print(self.earnings.data_color)
        elif string == 'revenue':
            print(self.revenue.status);print(self.revenue.status_data)
            print(self.revenue.data);print(self.revenue.data_color)
        elif string == 'cash_flow':
            print(self.cash_flow.status);print(self.cash_flow.status_data)
            print(self.cash_flow.data);print(self.cash_flow.data_color)
        elif string == 'gross_margin':
            print(self.gross_margin.status);print(self.gross_margin.status_data)
            print(self.gross_margin.data);print(self.gross_margin.data_color)
        elif string == 'net_margin':
            print(self.net_margin.status);print(self.net_margin.status_data)
            print(self.net_margin.data);print(self.net_margin.data_color)
        elif string == 'LT_growthRate':
            print(self.LT_growthRate.status);print(self.LT_growthRate.status_data)
            print(self.LT_growthRate.data);print(self.LT_growthRate.data_color)
        elif string == 'LT_debt':
            print(self.LT_debt.status);print(self.LT_debt.status_data)
            print(self.LT_debt.data);print(self.LT_debt.data_color)
        elif string == 'ROE':
            print(self.ROE.status);print(self.ROE.status_data)
            print(self.ROE.data);print(self.ROE.data_color)
        elif string == 'intrinsic_val':
            print(self.intrinsic_val.status);print(self.intrinsic_val.status_data)
            print(self.intrinsic_val.data);print(self.intrinsic_val.data_color)

    def compute_earnings(self):
        #load data
        self.earnings.data = self.in_earnings        
        
        #pass '0' as parameter to indicate 'earnings'
        self.compute_5years(0)
            
        #self.print_output('earnings')

    def compute_revenue(self):
        #load data
        self.revenue.data = self.in_revenue        
            
        #pass '1' as parameter to indicate 'revenue'
        self.compute_5years(1)
            
        #self.print_output('revenue')
                
    def compute_cashFlow(self):
        #load data
        self.cash_flow.data = self.in_cash_flow  
            
        #pass '2' as parameter to indicate 'cash flow'
        self.compute_5years(2)        
            
        #self.print_output('cash_flow')
            
    def compute_grossMargin(self):
        #input validation is not carried out
        #load data
        self.gross_margin.data.append(self.in_gross_margin)
        #set color. Has to compare value to competitors, this feature is not being implemented
        self.gross_margin.status = Output.black
        self.gross_margin.status_data = 'Black'
        self.gross_margin.data_color.append(Output.blue)
            
        #self.print_output('gross_margin')

    def compute_netMargin(self):
        #input validation is not carried out
        #load data
        self.net_margin.data.append(self.in_net_margin)
        #set color. Has to compare value to competitors, this feature is not being implemented
        self.net_margin.status = Output.black
        self.net_margin.status_data = 'Black'
        self.net_margin.data_color.append(Output.blue)
            
        #self.print_output('net_margin')

    def compute_LTgrowthRate(self):
        try:
            result_gr = self.GR_getMeanGrowthRate()
            
            #load data
            self.LT_growthRate.data.append(str(result_gr))
            
            #if Long term growth Rate exceeds 10%, set status to green
            threshold = 10
            self.LT_growthRate.status = Output.red
            self.LT_growthRate.status_data = 'Red'
            if result_gr > threshold:
                self.LT_growthRate.status = Output.green
                self.LT_growthRate.status_data = 'Green'
                
            self.LT_growthRate.data_color.append(Output.black)
                
            #self.print_output('LT_growthRate')
        except:
            #catch error
            print('compute_LTgrowthRate:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.LT_growthRate.data = ['compute_LTgrowthRate','','','','','']
            self.LT_growthRate.data_color = [Output.red,Output.red,Output.red,Output.red,Output.red,Output.red]
            self.LT_growthRate.status = Output.red
            self.LT_growthRate.status_data = 'Red'

    def GR_getMeanGrowthRate(self):
        try:
            #extract mean and 1 year ago growth rate
            mean_gr = self.convert_S2F(self.in_LT_growthRate[1])
            oneYearAgo_gr = self.convert_S2F(self.in_LT_growthRate[4])
            #computation method: take the mean of mean_growth_rate and 1_year_ago_growth_rate
            result_gr = (mean_gr + oneYearAgo_gr) / 2
        except:
            result_gr = 'mean growth rate error'
            print(result_gr)
            
        return result_gr

    def compute_LTdebt(self):
        try:
            #conservative debt: LT_debt < 3 x Net Income
            debt = self.convert_S2F(self.in_LT_debt)
            threshold = 3 * self.convert_S2F(self.in_earnings[-1])

            #load data
            self.LT_debt.data.append(self.in_LT_debt)
            
            self.LT_debt.status = Output.red
            self.LT_debt.status_data = 'Red'
            if debt < threshold:
                self.LT_debt.status = Output.green
                self.LT_debt.status_data = 'Green'
                
            self.LT_debt.data_color.append(Output.black)
                
            #self.print_output('LT_debt')
        except:
            #catch error
            print('compute_LTdebt:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.LT_debt.data = ['compute_LTdebt','','','','','']
            self.LT_debt.data_color = [Output.red,Output.red,Output.red,Output.red,Output.red,Output.red]
            self.LT_debt.status = Output.red
            self.LT_debt.status_data = 'Red'
            
    def compute_returnOnEquity(self):
        try:
            #extract ROE
            roe = self.convert_S2F(self.in_ROE)

            #load data
            self.ROE.data.append(self.in_ROE)

            #if return on equity exceeds 12%, set status to green
            threshold = 12
            self.ROE.status = Output.red
            self.ROE.status_data = 'Red'
            if roe > threshold:
                self.ROE.status = Output.green
                self.ROE.status_data = 'Green'                

            self.ROE.data_color.append(Output.black)
                
            #self.print_output('ROE')
        except:
            #catch error
            print('compute_ROE:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.ROE.data = ['compute_ROE','','','','','']
            self.ROE.data_color = [Output.red,Output.red,Output.red,Output.red,Output.red,Output.red]
            self.ROE.status = Output.red
            self.ROE.status_data = 'Red'
            
    def compute_intrinsicVal(self):
        try:
            #formula:
            #get projected cash flow for ten years => cash flow * long term growthRate
            #get discounted values by applying discounted factor to all 10 years of cash flow
            #get present value of company by adding up all the discounted values
            #get rough intrinsic val of one share by dividing present val with outstanding shares
            #get intrinsic val by adding net cash per share((cashEquivalents-totalDebt)/outstanding shares)
            
            outstandingShares = self.convert_S2F(self.in_shares_outstanding)

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
            for ind, cf in enumerate(pcf_list,1):
                present_val += (cf * (1 / ((1+discount_rate) ** ind)))

                rough_IV_per_share = present_val / outstandingShares
                intrinsic_val = rough_IV_per_share + net_cash_per_share

            #update data
            self.intrinsic_val.data.append(str(intrinsic_val))
            self.intrinsic_val.status = Output.black
            self.intrinsic_val.status_data = 'Black'
            self.intrinsic_val.data_color.append(Output.blue)
            #print('present_val: {0}'.format(present_val))
            #print('rough_iv_per share: {0}'.format(rough_IV_per_share))
            #self.print_output('intrinsic_val')
        except:
            #catch error
            print('compute_intrinsicVal:{0}:{1}'.format(sys.exc_info()[0].__doc__,sys.exc_info()[1].args[0]))
            self.intrinsic_val.data = ['compute_intrinsicVal','','','','','']
            self.intrinsic_val.data_color = [Output.red,Output.red,Output.red,Output.red,Output.red,Output.red]
            self.intrinsic_val.status = Output.red
            self.intrinsic_val.status_data = 'Red'

    def IV_netCashPerShare(self,outstandingShares):
        try:
            ST_debt = self.convert_S2F(self.in_ST_debt)
            LT_debt = self.convert_S2F(self.in_LT_debt)
            cash_equivalents = self.convert_S2F(self.in_cash_equivalents)

            #formula
            return_val = (cash_equivalents - (ST_debt + LT_debt)) / outstandingShares
        except:
            return_val = 'net cash per share error'
            print(return_val)
            print('ST_debt:{0}:{1}'.format(type(self.in_ST_debt),self.in_ST_debt));
            print('LT_debt:{0}:{1}'.format(type(self.in_LT_debt),self.in_LT_debt));
            print('cash_equivalents:{0}:{1}'.format(type(self.in_cash_equivalents),self.in_cash_equivalents));            
            
        return return_val

    def IV_projectCashFlow(self):
        try:
            cash_flow = self.convert_S2F(self.in_cash_flow[-1])
            #convert percentage to decimal
            growth_rate = self.GR_getMeanGrowthRate() / 100
            #print('growth rate: {0}'.format(growth_rate))
            #projected cash flow
            pcf = []
            #TTM is the baseline, no calculation needed
            pcf.append(cash_flow)
            #loop for 10 times, and calculate projected cash flow in 10 years
            ind = 0
            while ind < 9:
                #current projected cash flow is
                #previous projected cash flow +
                #previous projected cash flow * growth rate
                pcf.append(pcf[ind] * growth_rate + pcf[ind])
                ind += 1
        except:
            pcf = 'pcf error'
            print(pcf)
            
        return pcf
        
    def IV_discountRate(self):
        try:
            #discount rate based on beta value(adam khoo)
            beta = self.convert_S2F(self.in_beta)
            if beta < 0.801:
                discount_rate = 0.05
            elif beta < 0.901:
                discount_rate = 0.055
            elif beta < 1.001:
                discount_rate = 0.06
            elif beta < 1.101:
                discount_rate = 0.068
            elif beta < 1.201:
                discount_rate = 0.07
            elif beta < 1.301:
                discount_rate = 0.079
            elif beta < 1.401:
                discount_rate = 0.08
            elif beta < 1.501:
                discount_rate = 0.089
            else:
                discount_rate = 0.09
        except:
            discount_rate = 'discount_rate error'
            print(discount_rate)

        return discount_rate
