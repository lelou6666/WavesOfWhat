Run Fetch_from_cura.free.fr.py, it writes three csv files:
MilitaryMen_TimePlace.csv
ScientistsMedicalDoctors_TimePlace.csv
SportsChampions_TimePlace.csv
This is the main output.

NOTE that all html files will be overwritten!
unless you comment out the first loop in Fetch_from_cura.free.fr.py

Then you manually inspect duplicates with List_duplicates.py:

python List_duplicates.py SportsChampions_TimePlace.csv
Line 1355 = 574
python List_duplicates.py ScientistsMedicalDoctors_TimePlace.csv
Line 4331 = 1097
Line 4401 = 4387
python List_duplicates.py MilitaryMen_TimePlace.csv >mmduplicates.txt

187 lines of output in mmduplicates.txt,
it turns out all of them come from volume F2,
too many to inspect manually, so we simply remove all of them:
python Remove_duplicates.py MilitaryMen_TimePlace.csv >MilitaryMen_TimePlace_NoDuplicates.csv

Among SportsChampions and ScientistsMedicalDoctors two are false duplicates,
those are different people born on the same date at the same time.
Only one is a true duplicate: the same person in volumes A2 and E1.
We remove the second occurrence.

Also note that one person in MilitaryMan has an invalid date of birth: 1869-2-29
There was no Feb 29 in 1969, so we remove this person.

Finally, we split MilitaryMen_TimePlace_NoDuplicates.csv into two files:
Data from published volumes A3, D10, E1,
and
Data from the unpublished volume F2 where 33% of records were duplicates.
