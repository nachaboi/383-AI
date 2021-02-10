# COMPSCI 365
# Spring 2020
# YOUR NAME HERE
# Assignment 5: FAT16 Parsing

# Complete the relevant functions.
# Make sure to test your implementations.
# You can import any standard library.
# You can define any new function you want.

import struct

def readSectors(sample, startSec, endSec):
	return open(sample, "rb").read()[512*startSec:512*endSec]

def boot_sector_info(inputFile):
	"""
	Description: Read the given input file (assuming it is an image of a
	FAT16 filesystem), and extract the following information from the FAT16 boot sector
	(you can assume that ALL of these exist):

	- OEM Name (string)
	- Boot Sector Signature (bytes object)
	- Logical Sector Size in bytes (integer)
	- Sectors per Cluster (integer)
	- Cluster Size in bytes (integer)
	- Number of Reserved Sectors (integer)
	- Number of FATs (integer)
	- Maximum Number of Root Directories (integer)
	- Total Logical Sectors (integer) - careful offset 0x13 vs 0x20
	- Sectors per FAT (integer)
	- Volume ID (bytes object)
	- Volume Label (string)
	- FS Type Label (string)

	The input file will be given as a string filename, so you must
	open it and read it. Return the above information with the above
	given types in the following ordered list format:

	[ oem name string, boot sector signature bytes, logical sector size integer, ..., fs type label string ]

	EX:

	boot_sector_info("samples/fat16fs.img") = ["mkfs.fat", b'\x55\xaa', 512, 4, 2048,
	1, 2, 64, 24576, 24, b'\x1f\x37\x31\x74', "CS365      ", "FAT16   "]

	"""
	data = None
	with open(inputFile, "rb") as o:
		data = o.read()

	toReturn = []

	oemName = str(data[3:11])[2:10]
	toReturn.append(oemName)

	bootSectorSignature = data[510:512]
	toReturn.append(bootSectorSignature)

	logicalSectorSize = struct.unpack("<H", data[11:13])[0]
	toReturn.append(logicalSectorSize)

	sectorsPerCluster = data[13]
	toReturn.append(sectorsPerCluster)

	clusterSize = logicalSectorSize * sectorsPerCluster
	toReturn.append(clusterSize)

	numReservedSectors = struct.unpack("<H", data[14:16])[0]
	toReturn.append(numReservedSectors)

	numFATs = data[16]
	toReturn.append(numFATs)

	maxRootDirectories = struct.unpack("<H", data[17:19])[0]
	toReturn.append(maxRootDirectories)

	totalLogicalSectors = struct.unpack("<H", data[19:21])[0]
	if totalLogicalSectors == 0:
		totalLogicalSectors = struct.unpack("<I", data[32:36])[0]
	toReturn.append(totalLogicalSectors)

	totalSectorsPerFAT = struct.unpack("<H", data[22:24])[0]
	toReturn.append(totalSectorsPerFAT)

	volumeID = struct.pack('<I', *struct.unpack('>I', data[39:43]))
	toReturn.append(volumeID)

	volumeLabel = str(data[43:54])[2:13]
	toReturn.append(volumeLabel)

	fsTypeLabel = str(data[54:62])[2:10]
	toReturn.append(fsTypeLabel)

	return toReturn
	
def goThrough(fatTableBytes, num):
	# theLength = len(fatTableBytes) - 4
	# for i in range(0, theLength):
	index = num*2
	return struct.unpack("<H", fatTableBytes[index:index+2])[0]


def read_chain(fatTableBytes, startCluster):
	"""
	Description: Given the input FAT table bytes object, and a starting cluster integer
	(indexed from 0), read the chain of FAT table entries until a EOF marker is encountered.
	Then, return the chain of cluster numbers as an ordered list of integers.

	Remember, the chain may not be in order (ex. [20, 42, 13, 49]).

	EX:

	read_chain(readSectors("samples/fat16fs_subdir.img", 1, 25), 18) = [18, 19, 20]
	read_chain(readSectors("samples/fat16fs_subdir.img", 1, 25), 27) = [27]
	read_chain(readSectors("samples/fat16fs_subdir.img", 1, 25), 9) = [9]
	read_chain(readSectors("samples/fat16fs_subdir.img", 1, 25), 44) = [44, 45, 46, 47, 48, 49]

	"""
	# cur = startCluster
	# for i in range(0,4):
	# 	temp = (fatTableBytes[cur])
	# 	print(temp)
	# 	cur = temp

	# print(str(fatTableBytes))
	# print(fatTableBytes)
	# curSector = 0
	# i = 0
	# sectorList = 0
	# while i < 300:
	# 	a = (struct.unpack("<H", fatTableBytes[i:i+2])[0])
	# 	# if a >= 65528 or a == 0:
	# 	print("CURRENT SECTOR: " + str(curSector))
	# 	curSector += 1
	# 	print(a)
	# 	i += 2
	sectorList = [startCluster]
	cur = startCluster
	while True:
		nextIndex = goThrough(fatTableBytes,cur)
		if nextIndex > 65519 or nextIndex < 2:
			return sectorList
		else:
			sectorList.append(nextIndex)
		cur = nextIndex

