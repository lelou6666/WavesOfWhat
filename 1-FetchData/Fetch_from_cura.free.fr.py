import sys
filenames = [
'902gdA1.html',
'902gdA2.html',
'902gdA3.html',
'902gdD6.html',
'902gdD10.html',
'902gdE1.html',
'902gdF2.html',
]

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
def processVolA(srcFilename, dstFilename): # A relatively simple format
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'PRO')
	dest = open(dstFilename, 'wt')
	i = indexOfHeader+2 # +2 because of an empty line after the header
	while len(lines[i]) > 10:
		line = lines[i].split('\t')
		i+=1
		day   = line[3]
		month = line[4]
		year  = line[5]
		hour  = int(line[6]) + int(line[9])  # !!! NOTE -23 <= hour <= 47 after this !!!
		minute= line[7]
		second= line[8]
		latitude = line[10]
		longitude= line[11]
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume A\n')
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
	i = indexOfHeader+2 # +2 because of an empty line after the header
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
	dest.write('# End of data from Volume D6\n')
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
	i = indexOfHeader+3 # +3 because of two empty lines after the header
	while len(lines[i]) > 10:
		line = lines[i].replace('   ', '\t')  # replace
		line =     line.replace( '  ', '\t')
		line = line.split('\t')
		i+=1
		while len(line[2])==0: line.pop(2)
		if not line[2].startswith(professionCode):  continue
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
		else:					                hour,  minute = int(timeParts[0]), int(timeParts[1])
		if len(zoneParts)<2 or zone[-1]=='h':  zhour, zminute = int(zoneParts[0]), 0
		else:					               zhour, zminute = int(zoneParts[0]), int(zoneParts[1])
		UT = (hour + zhour)*60 + minute + zminute
		hour   = UT // 60
		minute = UT - hour*60
		second = '0'
		minute = str(minute)
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume D10\n')
	dest.close()

""" Vol.E1  Header and sample:
NUM	PRO      NAME              	         DAY   MON   YEA      H       CITY                     COD
0005    PH       AGACHE Pierre                   08    06    1927    17:10    Roubaix                   59
0006    MI     * AILLERET CHARLES                26    03    1907    15:00    Mantes-la-Jolie           78
0007    PH       ALBERTIN Robert                 22    11    1900    18:00    Bourg-en-Bresse           01
"""
def processVolE1(srcFilename, professionCode, dstFilename):  # A format similar to D10, but no '\t' except in the header !
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM')
	dest = open(dstFilename, 'at')
	i = indexOfHeader+2 # +2 because of an empty line after the header
	while len(lines[i]) > 10:
		line = lines[i]
		i+=1
		if not line[8:].startswith(professionCode):  continue
		day   = line[49:51]
		month = line[55:57]
		year  = line[61:65]
		hour  = int(line[69:71])
		minute=     line[72:74]
		second = '0'
		latitude = longitude ='-'
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume E1\n')
	dest.close()

""" Vol.F2  Header and sample:
NUM	DAY	MON	YEA	H	MN	SEC	TZ      LAT     LON     COD
3	08	07	1824	18	0	0	0	47N19	5E02	21
4	24	04	1849	12	0	0	-1	44N12	0E38	47
5	03	01	1821	19	0	0	0	48N07	5E08	52
"""
def processVolF2(srcFilename, dstFilename):  # A format similar to A1, A2, A3
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM')
	dest = open(dstFilename, 'at')
	i = indexOfHeader+2+616+6 # an empty line after the header, then 616 Liberation Fighters, then 6 more lines
	while len(lines[i]) > 10:
		line = lines[i].split('\t')
		i+=1
		day   = line[1]
		month = line[2]
		year  = line[3]
		hour  = int(line[4]) + int(line[7])  # !!! NOTE -23 <= hour <= 47 after this !!!
		minute= line[5]
		second= line[6]
		latitude = line[8]
		longitude= line[9]
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude)
	dest.write('# End of data from Volume F2\n')
	dest.close()

processVolA(  filenames[0],                'SportsChampions_TimePlace.csv')
processVolA(  filenames[1],       'ScientistsMedicalDoctors_TimePlace.csv')
processVolA(  filenames[2],                    'MilitaryMen_TimePlace.csv')
processVolD6( filenames[3],                'SportsChampions_TimePlace.csv')
processVolD10(filenames[4], 'SP',          'SportsChampions_TimePlace.csv')
processVolD10(filenames[4], 'SC', 'ScientistsMedicalDoctors_TimePlace.csv')
processVolD10(filenames[4], 'MI',              'MilitaryMen_TimePlace.csv')
processVolE1( filenames[5], 'MI',              'MilitaryMen_TimePlace.csv')
processVolE1( filenames[5], 'PH', 'ScientistsMedicalDoctors_TimePlace.csv')
processVolF2( filenames[6],                    'MilitaryMen_TimePlace.csv')
