import sys
dates = []
i=0
test_cases = open(sys.argv[1], 'r')

for test in test_cases:
	i+=1
	if test[0]=='#':
		dates.append('#')
		continue
	vars = test.split(',')
	y = str(int(vars[0].strip()))
	o = str(int(vars[1].strip()))
	d = str(int(vars[2].strip()))
	h = str(int(vars[3].strip()))
	m = str(int(vars[4].strip()))
	s = str(int(vars[5].strip()))

	res = y+'_'+o+'_'+d+'_'+h+'_'+m+'_'+s+'_'
	if res in dates:
		foundIdx = dates.index(res)
		print 'Line', i, '=', foundIdx+1
	dates.append(res)

test_cases.close()
