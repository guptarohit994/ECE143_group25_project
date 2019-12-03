import pandas as pd

def read_data(uc_name):
    """
    This function reads the data given specific school name and returns it.
    """
    file_name = 'ucop' + '_' + uc_name + '.csv'
    salary_data = pd.read_csv(file_name, thousands=',')
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

def summarize_professor_salary_data(uc_name):
    """
    This function takes uc school name (san diego, los angeles, berkeley) and prints some statistics about it.
    : param uc_name: (list), uc school name
    """
    assert uc_name in ['sandiego', 'losangeles', 'berkeley'], "you should enter sandiego, losangeles or berkeley as school names"
    
    print('UC ' + uc_name)
    salary_data = read_data(uc_name)
    salary_data = calculate_netsalary(salary_data)
    
    salary_data_professors = salary_data[salary_data['Title'].str.contains("PROF")]
    total_payment = salary_data_professors['TotalPay'];
    print('Total number of professors: ' + str(len(salary_data_professors))) 
    
    print('Mean: ' + str("%.2f" % total_payment.mean()) + '$');  
    print('Max: ' + str(total_payment.max()) + '$');  
    print('Min: ' + str(total_payment.min()) + '$');  
    print("_____________________________\n");
