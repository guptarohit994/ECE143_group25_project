import numpy as np
import matplotlib.pyplot as plt
import helper_salary as helper

def create_mean_salary_barchart(uc_schools):
    """
    This function takes a list of uc schools and it returns mean salary barchart.
    : param uc_schools: (list), uc schools
    """
    assert len(uc_schools) > 0
    
    y_pos = np.arange(len(uc_schools))
    mean_salary = helper.create_mean_salaries(uc_schools)

    fig, ax = plt.subplots(figsize=(10,5))
    plt.bar(y_pos, mean_salary, align='center', alpha=0.5)
    plt.xticks(y_pos, uc_schools)
    plt.ylabel('Mean Salary (in thousand $)', fontsize=16)
    plt.xticks(size = 12, rotation=0)
    plt.yticks(size = 12)

    plt.show()
