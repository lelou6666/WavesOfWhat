Run Fetch_from_cura.free.fr.py, it writes three csv files:
MilitaryMen_TimePlace.csv
ScientistsMedicalDoctors_TimePlace.csv
SportsChampions_TimePlace.csv
This is the main output.
Each line contains: year,month,day,hour,minute,second,latitude,longitude

(Note that here we process time zones very simply,
  and  -24 < hour < 48 in the output.
  So the astronomy calculations module must take care of this.)

NOTE that all html files will be overwritten! unless you
comment out the first loop in Fetch_from_cura.free.fr.py

You should then inspect duplicates using List_duplicates.py:

> python List_duplicates.py SportsChampions_TimePlace.csv
> Line 1355 = 574
> python List_duplicates.py ScientistsMedicalDoctors_TimePlace.csv
> Line 4331 = 1097
> Line 4401 = 4387
> python List_duplicates.py MilitaryMen_TimePlace.csv >mmDuplicates.txt

Among SportsChampions and ScientistsMedicalDoctors two are false duplicates,
those are different people born on the same date at the same time.
Only one is a true duplicate: the same person in volumes A2 and E1.
We remove the second occurrence.

187 lines of output in mmDuplicates.txt,
it turns out all of them come from volume F2,
too many to inspect manually, and there are no names in volume F2,
so we simply remove all of them:

python Remove_duplicates.py MilitaryMen_TimePlace.csv >MilitaryMen_TimePlace_NoDuplicates.csv

Note one person in MilitaryMen has an invalid date of birth: 1869-2-29
There was no Feb 29 in 1969, this person was commented out by Fetch_from_cura.free.fr.py

Finally, we split MilitaryMen_TimePlace_NoDuplicates.csv into two files:
data from published volumes A3, D10, E1,
and
data from the unpublished volume F2 where 33% of records were duplicates.
