import itertools, numpy as np
from datetime import datetime
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble     import *
np.random.seed(0)   # You should try other seeds

filenames  = ['SportsChampions_LongitudesSIDs.csv', 'ScientistsMedicalDoctors_LongitudesSIDs.csv', 'MilitaryMen_LongitudesSIDs.csv', 'ArmyProfessionals_LongitudesSIDs.csv']
#  From volumes:   A1, D6, D10                           A2, D10, E1                                    A3, D10, E1                   F2   This file is used as a testing set
sourceSets = [[]]*len(filenames)
freqs      = [[]]*len(filenames)
numSets    =      len(filenames)-1
numIterations = 1000  # If 1000 then full runtime is about 23 hours on a typical desktop with Intel Core i7 CPU. Full run is the run with all three 'if 1' below
#numIterations = 500  # 1000+ is OK, please use smaller values for "a quick check" only, to see whether scikit-learn and related packages produce the same output on your system

def buildLongitudeFeatures(mode):
    for n in range(numSets):
	file = open(filenames[n], 'rt')
	fromFile = [line.split(',') for line in file]
	freq = np.zeros(2018)
	for i in range(len(fromFile)):
		if (mode&1): line = list(itertools.chain.from_iterable([[0], fromFile[i][6:11]]))  # As in Robert Doolaard's research, only Jupiter, Saturn, Uranus, Neptune, Pluto
		else:        line = list(itertools.chain.from_iterable([[0], fromFile[i][1:11]]))  # All of them: Sun, Moon and 8 planets
		line[0] = int(fromFile[i][0])
		freq[line[0]] += 1
		for j in range(1, len(line)):
			if   mode<2:  line[j] =      float(line[j])
			elif mode<4:  line[j] = int( float(line[j])/30 )     # Quantize to 12 values
			elif mode<6:  line[j] = int( float(line[j])/90 )     # Quantize to  4 values
			elif mode<8:  line[j] = int( float(line[j])/180)     # Quantize to  2 values
			elif mode<10: line[j] = int( float(line[j])/30 ) % 3 # Quantize to 12 values, then mod 3
			else:         line[j] = int( float(line[j])/30 ) % 4 # Quantize to 12 values, then mod 4
		fromFile[i] = line
	sourceSets[n] = fromFile
	freqs[n] = freq

def buildSIDfeatures(mode):
    for n in range(numSets):
	file = open(filenames[n], 'rt')
	fromFile = [line.split(',') for line in file]
	freq = np.zeros(2018)
	for i in range(len(fromFile)):
		if (mode&1): line = list(itertools.chain.from_iterable([[0], fromFile[i][16:21]]))  # As in Robert Doolaard's research, only Jupiter, Saturn, Uranus, Neptune, Pluto
		else:        line = list(itertools.chain.from_iterable([[0], fromFile[i][11:21]]))  # All of them: Sun, Moon and 8 planets
		line[0] = int(fromFile[i][0])
		freq[line[0]] += 1
		for j in range(1, len(line)):
			v = float(line[j])
			if   mode<2: line[j] = v
			elif mode<4: line[j] = (1 if v>0 else -1) + int(v*2)  # Quantize to 4 values
			else:        line[j] = (1 if v>0 else -1)             # Quantize to 2 values
		fromFile[i] = line
	sourceSets[n] = fromFile
	freqs[n] = freq

