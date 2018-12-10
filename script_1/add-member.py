"""
Written by : Mirazus Salehin
Version : 1.0 
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
from Tkinter import *

def main():
    
	root = Tk()
	root.title("Auto Add Member")
	root.geometry("600x480")
	root.configure(background="white")
	
	Tops = Frame(root, width = 160, relief = SUNKEN) 
	Tops.pack(side = TOP) 
	Frame1 = Frame(root,width = 160,relief = SUNKEN)
	Frame1.configure(background="#3C5C99")
	Frame1.pack()
	Frame2 = Frame(root,width = 160,relief = SUNKEN)
	Frame2.pack()
	LabelFrame1 = LabelFrame(root,text="LOG",bg="white")
	LabelFrame1.pack(fill="both",expand="yes")
	tField = Text(LabelFrame1)
	tField.pack()
	Info = Label(Tops, font = ('helvetica', 40, 'bold'),text = "Facebook Auto Group \n Member Add",fg = "#3C5C99",bg="white", bd = 10, anchor='w') 
	Info.grid(row = 0, column = 0) 

	txt = StringVar()
	pswrd = StringVar()
	grp = StringVar()

	def reset():
		txt.set("")
		pswrd.set("")
		grp.set("")
	def MainActivity():
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
			tField.insert(" ERROR : Can't import required modules.Please install them first")

		localtime = time.asctime(time.localtime(time.time()))

		class NameImporter:

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
				tField.insert("Logging into "+str(UserNameEntry.get()))
				if client.isloggedIn() is True :
					tField.insert("\nLogging into "+str(UserNameEntry.get())+" successfull")
				elif client.isloggedIn() is False:
					tField.insert("\nLogging into "+str(UserNameEntry.get())+" unsuccessfull.Please try again.")
				file = open("email.csv","w")
				tField.insert("\nNew file friend-list.csv is created.")
			def Generate_CSV(self):
				tField.insert("Fetching all friends")
				users = client.fetchAllUsers()		# Fetches a list of all users you're currently chatting with, as `user` objects
				for user in users:
					file.write(user.name)		# storing friends' name into CSV file
					file.write(",\n")
			file.close()
			client.logout()

		class NameLoader:

			"""It presumes the CSV has a filename of emails.csv and is located in the same directory. 
			It loads email addresses into the emails array property.
			"""
			filename = 'friend-list.csv'
			friend_names = []

		  	def __init__(self):
		    	dir_path = os.path.realpath("/usr/bin")
		    	file_path = dir_path + '/' + self.filename
		    	if not os.path.isfile(file_path):
		      		tField.insert('ERROR : File does not exist: ' + self.filename +"\n")

		    with open(file_path, 'rb') as file:
		    	csv_reader = csv.reader(file)
		    	for names in csv_reader:
		    		self.friend_names.append(friend_names[0])

		    if len(self.friend_names) < 1:
		    	tField.insert("ERROR : There are no names in your supplied file")
		    else:
		    	tField.insert('Loaded ' + str(len(self.emails))+"\n")

		class Browser:
			delay = 3

			def __init__(self):
			    dir_path = os.path.realpath("usr/bin")
			    driver_path = dir_path + '/geckodriver'
			    tField.insert("Opening Browser....\n")
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
			      tField.insert('Navigating to: ' + url+"\n")
			      self.browser.get(url)
			      element_present = expected_conditions.presence_of_element_located((By.ID, wait_for))
			      WebDriverWait(self.browser, self.delay).until(element_present)
			    except TimeoutException:
			      tField.insert(error)

			def enter_login_details(self, email, password):
				"""
				:param email: Facebook `email`, `id` or `phone number`
				:param password: Facebook account password
				"""
			    try:
			      tField.insert('Entering login details')
			      email_field = self.browser.find_element_by_id('email')
			      pass_field = self.browser.find_element_by_id('pass')
			      email_field.send_keys(email)
			      pass_field.send_keys(password)
			      pass_field.submit()
			      element_present = expected_conditions.presence_of_element_located((By.ID, 'userNavigationLabel'))
			      WebDriverWait(self.browser, self.delay).until(element_present)
			    except TimeoutException:
			      tField.insert("ERROR : Login with your credentials unsuccessful"+"\n")

			def import_members(self, names):
			    tField.insert("Attempting to import names")
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
			    for name in names:
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

			name_operation =  NameImporter(str(UserNameEntry.get()),str(PasswordEntry.get()))
			name_operation.Generate_CSV()
			name_loader = NameLoader()
			browser = Browser()
			browser.navigate(url='https://www.facebook.com',wait_for='facebook',error='Unable to load the Facebook website')
			browser.enter_login_details(str(UserNameEntry.get()),str(PasswordEntry.get()))
			browser.navigate(url='https://www.facebook.com/groups/' + str(GroupNameEntry.get()),wait_for='pagelet_group_',error='Couldn\'t navigate to the group\'s members page')
			browser.import_members(name_loader.friend_names)

	t1 = Label(Frame1,text="Username :    ",bg="#3C5C99",fg="white",font = ('helvetica',16))
	t1.grid(row = 0, column = 0)

	UserNameEntry = Entry(Frame1,bg="white",fg="black",bd=0,exportselection=0,font = ('arial', 16),justify="left",textvariable=txt)
	UserNameEntry.grid(row = 0, column = 1)


	t2 = Label(Frame1,text="Password :     ",bg="#3C5C99",fg="white",font = ('helvetica',16))
	t2.grid(row = 1, column = 0)

	PasswordEntry = Entry(Frame1,bg="white",fg="black",bd=0,exportselection=0,show="*",font = ('arial', 16),justify="left",textvariable=pswrd)
	PasswordEntry.grid(row = 1, column = 1)

	t3 = Label(Frame1,text="Group name :",bg="#3C5C99",fg="white",font = ('helvetica',16))
	t3.grid(row=2,column=0)

	GroupNameEntry = Entry(Frame1,bg="white",fg="black",bd=0,exportselection=0,font = ('arial', 16),justify="left",textvariable=grp)
	GroupNameEntry.grid(row=2,column=1)

	imagetest1 = PhotoImage(file="reset-icon.gif")
	reset_button = Button(Frame2,image=imagetest1,  borderwidth = 0, bg = "white",fg="white", command = reset,relief=RAISED)
	reset_button.grid(row = 0, column = 1) 

	imagetest2 = PhotoImage(file="login-icon.gif")
	login_button = Button(Frame2,image=imagetest2,  borderwidth = 0, bg = "white",fg="white",relief=RAISED,command=MainActivity)
	login_button.grid(row = 0, column = 2)

	imagetest3 = PhotoImage(file="exit-icon.gif")
	exit_button = Button(Frame2,image=imagetest3,  borderwidth = 0, bg = "white",fg="white", command = root.quit,relief=RAISED)
	exit_button.grid(row = 0, column = 3)



    print('Import complete')
    root.mainloop()
if __name__ == '__main__':
  main()
