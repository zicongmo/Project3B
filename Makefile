# NAME: Zicong Mo, Benjamin Yang
# ID: 804654167, 904771533
# EMAIL: josephmo1594@ucla.edu, byang77@ucla.edu

default:
	gcc -Wall -Wextra -o lab3b lab3b.c
dist:
	tar -zvcf lab3b-804654167.tar.gz lab3b.c README Makefile
clean:
	rm -f lab3b-804654167.tar.gz lab3b
	