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
