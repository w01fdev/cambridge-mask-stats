# Cambridge Masks Stats
Program to output the wearing time and other statistics of a Cambridge 
N99 | FFP2 mask .the project is currently in the alpha phase. here only the 
execution in the terminal is dealt with.

## requirements
### python version
`Python >= 3.5`

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

#### example
```shell
masks-stats /home/w01fdev/Documents/masks.csv
```

output:
```shell
[TOTAL WORN TIME]
ID MASK                      HOURS
 1 The Admiral Pro           3
 2 The Churchill Pro         142
```