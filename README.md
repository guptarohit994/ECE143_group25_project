# ECE143_group25_project
 FA19 course final project

# Data Crawling

## UCOP
```
cd crawling_and_parsing
python ucop_crawler.py -h
```
Sample output (downcounts to 0) -
```
year:2018, location:Berkeley, headless:True, geckodriver_path:./geckodriver, output_dir:../data/csv/ucop/
=========================================================================================
Firefox Initialized in headless mode
Need to go through 589 more pages!!!
=========================================================================================
```
Usage - 
```
usage: ucop_crawler.py [-h] [--location [LOCATION]] [--year [YEAR]]
                       [--headless [HEADLESS]]
                       [--geckodriver_path [GECKODRIVER_PATH]]
                       [--output_dir [OUTPUT_DIR]]

Crawls information from UCOP Annual Wages webpage

optional arguments:
  -h, --help            show this help message and exit
  --location [LOCATION]
                        location whose wages to crawl, default:'San Diego'
  --year [YEAR]         year for which data to crawl, default:2018
  --headless [HEADLESS]
                        mode in which to launch browser, default:True
  --geckodriver_path [GECKODRIVER_PATH]
                        path to the geckodriver executable,
                        default:'./geckodriver'
  --output_dir [OUTPUT_DIR]
                        dir where to place the generated csv,
                        default:'../data/csv/ucop/'
```
