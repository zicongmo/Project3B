# NAME: Zicong Mo, Benjamin Yang
# ID: 804654167, 904771533
# EMAIL: josephmo1594@ucla.edu, byang77@ucla.edu

import sys
import os.path

def main():
	if len(sys.argv) != 2:
		print("Error: Bad arguments", file=sys.stderr)
		return
	if os.path.isfile(sys.argv[1]):
		with open(sys.argv[1], 'r') as f:
			lines = f.read().splitlines()
	else:
		print("Error: File could not be opened", file=sys.stderr)
		return

	superblock = ""
	inodes = []
	dirs = []
	free_blocks = []
	free_inodes = []
	indirect = []
	for l in lines:
		if l[:10] == 'SUPERBLOCK':
			superblock = l.split(',')
		if l[:6] == 'INODE':
			inodes.append(l.split(','))
		if l[:7] == 'DIRENT':
			dirs.append(l.split(','))
		if l[:6] == 'BFREE':
			free_blocks.append(l.split(','))
		if l[:6] == 'IFREE':
			free_inodes.append(l.split(','))
		if l[:9] == 'INDIRECT':
			indirect.append(l.split(','))

	if superblock == "":
		print("Error: Could not find superblock in file", file=sys.stderr)

	# Total number of blocks
	max_block = superblock[1]
	# Block number of first non-reserved inode
	first_available = superblock[7]

	# Scan direct blocks
	for i in range(len(inodes)):
		inode = inodes[i]
		for direct in range(12, 24):
			if inode[direct] < 0 or inode[direct] > max_block:
				print("INVALID BLOCK ", inode[direct], " IN INODE ", i, " AT OFFSET 0")
			elif inode[direct] < first_available:
				print("RESERVED BLOCK ", inode[direct], " IN INODE ", i, " AT OFFSET 0")

	# Scan indirect blocks
	for i in range(len(indirect)):
		ind = indirect[i]
		# Not completely sure if this is correct
		if ind[5] < 0 or ind[5] > max_block:
			if ind[2] == 1:
				print("INVALID INDIRECT BLOCK ", ind[5], " IN INODE ", ind[1], " AT OFFSET ", ind[3])
			if ind[2] == 2:
				print("INVALID DOUBLE INDIRECT BLOCK ", ind[5], " IN INODE ", ind[1], " AT OFFSET ", ind[3])
			if ind[2] == 3:
				print("INVALID TRIPLE INDIRECT BLOCK ", ind[5], " IN INODE ", ind[1], " AT OFFSET ", ind[3])
		elif ind[5] < first_available:
			if ind[2] == 1:
				print("RESERVED INDIRECT BLOCK ", ind[5], " IN INODE ", ind[1], " AT OFFSET ", ind[3])
			if ind[2] == 2:
				print("RESERVED DOUBLE INDIRECT BLOCK ", ind[5], " IN INODE ", ind[1], " AT OFFSET ", ind[3])
			if ind[2] == 3:
				print("RESERVED TRIPLE INDIRECT BLOCK ", ind[5], " IN INODE ", ind[1], " AT OFFSET ", ind[3])			

if __name__ == '__main__':
	main()
