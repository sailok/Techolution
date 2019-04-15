from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import csv
import datetime
import time
import numpy as np
import os


def sort_file():
	#lists and dictionaries to maintain data
	rows_dict={}
	sort_row=[]
	date={}
	
	#opening the data.csv file to sort the data
	with open('data.csv','r') as f:
		reader=csv.reader(f)
		
		for row in reader:
			#rows_dict stores date as key and no of jobs posted on that date as value
			#rows_dict['January 1st 2019']=['Job name 1','Job name 2']
			#decode converts date from January 1st 2019 -> January 1 2019
			x=decode(row[1])
			rows_dict.setdefault(x,[]).append(row[0])
			#date dict conatins decoded date as key as original date as value
			date[x]=row[1]

	#sorting the rows_dict based on the decoded dates
	for key in sorted(rows_dict,key= lambda date : datetime.datetime.strptime(date,'%B %d %Y')):
		#for each key and each value we are append that to a list
		for i in range(len(rows_dict[key])):
			sort_row.append([rows_dict[key][i],date[key]])
	
	#creating a new csv file
	path=os.getcwd()+'/sorted_data.csv'
	
	if os.path.exists(path):
		pass
	else:
		f=open('sorted_data.csv','w')
		f.close()
	
	#Writing the sorted data in to a file named sorted_data.csv
	with open(os.getcwd()+'/sorted_data.csv','w') as f:
		writer=csv.writer(f)	
		for i in sort_row:
			writer.writerow(i)

def decode(s):
	#decode converts date from January 1st 2019 -> January 1 2019
	for i in range(1,32):
		if i==1 or i==21 or i==31:
			s=s.replace(str(i)+'st',str(i))
		elif i==2 or i==22:
			s=s.replace(str(i)+'nd',str(i))
		elif i==3 or i==23:
			s=s.replace(str(i)+'rd',str(i))
		else:
			s=s.replace(str(i)+'th',str(i))
	return s

def csv_file(array):
	#creating a file called data.csv
	path=os.getcwd()+'/data.csv'
	
	if os.path.exists(path):
		pass
	else:
		f=open('data.csv','w')
		f.close()
	
	#appending the data in unsorted manner into file
	with open(os.getcwd()+'/data.csv','a') as f:
		writer=csv.writer(f)	
		for i in array:
			writer.writerow(i)

def unescape(s):
	#replaces all escape characters into symbols
	s=s.replace('&lt;','<')
	s=s.replace('&gt;','>')
	s=s.replace('&amp;','&')
	s=s.replace('&apos;',"'")
	s=s.replace('&qout;','"')	
	
	return s
	
def download(url,driver):
	#opening the webpage and parsing it through Beautiful soup
	driver.get(url)
	html_page=driver.page_source
	soup=BeautifulSoup(html_page)
	
	#this list contains no of categories of jobs 
	job_cat=[]
	jobType=soup.find('div',attrs={'id':'joblist'})
	data=jobType.findAll('div',attrs={'class':'ui segments'})

	for job in jobType:
		job_cat.append(job.find('h2').text)
	
	array=[]

	#for each category of job
	for i in range(1,len(job_cat)+1):
		#searching each job web element	
		xpath='//*[@id="joblist"]/div['+str(i)+']'
		elem=driver.find_element_by_xpath(xpath)
		
		#getting the no of jobs HTML element
		html_code=elem.get_attribute('innerHTML')
		b_soup=BeautifulSoup(html_code)
		data=b_soup.findAll('div',attrs={'class':'ui segment job_list_card'})	
		# for each job in that category
		for j in range(2,len(data)+2):
			#scraping the name of the job and storing it job_name
			job_name=data[j-2].find('h3',attrs={'class':'job_name text-ellipsis'}).text
			#removing escape characters
			job_name=unescape(job_name)
			
			#clicking on the job link
			xpath='//*[@id="joblist"]/div['+str(i)+']/div['+str(j)+']/div'
			driver.find_element_by_xpath(xpath).click()
			time.sleep(1)
			
			#parsing the web page
			html_page=driver.page_source
			soup=BeautifulSoup(html_page)
		
			#searching the webpage for date of posting
			jobType=soup.findAll('span',attrs={'class':'value'})
			
			#storing the date
			date=jobType[6].text
			
			#mainting a list which contains list of job name and date
			array.append([str(job_name),str(date)])		
			driver.back()
			time.sleep(1)
		
	#converts python list into csv file	
	csv_file(array)

def main():
	#using selenium to open the website
	url="https://techolution.app.param.ai/jobs"
	driver=webdriver.Chrome(executable_path='/home/sailok/Downloads/chromedriver_linux64/chromedriver')
	
	#downloading the website data
	download(url,driver)
	#sorting the downloading the data according to most old first
	sort_file()
	
if __name__=="__main__":
	main()
