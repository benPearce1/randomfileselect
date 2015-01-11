import os
import shutil
import getopt
import sys
import datetime
from random import choice, shuffle, randint

# data classes
class RandomDirectorySource:
	def __init__(self):
		self.SourcePath = ''
		self.DestinationPath = ''
		self.SelectionCount = 0

class Configuration:
	def __init__(self):
		self.hideoriginalnames = False
		self.filter = list()
		self.method = 'copy'
		self.verbose = False

# methods
def processConfigFile(configfile):
	with open(configfile) as f:
		config = f.readlines()
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
		if c.startswith('method'):
			value = c[c.index('=') + 1:].strip()
			configuration.method = value.lower()
			print('method = {0}'.format(configuration.method))
		if c.startwith('verbose'):
			value = c[c.index('=') + 1:].strip()
			configuration.verbose = value.upper() == 'TRUE'

def printHelp():
	print ('python {0} [-i filename | -f filter -m method -s path -o path -c count -h -v]'.format(os.path.basename(__file__)))
	print ('\t-i file	: input file name')
	print ('\t-f filter	: file extension filter, comma delimited list')
	print ('\t-m method : operation method (copy, zero, list)')
	print ('\t-h 		: hide original filenames, output will be sequentially numbered files')
	print ('\t-s path 	: source path')
	print ('\t-o path 	: output path')
	print ('\t-c count 	: number of files to pick')
	print ('\t-v 		: verbose output')

def printConfig():
	if configuration.verbose:
		print ('Running config:')
		print ('\tMethod: {0}'.format(configuration.method))
		print ('\tFilter: {0}'.format(configuration.filter))
		print ('\tHide original filenames: {0}'.format(configuration.hideoriginalnames))
		print ('Sources:')
		for s in sources:
			print ('\tSource path: {0}'.format(s.SourcePath))
			print ('\tDestionation path: {0}'.format(s.DestinationPath))
			print ('\tSelection count: {0}'.format(s.SelectionCount))

def validateConfig():
	if configuration.method in ('zero','touch', 'copy'):
		for s in sources:
			if s.DestinationPath == '':
				print ('Destination path missing')
				exit(1)

# -- main --

# read configuration file
opts, args = getopt.getopt(sys.argv[1:], 'i:f:m:ho:s:c:v')

if len(opts) == 0:
	printHelp()

sources = list()
destinationCounter = dict()
files = list()
configuration = Configuration()

for opt, arg in opts:
	if opt in ('-i'):
		configfile = arg
		print ('{1} Using configuration file: {0}'.format(configfile,datetime.datetime.now()))
		processConfigFile(configfile)
	if opt in ('-f'):
		configuration.filter = arg.split(',')
	if opt in ('-h'):
		if len(arg) > 0:
			configuration.hideoriginalnames = arg.upper() == 'TRUE'
		else:
			configuration.hideoriginalnames = True
	if opt in ('-m'):
		configuration.method = arg.lower()
	if opt in ('-s'):
		if len(sources) == 0:
			sources.append(RandomDirectorySource())
		sources[0].SourcePath = arg
	if opt in ('-o'):
		if len(sources) == 0:
			sources.append(RandomDirectorySource())
		sources[0].DestinationPath = arg
	if opt in ('-c'):
		if len(sources) == 0:
			sources.append(RandomDirectorySource())
		sources[0].SelectionCount = int(arg)
	if opt in ('-v'):
		configuration.verbose = True

printConfig()
validateConfig()

for s in sources:
	files = list()
	if s.DestinationPath != '':
		if s.DestinationPath in destinationCounter:
			destinationCounter[s.DestinationPath] += 1
		else:
			destinationCounter[s.DestinationPath] = 1
			for f in os.listdir(s.DestinationPath):
				os.remove(os.path.join(s.DestinationPath,f))

	for dirname, dirnames, filenames in os.walk(s.SourcePath):
		for filename in filenames:
			for type in configuration.filter:
				if filename.upper().endswith('.{0}'.format(type.upper())):
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
	# for f in files:
	# 	print (f)
	for i in range(0,s.SelectionCount):
		if len(files) > 0:
			file = files.pop()
			if configuration.method in ('copy'):
				print ("{0} Copying {1} to {2}".format(datetime.datetime.now(), file, s.DestinationPath))
				shutil.copy2(file, s.DestinationPath)
			elif configuration.method in ('list'):
				print (file)
			elif configuration.method in ('zero','touch'):
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

if configuration.verbose:
	print("{0} Done!".format(datetime.datetime.now()))
