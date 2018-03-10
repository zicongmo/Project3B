# NAME: Zicong Mo, Benjamin Yang
# ID: 804654167, 904771533
# EMAIL: josephmo1594@ucla.edu, byang77@ucla.edu

import sys
import os.path

def main():
	if len(sys.argv) != 2:
		print("Error: Bad arguments", file=sys.stderr)
		return
	if os.path.exists(sys.argv[1]):
		with open(sys.argv[1], 'r') as f:
			lines = f.read().splitlines()
	else:
		print("Error: File could not be opened", file=sys.stderr)
		return
	inodes = []
	dirs = []
	free_blocks = []
	for l in lines:
		if l[:10] == 'SUPERBLOCK':
			superblock = l.split(',')
		if l[:6] == 'INODE':
			inodes.append(l.split(','))
		if l[:7] == 'DIRENT':
			dirs.append(l.split(','))
		if l[:6] == 'BFREE':
			free_blocks.append(l.split(','))


if __name__ == '__main__':
	main()
