
import helper
import matplotlib.pyplot as plt
import pandas as pd

def boxplot_sorted(df, by, column):
    """Given a dataframe, makes it sorted by median value
    
    Arguments:
        df {DataFrame} -- input dataframe to use
        by {String} -- The rule for sorting
        column {String} -- The column to sort
    
    Returns:
        [DataFrame] -- THe sorted dataframe
    """
    df2 = pd.DataFrame({col:vals[column] for col, vals in df.groupby(by)})
    meds = df2.median().sort_values()
    return df2[meds.index]

def generate_boxplots(dept_list_to_use,figsize_len=35, figsize_wid=7):
    """Generate boxplots from department data
    
    Arguments:
        dept_list_to_use {[String]} -- List of departments to plot out
    
    Keyword Arguments:
        figsize_len {int} -- Length size of figure (default: {35})
        figsize_wid {int} -- Width size of figure (default: {7})
    """
    # obtaining data
    department_df = helper.generate_depts_df(dept_list_to_use)

    # plotting boxplots, for four criteria: "RcmndClass", "RcmndInstr", "StudyHrs/wk", and "AvgGradeReceived"
    fig, axes = plt.subplots(4,1, figsize=(figsize_len,figsize_wid*4))
    y_labels = ["Avg. Class Recommend %", "Avg. Instructor Recommend %", "Avg. Hours Studied Per Week", "Avg. Grade Received"]
    for i,criteria in enumerate(["RcmndClass", "RcmndInstr", "StudyHrs/wk", "AvgGradeReceived"]):
        df2 = boxplot_sorted(department_df[["Department",criteria]],"Department", criteria)
        boxplot = df2.boxplot(figsize=(figsize_len,figsize_wid), fontsize=13, ax = axes.flatten()[i])
        axes.flatten()[i].set_ylabel(y_labels[i], fontsize = 20)
        print("{}: Mean:{} Median:{} Std. Dev.:{}".format(criteria, department_df[criteria].mean(), department_df[criteria].median(), department_df[criteria].std()))
        axes.flatten()[i].set_xticklabels([helper.to_readable_dept_name(x.get_text()) for x in axes.flatten()[i].get_xticklabels()])