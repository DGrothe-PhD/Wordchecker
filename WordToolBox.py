#!/usr/bin/python 3
# -*- coding: utf-8 -*-

''' Python Module "WordToolBox"
'''
import os
import sys
import re

class TextToolBox:
	""" Filters word occurrences from texts, alphabetically"""
	def __init__(self, list_of_files, file_out):
		self.i=0
		self.list_of_files = list_of_files
		self.file_out = file_out
		self.__thebom='\xef\xbb\xbf'
		self.__brackets = {"(":")", "[":"]", "{":"}", "\"":"\"", "„":"“", "«":"»", "»":"«"}
		self.__lbs = list(self.__brackets.keys())
		self.__rbs = list(self.__brackets.values())
		self.WordList = []
		self.KWordList = [] # for comments in codes
		self.alphlist = []
		self.kalphlist = []
		self.CountingWords = {}
		self.KCountingWords = {}

# @todo: make these work
	def SetSearchWords(self, w, *wordseq):
		self.WordList.append(str(w))
		for q in wordseq:
			self.WordList.append(str(q))

	def SearchWordFinder(self, buff, dic):
		"""just search for the words in the search word list"""
		for q in self.WordList:
			if not (q in dic):
				dic.update({q: 0})
			if buff == q:
				dic[q]+=1
		return dic
	
	#plan: to search for word sequences as 'John Doe' and 'Max Mustermann'
	def SetAskWords(self):
		inc = True
		while inc:
			pathsw = input("Please enter a PATH to a file\n   wherein search words have been entered each in one line (or q for quitting): ")
			if pathsw is "Q" or pathsw is "q":
				sys.exit()
			filename = input("Please enter a filename: ")
			SWF = os.path.join(pathsw, filename)
			if os.path.exists(SWF):
				inc = False
			else:
				print(f"File {SWF} does not exist.")
		with open(SWF, "r+") as SWF_in:
			for line in SWF_in:
				q = line.rstrip()
				if len(q)>0:
					self.SetSearchWords(q)


