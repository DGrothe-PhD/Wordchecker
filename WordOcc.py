#!/usr/bin/python 3
# -*- coding: utf-8 -*-
''' Main script '''
import sys
from fileutils import FileMenu
from WordToolBox import TextToolBox

# Multiline comments in source files are 'counted as code' in programmer mode

def main():
	onset=True
	if len(sys.argv)>1:
		if sys.argv[1] == "--help" or sys.argv[1] == "/?":
			omode = "help"
			onset = False
		elif sys.argv[1] == "--prog" or sys.argv[1] == "/p":
			omode = "programmer"
		elif sys.argv[1] == "--refs" or sys.argv[1] == "/r":
			print("not ready yet") #open issue
			onset = False #open issue
			omode = "refsigns"
		elif sys.argv[1] == "--search" or sys.argv[1] == "/s":
			omode = "search"
		else:
			print(f"Unknown argument {sys.argv[1]}.")
			onset = False
			omode = "help"
	else:
		#default option used without any command-line argument
		omode = "textual"
	if onset:
		dafr = FileMenu()
		if dafr.FileManager():
			ttb = TextToolBox(dafr.GetInputFilesList(), dafr.GetOutputFile())
			ttb.WordStatistics(omode)
	else:
		ttb = TextToolBox("", "")
		ttb.WordStatistics(omode)
if __name__=="__main__":
	main();