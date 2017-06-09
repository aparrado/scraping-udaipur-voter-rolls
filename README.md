# scraping-udaipur-voter-rolls
Python code for automatically downloading and writing list of publicly available voter IDs and data from Udaipur district, Rajasthan

# workflow 
The 3 files in this repository execute a program which scrapes all the data available for voters registered in Udaipur district, Rajasthan. This information is located on the web-site of the Election Commissioner of Rajasthan. Here is the work-flow: 

1) The first file downloads all the relevant .pdfs from the website. 

2) The second file parses an arbitrary .pdf from this collection to generate a list of voter IDs. It then calls the third file. 

3) The third file contains a function that sends a voter ID to the website, automatically interacts with it, downloads the data and writes it to a CSV. 

# contributions welcome!

This project is still a work in progress. Here are changes that still need to be made: 

1) Error handling

2) Don't open a new browser instance every time a voter ID is sent to the website 

3) Download the draft voter rolls 

4) Use Amazon Web Service instances for practical execution 
