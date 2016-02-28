import sys
dates = []
test_cases = open(sys.argv[1], 'r')

for test in test_cases:
	if test[0]=='#':
		print test.strip()
		continue
	vars = test.split(',')
	y = str(int(vars[0].strip()))
	o = str(int(vars[1].strip()))
	d = str(int(vars[2].strip()))
	h = str(int(vars[3].strip()))
	m = str(int(vars[4].strip()))
	s = str(int(vars[5].strip()))

	res = y+'_'+o+'_'+d+'_'+h+'_'+m+'_'+s+'_'
	if not (res in dates):
		print test.strip()
		dates.append(res)

test_cases.close()
