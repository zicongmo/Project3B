# NAME: Zicong Mo, Benjamin Yang
# ID: 804654167, 904771533
# EMAIL: josephmo1594@ucla.edu, byang77@ucla.edu

default:
	ln -s run.sh lab3b
dist:
	tar -zvcf lab3b-804654167.tar.gz lab3b.py README Makefile run.sh
clean:
	rm -f lab3b-804654167.tar.gz lab3b
	