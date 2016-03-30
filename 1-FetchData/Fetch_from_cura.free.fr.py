import sys
filenames = [
'902gdA1.html',
'902gdA2.html',
'902gdA3.html',
'902gdA4.html',
'902gdA5.html',
'902gdA6.html',

'902gdD6.html',
'902gdD10.html',
'902gdE1.html',
'902gdE3.html',

'902gdF2.html',   # Don't use! Almost every Army Professional in this volume has a *twin* in one of the earlier volumes. Check with List_twins.py

'902gdA1y.html',  # A1 with names     # Helpful
'902gdA2y.html',  # A2 with names     #  to inspect
'902gdA3y.html',  # A3 with names     #   duplicates and twins
'902gdA4y.html',  # A4 with names     
'902gdA5y.html',  # A5 with names
'902gdA6y.html',  # A6 with names

'902gdB1.html',  # Series B. 24,950 Data : Hereditary Experiment
'902gdB2.html',
'902gdB3.html',
'902gdB4.html',
'902gdB5.html',
'902gdB6.html',
]

if 1:   # if 0 to avoid overwritting html files
	import urllib    # works fine in Python 2.7.6
	for filename in filenames:
		url = 'http://cura.free.fr/gauq/' + filename
		html = urllib.urlopen(url).read()
		file = open(filename, 'wt')
		file.write(html)
		file.close()

def readLinesFromFile(srcFilename, headerID):
	file = open(srcFilename, 'rt')
	lines = []
	i = indexOfPre = indexOfHeader = -1
	for line in file:
		lines.append(line)
		i += 1
		if line.find("<pre>") >= 0:  indexOfPre = i
		if indexOfPre>=0 and indexOfHeader<0 and line.startswith(headerID): indexOfHeader = i
	file.close()
	return lines, indexOfHeader

def writeOneLineToFile(file, y, m, d, h, mn, s, lat, lon):
	if not (-23 <= h <= 47):  sys.exit('Error: wrong hour')
	numDays = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	year = int(y)
	month= int(m)
	day  = int(d)
	if day>numDays[month-1] or (month==2 and day==29 and year%4!=0):
		file.write('# !Error! ')
	file.write( y+',' + m+',' + d+',' + str(h)+',' + mn+',' + s+',' + lat+',' + lon+'\n' )

""" Vol.A   Header and sample:
PRO	NUM	COU	DAY	MON	YEA	H	MN	SEC	TZ	LAT	LON	COD	CITY	
C	1	F	17	9	1937	17	0	0	0	44N50	0W34	33	BORDEAUX
C	18	F	15	2	1916	7	0	0	-1	49N 7	6E11	57	REDING
C	19	F	29	7	1918	0	0	0	0	44N12	0E38	47	AGEN
"""
def processVolA(srcFilename, dstFilename, howMany): # A relatively simple format
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'PRO')
	dest = open(dstFilename, 'wt')
	i0 = i = indexOfHeader+2 # +2 because of an empty line after the header
	while len(lines[i]) > 10 and i < i0 + howMany:
		line = lines[i].split('\t')
		i+=1
		day   = line[3]
		month = line[4]
		year  = line[5]
		hour  = int(line[6]) + int(line[9])  # !!! ATTN:  -23 <= hour <= 47 after this !!!
		minute= line[7]
		second= line[8]
		latitude = line[10]
		longitude= line[11]
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume A, ' + str(i-i0) + ' persons\n')
	dest.close()

