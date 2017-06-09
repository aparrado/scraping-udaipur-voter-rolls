#--------------------------------#
#------Akshat Goel---------------#
#------IDinsight-----------------#
#------Monday, Feb. 27th 2017----#
#--------------------------------#

### Will modify this description once this code is tested!!
### This code takes in a voter ID and then uses the Python Selenium package to automatically interact with the website
### It writes the collected data to a .csv file 
### It returns a list of voter IDs in the same household

## Changes to be made: 
## Don't open a new instance of the browser for each voter ID, just clear the text box and then input
## Error handling
## Download draft voter rolls 

## Importing required packages
import PyPDF2, re, time, string, pandas
import unicodecsv as csv

## Importing exceptions for exception handling
from selenium.common.exceptions import ElementNotSelectableException, ElementNotVisibleException 
from selenium.common.exceptions import ErrorInResponseException, InvalidElementStateException
from selenium.common.exceptions import NoSuchAttributeException, NoSuchElementException

## Importing web-driver components 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


## Set to your working directory
current_dir = "/Users/Akshat/Desktop/"

## Modify this as required
## Setting the path to the browser drivers
path_to_chromedriver = current_dir + 'Packages and software/chromedriver'
path_to_PhantomDriver = current_dir + 'Packages and software/phantomjs-2.1.1-macosx/bin/phantomjs'
	
## Storing target URL
url = "http://164.100.153.10/electoralroll/Default.aspx"

## Function that takes in a voter ID and returns: 1) information on every other voter ID in the household and 2) 	
def getHHdata(voter_id):

	## Running this code block launches a new instance of Chrome
	## Storing new instance of Chrome in object named 'browser'
	## Set to your working directory
	
	browser = webdriver.PhantomJS(executable_path = path_to_PhantomDriver)

	## Getting URL
	browser.get(url)

	## Sending voter ID to the box 
	browser.find_element_by_name("txtvidcardno").send_keys(voter_id)

	## Clicking search button 
	browser.find_element_by_name("Button1").click()

	## Waiting until individual results load - will change this to name or id rather than xpath
	element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="GridView2"]/tbody/tr[2]/td[1]/a')))

	## Clicking button for entire household - will change this to name or id rather than xpath
	browser.find_element_by_xpath('//*[@id="GridView2"]/tbody/tr[2]/td[1]/a').click()

	## Waiting until table loads
	element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'GridView1')))

	## Setting row and column numbers 
	## Using XPath here despite what Qayam said because html rows don't seem to have other attributes like name or id
	rows = browser.find_elements_by_xpath('//*[@id="GridView1"]/tbody/tr') 
	row_count = len(rows)
	col_count = 13 ## Ideally wouldn't have hard-coded this but couldn't get the code to calculate the no. of columns to work

	## Getting data by cell using list comprehension 
	data = [browser.find_element_by_xpath('//*[@id="GridView1"]/tbody/tr[' + str(row) +']/td[' +str(col) +']').text for row in range(2, row_count+1) for col in range(1,col_count + 1)]
	variable1 =  [data[j:j + col_count] for j in range(0, len(data), col_count)]
	
	## Storing voters 
	voter_hh = [data[j] for j in range(9, len(data),col_count)]

	## Storing in pandas data frame for easy export to .csv later
	pd = pandas.DataFrame(variable1)

	## Writing to file using pandas function
	## Encoding is very important to retain or else your spreadsheet software will not see the Hindi script
	with open(current_dir + 'test1.csv', 'a', encoding='utf-16') as f:
	
		## Will write the headers in the .csv soon! 
		pd.to_csv(f, header=False, encoding='utf-16', sep = '\t')
	
	## Returning list of voter IDs contained in the household so that we can remove from the to-do list in the calling script
	return(voter_hh)






