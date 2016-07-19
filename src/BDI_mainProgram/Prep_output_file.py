#!/usr/bin/env python3

import sys, time
import pyoo, pandas
import socket
from BDI_operations import *
from BDI_dataStruct import *

def oo_write_header(oo_sheet):
    #write file description
    oo_sheet[0,0].value = 'Fundamental analysis of the current S&P500 companies'
    oo_sheet[0,0].font_weight = pyoo.FONT_WEIGHT_BOLD

    #write analysis description
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
    hdr_rowStart = 13
    hdr_rowEnd = 518
    hdr_colStart = 0
    hdr_colEnd = 37
    oo_sheet[ hdr_rowStart : 15 , hdr_colStart : hdr_colEnd ].font_weight = pyoo.FONT_WEIGHT_BOLD
    oo_sheet[ hdr_rowStart+1 , hdr_colStart : hdr_colEnd ].values = ['Index','Symbol',
                                                                     'Name','Sector',
                                                                     'Status','2011','2012','2013','2014','2015','TTM',
                                                                     'Status','2011','2012','2013','2014','2015','TTM',
                                                                     'Status','2011','2012','2013','2014','2015','TTM',
                                                                     'Status','Gross Profit Margin (%)',
                                                                     'Status','Net Profit Margin (%)',
                                                                     'Status','LT Growth (%)',
                                                                     'Status','LT Debt (Millions)',
                                                                     'Status','ROE (%)',
                                                                     'Status','Intrinsic Val ($)']
    oo_sheet[ hdr_rowStart , 4 ].value = 'Earnings over 5 years (Millions)'
    oo_sheet[ hdr_rowStart , 11 ].value = 'Sales & Revenue over 5 years (Millions)'
    oo_sheet[ hdr_rowStart , 18 ].value = 'Operating Cash Flow over 5 years (Millions)'

    oo_sheet[ hdr_rowStart : hdr_rowEnd+1 , hdr_colStart : hdr_colEnd ].border_top_width = 75
    oo_sheet[ hdr_rowStart : hdr_rowEnd , 25 : hdr_colEnd ].border_width = 70
    oo_sheet[ hdr_rowStart : hdr_rowEnd , hdr_colStart : 5 ].border_left_width = 65
    oo_sheet[ hdr_rowStart : hdr_rowEnd , 11 ].border_left_width = 65    
    oo_sheet[ hdr_rowStart : hdr_rowEnd , 18 ].border_left_width = 65    
    oo_sheet[ hdr_rowStart+1 : hdr_rowEnd , 5 : 11 ].border_left_width = 40
    oo_sheet[ hdr_rowStart+1 : hdr_rowEnd , 12 : 18 ].border_left_width = 40
    oo_sheet[ hdr_rowStart+1 : hdr_rowEnd , 19 : 25 ].border_left_width = 40
    pass

filename = 'analysis.ods'
target = '../../output_files/' + filename
cf_csvfile = '../../input_files/constituents-financials.csv'

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
cf_data = pandas.read_csv(cf_csvfile)
cf_symbols = cf_data.Symbol.tolist()
cf_names = cf_data.Name.tolist()
cf_sectors = cf_data.Sector.tolist()

#Create input and output class, will be reused for all companies
BDI_input = Input()
BDI_output = Output()
ind = 1
valid = 1
#beginning row of data
data_rowNum = 15

#read htmls, execute computations and write to analysis.ods company by company
for i,item in enumerate(cf_symbols[:30]):
    cf_data = [i+1,cf_symbols[i],cf_names[i],cf_sectors[i]]
    oo_data = [data_rowNum,oo_sheet]
    
    BDI_read(cf_symbols[i],BDI_input)
    #clean up output
    BDI_clean(BDI_output)

    #compute only when inputs are valid, if not jump straight to write function
    BDI_compute(BDI_input,BDI_output)
    BDI_write(BDI_output,cf_data,oo_data)
    data_rowNum += 1

#save spreadsheet
print("-saving ods file...")
oo_doc.save(target)
time.sleep(1)

#close spreadsheet 
print("-closing ods file...")
oo_doc.close()
time.sleep(1)
