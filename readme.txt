We apply classifiers implemented in the scikit-learn machine learning package
to astronomical factors derived from natal data of Professionals Notabilities from Archives Gauquelin.
We train classifiers on pairs of professions, sportsmen vs scientists, sportsmen vs militaries, scientists vs militaries,
and training sets are always formed so that the yearly frequencies are equalized:
for every year y there is an equal number of profession A and profession B notabilites born in this year y.
Our goal is to build a classifier able to distinguish between professions (using astronomical factors only)
with an accuracy significantly higher than 0.5, and our null hypothesis is that in most of the years
the distribution of dates of birth is indistinguishible between professions and therefore
the accuracy must be close to 0.5.
When we use ecliptical longitudes the accuracy on validation sets is very close to 0.5,
regardless of how we quantize the longitudes (quantization to 12 values produces the popular Zodiac signs).
When we use the features suggested by Robert Doolaard's research, namely speed in distance
quantized to only two values, and the same set of planets as in his Waves Of Wars paper,
the mean accuracy is higher than 0.54 on validation sets and higher than 0.535 on our test set:
Army Professionals from the unpublished volume F of Archives Gauquelin.
Because there are thousands of persons in validation sets
the 0.54 mean accuracy is a statistically highly significant result.
