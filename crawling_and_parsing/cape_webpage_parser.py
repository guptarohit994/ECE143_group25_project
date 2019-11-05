from bs4 import BeautifulSoup

def get_parsed_rows_cape(html_source):
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
    output.append(header)
    
    for index,row in enumerate(table.find('tbody').find_all('tr')):
        values = [i.get_text().replace('"','').strip().replace(' ','') for i in row.find_all('td')]
        assert len(header)==len(values), "Unequal fields in header and this row"
        output.append(values)
        
    return output