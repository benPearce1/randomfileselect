class RandomDirectorySource:
	def __init__(self):
		self.SourcePath = ''
		self.DestinationPath = ''
		self.SelectionCount = 0

class Configuration:
	def __init__(self):
		self.hideoriginalnames = True
		self.filter = list()
		self.copyfiles = True

import os
import shutil
import getopt
import sys
import datetime
from random import choice, shuffle, randint

# read configuration file
configfile = 'randomshow.cfg'
opts, args = getopt.getopt(sys.argv[1:], 'i:', ['input='])

for opt, arg in opts:
	if opt in ('-i','--input'):
		configfile = arg

print ('{1} Using configuration file: {0}'.format(configfile,datetime.datetime.now()))		
with open(configfile) as f:
	config = f.readlines()

sources = list()
destinationCounter = dict()
files = list()
configuration = Configuration()

for c in config:
	c = c.strip()
	if c.startswith('source'):
		parts = c[c.index('=') + 1:].split(',')
		randomDir = RandomDirectorySource()
		randomDir.SourcePath = parts[0]
		randomDir.DestinationPath = parts[1]
		randomDir.SelectionCount = int(parts[2])
		sources.append(randomDir)
	if c.startswith('hideoriginalnames'):
		value = c[c.index('=') + 1:].strip()
		configuration.hideoriginalnames = value.upper() == 'TRUE'
		print('hideoriginalnames = {0}'.format(configuration.hideoriginalnames))
	if c.startswith('filter'):
		value = c[c.index('=') + 1:]
		configuration.filter = value.split('|')
	if c.startswith('copyfiles'):
		value = c[c.index('=') + 1:].strip()
		configuration.copyfiles = value.upper() == 'TRUE'
		print('copyfiles = {0}'.format(configuration.copyfiles))
	
for s in sources:
	files = list()
	if s.DestinationPath in destinationCounter:
		destinationCounter[s.DestinationPath] += 1
	else:
		destinationCounter[s.DestinationPath] = 1
		for f in os.listdir(s.DestinationPath):
			os.remove(os.path.join(s.DestinationPath,f))
		
	for dirname, dirnames, filenames in os.walk(s.SourcePath):
		for filename in filenames:
			for type in configuration.filter:
				if filename.endswith(type):
					files.append(os.path.join(dirname, filename))

		# Advanced usage:
		# editing the 'dirnames' list will stop os.walk() from recursing into there.
		if '.git' in dirnames:
			# don't go into any .git directories.
			dirnames.remove('.git')
	
	shuffle(files)

	# make it more random, shuffle it again
	shuffle(files)
	
	# create destination files
	for i in range(0,s.SelectionCount):
		if len(files) > 0:
			file = files.pop()
			if configuration.copyfiles:
				print ("{0} Copying {1} to {2}".format(datetime.datetime.now(), file, s.DestinationPath))
				shutil.copy2(file, s.DestinationPath)
			else:
				print ("{0} Touching {1} in {2}".format(datetime.datetime.now(),filename,s.DestinationPath))
				open(os.path.join(s.DestinationPath,file),'w').close()

# rename files if required
if configuration.hideoriginalnames:
	for d in destinationCounter:
		baseName = os.path.basename(os.path.normpath(d))
		for root,dirnames,filenames in os.walk(d):
			counter = 1
			for i in range(0,randint(1,100)):
				shuffle(filenames)
			for file in filenames:
				filename,extension = os.path.splitext(file)
				newFile = os.path.join(d,"{0} {1}{2}".format(baseName,counter,extension))
				os.rename(os.path.join(d,file), newFile)
				counter += 1

print("{0} Done!".format(datetime.datetime.now()))
