#############################################################################
#	All source files in the current directory are taken from this
#	github directory: https://github.com/datasets/s-and-p-500-companies
#	Credit goes to the author.
#############################################################################

all: ../../input_files/constituents-financials.csv

List_of_S%26P_500_companies.html:
	curl -o List_of_S%26P_500_companies.html "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

../../input_files/constituents.csv: List_of_S%26P_500_companies.html constituents.py
	python3 constituents.py

../../input_files/constituents-financials.csv: ../../input_files/constituents.csv constituents-financials.py
	python3 constituents-financials.py
