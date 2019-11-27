# ECE143_group25_project
 FA19 course final project
 
 ## Table of Contents
  * [Data Crawling](#data-crawling)
  * [Third Party Modules](#third-party-modules)

## Data Crawling

### UCOP
```
cd crawling_and_parsing
python ucop_crawler.py --location='Berkeley'
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

### CAPE

CAPE database is locked behind a *Single-Sign On (SSO)*. So, this crawler requires SSO username and password to be inserted in `./crawling_and_parsing/ucsd_triton_sso.py` to initiate a login request and **DUO push needs to be accepted** for a successful login

```
cd crawling_and_parsing
python cape_crawler.py
```
Sample output (eg. for CSE department, we want to do a quick crawl and place generated csv in `test` dir) -

`python cape_crawler.py --output_dir test/ --department 'CSE'`
```
department:CSE, detailed:False, headless:True, geckodriver_path:./geckodriver, output_dir:test/
=========================================================================================
Firefox Initialized in headless mode
*********** Initiating a SSO login ***********
*********** Successfully logged in ***********

Successfully parsed departments(1/1),        CSE results(2087 courses)        
=========================================================================================
```
Usage - 
```
usage: cape_crawler.py [-h] [--department DEPARTMENT] [--detailed DETAILED]
                       [--headless HEADLESS]
                       [--geckodriver_path [GECKODRIVER_PATH]]
                       [--output_dir [OUTPUT_DIR]]

Crawls information for all courses in various departments on CAPE webpage

optional arguments:
  -h, --help            show this help message and exit
  --department DEPARTMENT
                        specific department whose data to crawl. Either 1 or
                        all, default:'all'
  --detailed DETAILED   form of data scraping. Detailed are much slower.
                        default:'False'
  --headless HEADLESS   mode in which to launch browser, default:'True'
  --geckodriver_path [GECKODRIVER_PATH]
                        path to the geckodriver executable,
                        default:'./geckodriver'
  --output_dir [OUTPUT_DIR]
                        dir where to place the generated csv,
                        default:'../data/csv/cape/'
```
## Third Party Modules

The third party modules we used were:
* Numpy
* Pandas
* Matplotlib
* Scipy
