#!/usr/bin/env python3

from bs4 import *

html_head = '../../input_files/htmls/'
html_tail1 = '/MS_url1.txt'
html_tail2 = '/MS_url2.txt'
html_tail3 = '/MS_url3.txt'
html_tail4 = '/MS_url4.txt'
html_tail5 = '/R_url1.txt'
html_tail6 = '/R_url2.txt'

def BDI_read(symbol,BDI_input):
    html_tails = [html_tail1,
                  html_tail2,
                  html_tail3,
                  html_tail4,
                  html_tail5,
                  html_tail6]

    #convert the six html text files to BeautifulSoup htmls 
    html_pages = []
    for html_tail in html_tails:
        html_path = html_head + symbol + html_tail
        with open(html_path,'r') as fptr:
            html_data = fptr.read()
        html_pages.append(BeautifulSoup(html_data,'html.parser'))

    #html_pages[0] -> earnings,revenue
    #html_pages[1] -> long/short-term debt,cash & equivalent
    #html_pages[2] -> cash flow
    #html_pages[3] -> gross margin, net margin, return on equity
    #html_pages[4] -> Long Term growth rate
    #html_pages[5] -> Beta, outstanding shares    

    #Extract required data from html pages 
    BDI_input.get_earnings(html_pages[0])
    BDI_input.get_revenue(html_pages[0])
    BDI_input.get_LTdebt(html_pages[1])
    BDI_input.get_STdebt(html_pages[1])
    BDI_input.get_cashEquivalents(html_pages[1])
    BDI_input.get_cashFlow(html_pages[2])
    BDI_input.get_grossMargin(html_pages[3])
    BDI_input.get_netMargin(html_pages[3])
    BDI_input.get_returnOnEquity(html_pages[3])
    BDI_input.get_LTgrowthRate(html_pages[4])
    BDI_input.get_beta(html_pages[5])
    BDI_input.get_sharesOutstanding(html_pages[5])

def BDI_compute(BDI_input,BDI_output):
    #execute computation
    BDI_output.load_inputs(BDI_input)

    BDI_output.compute_earnings()
    BDI_output.compute_revenue()
    BDI_output.compute_cashFlow()
    BDI_output.compute_grossMargin()
    BDI_output.compute_netMargin()
    BDI_output.compute_LTgrowthRate()
    BDI_output.compute_LTdebt()
    BDI_output.compute_returnOnEquity()
    BDI_output.compute_intrinsicVal()

