from bs4 import BeautifulSoup

def get_parsed_rows_ucop(html_source, rows_expected=60, strict=True):
    '''
    Function that takes in source code of a page from https://ucannualwage.ucop.edu/wage/
    and returns list of list(columns as entries for each row).
    
    Parameters:
        html_source (str): Source code of a page from ucop wage website
        rows_expected (int,60): Number of rows that are expected to be parsed from this page
        strict (bool,True): Strictly checks for #rows = rows_expected. Otherwise, 1 <= #rows <= #rows_expected
    Returns:
        list: Contains list of columns as entries for each row
    
    '''
    assert isinstance(html_source,str) and html_source != '', "Contains the source code of an html page with row entries to be fetched"
    assert isinstance(rows_expected,int) and rows_expected >= 1, "rows_expected is an integer >= 1"
    assert isinstance(strict,bool), "strict should be a bool"
    
    soup = BeautifulSoup(html_source, 'html.parser')
    table = soup.find_all(id='list2')
    rows = table[0].find_all(role='row')
    
    if strict:
        assert len(rows)==rows_expected, f"(strict) found {len(rows)} rows but rows_expected is {rows_expected}"
    else:
        assert 1 <= len(rows) <= rows_expected, f"(not strict) found {len(rows)} rows but rows_expected is {rows_expected}"
    
    output = []
    
    for row in rows:
        # skip i == 1 since it is local SNo (for the page)
        data_per_row = [field.get_text() for i,field in enumerate(row) if i != 1]
        assert len(data_per_row)==10, "data_per_row does not have 10 rows"
        
        output.append(data_per_row)
        
    return output