"""
Written by : Mirazus Salehin
Version : Beta 
Requirements : python 2.7 or higher,appropiet seleniuum web driver
			   python modules - selenium,fbchat
NOTE: This programm is still on devlopment. So it may not work  sometimes.
	  Install python if you haven't installed it. https://www.python.org/
	  Selenium can be found in http://www.seleniumhq.org/ or install it through Python Package Index (pip)
	  > pip install selenium
	  fbchat can be found in https://github.com/carpedm20/fbchat or install it through Python Package Index (pip)
	  > pip install fbchat
"""
import os
import random
import sys
import time
import unicodedata
import argparse
import getpass
import csv

try :
	from fbchat import Client
	from fbchat.models import *
	from selenium import webdriver
	from selenium.common.exceptions import TimeoutException
	from selenium.webdriver.common.by import By
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.support import expected_conditions
	from selenium.webdriver.support.ui import WebDriverWait
except ImportError :
	print("Can't import required modules.Please install them first")
	sys.exit()

class EmailImporter:

	"""
	This class helps to get names of our facebook friends in a few seconds.
	And this also generate a CSV file containing the names
	"""
	def __init__(self,Email,Password):
		"""
		:param email: Facebook `email`, `id` or `phone number`
		:param password: Facebook account password
		"""
		client = Client(email=Email,password=Password,user_agent=None, max_tries=10, session_cookies=None)
		file = open("/usr/bin/email.csv","w")
	def Generate_CSV(self):
		users = client.fetchAllUsers()		# Fetches a list of all users you're currently chatting with, as `user` objects
		for user in users:
			file.write(user.name)		# storing friends' name into CSV file
			file.write(",\n")
	file.close()
	client.logout()

class EmailLoader:

	"""It presumes the CSV has a filename of emails.csv and is located in the same directory. 
	It loads email addresses into the emails array property.
	"""
	filename = 'emails.csv'
	emails = []

  	def __init__(self):
    	dir_path = os.path.realpath("/usr/bin")
    	file_path = dir_path + '/' + self.filename
    	if not os.path.isfile(file_path):
      		sys.exit('File does not exist: ' + self.filename)

    with open(file_path, 'rb') as file:
    	csv_reader = csv.reader(file)
    	for email in csv_reader:
    		self.emails.append(email[0])

    if len(self.emails) < 1:
    	sys.exit('There are no emails in your supplied file')
    else:
    	print('Loaded ' + str(len(self.emails)))

class Browser:
	delay = 3

	def __init__(self):
	    dir_path = os.path.realpath("usr/bin")
	    driver_path = dir_path + '/geckodriver'
	    self.browser = webdriver.Firefox(executable_path=driver_path)
	    """
	    I'm using Firefox Web Browser and geckodriver as selenium web driver.
	    I suggest you to use PhantomJS web browser with PhantomJS driver.
	    PhantomJS can be found in http://phantomjs.org/download.html
	    """

	def navigate(self, url, wait_for, error):
		"""
		:param url: the page to navigate to
		:param wait_for: div ID that can be found on the navigating page, this is used to ensure it has successfully loaded
		:param error:  an error message that is shown if the navigation is unsuccessful.This will only be shown if the try/catch block fails, 
						in which case it will exit the CLI and print the error message
		"""
	    try:
	      print('Navigating to: ' + url)
	      self.browser.get(url)
	      element_present = expected_conditions.presence_of_element_located((By.ID, wait_for))
	      WebDriverWait(self.browser, self.delay).until(element_present)
	    except TimeoutException:
	      sys.exit(error)

	def enter_login_details(self, email, password):
		"""
		:param email: Facebook `email`, `id` or `phone number`
		:param password: Facebook account password
		"""
	    try:
	      print('Entering login details')
	      email_field = self.browser.find_element_by_id('email')
	      pass_field = self.browser.find_element_by_id('pass')
	      email_field.send_keys(email)
	      pass_field.send_keys(password)
	      pass_field.submit()
	      element_present = expected_conditions.presence_of_element_located((By.ID, 'userNavigationLabel'))
	      WebDriverWait(self.browser, self.delay).until(element_present)
	    except TimeoutException:
	      sys.exit('Login with your credentials unsuccessful')

	def import_members(self, emails):
	    print('Attempting to import email addresses')
	    xpath = "//input[@placeholder='Enter name or email address...']"
	    """
	    This uses XPath which is a query language for working with HTML documents. 
	    We search for the add members input by looking up the placeholder. 
	    We then loop through the array of email addresses to invite, entering each email address character by character. 
	    This prevents the browser from locking up on the input. 
	    After each email address submission the script waits for at least one second before continuing. 
	    Add usage of import_members() and our automation script is complete.
	    """
	    add_members_field = self.browser.find_element_by_xpath(xpath)
	    for email in emails:
	      for c in email:
	        add_members_field.send_keys(self._get_base_character(c))
	      add_members_field.send_keys(Keys.RETURN)
	      time.sleep(random.randint(1,self.delay))

	@staticmethod
	def _get_base_character(c):
	    desc = unicodedata.name(unicode(c))
	    cutoff = desc.find(' WITH ')
	    if cutoff != -1:
	        desc = desc[:cutoff]
	    return unicodedata.lookup(desc)

def main():
	parser = argparse.ArgumentParser(description='This tool lets you invite people in bulk to your Facebook group')
	parser.add_argument('-e','--email', help='Your personal Facebook account email', required=True)
	parser.add_argument('-g','--group', help='The Facebook group name', required=True)
	args = vars(parser.parse_args())
	args['password'] = getpass.getpass()

	email_operation =  EmailImporter(args['email'],args['password'])
	email_operation.Generate_CSV()
	email_loader = EmailLoader()
	browser = Browser()
	browser.navigate(url='https://www.facebook.com',wait_for='facebook',error='Unable to load the Facebook website')
	browser.enter_login_details(args['email'], args['password'])
	browser.navigate(url='https://www.facebook.com/groups/' + args['group'],wait_for='pagelet_group_',error='Couldn\'t navigate to the group\'s members page')
	browser.import_members(email_loader.emails)
    print('Import complete')

if __name__ == '__main__':
  main()
