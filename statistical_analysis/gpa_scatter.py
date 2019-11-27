
import helper
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

def plot_gpa_scatter():
    """Plotting scatterplot of grades expected and grade received, using the general department list
    """
    # obtaining data
    department_df = helper.generate_depts_df(helper.general_dept_list)
    comp_criteria = ["AvgGradeExpected","AvgGradeReceived"]

    # generating scatterplot graph
    lower_bound = 1.5
    upper_bound = 4.02
    ax = department_df.plot.scatter(x=comp_criteria[0], y=comp_criteria[1], c= "grey",ylim=(lower_bound,upper_bound),xlim=(lower_bound,upper_bound), figsize=(10,10), fontsize=20, alpha = 0.3)
    ax.set_xlabel("Average Grade Expected", fontsize = 20)
    ax.set_ylabel("Average Grade Received", fontsize = 20)

    # computing least squares best fit line and adding it onto graph
    y = department_df["AvgGradeReceived"]
    x = department_df["AvgGradeExpected"]
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y)[0]
    print("m:{}, c:{}".format(m,c))
    ax.plot(np.linspace(lower_bound,4,10),np.linspace(lower_bound,4,10),c="red")
    ax.plot(np.linspace(lower_bound,4,10),(np.linspace(lower_bound,4,10)*m) + c,c="blue")