""" Vol.D6  Header and sample:
NUM	DAY	MON	YEA	H	MN	SEC	LAT	LON     NAME
1	5	1	1935	18	30	0	49N10	05E51	Adaczyk Marcel
2	15	3	1945	3	0	0	48N50	10E07	Adams Walter
3	14	11	1937	8	30	0	44N48	10E19	Adorni Vittorio
"""
def processVolD6(srcFilename, dstFilename):  # Here we have to derive time zone from longitude
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM')
	dest = open(dstFilename, 'at')
	i0 = i = indexOfHeader+2 # +2 because of an empty line after the header
	while len(lines[i]) > 10:
		line = lines[i].split('\t')
		i+=1
		day   = line[1]
		month = line[2]
		year  = line[3]
		hour  = int(line[4])
		minute= int(line[5])
		second= int(line[6])
		latitude = line[7]
		longitude= line[8]
		time = second + minute*60 + hour*3600
		longitudeParts = longitude.split('E')
		if len(longitudeParts)==1:  longitudeParts = longitude.split('W')
		zoneInLongitudeMinutes = int(longitudeParts[0])*60 + int(longitudeParts[1])
		zoneInTemporalSeconds = int(round(zoneInLongitudeMinutes / (180.0*60) * (12*3600)))
		if longitude.find('E')>=0:  time-=zoneInTemporalSeconds
		else:                       time+=zoneInTemporalSeconds
		hour   = time // 3600
		minute = str((time-hour*3600) // 60)
		second = str( time-hour*3600-int(minute)*60)
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume D6, ' + str(i-i0) + ' persons\n')
	dest.close()

""" Vol.D10  Header and sample:
NUM	NAME	                PRO     DAY	MON	YEA	H	TZ      LAT	LON     CICO
1	Aaron Harold		MI	21	6	1921	07:00	6h	40N29	86W8	Kokomo, IN
2	Aaron Henry		SP	5	2	1934	20:25	6h	30N41	88W3	Mobile, AL
3	Abramowicz Daniel	SP	13	7	1945	09:16	4h	40N22	80W37	Steubenville, OH
4	Adams Robert		SC	23	7	1926	06:17	5h	41N52	87W39	Chicago, IL
"""
def processVolD10(srcFilename, professionCode, dstFilename):  # A completely different format! Names are included.
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM')
	dest = open(dstFilename, 'at')
	i0, i = 0, indexOfHeader+3 # +3 because of two empty lines after the header
	while len(lines[i]) > 10:
		line = lines[i].replace('   ', '\t')  # replace
		line =     line.replace( '  ', '\t')
		line = line.split('\t')
		i+=1
		while len(line[2])==0: line.pop(2)
		if not line[2].startswith(professionCode):  continue
		i0+=1
		day   = line[3]
		month = line[4]
		year  = line[5]
		time  = line[6]
		zone  = line[7]
		latitude = line[8]
		longitude= line[9]
		timeParts = time.split(':')
		zoneParts = zone.split('h')
		if len(timeParts) < 2:                  hour,  minute = 12, 0
		else:                                   hour,  minute = int(timeParts[0]), int(timeParts[1])
		if len(zoneParts)<2 or zone[-1]=='h':  zhour, zminute = int(zoneParts[0]), 0
		else:                                  zhour, zminute = int(zoneParts[0]), int(zoneParts[1])
		UT = (hour + zhour)*60 + minute + zminute
		hour   = UT // 60
		minute = UT - hour*60
		second = '0'
		minute = str(minute)
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume D10, ' + str(i0) + ' persons\n')
	dest.close()

""" Vol.E1  Header and sample:
NUM	PRO      NAME              	         DAY   MON   YEA      H       CITY                     COD
0005    PH       AGACHE Pierre                   08    06    1927    17:10    Roubaix                   59
0006    MI     * AILLERET CHARLES                26    03    1907    15:00    Mantes-la-Jolie           78
0007    PH       ALBERTIN Robert                 22    11    1900    18:00    Bourg-en-Bresse           01
"""
def processVolE(srcFilename, professionCode, dstFilename):  # A format similar to D10, but no '\t' except in the header !
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM')
	dest = open(dstFilename, 'at')
	i0, i = 0, indexOfHeader+2 # +2 because of an empty line after the header
	while len(lines[i]) > 10:
		line = lines[i]
		i+=1
		if not line[8:].startswith(professionCode):  continue
		i0+=1
		day   = line[49:51]
		month = line[55:57]
		year  = line[61:65]
		hour  = int(line[69:71])
		minute=     line[72:74]
		second = '0'
		latitude = longitude ='-'
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume E1, ' + str(i0) + ' persons\n')
	dest.close()

""" Vol.F2  Header and sample:
NUM	DAY	MON	YEA	H	MN	SEC	TZ      LAT     LON     COD
3	08	07	1824	18	0	0	0	47N19	5E02	21
4	24	04	1849	12	0	0	-1	44N12	0E38	47
5	03	01	1821	19	0	0	0	48N07	5E08	52
"""
def processVolF2(srcFilename, dstFilename):  # A format similar to A1 ... A6
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM')
	dest = open(dstFilename, 'at')
	i0 = i = indexOfHeader+2+616+6 # an empty line after the header, then 616 Liberation Fighters, then 6 more lines
	while len(lines[i]) > 10:
		line = lines[i].split('\t')
		i+=1
		day   = line[1]
		month = line[2]
		year  = line[3]
		hour  = int(line[4]) + int(line[7])  # !!! ATTN:  -23 <= hour <= 47 after this !!!
		minute= line[5]
		second= line[6]
		latitude = line[8]
		longitude= line[9]
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume F2, ' + str(i-i0) + ' persons\n')
	dest.close()

if 1:
	processVolA(  filenames[0],                'SportsChampions_TimePlace.csv', 9999)   # 2087
	processVolA(  filenames[1],       'ScientistsMedicalDoctors_TimePlace.csv', 9999)   # 3643
	processVolA(  filenames[2],                    'MilitaryMen_TimePlace.csv', 9999)   # 3045, not 3046, because 1 has an invalid date of birth: 1869-Feb-29
	processVolA(  filenames[3],                       'Painters_TimePlace.csv', 1472)   # 1472
	processVolA(  filenames[4],                         'Actors_TimePlace.csv', 1408)   # 1407, not 1408, because 1 is a true duplicate: Francois Victor Arthur Gilles de Saint Germain (born on 1832-Jan-12), see also https://fr.wikipedia.org/wiki/Gilles_de_Saint-Germain
	processVolA(  filenames[5],                        'Writers_TimePlace.csv', 1352)   # 1352

	processVolD6( filenames[6],                'SportsChampions_TimePlace.csv')   # 449

	processVolD10(filenames[7], 'SP',          'SportsChampions_TimePlace.csv')   # 350
	processVolD10(filenames[7], 'SC', 'ScientistsMedicalDoctors_TimePlace.csv')   #  98
	processVolD10(filenames[7], 'MI',              'MilitaryMen_TimePlace.csv')   # 245
	processVolD10(filenames[7], 'AR',                 'Painters_TimePlace.csv')   #  89
	processVolD10(filenames[7], 'AC',                   'Actors_TimePlace.csv')   # 228
	processVolD10(filenames[7], 'WR',                  'Writers_TimePlace.csv')   # 103

	processVolE(  filenames[8], 'PH', 'ScientistsMedicalDoctors_TimePlace.csv')   # 974, not 975, because 1 is a true duplicate: Lucien Leger (born on 1912-Aug-29)
	processVolE(  filenames[8], 'MI',              'MilitaryMen_TimePlace.csv')   # 629
	processVolE(  filenames[9], 'PAI',                'Painters_TimePlace.csv')   #  91
	processVolE(  filenames[9], 'AC',                   'Actors_TimePlace.csv')   # 125
	processVolE(  filenames[9], 'WR',                  'Writers_TimePlace.csv')   # 210, not 211, because 1 is a true duplicate: Daniel Boulanger (born on 1922-Jan-24)

	processVolF2( filenames[10],                   'MilitaryMen_TimePlace.csv')   # Don't use! Almost every Army Professional in this volume has a *twin* in one of the earlier volumes. Check with List_twins.py

""" Vol.B   Header and sample:
NUM	SEX	DAY	MON	YEA	H	MN	SEC	Ci	TZ      LAT     LON	COD
1	F	22	5	1866	16	50	40		0	48N50	2E20	75
2	S	12	10	1925	22	0	0	15	0	48N50	2E20	75
3	F	22	11	1867	16	50	40		0	48N50	2E20	75
"""
def processVolB(srcFilename, dstFilename, mode): # A format very similar to vol.A format
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM')
	dest = open(dstFilename, mode)
	i0 = i = indexOfHeader+2 # +2 because of an empty line after the header
	while len(lines[i]) > 10:
		line = lines[i].split('\t')
		i+=1
		day   = line[2]
		month = line[3]
		year  = line[4]
		hour  = int(line[5]) + int(line[9])  # !!! ATTN:  -23 <= hour <= 47 after this !!!
		minute= line[6]
		second= line[7]
		latitude = line[10]
		longitude= line[11]
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume B, ' + str(i-i0) + ' persons\n')
	dest.close()

processVolB(filenames[17], 'HeredityVolB_TimePlace.csv', 'wt')
processVolB(filenames[18], 'HeredityVolB_TimePlace.csv', 'at')
processVolB(filenames[19], 'HeredityVolB_TimePlace.csv', 'at')
processVolB(filenames[20], 'HeredityVolB_TimePlace.csv', 'at')
processVolB(filenames[21], 'HeredityVolB_TimePlace.csv', 'at')
processVolB(filenames[22], 'HeredityVolB_TimePlace.csv', 'at')
