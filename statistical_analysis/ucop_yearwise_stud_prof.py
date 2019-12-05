import pandas as pd
import csv
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os


def get_ucop_dataset_facts(path, title_to_text_dict=None, verbose=False):
    '''
    function to get student opportunities out of ucop dataset
    :param path: path of the csv file
    :type path: str
    :param title_to_text_dict: dict containing mapping from title to text
    :type title_to_text_dict: dict
    :param verbose: verbosity, false by default
    :type verbose: bool
    :return: tuple (min_gpay, max_gpay, mean, median, std, count_student_jobs, count_total_jobs)
    '''
    assert isinstance(path, str) and os.path.exists(path), "path should be a string and should exist"
    assert isinstance(verbose, bool)

    df = pd.read_csv(path)
    
    # fill dict
    if title_to_text_dict is None:
        reader = csv.reader(open('../data/csv/ucop/ucop_title_to_text.csv', 'r'))
        title_to_text_dict = {}
        for row in reader:
            k, v = row
            title_to_text_dict[k] = v
    else:
        assert isinstance(title_to_text_dict, dict)
     
    # perform replacement to make distinction easier
    for index, item in enumerate(df['Title']):
        if item not in title_to_text_dict:
            if re.search('^STDT \d', item):
                df.at[index, 'Title'] = 'OTHER STUDENT TITLES'
        else:
            df.at[index, 'Title'] = title_to_text_dict[item]
    
    if verbose:
        print(df['Title'][df['Title'].str.contains('STUDENT')].value_counts())
    
    count_student_jobs = df['Title'][df['Title'].str.contains('STUDENT')].count()
    count_total_jobs = df['Title'].count()
    median = pd.to_numeric(df['GrossPay'][df['Title'].str.contains('STUDENT')].str.replace(',','')).median()
    mean = pd.to_numeric(df['GrossPay'][df['Title'].str.contains('STUDENT')].str.replace(',','')).mean()
    min_gpay = pd.to_numeric(df['GrossPay'][df['Title'].str.contains('STUDENT')].str.replace(',','')).min()
    max_gpay = pd.to_numeric(df['GrossPay'][df['Title'].str.contains('STUDENT')].str.replace(',','')).max()
    std = pd.to_numeric(df['GrossPay'][df['Title'].str.contains('STUDENT')].str.replace(',','')).std()
    
    if verbose:
        print(f"Total student titles:{count_student_jobs} out of {count_total_jobs}, {(count_student_jobs*100/count_total_jobs):.2f}%")
        print(f"Mean:{mean:.2f}, Median:{median:.2f}, Std:{std:.2f}")
        print(f"min:{min_gpay}, max:{max_gpay}")
    return (min_gpay, max_gpay, mean, median, std, count_student_jobs, count_total_jobs)


def fill_dict_with_student_data(verbose=False):
    '''
    function to fill the dictionary with data for student jobs after reading from datasets
    :param verbose: verbosity, false by default
    :type verbose: bool
    :return: dict
    '''
    assert isinstance(verbose, bool)

    student_jobs_stats = {}
    student_jobs_stats['student_avg_gpay'] = {}
    student_jobs_stats['student_avg_gpay']['san_diego'] = []
    student_jobs_stats['student_avg_gpay']['los_angeles'] = []
    student_jobs_stats['student_avg_gpay']['berkeley'] = []

    student_jobs_stats['student_med_gpay'] = {}
    student_jobs_stats['student_med_gpay']['san_diego'] = []
    student_jobs_stats['student_med_gpay']['los_angeles'] = []
    student_jobs_stats['student_med_gpay']['berkeley'] = []

    student_jobs_stats['percent_student_jobs'] = {}
    student_jobs_stats['percent_student_jobs']['san_diego'] = []
    student_jobs_stats['percent_student_jobs']['los_angeles'] = []
    student_jobs_stats['percent_student_jobs']['berkeley'] = []

    locations = ['san_diego', 'los_angeles', 'berkeley']
    labels = ['2014', '2015','2016','2017','2018']

    for location in locations:
        for year in labels:
            if verbose:
                print(f"*************{location},{year}*************")
            path = '../data/csv/ucop/ucop_' + location + '_' + year + '_auto.csv'
            min_gpay, max_gpay, mean, median, std, count_student_jobs, count_total_jobs = get_ucop_dataset_facts(path,verbose=verbose)
            student_jobs_stats['student_avg_gpay'][location].append(int(mean))
            student_jobs_stats['student_med_gpay'][location].append(int(median))
            student_jobs_stats['percent_student_jobs'][location].append(count_student_jobs*100/count_total_jobs)
            if verbose:
                print()

    return student_jobs_stats


