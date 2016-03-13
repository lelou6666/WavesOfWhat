Run Fetch_from_cura.free.fr.py
It writes three csv files:

 MilitaryMen_TimePlace.csv

 ScientistsMedicalDoctors_TimePlace.csv

 SportsChampions_TimePlace.csv

This is the main output.
Each line contains: year,month,day,hour,minute,second,latitude,longitude

Note that here we process time zones very simply,
and  -24 < hour < 48 in the output.
So the astronomy calculations module must take care of this.

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
Only one is a true duplicate, the same person in volumes A2 and E1.
We comment out the second occurrence:
# 1912,08,29,1,00,0,-,-

187 lines of output in mmDuplicates.txt,
it turns out all of them come from volume F2.
Then it turns out almost every Army Professional from F2 has a *twin*
in one of the earlier volumes:
> python List_twins.py MilitaryMen_TimePlace.csv >mmTwins.txt
We remove all of them, and don't use F2.

Note one person in MilitaryMen has an invalid date of birth: 1869-2-29
There was no Feb 29 in 1969, this person was commented out by Fetch_from_cura.free.fr.py

Finally, we split three *_TimePlace.csv files into trn_* and tst_*
as shown at the end of Fetch_from_cura.free.fr.py
