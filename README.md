# About
Simple crawler from specific URL.


# How to use
## Crawl
```
python main.py crawl [OPTION]
```
Options:
- *-pc, --poscat* - int, Position Category ID. Default: POSCAT_ID from utils/settings.py

## Create HTML
```
python main.py create-html [OPTION] FILENAME
```
Options:
- *-pc, --poscat* - int, Position Category ID. Default: POSCAT_ID from utils/settings.py

Arguments:
- *FILENAME* - filepath to export questions and answers in html
