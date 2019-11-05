from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from ucop_webpage_parser import get_parsed_rows_ucop
import csv



f = open('./../data/csv/ucop_san_diego_auto.csv', 'w')
writer = csv.writer(f)


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
driver.get("https://ucannualwage.ucop.edu/wage/")
print ("Headless Firefox Initialized")



total_num_pages = 1
pages_left = 1
first_time = True

while (pages_left > 0):
    
    if (first_time):
        # write header
        writer.writerow(['SNo','Year','Location','FirstName','LastName','Title',
                         'GrossPay','RegularPay','OvertimePay','OtherPay'])
        
        # select San Diego as Location
        select = Select(driver.find_element_by_id('wrapper').\
                               find_element_by_id('content').\
                               find_element_by_id('sform').\
                               find_element_by_id('location'))
        # print(select.options)
        # print([o.text for o in select.options]) # these are string-s
        select.select_by_visible_text('San Diego')

        # select 60 results to be viewed per page
        select_60 = Select(driver.find_element_by_id('wrapper').\
                           find_element_by_id('content').
                           find_element_by_id('gbox_list2').\
                           find_element_by_id('pager2').\
                           find_element_by_class_name('ui-pg-table').\
                           find_element_by_class_name('ui-pg-selbox')
                          )
        select_60.select_by_visible_text('60')

        # click on search
        driver.find_element_by_id('wrapper').\
               find_element_by_id('content').\
               find_element_by_id('sform').\
               find_element_by_id('searchButton').click()
            
#         # wait for click to complete, else time out
#         WebDriverWait(driver, 60, poll_frequency=60).until(lambda x: x.find_element_by_id('wrapper').
#                                                                        find_element_by_id('content').
#                                                                        find_element_by_id('load_list2').\
#                                                                        is_displayed()
#                                                           )

        while (driver.find_element_by_id('wrapper').
                      find_element_by_id('content').
                      find_element_by_id('load_list2').\
                      is_displayed()
              ):
            pass
        
        # get how many paged result has appeared
        total_num_pages = int(driver.
                              find_element_by_id('wrapper').\
                              find_element_by_id('content').\
                              find_element_by_id('pg_pager2').\
                              find_element_by_id('sp_1').\
                              text
                             )
        
        if (total_num_pages >= 1):
            # have already parsed this page
            pages_left = total_num_pages - 1
            print(f"Need to go through {pages_left} more pages!")
            
            # strict = false since results may be less than 60 on 1st page
            try:
                rows = get_parsed_rows_ucop(driver.page_source, strict=False)
                for row in rows:
                    writer.writerow(row)
            except AssertionError as e:
                print(f"caught exception {e} in get_parsed_rows_ucop!")
                #no need to write row in this case
        else:
            assert False, "Search yielded no result or wait for results to load expired. Maybe exit?"
        
        #set first time as false
        first_time = False
    else:
        #click on next
        driver.find_element_by_id('wrapper').\
               find_element_by_id('content').\
               find_element_by_id('pg_pager2').\
               find_element_by_id('next').click()
        
        while (driver.find_element_by_id('wrapper').
                       find_element_by_id('content').
                       find_element_by_id('load_list2').\
                       is_displayed()
              ):
            pass
        
        assert total_num_pages == int(driver.find_element_by_id('wrapper').\
                                             find_element_by_id('content').\
                                             find_element_by_id('pg_pager2').\
                                             find_element_by_id('sp_1').text),\
                          "Something went wrong! total_num_pages has changed now."

        pages_left -= 1
        print(f"Need to go through {pages_left} more pages!")
        try:
            if (pages_left == 0):
                # last page, results may be less than 60 => strict = False
                rows = get_parsed_rows_ucop(driver.page_source, strict=False)
            else:
                rows = get_parsed_rows_ucop(driver.page_source)
            for row in rows:
                writer.writerow(row)
        except AssertionError as e:
            print(f"caught exception {e} in get_parsed_rows_ucop!")
            #no need to write row in this case
#close f
f.close()


driver.quit()