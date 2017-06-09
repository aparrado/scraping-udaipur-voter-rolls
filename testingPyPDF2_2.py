#--------------------------------#
#------Akshat Goel---------------#
#------IDinsight-----------------#
#------Monday, Feb. 27th 2017----#
#--------------------------------#

### This file takes as input an arbitrary PDF file from the Rajasthan website
### It extracts household IDs and voter IDs
### Household IDs are extracted with an error
### Voter IDs are extracted exactly

### Changes to be made: 
### Don't open a new instance of the browser for each voter ID, just clear the text box and then input
### Error handling
### Download draft voter rolls 

## Importing required packages
import PyPDF2, re, time, string, pandas
import selenium_test as st
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

## Creating a PDF file object that Python can read
## Extracting information about the file
def dataFeatures(name):

	## Importing file object
	pdfFileObj = open(current_dir + name, 'rb') ##Insert the text file
	## Create file reader object
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	## Get ending page
	end_page = pdfReader.getNumPages()
	## Return statement
	return [pdfReader, end_page]

## Extracting all text data from a given page on a given .pdf
def dataConstruct(pdfReader, current_page):

	## Create page object from target page
	pageObj = pdfReader.getPage(current_page)
	## Extract the text
	pageObjtext = pageObj.extractText()
	## Split text into list so that we can use list comprehension commands later
	pageObjtext = pageObjtext.split(" ")
	##Creating tractable list to parse
	data = [re.sub("97(.*)567#",' ',s) for s in pageObjtext]
	##Return statement
	return(data)

## Getting voter IDs
## Missing values are coded as "RJ/00/000/000000"
def voterIDextract(data):

	##Extracting voter IDs
	voter_id = [data[i+1] for i in range(len(data)) if "97" in data[i]]
	##Recoding missing values
	voter_id = ["RJ/00/000/000000" if s == '' else s for s in voter_id]
	##Cleaning
	voter_id = [re.findall("([A-Z]{3}[////][0-9]{7})|(RJ[////][0-9]{2}[////][0-9]{3}[////][0-9]{6})",s) for s in voter_id]
	## Flattening list
	voter_id = [j for s in voter_id for i in s for j in i if j != '']
	#Printing output
	return(voter_id)

## Write output to file
def outputWrite(name):

	# Creating entire file object along with start and end page
	pdfRajasthan = dataFeatures(name)
	## Initializing page counters
	current_page = 2
	end_page = pdfRajasthan[1]
	## Initializing list of voters to send to website
	voters = []
		
	## Cycling through PDF to construct master list of voters
	while current_page < end_page:
		## Printing current and ending page so user knows how long to suffer
		print(current_page)	
		print(end_page)									
		## Constructing voter-IDs by calling the dataConstruct function page by page and appending							
		data = dataConstruct(pdfRajasthan[0], current_page) 	
		voters.append(voterIDextract(data)) 
		## Updating page number	  					
		current_page += 1										
		
	## Flattening lists
	voters1 = [j.strip() for s in voters for j in s]
	## Master list	
	voters2 = [j.strip() for s in voters for j in s] 
	## Deleting voter list 
	del voters		
	## Printing total no. of voters to do 
	print(len(voters2))
	
	## Function call - takes into account that we don't want to send the same voter IDs twice 	
	for voter in voters1:
		
		if voter in voters2 and voter != "RJ/00/000/000000": 
			print(voter) 
			## Calling function from other script
			## This call will write all the data for the retrieved voter IDs in the CSV and then also record them so they are not repeated
			voter_in_hh = st.getHHdata(voter)
			## Taking away leading and trailing white-space
			voter_in_hh = [j.strip() for j in voter_in_hh]
			## Removing all the voter IDs for which we get data from this call from master list
			voters2 = [x.strip() for x in voters2 if x not in voter_in_hh]
			## Print the number of remaining voters in the current .pdf file
			print(len(voters2))
			
## Initializing timer
t0 = time.time()

## Executing code
outputWrite("157.pdf")

## Stopping timer
t1 = time.time()

## Reporting time
print(t1 - t0)
