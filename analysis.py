import csv
from numpy import *

REPETITIONS = 6
reps = arange(REPETITIONS)
VPS = []

with open("./CoffeExpTimes", "rb") as file:
	allTrials = csv.reader(file,delimiter=",")
	for trial in allTrials: #1 trial is one VP
		tmp = []
		# adds name of person
		tmp.append(trial[1])
		# adds session ID, 0 = unconscious, 1 = conscious
		if "1" in tmp[0]:
			tmp.append(0) 
		if "2" in tmp[0]:
			tmp.append(1)
		# now put the 6 trials & the nr's of a switch 
		# seen in the array matching to that person
		timestorage = [[],[],[],[],[],[]]
		previous = 99999.9
		pos = -1
		counter = 0
		skipper = 0
		for time in trial:
			if skipper > 1: # skips name and date
				time = float(time)
				if time < previous : # which means that it must be a new round
					timestorage[pos]=counter
					pos = pos + 1
					counter = 1
					previous = time
				if time > previous:
					counter = counter + 1
					previous = time
			skipper = skipper +1
		timestorage[pos]=counter # last manual addition, because it would not do that because there is no next element it can compare to		
		while pos < 5: # manually set missing fields to zero
			pos = pos +1 
			timestorage[pos] = 0
		print timestorage
			 
					
