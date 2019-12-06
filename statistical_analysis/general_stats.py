import helper
import numpy as np
import pandas as pd

def get_general_statistics(name, dept_list_to_use):
    """Prints out the general statistics for the requested departments
    
    Arguments:
        name {String} -- The name of the department list
        dept_list_to_use {[String]} -- The list of departments
    """

    print('\n'+name)
    department_df = helper.generate_depts_df(dept_list_to_use)
    
    total_classes = len(department_df)
    print("Total # of courses recorded: {}".format(total_classes))
    total_profs = len(set(department_df["Instructor"]))
    print("Total # of professors recorded: {}".format(total_profs))

    # calculating response rate, separating based on summer session vs school year
    for name, rule in [["Total", lambda x: True], ["School Year", lambda x: x[:2] not in ["S1", "S2", "S3"]], ["Summer Session", lambda x: x[:2] in ["S1", "S2", "S3"]] ]:
        department_df = helper.generate_depts_df(helper.general_dept_list)
        department_df = department_df[department_df["Term"].apply(rule)]
        mean_respond_rate = np.average(department_df["EvalsMade"]/department_df["Enroll"])
        median_respond_rate = np.median(department_df["EvalsMade"]/department_df["Enroll"])
        std_respond_rate = np.std(department_df["EvalsMade"]/department_df["Enroll"])
        print("\n")
        print("{} mean response rate: {}".format(name, mean_respond_rate))
        print("{} median response rate: {}".format(name, median_respond_rate))
        print("{} response rate std: {}".format(name, std_respond_rate))
        
        
import helper_salary

def summarize_professor_salary_data(uc_name):
    """
    This function takes uc school name (san diego, los angeles, berkeley) and prints some statistics about it.
    : param uc_name: (list), uc school name
    """
    #assert uc_name in ['sandiego', 'losangeles', 'berkeley'], "you should enter sandiego, losangeles or berkeley as school names"
    
    print('UC ' + uc_name)
    salary_data = helper_salary.read_data(uc_name)
    salary_data = helper_salary.calculate_netsalary(salary_data)
    
    salary_data_professors = salary_data[salary_data['Title'].str.contains("PROF")]
    total_payment = salary_data_professors['TotalPay'];
    print('Total number of professors: ' + str(len(salary_data_professors))) 
    
    print('Mean: ' + str("%.2f" % total_payment.mean()) + '$');  
    print('Max: ' + str(total_payment.max()) + '$');  
    print('Min: ' + str(total_payment.min()) + '$');  
    print("_____________________________\n");
