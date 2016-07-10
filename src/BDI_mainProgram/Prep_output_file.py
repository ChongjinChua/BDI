#!/usr/bin/env python3

import sys, time
import pyoo, pandas
import socket
import subprocess as sub

def oo_write_header(oo_sheet):
    #write file description
    oo_sheet[0,0].value = 'Fundamental analysis of the current S&P500 companies'
    oo_sheet[0,0].font_weight = pyoo.FONT_WEIGHT_BOLD

    #write analysis description
    #oo_cells = oo_sheet[2:11,0:7]
    oo_sheet[2:11,0].values = ['Criteria','Earnings over 5 years','Sales and Revenues over 5 years',
                              'Operating Cash Flow over 5 years','Gross/Net profit margin','Long-Term Growth Rates',
                              'Long-Term Debt','Return On Equity','Intrinsic Value']
    oo_sheet[3:11,3].values = ['Increase over the years','Increase over the years','Increase over the years',
                              'Higher than closest competitors','Higher than 10%','3 x current net income after tax',
                              'Higher than 15%','Lower than current price']
    oo_sheet[2,0].font_weight = pyoo.FONT_WEIGHT_BOLD
    oo_sheet[2:12,0:6].border_top_width = 65
    oo_sheet[2:11,5].border_right_width = 75
    oo_sheet[2:11,0].border_left_width = 75
    oo_sheet[3:11,3].border_left_width = 75       

    #prepare header
    oo_sheet[13:15,0:29].font_weight = pyoo.FONT_WEIGHT_BOLD
    oo_sheet[14,0:29].values = ['Index','Symbol',
                                'Name','Sector',
                                'Status','2011','2012','2013','2014','2015','TTM',
                                'Status','2011','2012','2013','2014','2015','TTM',
                                'Status','2011','2012','2013','2014','2015','TTM',
                                'LT Growth (%)','LT Debt (Millions)','ROE (%)','Intrinsic Val ($)']
    oo_sheet[13,4].value = 'Earnings over 5 years (Millions)'
    oo_sheet[13,11].value = 'Sales & Revenue over 5 years (Millions)'
    oo_sheet[13,18].value = 'Operating Cash Flow over 5 years (Millions)'

    oo_sheet[13:519,0:29].border_top_width = 75
    oo_sheet[13:518,25:29].border_width = 70
    oo_sheet[13:518,0:5].border_left_width = 65
    oo_sheet[13:518,11].border_left_width = 65    
    oo_sheet[13:518,18].border_left_width = 65    
    oo_sheet[14:518,5:11].border_left_width = 40
    oo_sheet[14:518,12:18].border_left_width = 40
    oo_sheet[14:518,19:25].border_left_width = 40
    pass

filename = 'analysis.ods'
target = '../../output_files/' + filename
cf_csvfile = '../../input_files/constituents-financials.csv'
encoding = 'utf-8'

#use subprocess to make command line calls 
p = sub.Popen(['ls', target],stdout=sub.PIPE,stderr=sub.PIPE)
output,error = p.communicate()
output = output.decode(encoding).rstrip('\n'); error = error.decode(encoding).rstrip('\n')

#determine whether output file exist
file_exist = False
if output == target:
    file_exist = True

#if analysis.ods exist, delete it
if file_exist:
    print("-analysis.ods exist. removing...")
    sub.Popen(["rm",target])

#setup connection to soffice
oo_desktop = pyoo.Desktop()

#create a new analysis.ods
print("-creating new ods file...")
oo_doc = oo_desktop.create_spreadsheet()
time.sleep(1)

#get sheet
oo_sheet = oo_doc.sheets[0]

#populate spreadsheet with header
oo_write_header(oo_sheet)

#extract S&P500 company symbols,names,sectors
'''
cf_data = pandas.read_csv(cf_csvfile)
cf_symbols = cf_data.Symbol.tolist()
cf_name = cf_data.Name.tolist()
cf_sector = cf_data.Sector.tolist()
'''
#save spreadsheet
print("-saving ods file...")
oo_doc.save(target)
time.sleep(1)

#close spreadsheet 
print("-closing ods file...")
oo_doc.close()
time.sleep(1)
