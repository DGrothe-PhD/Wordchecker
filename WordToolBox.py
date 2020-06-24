# -*- coding: utf-8 -*-
''' Python Module "WordToolBox"
'''
import re

class TextToolBox:
	""" Filters word occurrences from texts, alphabetically"""
	def __init__(self, list_of_files, file_out):
		self.list_of_files = list_of_files
		self.file_out = file_out
		self.WordList = []
		self.KWordList = [] # for comments in codes
		self.alphlist = []
		self.kalphlist = []
		self.CountingWords = {}
		self.KCountingWords = {}

# @todo: make these work
	def SetSearchWords(self, wort, *wordseq):
		self.WordList.append(str(wort))
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
	

# ignore some punctuation for counting word occurences
# a point in the 
	def brush(self,y):
		y=y.rstrip(",.;:!?")
		y=y.lstrip("¿¡")
		return y

	def CharSweeper(self,tx):
		"""removes most of punctuation from words"""
		bracket={"(":")", "[":"]", "{":"}", "\"":"\"", "„":"“", "«":"»", "»":"«"}
		y = self.brush(tx)
		#keep pairs of brackets and pairs of quotation marks in the same word
		for u in bracket.keys():
			if (y.find(u)>-1) ^ (y.find(bracket[u])> -1 ):
				y=y.rstrip(bracket[u])
				y=y.lstrip(u)
		y = self.brush(y)
		return y

	def CharSweeperProgStyle(self,tx):
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
		fobj_vb.close()
	
	def WriteSection(self,the_file):
		"""Write section line to file"""
		with open(self.file_out, "a") as fobj_vb:
			bar = "\n"+"="*12+"\n"
			fobj_vb.write("\nFile: "+the_file+bar)
		fobj_vb.close()

	def CleanUp(self):
		"""Reset the buffer variables"""
		self.alphlist = []
		self.kalphlist = []
		self.CountingWords.clear()
		self.KCountingWords.clear()

	def CollectData(self,eing, OnlySearchWords=False):
		"""Read file line by line and register the words in CountingWords dictionnary"""
		with open(eing, "r+") as fobj_in:
			for line in fobj_in:
				zl = line.rstrip()
				wo = zl.split()
				linebuff=[]
				for w in wo:
					linebuff.append(self.CharSweeper(w))
				for w in linebuff:
					if OnlySearchWords:
						self.SearchWordFinder(w, self.CountingWords)
					else:
						self.WordFinder(w, self.CountingWords)
		fobj_in.close()
		return 0

	def CollectDataWithPoint(self,eing):
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
				for wort in woli: # count words in text
					self.WordFinder(wort, self.CountingWords)
				if pycommentfound:
					# filter and split comment
					lz = self.CharSweeperProgStyle(komm.rstrip())
					woli = lz.split()
					for wort in woli:
						self.WordFinder(wort, self.KCountingWords)
		fobj_in.close()

	def SetAlphList(self,dic):
		"""Sort alphabetically"""
		for q in dic.keys():
			self.alphlist.append(q)
		self.alphlist.sort()
		return self.alphlist

	def SetKAlphList(self,dic):
		"""Sort comment words alphabetically"""
		for q in dic.keys():
			self.kalphlist.append(q)
		self.kalphlist.sort()
		return self.kalphlist

	def SaveData(self):
		"""Save data in output file"""
		with open(self.file_out, "a") as fobj_vb:
			for q in self.alphlist:
				for teil in [q]:
					if (q in self.CountingWords):
						fobj_vb.write("\t".join([q, str(self.CountingWords[q])]) +"\n")
					else:
						print(f"Something strange happened: {q} isn't found in CountingWords!")
						break
			if len(self.kalphlist) > 0:
				print("__ Found some comments. __\n")
				fobj_vb.write("\n__ Found comments with following words therein:__\n")
				for q in self.kalphlist:
					for teil in [q]:
						if (q in self.KCountingWords):
							fobj_vb.write("\t".join([q, str(self.KCountingWords[q])]) +"\n")
						else:
							print(f"Something strange happened: {q} isn't found in CountingWords!")
							break
		fobj_vb.close()

	def helping(self):
		dht = "Display helping text.\n"
		print("Usage:\n======\n\n","--help or /? :\n\t ",dht,
		"no args  Word statistics in normal mode.\n",
		"--prog or /p :\n\t"," Word stats on Py scripts to collect \n","\t ","variable and obj.attribute names.\n")

	def Finish(self):
		self.SetAlphList(self.CountingWords)
		self.SaveData()
		self.CleanUp()

	def WordStatistics(self, opmode="textual"):
		opmodelist=["textual", "search", "programmer"]
		if opmode in opmodelist:
			self.Initialize()
			print(f"Word statistics in {opmode} mode.")
		# Parts
		if opmode=="textual":
			for x in self.list_of_files:
				self.WriteSection(x)
				self.CollectData(x)
				print("Finished on " + x)
				self.Finish()
		elif opmode=="search":
			pass
			# @todo search word mode to be implemented
			#this will use SetSearchWords(args)
			#and self.CollectData(x,True)
		elif opmode=="programmer":
			for x in self.list_of_files:
				self.WriteSection(x)
				self.CollectDataWithPoint(x)
				print("Finished on " + x)
				self.SetKAlphList(self.KCountingWords)
				self.Finish()
		elif opmode=="help":
			self.helping()
		else:
			self.helping()