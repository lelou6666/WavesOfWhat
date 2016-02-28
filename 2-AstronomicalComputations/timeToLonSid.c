#include <assert.h>
#include "swephexp.h" // from ftp://www.astro.com/pub/swisseph/src/swephexp.h

int planets[] = {
// This list is from swephexp.h
SE_SUN,
SE_MOON,
SE_MERCURY,
SE_VENUS,
SE_MARS,
SE_JUPITER,
SE_SATURN,
SE_URANUS,
SE_NEPTUNE,
SE_PLUTO
// what else?
};
#define NumPLANETS (sizeof(planets)/sizeof(planets[0]))
double fromSwe[6], maxabs[] = {
#include "maxAbs.h"
};

void main(int argc, char *argv[])
{
int i, ct, iflgret, iflg = SEFLG_TRUEPOS + SEFLG_SPEED + SEFLG_NOABERR + SEFLG_NOGDEFL;  // remove TRUEPOS?
char err[256], fileBuf[32768];

if (argc==1) {
	memset(maxabs, 0, sizeof(maxabs));
	double tjd_start  = swe_julday(1583,1,1,0,SE_GREG_CAL);
	double tjd_finish = swe_julday(2000,1,1,0,SE_GREG_CAL);
	for (double tjd = tjd_start; tjd < tjd_finish; tjd+=0.1) {
		for (i=0; i < NumPLANETS; ++i) {
			if ((iflgret=swe_calc_ut(tjd, planets[i], iflg, &fromSwe[0], err)) != iflg) printf("Error0: %d %x %x, %s\n",i,iflgret,iflg,err), exit(1);
			double v = fabs(fromSwe[5]);  if (v>maxabs[i])  maxabs[i]=v;
		}
	}
	for (i=0; i < NumPLANETS; ++i)  printf("%1.20f, // %d\n", maxabs[i], planets[i]);
	return;
}

FILE *fp = fopen(argv[1], BFILE_R_ACCESS);
if (fp)
for (ct = 0; ; ++ct) {
	fgets(fileBuf, sizeof(fileBuf), fp);
	if (feof(fp)) break;
	if (fileBuf[0]=='#' || strlen(fileBuf) < 5)  { --ct; continue; }
	char *p = &fileBuf[-1];
	int year = atoi(++p);  p = strchr(p, ',');  assert(p);
	int mon  = atoi(++p);  p = strchr(p, ',');  assert(p);
	int day  = atoi(++p);  p = strchr(p, ',');  assert(p);
	int hour = atoi(++p);  p = strchr(p, ',');  assert(p);
	int min  = atoi(++p);  p = strchr(p, ',');  assert(p);
	int sec  = atoi(++p);
	assert(-23<=hour && hour<=24+23 && 0<=min && min<=59 && 0<=sec && sec<=59);
	assert(year >= 1583); // Sorry, no support for Julian calendar yet
	i = 0;
	if (hour< 0)  --i, hour+=24;
	if (hour>23)  ++i, hour-=24;
	double tjd, time = hour + min / 60.0 + sec / 3600.0;
	int ret = swe_date_conversion(year, mon, day, time, 'g', &tjd);
	assert(ret==OK);
	tjd += i;
	swe_revjul(tjd, SE_GREG_CAL, &year, &mon, &day, &time);
	printf("%d",year);

	for (i=0; i < NumPLANETS; ++i) {
		if ((iflgret=swe_calc_ut(tjd, planets[i], iflg, &fromSwe[0], err)) != iflg) printf("Error1: %d %d %x %x, %s\n",ct,i,iflgret,iflg,err), exit(1);
		printf(",%2.9f", fromSwe[0]);
	}
	// Speed in distance, because Robert Doolaard's research suggests that it may be the key:
	// http://cyclesresearchinstitute.org/pdf/cycles-history/CRI200602-Doolaard-WavesofWars.pdf
	for (i=0; i < NumPLANETS; ++i) {
		if ((iflgret=swe_calc_ut(tjd, planets[i], iflg, &fromSwe[0], err)) != iflg) printf("Error2: %d %d %x %x, %s\n",ct,i,iflgret,iflg,err), exit(1);
		printf(",%2.9f", fromSwe[5] / maxabs[i]);
	}
	printf("\n");
}
}