def reverse_bit(num):
	total = 0
	if 128 & num == 128:
		total += 1
	if 64 & num == 64:
		total += 2
	if 32 & num == 32:
		total +=4
	if 16 & num == 16:
		total += 8
	if 8 & num == 8:
		total += 16
	if 4 & num == 4:
		total += 32
	if 2 & num == 2:
		total += 64
	if 1 & num == 1:
		total += 128
	return total


def directory_info(directoryBytes):
	"""
	Description: Read the given bytes object, which contains a sequence of directory entries (32B each),
	and extract the directory entries. You should continue extracting directory entries until
	you encounter an entry that starts with a null byte (0x00) or the end of the bytes object.

	You should only parse the directory entry IF all of the following apply:
	(1) The directory entry type is marked as a subdirectory or archive (don't handle LFNs),
	(2) the entry doesn't start with 0xe5 (previously deleted entry),
	(3) the entry doesn't start with 0x7e ("dot" entry).

	Return the following information on each directory in an ordered list of tuples (list order
	is the linear ordering in the "directory entry table"), where each directory is one tuple containing:

	- Short File Name (string)
	- Short File Extension (string)
	- File Attributes Byte (integer)
	- Starting Cluster Number (integer)
	- File Size in Bytes (integer)

	EX:

	directory_info(readSectors("samples/fat16fs.img", 49, 53)) = [
	("FILE1   ", "   ", 0x20, 9, 48),
	("FILE2   ", "   ", 0x20, 18, 5660),
	("FILE3   ", "   ", 0x20, 27, 96)
	]

	directory_info(readSectors("samples/fat16fs_subdir.img", 49, 53)) = [
	("FILE1   ", "   ", 0x20, 9, 48),
	("FILE2   ", "   ", 0x20, 18, 5660),
	("FILE3   ", "   ", 0x20, 27, 96),
	("PRIVATE ", "   ", 0x10, 3, 0)
	]

	directory_info(readSectors("samples/fat16fs_subdir.img", 57, 61)) = [
	("PDIR    ", "   ", 0x10, 50, 0),
	("PFILE1  ", "   ", 0x20, 6, 56)
	]

	directory_info(readSectors("samples/fat16fs_subdir.img", 245, 246)) = [
	("PFILE2  ", "   ", 0x20, 44, 10711)
	]

	"""
	toReturn = []
	# print(directoryBytes)
	times = int(len(directoryBytes)/32)
	for i in range(0,times):
		cur = i*32
		if directoryBytes[cur] == 0:
			break
		if 32 & (directoryBytes[cur+11]) != 32:
			if 16 & (directoryBytes[cur+11]) != 16:
				continue
		if directoryBytes[cur] == 229 or directoryBytes[cur] == 126 or directoryBytes[cur] == 46:
			continue
		# print(directoryBytes[cur])
		shortFileName = str(directoryBytes[cur:cur+8])[2:10]
		shortFileExt = str(directoryBytes[cur+8:cur+11])[2:5]
		fileAtrByte = directoryBytes[cur+11]
		startingClusterNum = struct.unpack("<H", directoryBytes[cur+26:cur+28])[0]
		fileSize = struct.unpack("<I", directoryBytes[cur+28:cur+32])[0]
		# print(shortFileName)
		# print(startingClusterNum)
		# print(fileAtrByte)
		# print()
		toReturn.append((shortFileName, shortFileExt, fileAtrByte, startingClusterNum, fileSize))

	return (toReturn)