def splitIntoTrainingAndValidation(A,B):
	freq1 = np.minimum(freqs[A], freqs[B])
	freq2 = np.copy(freq1)
	data1 = shuffle(sourceSets[A])    # Note this is a random shuffle, that's
	data2 = shuffle(sourceSets[B])    #                                   why we need numIterations>=100
	numFeatures  = len(data1[0]) - 1  # Minus one because the first item is year
	trainsetSize = int(sum(freq1))
	valiSet1size = int(len(data1) - trainsetSize)
	valiSet2size = int(len(data2) - trainsetSize)
	X  = np.zeros((trainsetSize*2, numFeatures))
	Xv1= np.zeros((valiSet1size,   numFeatures))
	Xv2= np.zeros((valiSet2size,   numFeatures))
	y  = np.zeros(trainsetSize*2)
	y[0:trainsetSize] = 1
	#print trainsetSize, valiSet1size, valiSet2size,
	assert len(data1)==trainsetSize+valiSet1size and len(data2)==trainsetSize+valiSet2size
	trnIdx = vldIdx = 0
	for item in data1:
		year = item[0]
		if freq1[year] > 0:
			freq1[year] -= 1
			X[trnIdx] = item[1:]
			trnIdx += 1
		else:
			Xv1[vldIdx] = item[1:]
			vldIdx += 1
	assert trnIdx==trainsetSize and vldIdx==valiSet1size
	vldIdx = 0
	for item in data2:
		year = item[0]
		if freq2[year] > 0:
			freq2[year] -= 1
			X[trnIdx] = item[1:]
			trnIdx += 1
		else:
			Xv2[vldIdx] = item[1:]
			vldIdx += 1
	assert trnIdx==trainsetSize*2 and vldIdx==valiSet2size
	X, y = shuffle(X, y)  # Just in case; perhaps no reason to shuffle here
	return X, y, Xv1, Xv2, valiSet1size, valiSet2size   # Xv1 has label 1, Xv2 has label 0

def validationMain(mode,clf):
	sum1 = sum2 = sum3 = sum4 = sum5 = sum6 = failures = 0
	for i in range(numIterations):
		for a in range(numSets):
			for b in range(a+1, numSets):
				X, y, Xv1, Xv2, valiSet1size, valiSet2size = splitIntoTrainingAndValidation(a,b)
				clf.fit(X, y)
				accuracy1 = clf.score(Xv1,  np.ones(valiSet1size))
				accuracy2 = clf.score(Xv2, np.zeros(valiSet2size))
				if accuracy1<=0.5: failures += 1
				if accuracy2<=0.5: failures += 1
				if a==0 and b==1:  sum1,sum2 = sum1 + accuracy1, sum2 + accuracy2
				if a==0 and b==2:  sum3,sum4 = sum3 + accuracy1, sum4 + accuracy2
				if a==1 and b==2:  sum5,sum6 = sum5 + accuracy1, sum6 + accuracy2
	print '%1.7f' % (sum1/numIterations), '%1.7f' % (sum2/numIterations),
	print '%1.7f' % (sum3/numIterations), '%1.7f' % (sum4/numIterations),
	print '%1.7f' % (sum5/numIterations), '%1.7f' % (sum6/numIterations), '%4d' % failures,
	grandMean = (sum1+sum2+sum3+sum4+sum5+sum6)/(numIterations*6)
	print ' Mean of 6 means: %1.7f' % grandMean, '%c' % ('!' if grandMean>bangThreshold else ' '), 'Mode', mode, datetime.utcnow()

def testingMain(mode,swapLabels,clf):
	sum1 = sum2 = sum3 = sum4 = sum5 = sum6 = failures = 0
	for i in range(numIterations):
		for a in range(2):
				if swapLabels:
					X, y, Xv1, Xv2, valiSet1size, valiSet2size = splitIntoTrainingAndValidation(2, a)  # here b=2
				else:
					X, y, Xv1, Xv2, valiSet1size, valiSet2size = splitIntoTrainingAndValidation(a, 2)  # here b=2
				clf.fit(X, y)
				data3 = shuffle(sourceSets[3])   # Perhaps no reason to shuffle?
				numFeatures = len(data3[0]) - 1  # Minus one because the first item is year
				testsetSize = len(data3)
				Xtest= np.zeros((testsetSize, numFeatures))
				for n in range(testsetSize):
					Xtest[n] = data3[n][1:]
				accuracy1 = clf.score(Xv1,   np.ones(valiSet1size))
				accuracy2 = clf.score(Xv2,  np.zeros(valiSet2size))
				if swapLabels:
					accuracy3 = clf.score(Xtest, np.ones(testsetSize)) # Same label as the validation set with same profession
				else:
					accuracy3 = clf.score(Xtest,np.zeros(testsetSize)) # Same label as the validation set with same profession
				if accuracy3<=0.5: failures += 1
				if a==0:  sum1,sum2,sum5 = sum1 + accuracy1, sum2 + accuracy2, sum5 + accuracy3
				if a==1:  sum3,sum4,sum6 = sum3 + accuracy1, sum4 + accuracy2, sum6 + accuracy3
	print '%1.7f' % (sum1/numIterations), '%1.7f' % (sum2/numIterations),
	print '%1.7f' % (sum3/numIterations), '%1.7f' % (sum4/numIterations), ' ',
	print '%1.7f' % (sum5/numIterations), '%1.7f' % (sum6/numIterations), '%4d' % failures,
	grandMean = (sum5+sum6)/(numIterations*2)
	print ' Mean of 2 means: %1.7f' % grandMean, '%c' % ('!' if grandMean>bangThreshold else ' '), 'Mode', mode, datetime.utcnow()

