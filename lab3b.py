#!/usr/local/cs/bin/python3
# NAME: Zicong Mo, Benjamin Yang
# ID: 804654167, 904771533
# EMAIL: josephmo1594@ucla.edu, byang77@ucla.edu

from math import ceil
import sys
import os.path

def main():
	if len(sys.argv) != 2:
		print("Error: Bad arguments", file=sys.stderr)
		sys.exit(1)
	if os.path.isfile(sys.argv[1]):
		with open(sys.argv[1], 'r') as f:
			lines = f.read().splitlines()
	else:
		print("Error: File could not be opened", file=sys.stderr)
		sys.exit(1)

	# These contain strings, not numbers, which is probably a bad design choice
	superblock = ""
	group = ""
	inodes = []
	dirs = []
	free_blocks = []
	free_inodes = []
	indirect = []
	for l in lines:
		if l[:10] == 'SUPERBLOCK':
			superblock = l.split(',')
		if l[:5] == 'GROUP':
			group = l.split(',')
		if l[:5] == 'INODE':
			inodes.append(l.split(','))
		if l[:6] == 'DIRENT':
			dirs.append(l.split(','))
		if l[:5] == 'BFREE':
			free_blocks.append(int((l.split(',')[1])))
		if l[:5] == 'IFREE':
			free_inodes.append(int((l.split(',')[1])))
		if l[:8] == 'INDIRECT':
			indirect.append(l.split(','))

	# Total number of blocks
	max_block = int(superblock[1])
	# Inodetable + ceiling(Number of inodes * inode_size / block_size)
	first_available = int(group[8]) + ceil((int(superblock[2]) * int(superblock[4]))/int(superblock[3]))
	# Dictionary associating each block number with list if inodes using it
	# The list contains the index into the inodes array to access the inode
	block = {}
	inode_dict = {}

	# Scan inode blocks
	# There's definitely a better way to do this
	for i in range(len(inodes)):
		inode = inodes[i]
		inode_num = int(inode[1])
		for direct in range(12, 24):
			block_num = int(inode[direct])
			if block_num < 0 or block_num > max_block:
				print("INVALID BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 0")
			elif block_num > 0 and block_num < first_available:
				print("RESERVED BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 0")
			elif block_num >= first_available:
				if block_num in block:
					block[block_num].append(i)
				else:
					block[block_num] = [i]

		block_num = int(inode[24])
		if block_num < 0 or block_num > max_block:
			print("INVALID INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 12")
		elif block_num > 0 and block_num < first_available:
			print("RESERVED INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 12")
		elif block_num >= first_available:
			if block_num in block:
				block[block_num].append(i)
			else:
				block[block_num] = [i]

		block_num = int(inode[25])
		if block_num < 0 or block_num > max_block:
			print("INVALID DOUBLE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 268")
		elif block_num > 0 and block_num < first_available:
			print("RESERVED DOUBLE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 268")
		elif block_num >= first_available:
			if block_num in block:
				block[block_num].append(i)
			else:
				block[block_num] = [i]

		block_num = int(inode[26])
		if block_num < 0 or block_num > max_block:
			print("INVALID TRIPLE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 65804")
		elif block_num > 0 and block_num < first_available:
			print("RESERVED TRIPLE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 65804")			
		elif block_num >= first_available:
			if block_num in block:
				block[block_num].append(i)
			else:
				block[block_num] = [i]

		if inode_num in inode_dict:
			inode_dict[inode_num].append(i)
		else:
			inode_dict[inode_num] = [i]

	# Scan indirect blocks
	# This isn't checked in the sanity check, so I hope it works
	for i in range(len(indirect)):
		ind = indirect[i]
		inode_num = int(ind[1])
		level = int(ind[2])		
		offset = int(ind[3])
		block_num = int(ind[5])
		# Not completely sure if this is correct
		if block_num < 0 or block_num > max_block:
			if level == 1:
				print("INVALID BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET", offset)
			if level == 2:
				print("INVALID INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET", offset)
			if level == 3:
				print("INVALID DOUBLE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET", offset)
		elif block_num < first_available:
			if level == 1:
				print("RESERVED BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET", offset)
			if level == 2:
				print("RESERVED INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET", offset)
			if level == 3:
				print("RESERVED DOUBLE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET", offset)			
		elif block_num >= first_available:
			if block_num in block:
				block[block_num].append(i)
			else:
				block[block_num] = [i]

	keys = list(block.keys())
	for b in range(first_available, max_block):
		if b not in keys and b not in free_blocks:
			print("UNREFERENCED BLOCK", b)
		if b in keys and b in free_blocks:
			print("ALLOCATED BLOCK", b, "ON FREELIST")
	for b in keys:
		# At least two inodes use the same block
		if len(block[b]) > 1:
			# Scan through block pointers of each inode
			for inode_index in block[b]:
				inode = inodes[inode_index]
				inode_num = int(inode[1])
				found = False
				for direct in range(12, 24):
					block_num = int(inode[direct])
					if block_num == b:
						print("DUPLICATE BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 0")
						found = True
						break
				block_num = int(inode[24])
				if block_num == b:
					print("DUPLICATE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 12")
					found = True

				block_num = int(inode[25])
				if block_num == b:
					print("DUPLICATE DOUBLE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 268")
					found = True

				block_num = int(inode[26])
				if block_num == b:
					print("DUPLICATE TRIPLE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET 65804")
					found = True

				# If it wasn't in inode entry, have to scan indirect entries for the block number
				# This isn't checked in sanity check either
				if not found:
					for i in range(len(indirect)):
						ind = indirect[i]
						inode_num = int(ind[1])
						level = int(ind[2])		
						offset = int(ind[3])
						block_num = int(ind[5])
						if block_num == b:
							if level == 1:
								print("DUPLICATE BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET", offset)
							if level == 2:
								print("DUPLICATE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET", offset)
							if level == 3:
								print("DUPLICATE DOUBLE INDIRECT BLOCK", block_num, "IN INODE", inode_num, "AT OFFSET", offset)

	keys = list(inode_dict.keys())
	
	# All reserved i-nodes
	for i in range(0, int(superblock[7])):
		if i in keys and i in free_inodes:
			print("ALLOCATED INODE", i, "ON FREELIST")
	
	# From first unreserved i-node to highest i-node in group
	for i in range(int(superblock[7]), int(group[3]) + 1):
		if i not in keys and i not in free_inodes:
			print("UNALLOCATED INODE", i, "NOT ON FREELIST")
		elif i in keys and i in free_inodes:
			print("ALLOCATED INODE", i, "ON FREELIST")
	
	# Do all DIRENT related checks
	ref_count = {}
	parent_child = {}
	# Hard-code first DIRENT as 2, may have to change this
	parent_child["2"] = "2"
	for i in range(len(dirs)):
		dir = dirs[i]
		inodenum = int(dir[3])
		#print(inodenum)
		if inodenum < 1 or inodenum > int(group[3]):
			print("DIRECTORY INODE", dir[1], "NAME", dir[6], "INVALID INODE", inodenum)
		elif inodenum not in keys:
			print("DIRECTORY INODE", dir[1],"NAME", dir[6],"UNALLOCATED INODE", inodenum)
		else:
			# Keep track of parents for valid inodes
			if dir[6] == "'.'":
				# Check if pointing to self
				if dir[1] != dir[3]:
					print("DIRECTORY INODE",dir[1],"NAME '.' LINK TO INODE", dir[3],"SHOULD BE",dir[1])
			elif dir[6] != "'..'":
				parent_child[dir[3]] = dir[1]
		# Increment reference count as needed
		if inodenum in ref_count:
			ref_count[inodenum] += 1
		else:
			ref_count[inodenum] = 1
	
	# Check if pointing to correct parent
	for i in range(len(dirs)):
		dir = dirs[i]
		if dir[6] == "'..'":
			if dir[3] != parent_child.get(dir[1]):
				print("DIRECTORY INODE",dir[1],"NAME '..' LINK TO INODE", dir[3],"SHOULD BE",parent_child.get(dir[1]))
    
	# Check if for each i-node links matches enumerated linkcount
	for i in range(len(inodes)):
		inode = inodes[i]
		linkcount = int(inode[6])
		inodenum = int(inode[1])
		if not inodenum in ref_count:
			print("INODE", inodenum, "HAS", 0, "LINKS BUT LINKCOUNT IS", linkcount)
		else:
			links = ref_count[inodenum]
			if links != linkcount:
				print("INODE", inodenum, "HAS", links, "LINKS BUT LINKCOUNT IS", linkcount)

if __name__ == '__main__':
	main()