# ignore some punctuation for counting word occurences
	def brush(self, y):
		y=y.rstrip(",.;:!?")
		y=y.lstrip("¿¡")
		return y
	

	def GBR(self, tx):
		a=[]
		for x in tx[::-1]:
			if x in self.__rbs:
				a.append(x)
			elif x.isalnum():
				break
		return a
	
	def GBL(self,tx):
		a = []
		for x in tx:
			if x in self.__lbs:
				a.append(x)
			elif x.isalnum():
				break
		return a
	
	def CharSweeper(self, tx):
		"""removes most of punctuation from words"""
		#keep pairs of brackets and pairs of quotation marks in the same word
		y=tx
		atright= self.GBR(y)
		atleft = self.GBL(y)
		sl="¿¡"
		sr=",.;:!?"
		for u in atleft:
			pos = [y.find(u), y.rfind(self.__brackets[u])]
			# if exclusively opening or closing brackets
			if max(pos)>-1 and (min(pos)==max(pos) or min(pos)==-1):
				sl+=u
		y = y.lstrip(sl)
		#
		for u in atright:
			nu = self.__lbs[self.__rbs.index(u)]
			pos = [y.find(nu), y.rfind(u)]
			# if exclusively opening or closing brackets
			if max(pos)>-1 and (min(pos)==max(pos) or min(pos)==-1):
				sr+=u
		y=y.rstrip(sr)
		return y

	def CharSweeperProgStyle(self, tx):
		"""remove any punctuation while keeping OOP class-member syntax '.:' in programming code"""
		y=tx
		for u in ",;\"\\/()[]{}!?":
			y=y.replace(u,"")
		return y

	def WordFinder(self, q, dic):
		"""If new word, put in list, else increment its counter"""
		if not (q in dic):
			dic.update({q: 1})
		else:
			dic[q]+=1
		return dic

	def Initialize(self):
		"""Write headline to file"""
		with open(self.file_out, "w") as fobj_vb:
			bar = "\n"+"="*12+"\n"
			fobj_vb.write("Result of word counting:\n"+bar)
		self.i+=1
		fobj_vb.close()
	
	def WriteSection(self, the_file):
		"""Write section line to file"""
		with open(self.file_out, "a") as fobj_vb:
			bar = "\n"+"="*12+"\n"
			fobj_vb.write("\nFile: "+the_file+bar)
			print(f"Reading file {the_file}.")
			self.i+=1
			fobj_vb.close()

	def CleanUp(self):
		"""Reset the buffer variables"""
		self.alphlist = []
		self.kalphlist = []
		self.CountingWords.clear()
		self.KCountingWords.clear()

	def CollectData(self, eing, OnlySearchWords=False):
		"""Read file line by line and register the words in CountingWords dictionnary"""
		with open(eing, "r+") as fobj_in:
			self.n_lins = 0
			self.n_wds = 0
			for line in fobj_in:
				zl = line.rstrip()
				self.n_lins+=1
				# if there's a BOM then ignore it
				if zl.find(self.__thebom)==0:
					zl = zl[3:]
				# ignore empty lines
				if len(zl)==0:
					continue
				# Word occurrence algorithm
				wo = zl.split()
				linebuff=[]
				self.n_wds+=len(wo)
				for w in wo:
					linebuff.append(self.CharSweeper(w))
				for w in linebuff:
					if OnlySearchWords:
						self.SearchWordFinder(w, self.CountingWords)
					else:
						self.WordFinder(w, self.CountingWords)
		self.i+=1
		fobj_in.close()

	def CollectDataWithPoint(self, eing):
		"""For counting words and expressions in programming scripts"""
		with open(eing, "r+") as fobj_in:
			for line in fobj_in:
				pycommentfound = (line.find("#")>=0)
				# @todo finding multiline comments
				if pycommentfound:
					lili = line.split("#")
					line = lili[0]
					# is there a text before the # comment so store it
					del lili[0] # delete text before '#' from the comment
					komm= "".join(lili) # the comment part
				# filter and split text
				lz = self.CharSweeperProgStyle(line.rstrip())
				woli = lz.split()
				for w in woli: # count words in text
					self.WordFinder(w, self.CountingWords)
				if pycommentfound:
					# filter and split comment
					lz = self.CharSweeperProgStyle(komm.rstrip())
					woli = lz.split()
					for w in woli:
						self.WordFinder(w, self.KCountingWords)
		self.i+=1
		fobj_in.close()

	#next issue
	def CollectDataWithRefSigns(self, x):
		pass
		
	def SetAlphList(self, dic):
		"""Sort alphabetically"""
		self.n_keys = len(dic)
		self.n_ens=sum(dic.values())
		for q in dic.keys():
			self.alphlist.append(q)
		self.alphlist.sort()
		return self.alphlist

	def SetKAlphList(self, dic):
		"""Sort comment words alphabetically"""
		for q in dic.keys():
			self.kalphlist.append(q)
		self.kalphlist.sort()
		return self.kalphlist

	def SaveData(self):
		"""Save data in output file"""
		with open(self.file_out, "a") as fobj_vb:
			for q in self.alphlist:
			#	for teil in [q]:
				if (q in self.CountingWords):
					fobj_vb.write(f"{q}\t{self.CountingWords[q]}\n")
				else:
					print(f"Something strange happened: {q} isn't found in CountingWords!")
					break
			if len(self.kalphlist) > 0:
				print("__ Found some comments. __\n")
				fobj_vb.write("\n__ Found comments with following words therein:__\n")
				for q in self.kalphlist:
			#		for teil in [q]:
					if (q in self.KCountingWords):
						fobj_vb.write(f"{q}\t{self.KCountingWords[q]}\n")
					else:
						print(f"Something strange happened: {q} isn't found in CountingWords!")
						break
			fobj_vb.write(f"\nFile: {self.n_lins} lines ==> {self.n_wds} words (estimated), {self.n_ens} findings of {self.n_keys} different words.\n")
		self.i+=1
		fobj_vb.close()

	def helping(self):
		dht = "Display helping text.\n"
		print("Usage:\n======\n\n","--help or /? :\n\t ",dht,
		"no args  Word statistics in normal mode.\n",
		"--prog or /p :\n\t", " Word stats on Py scripts to collect \n","\t ","variable and obj.attribute names.\n",
		"--search or /s :\n\t", "Search for user-defined search terms.\n")

	def Finish(self, x):
		print(f"Finished on {x}")
		self.SetAlphList(self.CountingWords)
		self.SaveData()
		self.CleanUp()
		print(f"Es wurde {self.i} mal Datei geschlossen")

	def WordStatistics(self, opmode="textual"):
		opmodelist = ["textual", "search", "programmer"]#"refsigns", 
		if opmode in opmodelist:
			self.Initialize()
			print(f"Word statistics in {opmode} mode.")
		# Parts
		if opmode == "textual":
			for x in self.list_of_files:
				self.WriteSection(x)
				self.CollectData(x, False)
				self.Finish(x)
		# Search part
		elif opmode == "search":
			self.SetAskWords()
			for x in self.list_of_files:
				self.WriteSection(x)
				self.CollectData(x, True)
				self.Finish(x)
		# Programmer part
		elif opmode == "programmer":
			for x in self.list_of_files:
				self.WriteSection(x)
				self.CollectDataWithPoint(x)
				self.SetKAlphList(self.KCountingWords)
				self.Finish(x)
		# Refsigns part
		elif opmode == "refsigns":
			print("not ready yet")
			'''for x in self.list_of_files:
				self.WriteSection(x)
				self.CollectDataWithRefSigns(x)
				self.Finish()'''
		# Helping part
		elif opmode == "help":
			self.helping()
		else:
			self.helping()