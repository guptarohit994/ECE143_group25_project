from argparse import ArgumentParser
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from cape_webpage_parser import get_parsed_rows_cape
from ucsd_triton_sso import initiate_sso_login
import csv
from sys import stdout
from os import path



def do_cape_crawl(department='all', detailed=False, headless=True, geckodriver_path='./geckodriver', output_dir="."):
    '''
    Crawls information for all courses in various departments on CAPE webpage
    :param department: specific department whose data to crawl, default:'all'
    :type department: str
    :type detailed: form of data scraping. Detailed are much slower. default:False
    :type detailed: bool
    :param headless: mode in which to launch browser, default:True
    :type headless: bool
    :param geckodriver_path: path to the geckodriver executable, default:'./geckodriver'
    :type geckodriver_path: str
    :param output_dir: dir where to place the generated csv, default:'.''
    :type output_dir: str
    '''
    assert isinstance(department,str), "department should be a str"
    assert isinstance(headless,bool), "headless should be a bool"
    assert isinstance(geckodriver_path,str) and path.exists(geckodriver_path), f"geckodriver does not exist at {geckodriver_path}"
    assert isinstance(output_dir,str) and path.isdir(output_dir), f"Not a valid directory:{output_dir}"
    
    department = department.upper()

    options = Options()
    options.headless = headless

    driver = Firefox(options=options, executable_path=geckodriver_path)
    driver.get("https://cape.ucsd.edu/responses/Results.aspx")
    
    print ('Firefox Initialized in %s mode'%('headless' if headless else 'head'))


    initiate_sso_login(driver)


    # # we expect a security warning   
    # # try:
    # WebDriverWait(driver, 120).until(EC.alert_is_present(),
    #                                'Timed out waiting for a successful SSO login. Check credentials?')
    # #Switch the control to the Alert window
    # alert = driver.switch_to.alert

    # #Retrieve the message on the Alert window
    # msg = alert.text

    # #use the accept() method to accept the alert
    # alert.accept()
    # print(f"Alert Accepted:\n{' '.join(msg.strip().split())}")

    # # except NoAlertPresentException:
    # #     raise 

    # # except TimeoutException:
    # #     pass

    # wait for cape page to load after SSO
    status = WebDriverWait(driver, 30, poll_frequency=0.5).until(lambda x: x.find_element_by_id('ctl00_ContentPlaceHolder1_ddlDepartments'),
                                                                 'Timed out waiting for SSO -> CAPE webpage loading. Check credentials.')

    print("*********** Successfully logged in ***********")

    select_dept = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlDepartments'))
    departments = [o.text for o in select_dept.options if o.text != "Select a Department"]

    departments_keyworded = [dept.split()[0] for dept in departments]

    assert department in departments_keyworded or department=='ALL', f"invalid department supplied. Should be one of {departments_keyworded} or ALL"
    
    if department != 'ALL':
        departments = [ departments[departments_keyworded.index(department)] ]

    total_departments = len(departments)

    print("")

    # select departments one at a time and create their csv
    for index,dept in enumerate(departments):
        dept_keyword = dept.split()[0]

        # if dept_keyword not in ['INTL','ICAM', 'ERC','TMC', 'RELI', ]:
        #     continue

        # if dept_keyword in ['FILM','ESYS','DOC','CGS','CENG','ENVR','FPMU','JUDA','LATI','TWS','LAWS','REV','WARR','SDCC','MUIR','HMNR','CONT','SXTH','STPA']:
        #     continue

        select_dept.select_by_visible_text(dept)
        # click on submit button
        driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnSubmit').click()

        # there's a small delay between click and this element getting displayed
        # returns true
        status = WebDriverWait(driver, 30, poll_frequency=0.5).until(lambda x: x.find_element_by_id('ctl00_ContentPlaceHolder1_UpdateProgress1').is_displayed())

        # shoud return false now
        status = WebDriverWait(driver, 30, poll_frequency=0.5).until_not(lambda x: x.find_element_by_id('ctl00_ContentPlaceHolder1_UpdateProgress1').is_displayed())
        assert status == False, "Page is still loading!"


        try:
            rows = get_parsed_rows_cape(dept=dept_keyword, dept_num=(index+1), total_dept=total_departments, html_source=driver.page_source, driver=driver, detailed=detailed)
            if (len(rows) <= 1):
                print(f"Didn't find any valid row for {dept_keyword}!")
            else:
                f = open(f"{output_dir}/./cape_{dept_keyword}_auto.csv", 'w')
                writer = csv.writer(f)
                for row in rows:
                    writer.writerow(row)
                f.close()

                stdout.write('\r')
                # exclude header
                print_string = f"{dept_keyword} results({len(rows)-1} courses)"
                # need to pad with spaces to keep the above string of fixed length, otherwise remains are not cleaned from screen
                stdout.write(f"Successfully parsed departments({index+1}/{total_departments}), {'{s:{c}^{n}}'.format(s=print_string,n=40,c=' ')}")
                stdout.flush()
        except AssertionError as e:
                print(f"caught exception {e} in get_parsed_rows_cape for {dept_keyword}!")
                #no need to write row in this case

    print("")

    driver.quit()

if __name__ == "__main__":
    parser = ArgumentParser(description='Crawls information for all courses in various departments on CAPE webpage')
    parser.add_argument('--department', type=str,default='all',
                        help='specific department whose data to crawl. Either 1 or all, default:\'all\'')
    parser.add_argument('--detailed', type=str,default='False',
                        help='form of data scraping. Detailed are much slower. default:\'False\'')
    parser.add_argument('--headless', type=str,default='True',
                        help='mode in which to launch browser, default:\'True\'')
    parser.add_argument('--geckodriver_path', type=str, nargs='?', default='./geckodriver',
                        help='path to the geckodriver executable, default:\'./geckodriver\'')
    parser.add_argument('--output_dir', type=str, nargs='?', default='../data/csv/cape/',
                        help='dir where to place the generated csv, default:\'../data/csv/cape/\'')
    args = parser.parse_args()

    if args.headless == 'False':
        headless = False
    else:
        headless = True

    if args.detailed == 'True':
        detailed = True
    else:
        detailed = False

    print(f"department:{args.department}, detailed:{detailed}, headless:{args.headless}, geckodriver_path:{args.geckodriver_path}, output_dir:{args.output_dir}")

    print("=========================================================================================")
    do_cape_crawl(department=args.department, detailed=detailed, headless=headless, geckodriver_path=args.geckodriver_path, output_dir=args.output_dir)
    print("=========================================================================================")

