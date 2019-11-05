from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from cape_webpage_parser import get_parsed_rows_cape
from ucsd_triton_sso import initiate_sso_login
import csv


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
driver.get("http://cape.ucsd.edu/responses/Results.aspx")
print ("Headless Firefox Initialized")


initiate_sso_login(driver)


# we expect a security warning   
# try:
WebDriverWait(driver, 120).until(EC.alert_is_present(),
                               'Timed out waiting for a successful SSO login. Check credentials?')
#Switch the control to the Alert window
alert = driver.switch_to.alert

#Retrieve the message on the Alert window
msg = alert.text

#use the accept() method to accept the alert
alert.accept()
print(f"Alert Accepted:\n{msg}")

# except NoAlertPresentException:
#     raise 

# except TimeoutException:
#     pass

# wait for cape page to load after SSO
status = WebDriverWait(driver, 30, poll_frequency=0.5).until(lambda x: x.find_element_by_id('ctl00_ContentPlaceHolder1_ddlDepartments'),
                                                             'Timed out waiting for SSO -> CAPE webpage loading')

print("====================== Successfully logged in ====================")

select_dept = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlDepartments'))
departments = [o.text for o in select_dept.options if o.text != "Select a Department"]


# select departments one at a time and create their csv
for dept in departments:
    dept_keyword = dept.split()[0]
    f = open(f"./../data/csv/cape/cape_{dept_keyword}_auto.csv", 'w')
    writer = csv.writer(f)

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
        rows = get_parsed_rows_cape(driver.page_source)
        if (len(rows) == 0):
            print(f"Didn't find any valid row for {dept_keyword}!")
        else:
            for row in rows:
                writer.writerow(row)
            print(f"Successfully parsed {dept_keyword} results({len(rows)} items)")
    except AssertionError as e:
            print(f"caught exception {e} in get_parsed_rows_cape for {dept_keyword}!")
            #no need to write row in this case

    f.close()


driver.quit()

