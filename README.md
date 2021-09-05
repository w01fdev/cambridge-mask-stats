# Cambridge Mask Stats
**Application to output the wearing time and other statistics of a Cambridge 
N99 | FFP2 mask.**

the program is in the alpha phase. this means that the api 
will probably change often. the code is written in such a way that the syntax 
in the console is maintained or at least only minimal changes are made. this 
description also only deals with the terminal. the api will be described 
in the documentation of the code, if this is necessary. it is tried to write 
the code in a way that it is easy to understand.

the application is intended exclusively for the pro version of the cambridge 
mask, which should be worn for a maximum of 340 hours. the minutes are 
calculated automatically for aqi_level higher than 2, so that the wear is 
displayed correctly.

if there is no entry in the csv for a day between the start and end date, the 
time carried is automatically set to 0 for that day. this means that for months 
that lie between the start and end month *count_d* also counts the days for 
which the mask was not worn or for which there is no entry in the csv file.

when predicting the end of life of a mask, the average value in minutes for the 
number of days (standard: 30) passed in the argument *days* for the calculation. 
if there is no value for one of these days, the value for this day is 
calculated as 0. the mean value is calculated from all masks worn, not per mask.

**only 1 mask per day can be recorded! Otherwise there is a *ValueError*.**

## requirements
### python version
`Python >= 3.6`

### dependencies
```text
numpy==1.21.2
pandas==1.3.2
python-dateutil==2.8.2
pytz==2021.1
six==1.16.0
```

## pip installation (with dependencies)
```shell
pip install cambridge-mask-stats
```

## csv file
### the CSV file to import needs the following header:
`date,id,model,aqi_level,minutes_worn`

* date -> format yyyy-mm-dd
* id -> mask id. preferably consecutive numbering
* model -> mask model like 'The Churchill Pro'
* aqi_level -> from 1-5 according to the data in the manual (1 = aqi below 50, 2 = 50 - 100 ...)
* minutes_worn -> minutes worn on this date

## execute
```shell
mask-stats <FILEPATH>
```

## abbreviations in the output
* count_d -> days in the month for which data are available
* eol_d -> prediction in how many days the mask will probably reach its end of life
* eol_date -> prediction on which date the mask will probably reach the end of life
* hrs -> hours (really worn)
* mean_min_d -> mean minutes daily  
* pct -> percent | percentage (determined from sum_min_ratio)
* sum_hrs -> summary hours 
* sum_min -> summary minutes
* *_ratio -> values under consideration of the ratio (aqi_level > 2)

#### usage
```shell
usage: cambridge_mask_stats.py [-h] [--days DAYS] file

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  --days DAYS, -d DAYS  days to be used in the end of life prediction. enter 0 for all [default: 30]
```

#### examples
```shell
masks-stats /home/w01fdev/Documents/masks.csv
```

#### output
```text
******************* StatsMasks *******************
worn | wear           hrs  hrs_ratio   pct  eol_d    eol_date
id model                                                     
1  The Admiral Pro     10         12  3.53    335  2022-08-06
2  The Churchill Pro   15         27  7.94    319  2022-07-21

***************** StatsDateRange *****************
worn | wear  count_d  mean_min_d  mean_min_d_ratio  sum_min  sum_min_ratio  sum_hrs  sum_hrs_ratio   pct
2020-08-31         1          58                58       58             58        0              0  0.28
2020-09-30        30           9                18      278            563        4              9  2.76
2020-10-31        31          39                56     1237           1759       20             29  8.62
```

## list of possible extensions
- output of plots
- days worn for each mask
- percentage change in wearing time compared to last month