We apply algorithms implemented in the scikit-learn machine learning package
to astronomical factors derived from natal data of persons from Archives Gauquelin.
We train and evaluate classifiers on pairs of groups:
sportsmen versus scientists,
sportsmen  vs Hereditary Experiment subjects from Series B,
scientists vs Hereditary Experiment subjects from Series B.

Splitting into training, validation and testing sets is always done in a stratified fashion:
balanced sets are built so that the yearly frequencies are equalized.
That is, for every year Y there is an equal number of group 1 and group 2 subjects born
in this year Y that are put into a balanced set:  minimum(number of group1 born in Y, group2 born in Y).
All extra subjects are put into a testing set.

Because such splitting depends on the order of subjects in the list,
we repeat the splitting-training-evaluation procedure a number of times,
each time with a random shuffle, and output the average accuracy across all the iterations.

Each balanced set is then further split into a training and a validation set, 80% / 20%
such that both of the two are again balanced.
Validation sets are used to select features,
the only classifier we apply is LogisticRegression() with all the default parameters.

Our goal is to find a method able to distinguish between groups (using astronomical factors only)
with an accuracy significantly higher than 0.5, and our null hypothesis is that in most of the years
the distribution of times of birth is indistinguishable between groups,
and therefore the classification accuracy must be close to 0.5.

In the Sportsmen-vs-Scientists pair the mean accuracy is higher than 52.59% on testing sets,
in the Sportsmen-vs-H.E.subjects pair it is higher than 53%,
and because there are more than 22 thousand persons in testing sets
the 0.53 mean accuracy is a statistically highly significant result.
Please see files Output*.txt for more details.

Sizes of groups:
 2886 sports champions from all volumes, namely A1, D6, D10
 4715 scientists & medical doctors from all volumes, namely A2, D10, E1
24940 Hereditary Experiment subjects from volume B

Sizes of training, validation and testing sets:
2264 training,  564 validation, test sets: 1472 and  3301 - sportsmen vs scientists
4290 training, 1074 validation, test sets:  204 and 22258 - sportsmen vs H.E. subjects
5478 training, 1364 validation, test sets: 1294 and 21519 - scientists vs H.E. subjects

Archives Gauquelin: http://cura.free.fr/gauq/17archg.html
