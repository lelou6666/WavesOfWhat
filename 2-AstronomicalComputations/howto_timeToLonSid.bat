@echo 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, >maxabs.h
@gcc -std=c99 -O3 -DUSE_DLL timeToLonSid.c swedll32.lib -o timeToLonSid.exe
@timeToLonSid.exe >maxabs.h
@gcc -std=c99 -O3 -DUSE_DLL timeToLonSid.c swedll32.lib -o timeToLonSid2.exe
@timeToLonSid2.exe          SportsChampions_TimePlace.csv          >SportsChampions_LongitudesSIDs.csv
@timeToLonSid2.exe ScientistsMedicalDoctors_TimePlace.csv >ScientistsMedicalDoctors_LongitudesSIDs.csv
@timeToLonSid2.exe              MilitaryMen_TimePlace.csv              >MilitaryMen_LongitudesSIDs.csv
@timeToLonSid2.exe             HeredityVolB_TimePlace.csv             >HeredityVolB_LongitudesSIDs.csv
