import sklearn, scipy, numpy as np
from datetime import datetime
from sklearn.utils             import shuffle
from sklearn.linear_model      import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif   # As on scikit-learn.org/stable/modules/feature_selection.html
np.random.seed(0)	# You should check other seeds

filenames = [                        # We assume each file contains: year, then 20 primary features (10 ecliptic longitudes, 10 currently unused speeds in distance)
'SportsChampions_LongitudesSIDs.csv',
'ScientistsMedicalDoctors_LongitudesSIDs.csv', 
#'HeredityVolB_LongitudesSIDs.csv',             # Just two groups at a time in this version of code
]

numCelestialBodies = 10                     # TODO: dwarf planets? orbital points?
numPrimaryFeatures = numCelestialBodies*2

print str(datetime.utcnow())[0:19], "  sklearn %s  scipy %s  numpy %s" % (sklearn.__version__, scipy.__version__, np.__version__)
freqs      = []
sourceSets = []  # The n-th element is a 2d array with features of persons in filenames[n]. Rows are persons and columns are features
for filename in filenames:
	file = open(filename, 'rt')
	fromFile = []
	freq = np.zeros(2018)
	for line in file:
		line = line.split(',')
		assert len(line) == numPrimaryFeatures+1    #  +1 because the first item is year
		year = int(line[0])
		features = [ year ]
		freq[year] += 1

		for i in range(numCelestialBodies):  # Ecliptic longitudes of Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
			features.append( float(line[i+1]) )     #  +1 because the first item is year

		for i in range(7):  # Major aspects, as on en.wikipedia.org/w/index.php?title=Astrological_aspect&oldid=709116104#Major_aspects
			count1 = count3 = count4 = count6 = 0
			for k in range(7):
				a = (features[k+1] - features[i+1] + 360) % 360    # TODO: Declinations? True angles in 3D space instead of ecliptic longitudes?
				if   abs(a-180) <= 8 or abs(a-180) >= 172:  count1 += 1   # TODO: summarize more, so that only 3 or 2 are left?
				elif abs(a-120) <= 6 or abs(a-240) <= 6:    count3 += 1
				elif abs(a- 90) <= 6 or abs(a-270) <= 6:    count4 += 1
				elif abs(a- 60) <= 4 or abs(a-300) <= 4:    count6 += 1   # TODO: minor aspects?
			features.append(count1*0.75)  # because the total width is 32 degrees
			features.append(count3)       #         the total width is 24 degrees
			features.append(count4)       #         the total width is 24 degrees
			features.append(count6*1.5)   # because the total width is 16 degrees

		for i in range(numCelestialBodies):  # TODO: output tells us that features 6,7,8,9 (Saturn...Pluto) are never used. Should we rescale them differently?
			features[i+1] /= 180     # Recale to [0, 2], approximately the same range as the aspect counts, they are rarely > 2

		fromFile.append(features)

	sourceSets.append(fromFile)
	freqs.append(freq)
numFeatures = len(sourceSets[0][0]) - 1  # Minus one because the first item is year

def splitIntoTrainingAndValidation(A, B):
	data1 = shuffle(sourceSets[A])    # Note this is a random shuffle, that's
	data2 = shuffle(sourceSets[B])    #                                   why we need many iterations
	freqM = np.minimum(freqs[A], freqs[B])
	freq1tr = np.round(freqM * 0.8)        # Randomly selected 80% for the training set,
	freq1va = freqM - freq1tr              # and the remaining 20% for the validation set
	freq2tr = np.copy(freq1tr)
	freq2va = np.copy(freq1va)
	trainsetSize = int(sum(freq1tr))
	valdnsetSize = int(sum(freq1va))
	testSet1size = len(data1) - trainsetSize - valdnsetSize
	testSet2size = len(data2) - trainsetSize - valdnsetSize
	X  = np.zeros((trainsetSize*2,            numFeatures))
	Xv = np.zeros((valdnsetSize*2,            numFeatures))
	Xt = np.zeros((testSet1size+testSet2size, numFeatures))
	y  = np.ravel([([0]*trainsetSize) + ([1]*trainsetSize)])
	yv = np.ravel([([0]*valdnsetSize) + ([1]*valdnsetSize)])
	yt = np.ravel([([0]*testSet1size) + ([1]*testSet2size)])
	trnIdx = vldIdx = tstIdx = 0
	for item in data1:
		year = item[0]
		if   freq1tr[year] > 0:   X[trnIdx], trnIdx, freq1tr[year]  =  item[1:],  trnIdx+1,  freq1tr[year]-1
		elif freq1va[year] > 0:  Xv[vldIdx], vldIdx, freq1va[year]  =  item[1:],  vldIdx+1,  freq1va[year]-1
		else:                    Xt[tstIdx], tstIdx                 =  item[1:],  tstIdx+1
	assert trnIdx==trainsetSize   and vldIdx==valdnsetSize   and tstIdx==testSet1size
	for item in data2:
		year = item[0]
		if   freq2tr[year] > 0:   X[trnIdx], trnIdx, freq2tr[year]  =  item[1:],  trnIdx+1,  freq2tr[year]-1
		elif freq2va[year] > 0:  Xv[vldIdx], vldIdx, freq2va[year]  =  item[1:],  vldIdx+1,  freq2va[year]-1
		else:                    Xt[tstIdx], tstIdx                 =  item[1:],  tstIdx+1
	assert trnIdx==trainsetSize*2 and vldIdx==valdnsetSize*2 and tstIdx==testSet1size+testSet2size
	X, y = shuffle(X, y)   # Just in case... perhaps no reason to shuffle again here?
	fs = SelectKBest(f_classif, k = numFeatures)   # TODO: try other feature selection methods?
	fs.fit(np.concatenate((X, Xv)), np.concatenate((y, yv)))
	return X, y, Xv, yv, Xt, yt, testSet1size, testSet2size, fs.scores_