def BDI_write(BDI_output,cf_data,oo_data):
    data_rowCursor, oo_sheet = oo_data
    data_colCursor = 0
    offset = 7

    #write ind, symbol, name, sector
    oo_sheet[ data_rowCursor , data_colCursor : 4 ].values = cf_data
    data_colCursor += 4

    #write earnings
    #validate that valid data exist
    earnings = BDI_output.earnings
    if earnings.data:
        oo_sheet[ data_rowCursor , data_colCursor ].background_color = earnings.status
        oo_sheet[ data_rowCursor , data_colCursor ].text_color = earnings.status
        oo_sheet[ data_rowCursor , data_colCursor ].value = earnings.status_data
        data_colCursor += 1
        for index,item in enumerate(earnings.data):
            oo_sheet[ data_rowCursor , data_colCursor ].value = item
            oo_sheet[ data_rowCursor , data_colCursor ].text_color = earnings.data_color[index]
            data_colCursor += 1
    else:
        oo_sheet[ data_rowCursor , data_colCursor ].value = 'error'
        data_colCursor += 1

    #write revenue
    #validate that valid data exist
    revenue = BDI_output.revenue
    if revenue.data:
        oo_sheet[ data_rowCursor , data_colCursor ].background_color = revenue.status
        oo_sheet[ data_rowCursor , data_colCursor ].text_color = revenue.status
        oo_sheet[ data_rowCursor , data_colCursor ].value = revenue.status_data
        data_colCursor += 1
        for index,item in enumerate(revenue.data):
            oo_sheet[ data_rowCursor , data_colCursor ].value = item
            oo_sheet[ data_rowCursor , data_colCursor ].text_color = revenue.data_color[index]
            data_colCursor += 1
    else:
        oo_sheet[ data_rowCursor , data_colCursor ].value = 'error'
        data_colCursor += 1

    #write cash flow
    #validate that valid data exist
    cash_flow = BDI_output.cash_flow
    if cash_flow.data:
        oo_sheet[ data_rowCursor , data_colCursor ].background_color = cash_flow.status
        oo_sheet[ data_rowCursor , data_colCursor ].text_color = cash_flow.status
        oo_sheet[ data_rowCursor , data_colCursor ].value = cash_flow.status_data
        data_colCursor += 1
        for index,item in enumerate(cash_flow.data):
            oo_sheet[ data_rowCursor , data_colCursor ].value = item
            oo_sheet[ data_rowCursor , data_colCursor ].text_color = cash_flow.data_color[index]
            data_colCursor += 1
    else:
        oo_sheet[ data_rowCursor , data_colCursor ].value = 'error'
        data_colCursor += 1

    #write gross profit margin
    #validate the data
    gross_margin = BDI_output.gross_margin
    if gross_margin.data:
        oo_sheet[ data_rowCursor , data_colCursor ].background_color = gross_margin.status
        oo_sheet[ data_rowCursor , data_colCursor ].text_color = gross_margin.status
        oo_sheet[ data_rowCursor , data_colCursor ].value = gross_margin.status_data
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = gross_margin.data[0]
        oo_sheet[ data_rowCursor , data_colCursor+1 ].text_color = gross_margin.data_color[0]
    else:
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = 'error'
    data_colCursor += 2

    #write net profit margin
    #validate the data
    net_margin = BDI_output.net_margin
    if net_margin.data:
        oo_sheet[ data_rowCursor , data_colCursor ].background_color = net_margin.status
        oo_sheet[ data_rowCursor , data_colCursor ].text_color = net_margin.status
        oo_sheet[ data_rowCursor , data_colCursor ].value = net_margin.status_data
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = net_margin.data[0]
        oo_sheet[ data_rowCursor , data_colCursor+1 ].text_color = net_margin.data_color[0]
    else:
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = 'error'
    data_colCursor += 2    

    #write LT_growthRate
    #validate the data
    LT_growthRate = BDI_output.LT_growthRate
    if LT_growthRate.data:
        oo_sheet[ data_rowCursor , data_colCursor ].background_color = LT_growthRate.status
        oo_sheet[ data_rowCursor , data_colCursor ].text_color = LT_growthRate.status
        oo_sheet[ data_rowCursor , data_colCursor ].value = LT_growthRate.status_data
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = LT_growthRate.data[0]
        oo_sheet[ data_rowCursor , data_colCursor+1 ].text_color = LT_growthRate.data_color[0]
    else:
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = 'error'
    data_colCursor += 2

    #write Long term debt
    #validate the data
    LT_debt = BDI_output.LT_debt
    if LT_debt.data:
        oo_sheet[ data_rowCursor , data_colCursor ].background_color = LT_debt.status
        oo_sheet[ data_rowCursor , data_colCursor ].text_color = LT_debt.status        
        oo_sheet[ data_rowCursor , data_colCursor ].value = LT_debt.status_data
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = LT_debt.data[0]
        oo_sheet[ data_rowCursor , data_colCursor+1 ].text_color = LT_debt.data_color[0]
    else:
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = 'error'
    data_colCursor += 2

    #write Return on equity
    #validate the data
    ROE = BDI_output.ROE
    if ROE.data:
        oo_sheet[ data_rowCursor , data_colCursor ].background_color = ROE.status
        oo_sheet[ data_rowCursor , data_colCursor ].text_color = ROE.status
        oo_sheet[ data_rowCursor , data_colCursor ].value = ROE.status_data
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = ROE.data[0]
        oo_sheet[ data_rowCursor , data_colCursor+1 ].text_color = ROE.data_color[0]
    else:
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = 'error'
    data_colCursor += 2

    #write Intrinsic Value
    #validate the data
    intrinsic_val = BDI_output.intrinsic_val
    if intrinsic_val.data:
        oo_sheet[ data_rowCursor , data_colCursor ].background_color = intrinsic_val.status
        oo_sheet[ data_rowCursor , data_colCursor ].text_color = intrinsic_val.status
        oo_sheet[ data_rowCursor , data_colCursor ].value = intrinsic_val.status_data
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = intrinsic_val.data[0]
        oo_sheet[ data_rowCursor , data_colCursor+1 ].text_color = intrinsic_val.data_color[0]
    else:
        oo_sheet[ data_rowCursor , data_colCursor+1 ].value = 'error'
    data_colCursor += 2
    
        
def BDI_clean(BDI_output):
    BDI_output.earnings.data_color = []
    BDI_output.revenue.data_color = []
    BDI_output.cash_flow.data_color = []    
    BDI_output.gross_margin.data = []
    BDI_output.gross_margin.data_color = []    
    BDI_output.net_margin.data = []
    BDI_output.net_margin.data_color = []    
    BDI_output.LT_growthRate.data = []
    BDI_output.LT_growthRate.data_color = []    
    BDI_output.LT_debt.data = []
    BDI_output.LT_debt.data_color = []    
    BDI_output.ROE.data = []
    BDI_output.ROE.data_color = []    
    BDI_output.intrinsic_val.data = []
    BDI_output.intrinsic_val.data_color = []    

    '''
    save space doing it this way, but takes longer
    while BDI_output.gross_margin.data:
        BDI_output.gross_margin.data.pop()
        BDI_output.gross_margin.data_color.pop()
    '''
    
