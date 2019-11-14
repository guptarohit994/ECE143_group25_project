from bs4 import BeautifulSoup
import re
import string
from nltk.corpus import stopwords
from collections import defaultdict
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from sys import stdout

def get_parsed_rows_cape(dept, dept_num, total_dept, html_source, driver):
    '''
    Function that takes in source code of a page from http://cape.ucsd.edu/responses/Results.aspx
    and returns list of list(columns as entries for each row).

    Parameters:
        html_source (str): Source code of a page from cape website
    Returns:
        list: Contains list of columns as entries for each row

    '''
    assert isinstance(html_source,str) and html_source != '', "Contains the source code of an html page with row entries to be fetched"

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(html_source, 'html.parser')
    table = soup.find(id='ctl00_ContentPlaceHolder1_gvCAPEs')

    output = []

    header = [i.get_text().replace(' ','') for i in table.find('thead').find_all('th')]
    # Instructor
    # Course
    # Term
    # Enroll
    # EvalsMade
    # RcmndClass
    # RcmndInstr
    # StudyHrs/wk
    # AvgGradeExpected
    # AvgGradeReceived
    # output.append(header)

    columns_found = [*header]
    dept_dict = {}
    
    # each row is a course,instructor,term on the dept page
    for course_num,row in enumerate(table.find('tbody').find_all('tr')):
        # value per header
        fixed_values = []
        this_course_dict = {}
        # used to skip courses prior to FA12 as they have different format
        stop_processing = False
        
        # iterating through columns of course on a dept page
        for index,i in enumerate(row.find_all('td')):
            fixed_values.append(i.get_text().replace('"','').strip().replace(' ',''))
            
            # check there is a hyperlink element
            a_element = i.find_all('a', href=True)
            if (len(a_element) > 0):
                assert len(a_element) == 1, "expected only 1 href in the course column per row"
                assert index == 1, "Expected a href only in Course column (index=1)"
                a_element_link = a_element[0]['href']
                a_element_id = a_element[0]['id']

                more_course_dict = crawl_parse_course_offering_page("https://cape.ucsd.edu/responses/" + a_element_link, driver)
                
                new_columns_found = [j for j in list(more_course_dict.keys()) if j not in columns_found]
                
                
                if len(more_course_dict.keys()) == 0:
                    print("")
                    print(f"No valid results found for {dept} course {course_num+1} and link: {a_element_link}")
                    stop_processing = True
                else:
                    stdout.write('\r')
                    print_string = f"{dept} results({course_num+1} courses)"
                    # need to pad with spaces to keep the above string of fixed length, otherwise remains are not cleaned from screen
                    stdout.write(f"             parsing department ({dept_num}/{total_dept}), {'{s:{c}^{n}}'.format(s=print_string,n=40,c=' ')}")
                    stdout.flush()

                columns_found += new_columns_found
                
                this_course_dict.update(more_course_dict)
        
        if stop_processing:
            break

        assert len(header)==len(fixed_values), f"Unequal fields in header:{header} and this row:{fixed_values}"
        # key = column, value = value
        this_course_dict.update({header[j]:fixed_values[j] for j in range(len(header))})
        
        # finally add an entry to the dept dict
        dept_dict[course_num] = defaultdict(lambda:'0', this_course_dict)
    
    #get_parsed_rows_cape.dept_dict = dept_dict
    
    output.append(columns_found)
    
    # now query each course dict to fill in columns even it may not originally have
    # we'll use default dict for such cases
    for course in dept_dict.keys():
        output.append([dept_dict[course][col] for col in columns_found])
    
    return output



def crawl_parse_course_offering_page(href, driver):
    # get handles of all pages currently open
    current_tabs = driver.window_handles
    
    # currently can't handle duplicate tabs opened
    assert len(current_tabs) == len(set(current_tabs)), "Only unique tabs allowed to be opened at a time"
    
    # open the link in new tab
    #driver.execute_script("window.open('https://google.com');")
    driver.execute_script(f"window.open('{href}');")
    assert len(driver.window_handles) == (len(current_tabs)+1), f"New tab({href}) did not open"
    
    # get the handle to tab just opened
    new_tab_handle = (set(driver.window_handles) - set(current_tabs)).pop()
    
    # make sure you're on this new tab - href
    driver.switch_to.window(new_tab_handle)
    
    try:
        # wait until the page loads
        status = WebDriverWait(driver, 30, poll_frequency=0.5).\
                    until(lambda x: x.find_element_by_id('btnClick').is_displayed())
    except TimeoutException:
        driver.close()
        # need to switch to any tabs open, driver's handle is now invalid
        driver.switch_to.window(current_tabs[-1])
        return {}
    
    source = driver.page_source
    
    # close this new tab
    driver.close()
    
    # need to switch to any tabs open, driver's handle is now invalid
    driver.switch_to.window(current_tabs[-1])
    
    # now parse the page
    soup = BeautifulSoup(source, 'html.parser')
    table = soup.find(id='ctl00_ContentPlaceHolder1_dlQuestionnaire')
    
    # strip punctations
    punc_table = str.maketrans('','',string.punctuation)
    q_options = []

    q_pat_str = 'ctl00_ContentPlaceHolder1_dlQuestionnaire_ctl(\d+)_lblQuestionText'
    q_pat = re.compile(q_pat_str)
    possible_q_num = [i for i in q_pat.findall(str(table))]

    # only valid q will be in dict
    q_a_dict = {}
    max_count_questions = len(possible_q_num)

    for i in possible_q_num:
        # check if answers exist to confirm whether question is valid
        a_pat_str = "ctl00_ContentPlaceHolder1_dlQuestionnaire_ctl" + i + "_rptChoices_ctl\d+_rbSelect"
        a_pat = re.compile(a_pat_str)

        answers = [str(table.find(id=i)).split('<br/>')[1].replace('%','') for i in a_pat.findall(str(table))]

        # valid question
        if (len(answers) > 0):
            # if options dont exist for this q_num, it is possible that question is invalid or 
            # previously known options can be used
            # check if options exist for this question or we need to use previously known options
            o_id = 'ctl00_ContentPlaceHolder1_dlQuestionnaire_ctl' + i + '_trChoiceText'

            o_tag = table.find(id=o_id)
            if o_tag is not None:
                options = [j.get_text().translate(punc_table).replace(' ','_') for j in o_tag.find_all('b')]
                # remove these
                for option in ['Resp', 'Mean', 'StDev']:
                    if option in options:
                        options.remove(option)

            # all options should have answers (values in %)
            assert len(options) == len(answers), f"options:{options}, answers:{answers}"

            # fill the dict
            # key = question_option, value = answer
            q_id = 'ctl00_ContentPlaceHolder1_dlQuestionnaire_ctl' + i + '_lblQuestionText'
            q = table.find(id=q_id).get_text().lower().translate(punc_table).replace(' ','_')
            # remove stop words
            q = '_'.join([word for word in q.split('_') if word.lower() not in stopwords.words('english')])

            for j in range(len(options)):
                # just to confirm removing stopwords is not making 2 questions same
                assert q + "_" + options[j] not in q_a_dict
                q_a_dict[q + "_" + options[j]] = answers[j]
            
    return q_a_dict
    