def fill_dict_with_all_prof_data(verbose=False):
    '''
    function to fill the dictionary with data for all types of professors after reading from datasets
    :param verbose: verbosity, false by default
    :type verbose: bool
    :return: tuple of dicts in order 
    '''
    assert isinstance(verbose,bool)

    locations = ['san_diego', 'los_angeles', 'berkeley']
    labels = ['2014', '2015','2016','2017','2018']

    prof_dict = {}
    assoc_prof_dict = {}
    asst_prof_dict = {}

    properties = ['count', 'mean_gpay', 'median_gpay', 'std_gpay']
    for item in properties:
        prof_dict[item] = {}
        assoc_prof_dict[item] = {}
        asst_prof_dict[item] = {}


    for location in locations:
        for item in properties:
            prof_dict[item][location] = []
            assoc_prof_dict[item][location] = []
            asst_prof_dict[item][location] = []
            
        
        for year in labels:
            df = pd.read_csv('../data/csv/ucop/ucop_' + location + '_' + year + '_auto.csv', thousands=',')
            df_title_gpay = df[['Title','GrossPay']][df['Title'].str.contains('PROF')]
            prof_series = df_title_gpay['GrossPay']
            prof_dict['count'][location].append(prof_series.count())
            prof_dict['mean_gpay'][location].append(prof_series.mean())
            prof_dict['median_gpay'][location].append(prof_series.median())
            prof_dict['std_gpay'][location].append(prof_series.std())
            
            df_assoc_title_gpay = df_title_gpay[df_title_gpay['Title'].str.contains('ASSOC')]
            assoc_prof_series = df_assoc_title_gpay['GrossPay']
            assoc_prof_dict['count'][location].append(assoc_prof_series.count())
            assoc_prof_dict['mean_gpay'][location].append(assoc_prof_series.mean())
            assoc_prof_dict['median_gpay'][location].append(assoc_prof_series.median())
            assoc_prof_dict['std_gpay'][location].append(assoc_prof_series.std())
            
            df_asst_title_gpay = df_title_gpay[df_title_gpay['Title'].str.contains('ASST')]
            asst_prof_series = df_asst_title_gpay['GrossPay']
            asst_prof_dict['count'][location].append(asst_prof_series.count())
            asst_prof_dict['mean_gpay'][location].append(asst_prof_series.mean())
            asst_prof_dict['median_gpay'][location].append(asst_prof_series.median())
            asst_prof_dict['std_gpay'][location].append(asst_prof_series.std())

    return (prof_dict, assoc_prof_dict, asst_prof_dict)
        

def grouped_bar_plot(my_dict, labels, figsize, figname, title='', ylabel='', save=False, grids=False):
    '''
    Function to plot a grouped bar plot
    :param my_dict: dictionary containing data for students
    :type my_dict: dict
    :param labels: list of x-axis labels. years as string
    :type labels: list
    :param figsize: size of the figure to generate
    :type figsize: tuple
    :param figname: name of the figure to be generated
    :type figname: str
    :param title: title of the figure
    :type title: str
    :param ylabel: y-axis label in the figure
    :type ylabel: str
    :param save: set true if figure has to be saved
    :type save: bool
    :param grids: set true if grids are needed in figure
    :type grids: bool
    '''
    assert isinstance(my_dict,dict), "my_dict should be a dict"
    assert isinstance(labels, list) and all(isinstance(i,str) for i in labels)
    assert isinstance(figsize,tuple) and all(isinstance(i,int) for i in figsize), "figsize should be a tuple of ints"
    assert isinstance(figname, str)
    assert isinstance(title,str)
    assert isinstance(ylabel, str)
    assert isinstance(save, bool)
    assert isinstance(grids, bool)

    plt.rcParams["figure.figsize"] = figsize
    width = 0.5  # the width of the bars

    x = np.arange(len(labels))  # the label locations
    fig, ax = plt.subplots()
    rects = []

    count_grouped_bars = len(my_dict.keys())
    for index,i in enumerate(my_dict.keys()):
        rects.append(ax.bar(x - (width/2 - (index * width/count_grouped_bars)), my_dict[i], width/count_grouped_bars, label=i))


    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc="upper left")


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    if grids:
        plt.grid()
    ax.set_axisbelow(True)
    fig.tight_layout()
    if save:
        plt.savefig(figname)
    plt.show()



def line_plots(my_dict, labels, figsize, figname, title='', ylabel='', save=False, grids=False):
    '''
    Function to plot line plots
    :param my_dict: dictionary containing data for students
    :type my_dict: dict
    :param labels: list of x-axis labels. years as string
    :type labels: list
    :param figsize: size of the figure to generate
    :type figsize: tuple
    :param figname: name of the figure to be generated
    :type figname: str
    :param title: title of the figure
    :type title: str
    :param ylabel: y-axis label in the figure
    :type ylabel: str
    :param save: set true if figure has to be saved
    :type save: bool
    :param grids: set true if grids are needed in figure
    :type grids: bool
    '''
    assert isinstance(my_dict,dict), "my_dict should be a dict"
    assert isinstance(labels, list) and all(isinstance(i,str) for i in labels)
    assert isinstance(figsize,tuple) and all(isinstance(i,int) for i in figsize), "figsize should be a tuple of ints"
    assert isinstance(figname, str)
    assert isinstance(title,str)
    assert isinstance(ylabel, str)
    assert isinstance(save, bool)
    assert isinstance(grids, bool)

    plt.rcParams["figure.figsize"] = figsize
    width = 0.5  # the width of the bars

    x = np.arange(len(labels))  # the label locations
    fig, ax = plt.subplots()

    for index,i in enumerate(my_dict.keys()):
        ax.plot(labels, my_dict[i], label=i)


    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    if grids:
        plt.grid()
    ax.set_axisbelow(True)
    fig.tight_layout()
    if save:
        plt.savefig(figname)
    plt.show()