import pandas as pd
import helper_salary as helper

def summarize_professor_salary_data(uc_name):
    """
    This function takes uc school name (san diego, los angeles, berkeley) and prints some statistics about it.
    : param uc_name: (list), uc school name
    """
    assert uc_name in ['sandiego', 'losangeles', 'berkeley'], "you should enter sandiego, losangeles or berkeley as school names"
    
    print('UC ' + uc_name)
    salary_data = helper.read_data(uc_name)
    salary_data = helper.calculate_netsalary(salary_data)
    
    salary_data_professors = salary_data[salary_data['Title'].str.contains("PROF")]
    total_payment = salary_data_professors['TotalPay'];
    print('Total number of professors: ' + str(len(salary_data_professors))) 
    
    print('Mean: ' + str("%.2f" % total_payment.mean()) + '$');  
    print('Max: ' + str(total_payment.max()) + '$');  
    print('Min: ' + str(total_payment.min()) + '$');  
    print("_____________________________\n");
