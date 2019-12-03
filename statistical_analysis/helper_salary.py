import pandas as pd

def read_data(uc_name):
    """
    This function reads the data given specific school name and returns it.
    """
    csv_location = "../data/csv/ucop"
    file_name = 'ucop' + '_' + uc_name + '_' + 2018 + '_' + 'auto' + '.csv'
    relative_path = csv_location + '/' + file_name
    salary_data = pd.read_csv(relative_path, thousands=',')
    return salary_data
    
def calculate_netsalary(salary_data):
    """
    This function takes salary data and formats its columns in order to create net salary column.
    : param salary_data: (pd.DataFrame), salary data   
    : return: salary_data_formatted: (pd.DataFrame), salary data added net salary column 
    """
    
    del salary_data['GrossPay'];
    # Turning pay columns into numeric ones and create TotalPay column:
    salary_data[['RegularPay', 'OvertimePay', 'OtherPay']] = salary_data[['RegularPay', 'OvertimePay', 'OtherPay']].apply(pd.to_numeric)  
    salary_data['TotalPay'] = salary_data['RegularPay'] + salary_data['OvertimePay'] + salary_data['OtherPay']
    return salary_data

def create_mean_salaries(uc_schools):
    """
    This function takes a list of uc schools and it returns mean salary values.
    : param uc_schools: (list), uc schools
    : return: mean_salaries: (list), mean salary values for specified uc schools
    """
    assert len(uc_schools) > 0
    
    mean_salaries = list()
    for school in uc_schools:
        salary_data = read_data(school)
        salary_data = calculate_netsalary(salary_data)
        salary_data_professors = salary_data[salary_data['Title'].str.contains("PROF")]
        total_payment = salary_data_professors['TotalPay'];
        mean_salaries.append(int(total_payment.mean())/1000) 
    return mean_salaries
