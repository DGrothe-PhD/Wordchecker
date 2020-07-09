#!/usr/bin/python 3
# -*- coding: utf-8 -*-
''' Python 
'''
import re
import glob
import os

class FileMenu:
	"""Interactive console menu for selecting the text files."""
	def __init__(self):
		self.__progtitle = "\n ."+("_"*27)+". \n||      Word Occurrence      ||"+"\n"+("="*31)+"\n\nHello user!\r\n"
		self.__again= True
		self.InputFileList=[]
		self.OutputFilename = "WordStati__Outputfile.txt"
		self.UIStr = "WordStati__Inputfile.txt"
		self.IfFurther = ""
#
	def SetInputFilesList(self):
		""" interactive method that lets a user type in filenames one-by-one or in a comma-separated sequence"""
		while self.__again==True:
			ques = "".join([self.__progtitle , 
				"Which text file(s) do you want to filter?\n",
				"Files should be in the active directory, or (relative) paths,\n",
				"Note: strictly avoid commas and blanks in filenames",
				"Example: file1.txt, file2.txt .\r\n"])
			self.UIStr= input(ques)
			self.IfFurther= input("Further file(s)? (j or y):")
			if self.IfFurther=="j" or self.IfFurther=="y":
				self.__again=True
			else:
				self.__again=False
				print("File input completed.\n")
			zz = re.sub("[|<>]","",self.UIStr)
			self.UIStr = zz
			zi = self.UIStr.split(", ")
			for x in zi:
				self.InputFileList.append(x)
#######
			if os.path.exists(SWF):
				inc = False
			else:
				print(f"File {SWF} does not exist.")


	def SetInputGlobbedFilesList(self):
		inc = True
		while inc:
			ques = "".join([self.__progtitle , 
			 "Write down a path name such as \"./subfolder\" or\r\n",
			 " \"C:\\Users\\XYZ\\Documents\\\".\r\n"])
			pathanswer = input(ques)
			if os.path.exists(pathanswer):
				inc = False
			else:
				print(f"\n Error: Path {pathanswer} does not exist.")
		fileprefix = ""
		ques = "Special prefix or use all *.txt files in that subfolder?\n  (Just press enter if 'all *.txt' is okay)\n"
		fileprefix = input(ques)
		self.InputFileList = glob.glob(os.path.join(pathanswer, fileprefix+"*.txt"))
#
	def SetOutputFile(self):
		tooshort=True
		while tooshort:
			a = input("Where do you want to save the filtered word list?:")
			if len(a)>3:
				tooshort=False
				if not(len(a)>4 and a.endswith(".txt")):
					self.OutputFilename = a +".txt"
				else:
					self.OutputFilename = a
			else:
				print("That filename was too short.")
#
	def GetOutputFile(self):
		return self.OutputFilename

	def GetInputFilesList(self):
		return self.InputFileList
#
	def Explaining(self):
		print("Okay, the filtering of the files:\n")
		for x in self.InputFileList:
			print(" - "+x)
		print("\nwill be saved in " + self.OutputFilename + ".\n")
		yesno= input("Is that okay? (j or y)")
		if yesno == '' or yesno[0] =="j" or yesno[0]=="y":
			stat = True
		else:
			stat = False
		return stat
#
	def FileManager(self,globbing=True):
		if globbing:
			self.SetInputGlobbedFilesList()
		else:
			self.SetInputFilesList()
		self.SetOutputFile()
		stat = self.Explaining()
		return stat