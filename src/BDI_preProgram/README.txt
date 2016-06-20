#############################################################################
#	All source files in the current directory are taken from this
#	github directory: https://github.com/datasets/s-and-p-500-companies
#	Credit goes to the author.
#############################################################################

Run the scripts

These Linux scripts scrape data from Wikipedia page about S&P500 and computes a datapackage augmented with yahoo webservices.

They have been tested under Debian Jessy.
Install the dependencies

The scripts work with some python and shell scripts glued together with a Makefile.

Install the required python libraries :

cd scripts
pip install -r requirements.txt

You can also work on a virtualenv .
Run the scripts

make

