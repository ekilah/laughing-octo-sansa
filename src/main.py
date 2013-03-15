#############################################
# By: Monroe Ekilah
#
# For: HeyZap Interview Coding Challenge
#
# On: 3/15/2013
#############################################


import re #regular expressions
import sys #argv


def main():
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#Counters setup
	#
	#You can customize which counters are going to be kept track of by adding entries to the dictionaries below.
		# Add an entry to pageIdToNames to give a nice name for the print out at the end
		# Add a regular expression for whatever will match in the entire block of text for the server log of interest to pageIdToRegexDict (with the same key as what you entered into the first dictionary)
		#Add an empty dictionary entry with the same key to pageCounters
		#Add another dictionary entry with value=0 for both uniqueVisits and totalVisits, with the same key
	#I ran out of time to make this happen from a file, but it could be done.
	
	
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
	
	
	
	uniqueVisits={0:0, 1:0, 2:0, 3:0}#keeps track of unique visits to each page in pageIdToRegexDict
	totalVisits={0:0, 1:0, 2:0, 3:0}#same as above, but for total visits
	
	ipRegex = r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}' #matches an IP address
	
	
	
	
	
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#Funnel Paths setup
	#
	#Ran out of time to make this fully functional, bug free, and easily extendable. However, the counters are such. This implementation got further than I thought I would in the amount of time given, though.
	
	
	#each funnel path has a dictionary of IP addresses to steps/options that the IP address is currently oni n that funnel path.
		#the inner dictionary will map IP addresses to a {step:option} dictionary
	funnelPathTracker ={
		0: {},
		1: {}		
	}
	
	#each funnel path is a dictionary entry that corresponds to a dictionary of each URL in the path
	funnelPathRegexDict={
		0: {
			0: [r'http://www.heyzap.com/\]'],
			1: [r'http://www.heyzap.com/publishers/new_site\]'],
			2: [r'http://www.heyzap.com/publishers/get_embed.*\]']
		},
		1: {
			0: [r'http://www.heyzap.com/\]'],
			1: [r'http://www.heyzap.com/developers\]'],
			2: [r'http://www.heyzap.com/developers/new_game\]'],
			3: [r'http://www.heyzap.com/developers/import_games.*\]', r'http://www.heyzap.com/developers/new_inventory_item.*\]', r'http://www.heyzap.com/developers/upload_game_simple\?.*\]']
		}
	}
	
	
	#a dictionary entry for each funnel path, where each entry is:
		#a dictionary entry between the step number in this funnel and the number of users who fell off at this step's option
	fellOffAtFunnelPathStepAndOption={
		0:{0:{0:0},1:{0:0},2:{0:0}},
		1:{0:{0:0},1:{0:0},2:{0:0},2:{0:0,1:0,2:0}}
	}
	
	#for each funnel, an array that contains
		#a dictionary of IP addresses to number of times they finished the funnel at the option track signified by the array index
		
	#number/uniques per funnel path is the sum of the num(keys) for each entry in the dictionary
	completedFunnelPathAtOption={
		0:[{}],
		1:[{},{},{}]
	}
	
	
	
	
	
	#print pageCounters
	#print uniqueVisits
	
	if len(sys.argv)>1:
		logFile = open(sys.argv[1], 'r')#command line arg for log file
	else:
		logFile = open('../log/production.log.6', 'r')#default if no file provided
		
	#logFile = open('../log/oneFunnelTest.log', 'r')
	logFile.readline()
	logFile.readline()#get rid of first newlines in log file (assumed to always be there)
	
	hitText = [] #store a block of text from the log that represents one server action
	newlineCount = 0#assume that entries in log are always separated by 2 newlines, this keeps track of how many we've seen so far
	#quit = False
	lineNumber = 2;#keeps track of line number (approx) for error reporting (debugging)
	
	#while quit == False:
	
	#get the next page hit description block
	for line in logFile:
		lineNumber +=1
		if re.search(r'^\n$', line)!=None:#if line read is a newline only
			#print "FOUND NEWLINE"
			newlineCount+=1
		else:
			hitText.append(line)
			newlineCount = 0 #if only one newline is found, keep processing the next line as part of this block
		if newlineCount==2:
			#skips = 0
			#while re.search(r'^\n$', logFile.readline())!=None:
				#print "Skipping line #" + str(skips + lineNumber)
				#skips +=1
				####can't do the above because you can't modify the iterator inside the loop (oh well)
				####this was an attempt to not assume 2 lines per server log entry
				
			newlineCount=0#reset for next iteration
			
			ipAddress = re.search(ipRegex, hitText[0])#store IP address from first line of log entry for Funnel tracking
			if ipAddress == None:
				print "\n********\n\tPotential ERROR in log: no IP address found on header line of log block. Near line: " + str(lineNumber)
				print "\tSearching for IP address in this text: " + hitText[0] + "\n********\n"
			else:
				ipAddress = ipAddress.group(0)#get string match for IP address out of regex match object
				#print ipAddress
			
			#~~~~~~
			#Counters implementation
			for line in hitText: #for each line in this one server log entry
				#print line
				for key in pageIdToRegexDict.keys(): # for each regex we are going to check against the server log entry
					#print '' + str(key) + pageIdToRegexDict[key]
					if re.search(pageIdToRegexDict[key], line) != None:
						#string at this location of hitText matched URL regex at index 'key'
						
						#print 'hit on key: ' + str(key) + ', value: ' + str(pageIdToRegexDict[key])
						
						if ipAddress in pageCounters[key]:
							#not a unique visit
							pageCounters[key][ipAddress] += 1
						else:#this is the first visit to this regex-matched URL by this IP address
							pageCounters[key][ipAddress] = 1
							uniqueVisits[key]+=1
						
						totalVisits[key]+=1 #regardless of visit count, track total visits
						
						
						
			#~~~~~~~~~
			#Funnels implementation - incomplete/not fully tested due to time limitations
			
			#note - I know the nested for loops are bad efficiency-wise, however because of the complex dictionary structures I used to store the data, this was my quickest and best bet. some of the loss will be gained back since the dictionary structures should maintain O(1) efficiency (as hash tables)
			
			
			doneWithThisFunnel=False #allows me to skip for loop iterations if I already found a hit for the current funnel
			
			#last line of hitText should have URL to search for funnel.
			
			#print "Checking line for funnels:\n\t" + hitText[len(hitText)-1]
						
			for index in funnelPathRegexDict.keys():#gets each funnel (list of regexes)
				doneWithThisFunnel=False
				updatedThisIPInThisFunnel=False
				
				#print "Checking funnel path #" + str(index)
				for secondIndex in funnelPathRegexDict[index].keys():#gets each regex array for this funnel (each step of this funnel)
					#print "\tChecking step #"+str(secondIndex)+" of funnel path #"+str(index) 
					regexArray = funnelPathRegexDict[index][secondIndex]
					
					#updatedThisIPInThisFunnel=False
					
					for regex in regexArray:
						#print "\t\tChecking url#"+str(regexArray.index(regex))+" for funnel:path{"+str(index)+","+str(secondIndex)+"}"
						searchStr = hitText[len(hitText)-1]#last string has URL to search for in log entries
						match = re.search(regex, searchStr)
						if match != None:
							#URL matched a funnel path entry
							updatedThisIPInThisFunnel=True
							url = match.group(0)
							#print "\t\tFound matching url for funnel:path{"+str(index)+","+str(secondIndex)+"}: " + url
						
							if ipAddress in funnelPathTracker[index].keys() and secondIndex in funnelPathTracker[index][ipAddress].keys():
								#already were at this step in the funnel, do nothing (?)
								#print "\t\t Funnel:path{"+str(index)+","+str(secondIndex)+"} already contained IP: " + ipAddress
								x=5#doing nothing (else statement needs some code to be here... haha
							else:
								#store the {funnel step: funnel option} pair in the tracker dictionary entry for this funnel and this IP address
								if secondIndex != max(funnelPathRegexDict[index].keys()):
									funnelPathTracker[index][ipAddress] = {secondIndex: regexArray.index(regex)}
								else:
									#completed funnel. clear old funnel path entries and remember that we completed!
									if ipAddress in completedFunnelPathAtOption[index][regexArray.index(regex)].keys():
										completedFunnelPathAtOption[index][regexArray.index(regex)][ipAddress]+=1
									else:
										completedFunnelPathAtOption[index][regexArray.index(regex)][ipAddress]=1
									#print "FUNNEL COMPLETE! Current state of completedFunnelPathAtOption:"
									#print "\t", completedFunnelPathAtOption
									funnelPathTracker[index][ipAddress]={}#clear old path information for this IP on this funnel
							doneWithThisFunnel = True
							break #go to next funnel path if we found a hit on this one
								
					if doneWithThisFunnel==True:
						break
						
									
				if updatedThisIPInThisFunnel==False:
					#IP address was never found in this funnel. Record it as fallen off if it was on this funnel track before
					if ipAddress in funnelPathTracker[index].keys():#if this IP is listed in this funnel track
						if len(funnelPathTracker[index][ipAddress].keys())>=1:
							stepNumToRemoveOptionFrom = funnelPathTracker[index][ipAddress].keys()[0]
							optionNum = funnelPathTracker[index][ipAddress][stepNumToRemoveOptionFrom]
						
							if optionNum in fellOffAtFunnelPathStepAndOption[index][stepNumToRemoveOptionFrom].keys():
								fellOffAtFunnelPathStepAndOption[index][stepNumToRemoveOptionFrom][optionNum] +=1
							else:
								fellOffAtFunnelPathStepAndOption[index][stepNumToRemoveOptionFrom][optionNum] = 1
						
						
							del funnelPathTracker[index][ipAddress]
								
						
			hitText=[] #reset array of strings for next iteration
		#quit = True
		
		
	#almost done, but those paths left incomplete in the "funnelPathTracker" need to be migrated to fellOffAtFunnelPathStepAndOption
	#RAN OUT OF TIME TO IMPLEMENT THIS PART. However, the code would be similar to the above large loops. 
	
	
		
	
	#print uniqueVisits
	#print "\n"
	#print totalVisits
	
	print "\nMonroe Ekilah's HeyZap Internship Coding Challenge"
	print "\n\n-------->NOTE: I ran out of time to fully test the funnels, or to migrate those paths left\n\
	 hanging (funnels in progress) at the end of the log file to my dictionary of paths that didn't\n\
	 finish. However, this latter flaw may or may not represent the desired effect, since maybe\n\
	 midnight just rolled around and lots of people are using the app still. Regardless, I ran out\n\
	 of time to implement a fix for this, but I recognize it.\n"
	
	print "\nUnique hits for:"
	print "-----------------"
	for i in uniqueVisits.keys():
		print "\t" + pageIdToNames[i] + ": " + str(uniqueVisits[i])
		
	
	print "\nTotal hits for:"
	print "-----------------"
	for i in totalVisits.keys():
		print "\t" + pageIdToNames[i] + ": " + str(totalVisits[i])
		
	print "\n"
	#print fellOffAtFunnelPathStepAndOption
	#print "\n"
	#print funnelPathTracker
	#print"\n"
	#print completedFunnelPathAtOption
	
	
	print "\nNumber of unique 'Publisher's Front Page' funnel paths:"
	print "---------------------------------------------------------"
	print "\tCompleted: " + str(len(completedFunnelPathAtOption[0][0].keys()))
	for i in fellOffAtFunnelPathStepAndOption[0].keys():
		for j in fellOffAtFunnelPathStepAndOption[0][i].keys():
			print "\tFell off at step #" + str(i+1) + ", option #"+str(j+1)+": " + str(fellOffAtFunnelPathStepAndOption[0][i][j])
	
	print "\nNumber of 'Devs' funnel paths (Option #1: import_games):"
	print "-----------------------------------------------------------------"
	print "\tUnique IPs completed: " + str(len(completedFunnelPathAtOption[1][0].keys()))
	print "\tFell off at step #1, option #1: " + str(fellOffAtFunnelPathStepAndOption[1][0][0])
	print "\tFell off at step #2, option #1: " + str(fellOffAtFunnelPathStepAndOption[1][1][0])
	print "\n\tNote: first two steps of the above are the same for the rest of the Dev funnels, and weren't repeated.\n"
	print "\nNumber of 'Devs' funnel paths (Option #2: new_inventory_item):"
	print "-----------------------------------------------------------------------"
	print "\tUnique IPs completed: " + str(len(completedFunnelPathAtOption[1][1].keys()))
	#print "\tFell off at step #" + str(3) + ", option #"+str(2)+": " + str(fellOffAtFunnelPathStepAndOption[1][2][1])
	
	print "\nNumber of 'Devs' funnel paths (Option #3: upload_game_simple):"
	print "----------------------------------------------------------------------"
	print "\tUnique IPs completed: " + str(len(completedFunnelPathAtOption[1][2].keys()))
	#print "\tFell off at step #" + str(3) + ", option #"+str(3)+": " + str(fellOffAtFunnelPathStepAndOption[1][2][2])
	
	
	print"\n\n\tThis was a very interesting challenge! I had to spend a decent amount of extra time\n\
	brushing up on my Python skills beforehand, because I've only used it sparingly in the\n\
	past, so please excuse me if I did some naive things here. It is still a fairly new language to me!\n\n"

	
	
if __name__ == '__main__':#runs main() if this module is being run directly rather than being included in another script
	main()
