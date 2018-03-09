// NAME: Zicong Mo, Benjamin Yang
// ID: 804654167, 904771533
// EMAIL: josephmo1594@ucla.edu, byang77@ucla.edu

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>

const int LINE_SIZE = 1024;
const char delimiter = ',';
const int MAX_LINE_ENTRIES = 32; // INODE entries have 27 entries

/* Reads in a comma separated line, outputs an array of pointers to the values 
   Replaces each comma with a null character */
char** parse_csv_line(char* line, int* num_entries){
	char** output = malloc(sizeof(char*)*MAX_LINE_ENTRIES);
	int entries = 0;
	int start = 0;
	int i;
	int max_length = strlen(line);
	for(i = 0; i < max_length; i++){
		if(line[i] == delimiter){
			line[i] = '\0';
			output[entries] = line + start;
			start = i+1;
			entries++;
		}
	}
	/* Get the null terminated entry at the end */
	output[entries] = line + start;
	entries++;

	*num_entries = entries;
	return output;
}


int main(int argc, char** argv){
	/* Parse arguments */
	if(argc != 2){
		fprintf(stderr, "Error: Bad arguments\n");
		exit(1);
	}
	int a;
	while(1){
		static struct option long_options[] = {
			{0, 0, 0 ,0}
		};
		int option_index = 0;
		a = getopt_long(argc, argv, "", long_options, &option_index);
		if(a == -1){
			break;
		}
		switch(a){
			case '?':
				exit(1);
			default:
				break;
		}
	}

	FILE* fp = fopen(argv[1], "r");
	if(fp == NULL){
		fprintf(stderr, "Error: Could not open file\n");
		exit(1);
	}

	char line[LINE_SIZE];
	/* Scan the .csv for superblock info 
	   Should be the first line, but not guaranteed to be formatted like this */
	while(fgets(line, LINE_SIZE, fp) != NULL){
		if(strncmp(line, "SUPERBLOCK", 10) == 0){
			break;
		}
	}
	/* Superblock info not found */
	if(feof(fp)){
		fprintf(stderr, "Error: Superblock info not found in file\n");
		exit(1);
	}

	/* Replace the last newline in line with a null character */
	line[strlen(line)-1] = '\0';

	int num_entries;
	char** super_entries = parse_csv_line(line, &num_entries);
	int i;
	for(i = 0; i < num_entries; i++){
		printf("%s\n", super_entries[i]);
	}
	exit(0);
}