def fat16_parse(inputFile): # BONUS
	"""
	**BONUS QUESTION: 20 POINTS**
	Description: Read the given input file (where inputFile is given as a string filename),
	and recursively extract all directory entries using the directory_info function
	you previously completed.

	Return the directory entries in a list of lists, where each inner list is an output
	list from the directory_info function on one of the directories stored in the
	FAT16 FS (including the root directory). This list order does not matter (so you can
	do breadth-first or depth-first, whichever you prefer).

	EX:

	fat16_parse("samples/fat16fs_subdir.img") = [
		[("FILE1   ", "   ", 0x20, 9, 48), ("FILE2   ", "   ", 0x20, 18, 5660), ("FILE3   ", "   ", 0x20, 27, 96), ("PRIVATE ", "   ", 0x10, 3, 0)],
		[("PDIR    ", "   ", 0x10, 50, 0), ("PFILE1  ", "   ", 0x20, 6, 56)],
		[("PFILE2  ", "   ", 0x20, 44, 10711)]
	]
	"""
	toReturn = []
	theInfo = boot_sector_info(inputFile)
	startSec = theInfo[5] + (theInfo[6]*theInfo[9])
	endSec = int(((theInfo[7]*32)/theInfo[2]) + startSec)
	# print(startSec)
	# print(endSec)
	data = readSectors(inputFile,startSec,endSec)
	data = directory_info(data)
	# print(data)
	toReturn.append(data)
	subs = []
	for i in data:
		if i[4] == 0 and (16 & i[2] == 16):
			subs.append(i[3])
	while len(subs) != 0:
		loc = subs[0]
		# locBeg = loc * theInfo[3] + startSec
		locBeg = (theInfo[3] * (loc - 1)) + startSec

		locEnd = int(((theInfo[7]*32)/theInfo[2]) + locBeg) 
		# print(locBeg)
		# print(locEnd)
		data = readSectors(inputFile,locBeg,locEnd)
		# print(data)
		data = directory_info(data)
		# print(data)
		toReturn.append(data)
		for i in data:
			if i[4] == 0 and (16 & i[2] == 16):
				subs.append(i[3])
		subs.remove(loc)
	return toReturn





def fragmented_score(inputFile, cost=5): # BONUS
	"""
	**BONUS QUESTION: 15 POINTS**
	Description: Read the given input file (where inputFile is given as a string filename),
	and parse the FAT table to obtain all of the cluster chains. For each cluster chain, do
	the following for each two sequence pairs of clusters A and B:

	(1) Get the number of clusters distance between A and B and subtract by 1 (ex. [49, 50] = 0),
	(2) Add that value to a running sum of cluster distances.

	Then, multiply the running sum by the cost value, and divide by the total size
	of the filesystem in bytes (i.e. = sector size * number of sectors; both from boot sector).
	Return that final value as the fragmented score.

	Remember to be careful with distances - something like [50, 20, 32] is possible.

	EX:

	fragmented_score("samples/fat16fs.img") = 0
	fragmented_score("samples/fat16fs_frag1.img") = (3 * 5) / (24576 * 512)
	fragmented_score("samples/fat16fs_frag2.img", 85) = (12826 * 85) / (24576 * 512)
	"""
	theInfo = boot_sector_info(inputFile)
	startSec = theInfo[5]
	endSec = (theInfo[6]*theInfo[9]) + startSec
	data = readSectors(inputFile, startSec, endSec)
	notable = []
	for i in fat16_parse(inputFile):
		for j in i:
			notable.append(read_chain(data, j[3]))
	print(notable)

	# data = readSectors(inputFile, startSec, endSec)
	# prelim = []
	# for i in range(0, 65536): #need cluster id's
	# 	try:
	# 		cur = read_chain(data, i)
	# 		if len(cur) > 1:
	# 			prelim.append(cur)
	# 	except:
	# 		break
	# totalDist = 0
	# print(prelim)
	# for i in notable:
	# 	for j in range(0,len(i)-1):
	# 		totalDist += abs(i[j]-i[j+1]) - 1
	# return totalDist



# print(boot_sector_info("samples/fat16fs.img"))
# print(read_chain(readSectors("samples/fat16fs_subdir.img", 1, 25), 44))

# print(directory_info(readSectors("samples/fat16fs.img", 49, 53)))
# print(directory_info(readSectors("samples/fat16fs_subdir.img", 49, 53)))
# print(directory_info(readSectors("samples/fat16fs_subdir.img", 57, 61)))
# print(directory_info(readSectors("samples/fat16fs_subdir.img", 245, 246)))

# print(fat16_parse("samples/fat16fs_subdir.img"))
# print(directory_info(readSectors("samples/fat16fs_subdir.img", 57, 61)))
# print(fragmented_score("samples/fat16fs_frag1.img"))

# print(fragmented_score("samples/fat16fs.img", 85))
# print(readSectors("samples/fat16fs_subdir.img", 57, 61)) #sector 1
# for i in range(1,50):
# 	print(i)
# 	print(directory_info(readSectors("samples/fat16fs_subdir.img", 57+(4*i), 61+(4*i))))









