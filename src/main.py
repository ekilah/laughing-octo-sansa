


import re #regular expressions


















def main():
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#Counters setup
	
	
	pageIdToNames = {
		0: "HeyZap Home Page",
		1: "HeyZap Payments Page",
		2: "HeyZap Payments Item Lookup",
		3: "Gameplays with Weebly Embed Key"
	}
	
	#maps an integer ID for page match regular expressions to the regex itself
	pageIdToRegexDict= {
		0: r'\[http://www.heyzap.com/\]',
		1: r'\[http://www.heyzap.com/payments/\]',
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
	totalVisits={0:0, 1:0, 2:0, 3:0}
	
	ipRegex = r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}' #matches an IP address
	
	
	
	
	
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#Funnel Paths setup
	
	
	#each funnel path has a dictionary of IP addresses to steps/options that the IP address is currently oni n that funnel path.
	funnelPathTracker ={
		0: {},
		1: {}		
	}
	
	#each funnel path is a dictionary entry that corresponds to a dictionary of each URL in the path
	funnelPathRegexDict={
		0: {
			0: [r'http://www.heyzap.com/'],
			1: [r'http://www.heyzap.com/publishers/new_site'],
			2: [r'http://www.heyzap.com/publishers/get_embed']
		},
		1: {
			0: [r'http://www.heyzap.com/'],
			1: [r'http://www.heyzap.com/developers'],
			2: [r'http://www.heyzap.com/developers/new_game'],
			3: [r'http://www.heyzap.com/developers/import_games', r'http://www.heyzap.com/developers/new_inventory_item', r'http://www.heyzap.com/developers/upload_game_simple']
		}
	}
	
	
	#a dictionary entry for each funnel path, where each entry is:
		#a dictionary entry between the step number in this funnel and the number of users who fell off at this step:option
	fellOffAtFunnelPathStepAndOption={
		0:{0:{0:0},1:{0:0},2:{0:0}},
		1:{0:{0:0},1:{0:0},2:{0:0},2:{0:0,1:0,2:0}}
	}
	
	
	
	
	
	#print pageCounters
	#print uniqueVisits
	
	logFile = open('../log/production.log.6', 'r')
	#slogFile = open('../log/reallySmall.log', 'r')
	logFile.readline()
	logFile.readline()
	
	hitText = []
	newlineCount = 0
	quit = False
	lineNumber = 2;
	
	while quit == False:
	
		#get the next page hit description block
		for line in logFile:
			lineNumber +=1
			if re.search(r'^\n$', line)!=None:
				#print "FOUND NEWLINE"
				newlineCount+=1
			else:
				hitText.append(line)
				newlineCount = 0 #if only one newline is found, keep processing as part of this block
			if newlineCount==2:
				#print "searching..."
				newlineCount=0
				
				ipAddress = re.search(ipRegex, hitText[0])
				if ipAddress == None:
					print "\n********\n\tPotential ERROR in log: no IP address found on header line of log block. Near line: " + str(lineNumber)
					print "\tSearching for IP address in this text: " + hitText[0] + "\n********\n"
				else:
					ipAddress = ipAddress.group(0)
					#print ipAddress
				
				#~~~~~~
				#Counters
				for line in hitText:
					#print line
					for key in pageIdToRegexDict.keys():
						#print '' + str(key) + pageIdToRegexDict[key]
						if re.search(pageIdToRegexDict[key], line) != None:
							#string at this location of hitText matched URL regex at index 'key'
							#print 'hit on key: ' + str(key) + ', value: ' + str(pageIdToRegexDict[key])
							
							if ipAddress in pageCounters[key]:
								#not a unique visit
								pageCounters[key][ipAddress] += 1
							else:
								pageCounters[key][ipAddress] = 1
								uniqueVisits[key]+=1
							totalVisits[key]+=1
							
				#~~~~~~~~~
				#Funnels
				
				
				
							
				
				
				
				hitText=[]
		quit = True
	
	#print uniqueVisits
	#print "\n"
	#print totalVisits
	
	
	print "\nUnique hits for:"
	print "-----------------"
	for i in uniqueVisits.keys():
		print "\t" + pageIdToNames[i] + ": " + str(uniqueVisits[i])
		
	
	print "\nTotal hits for:"
	print "-----------------"
	for i in totalVisits.keys():
		print "\t" + pageIdToNames[i] + ": " + str(totalVisits[i])
		
	
	
	
	
if __name__ == '__main__':#runs main() if this module is being run directly rather than being included in another script
        main()
