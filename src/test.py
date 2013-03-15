import re

def main():
	
	newlineCount=0
	logFile=open('../log/oneBlock.log')
	
	for line in logFile:
			#hitText.append(line)
			if re.search(r'^\n$', line)!=None:
				print "FOUND NEWLINE"
				newlineCount+=1
			else:	
				print "nope"
	print logFile
main()
