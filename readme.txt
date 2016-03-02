We apply 15 classifiers implemented in the scikit-learn machine learning package
to astronomical factors derived from natal data of Professionals Notabilities from Archives Gauquelin.
We train and evaluate classifiers on pairs of professions,
sportsmen versus scientists, sportsmen vs military, scientists vs military.

Splitting into training and validation sets is always done in a stratified fashion:
training sets are built so that the yearly frequencies are equalized.
That is, for every year Y there is an equal number of
profession A and profession B notabilities 
born in this year Y that are put into a training set.
All extra notabilities are put into a validation set.
Because such splitting depends on the order of notabilities in the list,
we repeat the splitting-training-evaluation procedure a number of times,
each time with a random shuffle, and output the average accuracy across all the iterations.

Our goal is to find a classifier able to distinguish between professions (using astronomical factors only)
with an accuracy significantly higher than 0.5, and our null hypothesis is that in most of the years
the distribution of dates of birth is indistinguishable between professions,
and therefore the classification accuracy must be close to 0.5.

When we use ecliptic longitudes the mean accuracy on validation sets is not higher than 0.5026,
regardless of how we quantize the longitudes (quantization to 12 values produces the popular Zodiac signs).
When we use the features suggested by Robert Doolaard's research, namely speed in distance
quantized to only two values, and the same set of planets as in his Waves Of Wars paper,
the mean accuracy is higher than 0.54 on validation sets and higher than 0.535 on our test set,
375 Army Professionals from the unpublished volume F of Archives Gauquelin.

Because there are thousands of persons in validation sets
the 0.54 mean accuracy is a statistically highly significant result.

Sizes of groups:
2886 sports champions
4715 scientists & medical doctors
3919 military men

Sizes of training and validation sets:
1414*2  1472  3301 - sportsmen vs scientists
1374*2  1512  2545 - sportsmen vs military
3392*2  1323   527 - scientists vs military

Quadratic Discriminant Analysis classifier apparently performs best on validation sets.
Mean accuracies (across 1000 iterations) are
0.553 and 0.559 - sportsmen and scientists in the Sportsmen-vs-Scientists pair
0.402 and 0.706 - sportsmen and military
0.418 and 0.659 - scientists and military
The mean of 6 means is 0.5497 for this classifier.
It correctly classifies 2658 persons on average in the first pair:
floor(0.5530713*1472) + floor(0.5588122*3301) = 814 + 1844 = 2658

Archives Gauquelin:
http://cura.free.fr/gauq/17archg.html
Robert Doolaard's research:
http://cyclesresearchinstitute.org/pdf/cycles-history/CRI200602-Doolaard-WavesofWars.pdf
