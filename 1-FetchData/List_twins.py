# List persons such that the nearest neighbour is less than 3 hours away

import sys
dates = []
times = []
i=0
file = open(sys.argv[1], 'r')

for line in file:
	i+=1
	if line[0]=='#':
		dates.append('#')
		times.append('#')
		continue
	vars = line.split(',')
	y = str(int(vars[0].strip()))
	o = str(int(vars[1].strip()))
	d = str(int(vars[2].strip()))
	h = str(int(vars[3].strip()))
	m = str(int(vars[4].strip()))
	s = str(int(vars[5].strip()))

	date = y+'_'+o+'_'+d
	time = int(h)*3600 + int(m)*60 + int(s)

	indxOfNearest = 0
	diffOfNearest = 3*60*60    # 3 hours
	j = 0
	for ymd in dates:
		j += 1
		if ymd==date:
			diff = abs(time-times[j-1])
			if diff < diffOfNearest:
				diffOfNearest = diff
				indxOfNearest = j
	if indxOfNearest > 0:
		print "Line %4d" % i, "~= %4d :  " % indxOfNearest, "%5d" % diffOfNearest,
		if diffOfNearest > 60*60:    # bigger than 1 hour
			print '!!!'
		else:
			print

	dates.append(date)
	times.append(time)

file.close()
