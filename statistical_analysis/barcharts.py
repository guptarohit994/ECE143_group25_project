def create_mean_salary_barchart(uc_schools):
    """
    This function takes a list of uc schools and it returns mean salary barchart.
    : param uc_schools: (list), uc schools
    """
    assert len(uc_schools) > 0
    
    y_pos = np.arange(len(uc_schools))
    mean_salary = create_mean_salaries(uc_schools)

    fig, ax = plt.subplots(figsize=(10,5))
    plt.bar(y_pos, mean_salary, align='center', alpha=0.5)
    plt.xticks(y_pos, uc_schools)
    plt.ylabel('Mean Salary (in thousand $)', fontsize=16)
    plt.xticks(size = 12, rotation=0)
    plt.yticks(size = 12)

    plt.show()

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
