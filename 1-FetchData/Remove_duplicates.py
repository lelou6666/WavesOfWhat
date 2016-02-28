import sys
dates = []
i=0
test_cases = open(sys.argv[1], 'r')

for test in test_cases:
	i+=1
	if test[0]=='#':
		print test.strip()
		continue
	vars = test.split(',')

	y = vars[0].strip()
	o = vars[1].strip()
	d = vars[2].strip()
	h = vars[3].strip()
	m = vars[4].strip()
	s = vars[5].strip()

	y = str(int(y))
	o = str(int(o))
	d = str(int(d))
	h = str(int(h))
	m = str(int(m))
	s = str(int(s))

	res = y+'_'+o+'_'+d+'_'+h+'_'+m+'_'+s+'_'
	if not (res in dates):
		print test.strip()
		dates.append(res)

test_cases.close()
