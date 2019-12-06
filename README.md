# Analysis of Education & Compensation at UC Schools
ECE143 FA19 Group 25 Term Project
 
 ## Table of Contents
  * [Directory Structure](#directory-structure)
  * [Data Crawling](#data-crawling)
  * [Third Party Modules](#third-party-modules)

## Directory Structure

  * crawling_and_parsing
      * Contains all parsers and crawlers
      * `geckodriver`
  * data
      * Contains data crawled from CAPE, UCOP
      * Also contains merged dataset that we created
  * statistical_analysis
      * Contains modules and notebooks used for analysizing `data`
      * `Graphs.ipynb` shows the figures that made it to the presentation
  * `ECE_143_Group_25_Presentation.pdf` 
      * The final set of slides
      * Also contains some backup slides which were hard to let go :(

## Data Crawling

### UCOP
```
cd crawling_and_parsing
python ucop_crawler.py --output_dir . --location='Berkeley'
```
Sample output (downcounts to 0) -
```
year:2018, location:Berkeley, headless:True, geckodriver_path:./geckodriver, output_dir:.
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

`python cape_crawler.py --output_dir . --department 'CSE'`
```
department:CSE, detailed:False, headless:True, geckodriver_path:./geckodriver, output_dir:.
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

The third party modules we used are mentioned in `requirements.txt`. To install these Python dependencies and modules - 

```
pip install -r requirements.txt
```

**Although `geckodriver` is present in this repository, it also needs [Firefox Quantum (v63.0+)](https://www.mozilla.org/en-US/firefox/ "Mozilla Homepage") to work with which should be manually installed.**
