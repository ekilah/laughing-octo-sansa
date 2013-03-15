


import re #regular expressions


















def main():
	
	#maps an integer ID for page match regular expressions to the regex itself
	pageIdToRegexDict= {
		0: r'\[http://www.heyzap.com/\]',
		1: r'\[http://www.heyzap.com/payments\]',
		2: r'\[http://www.heyzap.com/payments/get_item/\?cb=[\d]+\]',
		3: r'Parameters: {"permalink"=>"[A-z0-9-]+", "embed_key"=>"12affbbace", "action"=>"index", "controller"=>"heyzap".*}'
	}
	
	#number of hits per page in pageIdToRegexDict
	#key = pageID
	#value = dictionary
		#key: IP address
		#value: num/hits
	pageCounters={
		0:{}, 1:{}, 2:{}, 3:{}
	}
	
	
	
	uniqueVisits={0:0, 1:0, 2:0, 3:0}
	
	
	ipRegex = r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}' #matches an IP address
	
	
	
	#print pageCounters
	#print uniqueVisits
	
	logFile = open('../log/reallySmall.log', 'r')
	logFile.readline()
	logFile.readline()
	
	hitText = []
	newlineCount = 0
	quit = False
	
	while quit == False:
	
		#get the next page hit description block
		for line in logFile:
			hitText.append(line)
			if re.search(r'^\n$', line)!=None:
				#print "FOUND NEWLINE"
				newlineCount+=1
			if newlineCount==2:
				#print "searching..."
				newlineCount=0
				
				ipAddress = re.search(ipRegex, hitText[0]).group(0)
				if ipAddress == None:
					print "********ERROR: No IP address found in block..."
				
				for line in hitText:
					#print line
					for key in pageIdToRegexDict.keys():
						#print '' + str(key) + pageIdToRegexDict[key]
						if re.search(pageIdToRegexDict[key], line) != None:
							#string at this location of hitText matched URL regex at index 'key'
							#print 'hit on key: ' + str(key) + ', value: ' + str(pageIdToRegexDict[key])
							x=5
							
							if ipAddress in pageCounters[key]:
								#not a unique visit
								pageCounters[key][ipAddress] += 1
							else:
								pageCounters[key][ipAddress] = 1
								uniqueVisits[key]+=1
							
							
						#else:
							#print 'miss on key: ' + str(pageIdToRegexDict[key])
				#print "done searching keys"
				hitText=[]
		quit = True
	
	print uniqueVisits
	print "\n"
	print pageCounters
	
	
	
	
	
	
	
	
	
if __name__ == '__main__':#runs main() if this module is being run directly rather than being included in another script
        main()
