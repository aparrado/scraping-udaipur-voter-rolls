#--------------------------------#
#------Akshat Goel---------------# 
#------IDinsight-----------------# 
#------Thursday, Feb. 23rd 2017--#
#--------------------------------#

## Importing relevant libraries 
import requests, os, time

## Beginning timer
start_time = time.time()

#Description:
#This function takes as input the serial no. of the last polling booth on an assembly web-page 
#It creates a directory to store the files
#It cycles through each .pdf by updating the serial number of the polling both
#It writes each file to the created directory
#The final output is a collection of PDF files (one per polling booth) that give the list of voters registered at that booth

def downloadVoterListPDF(end_url_no, ac_no):
	
	
	#Storing current working directory [Change to yours!]
	current_dir = "/Users/Akshat/Desktop/IDinsight/Tech_Team/Scraping/Udaipur/"
	
	#Store .pdfs in file
	#Ensure program does not throw an error if the directory already exists
	os.makedirs("AC No." + str(format(ac_no, '03d')), exist_ok=True) 
	
	#Initializing current URL to track where the script has reached  
	current_url_no = 1
	
	while not current_url_no > end_url_no: 
		
		#Get PDF
		res = requests.get("http://www.ceorajasthan.nic.in/erolls/pdf/dper-07/A" + str(format(ac_no, '03d')) + "/A" + str(format(ac_no, '03d')) + str(format(current_url_no, '03d')) +".pdf")
		type(res)
		res.status_code == requests.codes.ok
	
		#Write PDF
		with open( current_dir + "AC No." + str(format(ac_no, '03d'))+"/"+ str(format(current_url_no, '03d')) + ".pdf", 'wb') as f:
			f.write(res.content)
    
    	#Update URL to the next page
		current_url_no = current_url_no + 1 
		
		
#Testing function 

downloadVoterListPDF(286,149)
print("Done!")

downloadVoterListPDF(279,150)
print("Done!")

downloadVoterListPDF(307,151)
print("Done!")

downloadVoterListPDF(257,152)
print("Done!")

downloadVoterListPDF(216,153)
print("Done!")

downloadVoterListPDF(259,154)
print("Done!")

downloadVoterListPDF(264,155)
print("Done!")

downloadVoterListPDF(280,156)
print("Done!")

#Timing function
print(time.time() - start_time)


#Still need to add: 

#1) Scraped names and numbers to automate function calls (and get rid of the hard-coding)

#2) Multi-threaded code for faster execution


