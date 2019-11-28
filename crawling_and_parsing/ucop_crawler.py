from argparse import ArgumentParser
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from ucop_webpage_parser import get_parsed_rows_ucop
import csv
from sys import stdout
from os import path


def do_ucop_crawl(location='San Diego', year=2018, headless=True, geckodriver_path='./geckodriver', output_dir="."):
    '''
    function to crawl the search results from the UCOP Salary webpage

    :param location: which location to use. default:'San Diego'
    :type location: str
    :param year: year for which wages need to be gathered. default:2018
    :type year: int
    :param headless: mode in which to launch browser, default:True
    :type headless: bool
    :param geckodriver_path: path to the geckodriver executable, default:'./geckodriver'
    :type geckodriver_path: str
    :param output_dir: dir where to place the generated csv, default:'../data/csv/ucop/''
    :type output_dir: str
    '''
    assert isinstance(location,str), "location should be a string"
    # would get stricter later
    assert isinstance(year,int) and 0 <= year <= 2019, "year should be a int"
    assert isinstance(headless,bool), "headless should be a bool"
    assert isinstance(geckodriver_path,str) and path.exists(geckodriver_path), f"geckodriver does not exist at {geckodriver_path}"
    assert isinstance(output_dir,str) and path.isdir(output_dir), f"Not a valid directory:{output_dir}"

    options = Options()
    options.headless = headless

    driver = Firefox(options=options, executable_path=geckodriver_path)
    driver.get("https://ucannualwage.ucop.edu/wage/")
    
    print ('Firefox Initialized in %s mode'%('headless' if headless else 'head'))

    # it is critical to load year first because when you select year, location gets reset
    # select year
    #['2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
    select = Select(driver.find_element_by_id('year'))
    options_years = [o.text for o in select.options]

    assert str(year) in options_years, f"year can be {options_years}"
    select.select_by_visible_text(str(year))

    # select location
    select = Select(driver.find_element_by_id('location'))
    options_locations = [o.text for o in select.options]

    if 'Select a Location' in options_locations:
        options_locations.remove('Select a Location')

    assert location in options_locations, f"location can be {options_locations} for year {year}"
    select.select_by_visible_text(location)

    # select 60 results to be viewed per page
    results_per_page = 60
    select = Select(driver.find_element_by_id('pager2').find_element_by_class_name('ui-pg-selbox'))
    options_results_per_page =  [o.text for o in select.options]

    assert str(results_per_page) in options_results_per_page, f"results_per_page can only be {options_results_per_page}"
    select.select_by_visible_text(str(results_per_page))

    # click on search
    driver.find_element_by_id('searchButton').click()

    # # wait for click to complete, else time out
    # WebDriverWait(driver, 60, poll_frequency=60).until(lambda x: x.find_element_by_id('load_list2').is_displayed())

    # wait until results are being loaded
    # TODO unclean, try using above commented code
    while (driver.find_element_by_id('load_list2').is_displayed()):
        pass

    name_for_file = '_'.join(location.lower().split())
    f = open(f"{output_dir}/./ucop_{name_for_file}_{year}_auto.csv", 'w')
    #f = open(f"../../data/csv/ucop/ucop_{name_for_file}_{year}_auto.csv", 'w')
    writer = csv.writer(f)

    # write header
    writer.writerow(['SNo','Year','Location','FirstName','LastName','Title',
                     'GrossPay','RegularPay','OvertimePay','OtherPay'])

    # get how many paged result has appeared
    total_num_pages = int(driver.find_element_by_id('sp_1').text)
    pages_left = total_num_pages
    
    if total_num_pages < 1:
        assert False, "Search yielded no result or wait for results to load expired."
    
    while (pages_left > 0):
        
        # need to click on next and wait from 2nd page onwards
        if (pages_left != total_num_pages):
            driver.find_element_by_id('next').click()
            
            # wait until results are being loaded
            # TODO unclean, try using above commented code
            while (driver.find_element_by_id('load_list2').is_displayed()):
                pass
            
            assert total_num_pages == int(driver.find_element_by_id('sp_1').text), "Something went wrong! total_num_pages has changed now."
        
        # strict = false since results may be less than 60 on 1st page
        try:
            rows = get_parsed_rows_ucop(driver.page_source, strict=False)
            for row in rows:
                writer.writerow(row)
        except AssertionError as e:
            print(f"caught exception {e} in get_parsed_rows_ucop!")
            #no need to write row in this case
        
        pages_left -=  1
        stdout.write('\r')
        stdout.write(f"Need to go through {pages_left} more pages!")
        stdout.flush()

    print("")
    
    #close f
    f.close()
    
    driver.quit()


if __name__ == "__main__":
    parser = ArgumentParser(description='Crawls information from UCOP Annual Wages webpage')
    parser.add_argument('--location', type=str, nargs='?', default='San Diego',
                        help='location whose wages to crawl, default:\'San Diego\'')
    parser.add_argument('--year', type=int, nargs='?', default=2018,
                        help='year for which data to crawl, default:2018')
    parser.add_argument('--headless', type=str, default='True',
                        help='mode (False/True) in which to launch browser, default:True')
    parser.add_argument('--geckodriver_path', type=str, nargs='?', default='./geckodriver',
                        help='path to the geckodriver executable, default:\'./geckodriver\'')
    parser.add_argument('--output_dir', type=str, nargs='?', default='../data/csv/ucop/',
                        help='dir where to place the generated csv, default:\'../data/csv/ucop/\'')
    args = parser.parse_args()

    if args.headless == 'False':
        headless = False
    else:
        headless = True

    print(f"year:{args.year}, location:{args.location}, headless:{headless}, geckodriver_path:{args.geckodriver_path}, output_dir:{args.output_dir}")
    print("=========================================================================================")
    do_ucop_crawl(location=args.location, year=args.year, headless=headless, geckodriver_path=args.geckodriver_path, output_dir=args.output_dir)
    print("=========================================================================================")