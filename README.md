# Cambridge Masks Stats
**Program to output the wearing time and other statistics of a Cambridge 
N99 | FFP2 mask.**

the program is in the alpha phase. this means that the api 
will probably change often. when running it in the terminal, care is taken to 
maintain the syntax if possible. this description also only deals with the terminal. the api will be described 
in the documentation of the code, if this is necessary. it is tried to write 
the code in a way that it is easy to understand.

## requirements
### python version
`Python >= 3.6`

### dependencies
```text
numpy==1.21.1
pandas==1.3.1
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
* hrs -> hours
* mean_min_d -> mean minutes daily  
* pct -> percent | percentage
* sum_hrs -> summary hours 
* sum_min -> summary minutes

#### example
```shell
masks-stats /home/w01fdev/Documents/masks.csv
```

#### output
```text
******************* StatsMasks *******************
worn | wear           hrs    pct
id model                        
1  The Admiral Pro     73  21.47
2  The Churchill Pro  235  69.12

***************** StatsDateRange *****************
worn | wear  count_d  mean_min_d  sum_min  sum_hrs    pct
2020-08-31         1          58       58        0   0.28
2020-09-30        30           9      278        4   1.36
2020-10-31        31          39     1237       20   6.06
2020-11-30        30         107     3235       53  15.86
2020-12-31        31          62     1940       32   9.51
2021-01-31        31          49     1520       25   7.45
2021-02-28        28          52     1478       24   7.25
2021-03-31        31          52     1618       26   7.93
```
