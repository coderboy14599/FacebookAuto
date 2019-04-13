from tkinter import *
import tkinter.ttk
import os
import time
import random
from xml.dom.minidom import parse
import xml.dom.minidom
try:
    from fbchat import Client
    from fbchat.models import *
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    os.system("py -m pip install fbchat")
    os.system("py -m pip install selenium")
    time.sleep(5.0)
    from fbchat import Client
    from fbchat.models import *
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.ui import WebDriverWait


class ApplicationGUI:
    """Main GUI class"""

    def __init__(self, master):
        self.master = master
        self.master = Tk()
        self.master.title("Auto Add Member")
        self.master.geometry("280x480")
        self.master.resizable(0, 0)
        self.CreateFrames()
        self.CreateWidgets()

    def CreateFrames(self):
        self.RootFrame = Frame(self.master, relief=FLAT)
        self.LabelFrame1 = LabelFrame(self.RootFrame, text="Required")
        self.LabelFrame2 = LabelFrame(self.RootFrame, text="Command Palate")
        self.LabelFrame3 = LabelFrame(self.RootFrame, text="Advance Menu")
        self.LabelFrame4 = LabelFrame(self.RootFrame, text="LOG")
        self.Frame1 = Frame(self.LabelFrame1, relief=FLAT)
        self.Frame2 = Frame(self.LabelFrame2, relief=FLAT)
        self.Frame3 = Frame(self.LabelFrame3, relief=FLAT)
        self.RootFrame.pack(side=TOP)
        self.Frame1.grid(row=0, column=0, padx=5)
        self.Frame2.grid(row=0, column=0, padx=5)
        self.Frame3.grid(row=0, column=0, padx=5)
        self.LabelFrame1.grid(row=0, column=0, pady=5)
        self.LabelFrame2.grid(row=1, column=0)
        self.LabelFrame3.grid(row=2, column=0, pady=5)
        self.LabelFrame4.grid(row=3, column=0)

    def CreateWidgets(self):
        username_ = StringVar()
        password_ = StringVar()
        group_name = StringVar()

        def reset():
            username_.set("")
            password_.set("")
            group_name.set("")
        self.t1 = Label(self.Frame1, text="Username :", fg="black", ).grid(row=0, column=0)
        self.t2 = Label(self.Frame1, text="Password :", fg="black").grid(row=1, column=0)
        self.t3 = Label(self.Frame1, text="Group Name :", fg="black").grid(row=2, column=0)
        self.t4 = Label(self.Frame3, text="Login Attempt :", fg="black").grid(row=0, column=0)
        self.t5 = Label(self.Frame3, text="Time Interval :", fg="black").grid(row=1, column=0)
        self.UserNameEntry = Entry(self.Frame1, bg="white", fg="black", bd=1, exportselection=0, justify="left", textvariable=username_).grid(row=0, column=1)
        self.PasswordEntry = Entry(self.Frame1, bg="white", fg="black", bd=1, exportselection=0, justify="left", textvariable=password_, show="*").grid(row=1, column=1)
        self.GroupNameEntry = Entry(self.Frame1, bg="white", fg="black", bd=1, exportselection=0, justify="left", textvariable=group_name).grid(row=2, column=1)
        self.Button1 = Button(self.LabelFrame2, text="Reset", borderwidth=3, fg="black", relief=RAISED, justify=CENTER, command=reset(), padx=2, pady=2).grid(row=0, column=0, padx=10, pady=2)
        self.Button2 = Button(self.LabelFrame2, text="Log in", borderwidth=3, fg="black", relief=RAISED, justify=CENTER, padx=2, pady=2).grid(row=0, column=1, padx=10, )
        self.Button3 = Button(self.LabelFrame2, text="Add Member", borderwidth=3, fg="black", relief=RAISED, justify=CENTER, padx=2, pady=2).grid(row=0, column=2, padx=10, )

    def GetValues(self):
        global Username
        global Password
        global GroupName
        Username = self.UserNameEntry.get()
        Password = self.PasswordEntry.get()
        GroupName = self.GroupNameEntry.get()


class MainActivity:

    class NameImporter:
        """
        This class helps to get names of our facebook friends in a few seconds.
        And this also generate a CSV file containing the names
        """
        def __init__(self, email, password):
            """
            :param email: Facebook `email`, `id` or `phone number`
            :param password: Facebook account password
            """
            self.client = Client(email=email, password=password, user_agent=None, max_tries=10, session_cookies=None)
            self.XMLfile = open("C:\\Windows\\NameList.xml", "w")

        def Generate_XML(self):
            users = self.client.fetchAllUsers()  # Fetches a list of all users you're currently chatting with, as `user` objects
            self.XMLfile.write("<FriendList UserName="+Username+"Total="+str(len(users))+">")
            for user in users:
                self.XMLfile.write("<Name>"+user.name+"</Name>\n")  # storing friends' name into CSV file
            self.XMLfile.write("</FriendList>")
            self.XMLfile.close()
            self.client.logout()

    class NameLoader:
        global friends_names
        friends_names = []

        def __init__(self):
            DOMTree = xml.dom.minidom.parse("C:\\Windows\\NameList.xml")
            FriendList = DOMTree.documentElement
            friends = FriendList.getElementsByTagName("FriendList")
            for f in friends:
                Name = friends.getElementsByTagName("Name")[0]
                friends_names.append(Name.childNodes[0].data)

    class Browser:

        def __init__(self):
            dir_path = os.path.realpath("C:\Windows")
            driver_path = dir_path + '\\geckodriver'
            self.browser = webdriver.Firefox(executable_path=driver_path)
            self.delay = 3

        def navigate(self, url, wait_for):
            """
            :param url: the page to navigate to
            :param wait_for: div ID that can be found on the navigating page, this is used to ensure it has successfully loaded
            """
            self.browser.get(url)
            element_present = expected_conditions.presence_of_element_located((By.ID, wait_for))
            WebDriverWait(self.browser, self.delay).until(element_present)

        def enter_login_details(self, email, password):
            """
            :param email: Facebook `email`, `id` or `phone number`
            :param password: Facebook account password
            """
            try:
                email_field = self.browser.find_element_by_id('email')
                pass_field = self.browser.find_element_by_id('pass')
                email_field.send_keys(email)
                pass_field.send_keys(password)
                pass_field.submit()
                element_present = expected_conditions.presence_of_element_located((By.ID, 'userNavigationLabel'))
                WebDriverWait(self.browser, self.delay).until(element_present)
            except TimeoutException:
                print("ERROR : Login with your credentials unsuccessful" + "\n")

        def import_members(self, membernames):
            xpath = "//input[@placeholder='Enter name or email address...']"
            add_members_field = self.browser.find_element_by_xpath(xpath)
            for name in membernames:
                add_members_field.send_keys(name)
                add_members_field.send_keys(Keys.RETURN)
                time.sleep(random.randint(1, self.delay))


app = ApplicationGUI(tkinter.Tk)
app.CreateFrames()
app.CreateWidgets()
app.master.mainloop()

activity = MainActivity()
activity.NameImporter.Generate_XML()
activity.Browser.navigate("https://www.facebook.com","facebook")
activity.Browser.enter_login_details()
activity.Browser.import_members()


