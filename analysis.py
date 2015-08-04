import csv
from numpy import *
from matplotlib.pyplot import *
from scipy import stats

REPETITIONS = 6
P_BORDER = 0.05

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
		# now add the numbers to our tmp array which represents a VP
		tmp.append(timestorage)
		# now that we collected all data we can add this tmp VP as a final VP to the VPS array
		VPS.append(tmp)

for VP in VPS:
	print "Subject ",VP[0], ", Session ",VP[1]+1
	print "%4s %4s %4s %4s %4s %4s"% (1,2,3,4,5,6)
	print "%4s %4s %4s %4s %4s %4s" % (VP[2][0],VP[2][1],VP[2][2],VP[2][3],VP[2][4],VP[2][5])
	print "Mean: ",mean(VP[2])," Std: ",std(VP[2])," Variance: ",var(VP[2])," Median: ",median(VP[2])
	print

# graphical analysis, Boxplots...
figure()
#collect all arrays in one
hugearray = []
names = []
for VP in VPS:
	hugearray.append(VP[2])
	names.append(VP[0])
boxplot(hugearray)
xticks((1+arange(len(VPS))), names, size='small')
xlabel("Subject")
ylabel("Nr of switches")


with open('collectedResults.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(VPS)

# statistical analysis part 2 - comparison of medians
# It is not normally distributed with just 6 values per person... so we assume it is not normally distributed
for i,current in enumerate(hugearray):
	if i%2==0: # just do this every second step
		f_value, p_value = stats.f_oneway(hugearray[i],hugearray[i+1])
		if p_value < P_BORDER:
			print "Significant difference between ",names[i], " and ",names[i+1],". p-value: ",p_value
		if p_value > P_BORDER:
			print "No Significance between ",names[i], " and ",names[i+1],". p-value: ",p_value

show()

					
