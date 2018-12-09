""" 
		Version : Experimental
"""
try:
	from fbchat import Client
	from fbchat.models import *
except ImportError :
	import sys
	print("Can not import required modules.Try installing \' fbchat \' modules and try again\n")
	print("\nRead the documentation")
	sys.exit()	# terminating script
from getpass import getpass
import time

ASCIIBomb = """\             . . .                         
		              \|/                          
		            `--+--'                        
		              /|\                          
		             ' | '                         
		               |                           
		               |                           
		           ,--'#`--.                       
		           |#######|                       
		        _.-'#######`-._                    
		     ,-'###############`-.                 
		   ,'#####################`,               
		  /#########################\              
		 |###########################|             
		|#############################|            
		|#############################|            
		|#############################|            
		|#############################|            
		 |###########################|             
		  \#########################/              
		   `.#####################,'               
		     `._###############_,'                 
		        `--..#####..--'
"""
print ASCIIBomb		# just to give a cool look to terminal

class Help():
	def __init__(self):
		print("Script Help ")
	def BombingModeHelp(self):
		print("\nMode_1() will sent message to every user of client's friend list")
		print("\nMode_2() will send message to a certain victim")
		print("\nMode_3() will send message to a certain page")

username = input('\nPlease enter your username or email or mobile number :')
password = getpass.getpass()
client = Client('username','password')		#logging in

if client.isLoggedIn() is True:
	class FbBomber():
		
		def __init__(self):
			self.users = client.fetchAllUsers()	# All friends have fetched
			UserData = open("UserData.dat","w")	# UserData will preserve every user data
			for user in self.users:
				UserData.write("Name : ",user.name,"ID : ",user.uid)
			UserData.close()	# closing the file
		
		def Mode_1(self):
		# Mode_1() will sent message to every user of client's friend list
			for user in self.users:
				client.send(Message(text='Hi victim!'), thread_id=user.uid, thread_type=ThreadType.USER)
		
		def Mode_2(self,NameOfUser=client.name,MessageCount=1):
		# Mode_2() will send message to a certain friend
		# : param NameOfUser : type str :name of the user to send message.default is client
		# : param MessageCount : type int : how many message to send.defalut is 1
		user = searchForUser('NameOfUser')[0]	
		# `searchForUsers` searches for the user and gives us a list of the results,and then we just take the first one, aka. the most likely one:
		print("Fetched the following Info...\n")
		print('user ID: {}'.format(user.uid))
		print("user's name: {}".format(user.name))
		print("user's photo: {}".format(user.photo))
		print("Is user client's friend: {}".format(user.is_friend))
		for i in xrange(1,MessageCount):
			client.send(Message(text='Hi victim!'), thread_id=user.uid, thread_type=ThreadType.USER)
			time.sleep(5)	# send message after every 5 seconds just to piss victim off
			client.changeThreadColor(ThreadColor.MESSENGER_BLUE, thread_id=user.uid,thread_type=ThreadType.USER)
		
		def Mode_3(self,PageName,MessageCount=1):
			# Mode_3() will send message to a certain page
			# : param PageName : type str :name of the Page to send message
			# : param MessageCount : type int : how many message to send. Default is 1
			Page = client.searchForPages(PageName,limit=1)[0]	
			for i in xrange(1,MessageCount):
				client.send(Message(text='Hi victim!'), thread_id=Page.uid, thread_type=ThreadType.PAGE)
				time.sleep(5)
	#----------------#
	# END OF FbBomber class
	#----------------#
	MainActivity = FbBomber()
	print("\n Choose bombing Mode \n")
	print("[1]->Bombing Mode 1\n")
	print("[2]->Bombing Mode 2\n")
	print("[3]->Bombing Mode 3\n")
	ModeChoice = int(input())
	if ModeChoice>=1 and ModeChoice<=3 :
		if ModeChoice == 1:
			MainActivity.Mode_1()
		elif ModeChoice == 2:
			MainActivity.Mode_2()
		elif BombingModeChoice == 3:
			MainActivity.Mode_3()
	elif ModeChoice <1 or BombingModeChoice >3 :
		print("Choice Error!")