if 1:	#  'if 0'  when you want to skip this step
	print 'Ecliptic longitudes:'
	bangThreshold = 0.51
	modes = range(12)
	for mode in modes:
		buildLongitudeFeatures(mode)
		validationMain(mode, LogisticRegression(penalty='l1'))
		validationMain(mode, LogisticRegression(penalty='l2'))
		validationMain(mode, RandomForestClassifier())
	print 'SIDs:'
	modes = range(6)
	for mode in modes:
		buildSIDfeatures(mode)
		validationMain(mode, LogisticRegression(penalty='l1'))
		validationMain(mode, LogisticRegression(penalty='l2'))
		validationMain(mode, RandomForestClassifier())
	# After this step we only use SID features, and pick the only mode providing grandMean accuracy > 54%

from sklearn.svm          import SVC
from sklearn.tree         import DecisionTreeClassifier
from sklearn.tree         import    ExtraTreeClassifier
from sklearn.neighbors    import   KNeighborsClassifier
from sklearn.neighbors    import NearestCentroid
from sklearn.naive_bayes  import GaussianNB
from sklearn.discriminant_analysis import    LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

if 1:	#  'if 0'  when you want to skip this step
	print 'Other classifiers:'
	bangThreshold = 0.5405
	mode = 5
	buildSIDfeatures(mode)
	validationMain(mode+0.01, AdaBoostClassifier())
	validationMain(mode+0.02, BaggingClassifier(KNeighborsClassifier()))  # as on http://scikit-learn.org/stable/modules/ensemble.html
	validationMain(mode+0.03, DecisionTreeClassifier())
	validationMain(mode+0.04,    ExtraTreeClassifier())
	validationMain(mode+0.05,   ExtraTreesClassifier())
	validationMain(mode+0.06, GaussianNB())
	validationMain(mode+0.07, GradientBoostingClassifier())
	validationMain(mode+0.08, KNeighborsClassifier())
	validationMain(mode+0.09, LinearDiscriminantAnalysis())
	validationMain(mode+0.10, LogisticRegression(penalty='l1'))
	validationMain(mode+0.11, LogisticRegression(penalty='l2'))
	validationMain(mode+0.12, NearestCentroid())
	validationMain(mode+0.13, QuadraticDiscriminantAnalysis())
	validationMain(mode+0.14, RandomForestClassifier())
	validationMain(mode+0.15, SVC())   # !!! Is very slow !!!
	# After this step we pick the top 5 classifiers (with best grandMean accuracy)

if 1:	#  'if 0'  when you want to skip this step
	print 'Testing set:'
	numSets = len(filenames)  # Needed for testing, because our testing set is in the last file
	bangThreshold = 0.51
	mode = 5
	buildSIDfeatures(mode)
	testingMain(mode+0.03, False, DecisionTreeClassifier())
	testingMain(mode+0.04, False,    ExtraTreeClassifier())
	testingMain(mode+0.05, False,   ExtraTreesClassifier())
	testingMain(mode+0.13, False, QuadraticDiscriminantAnalysis())
	testingMain(mode+0.15, False, SVC())   # !!! Is very slow !!!
	print 'Now lets try swapping labels:'
	testingMain(mode+0.13, True,  QuadraticDiscriminantAnalysis())