classifier = LogisticRegression()
sumTestingSetAccuracy = sum1 = sum2 = 0

for ni in range(1, 10**6+1):  # Everything below will be executed a million times!
	X, y, Xv, yv, Xt, yt, testSet1size, testSet2size, featureScores = splitIntoTrainingAndValidation(0, 1)
	if ni==1:  print "Sizes of sets: ", X.shape[0], Xv.shape[0], testSet1size, testSet2size, " in training set, validation set, two test sets"
	bestFeatureSet = []

	# >>> Validation <<<   As of now, bestFeatureSet is the only output of validation phase. We could also pick a classifier here.
	candidateFeatures = np.asarray(sorted(zip(featureScores, range(len(featureScores)))))[:,1]
	X_training = X[ :, candidateFeatures[-1]].reshape(-1,1)  # X  with only a subset of features
	X_validatn = Xv[:, candidateFeatures[-1]].reshape(-1,1)  # Xv with only a subset of features
	bestValidationAccuracy = -1.0
	for numFeaturesSelected in range(2, 21):  # Up to 20 features
		featureIndex = candidateFeatures[-numFeaturesSelected]
		X_training = np.hstack((X_training, X[ :, featureIndex].reshape(-1,1)))
		X_validatn = np.hstack((X_validatn, Xv[:, featureIndex].reshape(-1,1)))
		if numFeaturesSelected>2:
			classifier.fit(X_training, y)
			trainingAccuracy   = classifier.score(X_training, y)
			validationAccuracy = classifier.score(X_validatn, yv)
			if trainingAccuracy > 0.5 and validationAccuracy > bestValidationAccuracy:
				bestValidationAccuracy = validationAccuracy
				bestFeatureSet = list(reversed(np.int32(candidateFeatures[-numFeaturesSelected:])))
			if numFeaturesSelected >= len(bestFeatureSet) + 3:  break  # Stop if the last 3 features were not helpful
			bestValidationAccuracy += 0.0001  # A small penalty for increasing the model complexity
	if bestFeatureSet==[]:  bestFeatureSet = list(reversed(np.int32(candidateFeatures[-3:])))     # Or assert bestFeatureSet!=[] ? Never happens?
	# TODO: exclude one feature from bestFeatureSet if this improves bestValidationAccuracy. Then maybe another one... while bVA improves.
			
	# >>> Testing <<<   Build training and testing sets with the selected subset of features. Train classifier. Report accuracy on the testing sets.
	X, y = np.concatenate((X, Xv)), np.concatenate((y, yv))
	for  feature in bestFeatureSet:
		if feature==bestFeatureSet[0]:
			X_training = X[ :, feature].reshape(-1,1)  # X  with only a subset of features
			X_testing  = Xt[:, feature].reshape(-1,1)  # Xt with only a subset of features
		else:
			X_training = np.hstack((X_training, X[ :, feature].reshape(-1,1)))
			X_testing  = np.hstack((X_testing , Xt[:, feature].reshape(-1,1)))
	X_training, y = shuffle(X_training, y)   # Just in case... perhaps no reason to shuffle again here?
	classifier.fit(X_training, y)
	accuracy1 = classifier.score(X_testing[:testSet1size], yt[:testSet1size])  # Test Set 1
	accuracy2 = classifier.score(X_testing[testSet1size:], yt[testSet1size:])  # Test Set 2
	testingSetAccuracy = (accuracy1 + accuracy2)/2
	sum1 += accuracy1
	sum2 += accuracy2
	sumTestingSetAccuracy += testingSetAccuracy
	print "%4d iterations: the average testingSetAccuracy is %1.7f = (%1.7f+%1.7f)/2 " % (ni, sumTestingSetAccuracy/ni, sum1/ni, sum2/ni),
	print "This time it's %1.7f = (%1.7f+%1.7f)/2, %d features:" % (testingSetAccuracy, accuracy1, accuracy2, len(bestFeatureSet)), bestFeatureSet
