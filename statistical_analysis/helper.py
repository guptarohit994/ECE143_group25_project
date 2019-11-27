"""
Contains general information and helper functions for the statistical analysis of CAPES and salary Data.
"""

import pandas as pd
import pickle
import os
import numpy as np

# generating list of departments at UCSD
cache_loc = "./CAPES_Cache"
department_list = []
for root, dirs, files in os.walk(cache_loc):
    for f in files:
        department_list.append(f.split("_")[1])
department_list = list(set(department_list))
master_blacklist = ["FILM","MUIR","SXTH","WARR","CONT","REV","ERC","WCWP", "CAT", "MMW", "SOE", "DOC", "SDCC", "TMC", "HMNR"] 

# Subsets of departments at UCSD to use for visualization
general_dept_list = [x for x in department_list if (x not in master_blacklist)]
STEM_dept_list = ["PHYS","CENG","CHEM", "BENG","MATH", "ECON", "MAE", "ECE","CSE","COGS","FPMU","SE","NENG","ESYS","PSYC","BIOL","SIO","ENVR"]
non_STEM_dept_list = [x for x in department_list if (x not in master_blacklist+STEM_dept_list)]


def generate_depts_df(dept_list_to_use):
    """generates and returns the dataframe from the scraped data, that are in the departments requested
    
    Arguments:
        dept_list_to_use {[String]} -- A list of departments to use
    
    Returns:
        DataFrame -- The CAPES dataframe
    """
    department_df = pd.DataFrame()
    for dept in dept_list_to_use:
        df = pd.read_pickle(os.path.join(cache_loc,"cape_{}_auto_df.pkl".format(dept)))
        df["Department"] = dept
        department_df = department_df.append(df)
    return department_df


def to_readable_dept_name(dept_name):
    """Converts a department acronym into the full name
    
    Arguments:
        dept_name {String} -- The department acronym
    
    Returns:
        String -- The department's full name
    """
    depts = ['TWS', 'BIOL', 'RSM', 'MUS', 'COMM', 'ECON', 'CHIN', 'NENG', 'CGS', 'LAWS', 'USP', 'ETHN', 'EDS', 'BENG', 'LING', 'SOC', 'RELI', 'VIS', 'FPMU', 'HUM',
             'PSYC', 'PHIL', 'STPA', 'COGS', 'ECE', 'ANTH', 'CENG', 'MATH', 'INTL', 'CHEM', 'ICAM', 'SIO', 'THEA', 'HIST', 'PHYS', 'JUDA', 'LATI', 'POLI', 'ESYS',
             'CSE', 'LIT', 'JAPN', 'HDP', 'MAE', 'ENVR', 'SE']
    readable = ['3rd\nWorld\nStudies', "Biology", "Rady\nSchool\nof Mgmt", "Music", "Communi-\ncations","Economics","Chinese","Nano\nEngineering","Gender\nStudies", "Law", "Urban\nStudies","Ethnic\nStudies","Education\nStudies", "Biology\nEngineering", "Linguistics",
               "Sociology", "Religion", "Visual\nArts", "Medicine", "Humanities", "Psychology", "Phil-\nosophy", "Sci-tech\nPublic\nAffairs", "Cognitive\nScience", "ECE", "Anthro-\npology", "Chemical\nEngineering", "Math", "Inter-\nnational\nStudies", "Chemistry",
               "Comp.\nArts", "Scripps\nOceanography", "Theatre","History","Physics","Judaic\nStudies", "Latin\nAmerican\nStudies", "Political\nScience", "Environmental\nSystems","CSE","Liter-\nature", "Japanese", "Human\nDev.",
               "Mech. &\nAero.\nEngineering", "Environmental\nStudies", "Structural\nEngineering"]
    
    convert_dict = {depts[i]:readable[i] for i in range(len(depts))}
    return convert_dict[dept_name]

def general_to_conditioned_df(general_df, condition):
    """Given a general dataframe, converts it to a "conditioned" instructor, course, or term-based
    dataframe where each row represents a class.
    
    Arguments:
        general_df {DataFrame} -- The raw dataframe imported as a csv from the capes dataset
        condition {String} -- The condition to organize the dataframe. Must be "Instructor",
        "Course", or "Term"
    
    Returns:
        dataframe -- the conditioned dataframe
    """
    assert condition in ["Instructor", "Course", "Term"]
    
    class_cols = general_df.columns.values.tolist()
    if condition == "Instructor":
        cols_to_remove = ["Course", "Term"]
    elif condition == "Course":
        cols_to_remove = ["Instructor", "Term"]
    else:
        cols_to_remove = ["Instructor", "Course"]
    
    for col in cols_to_remove:
        class_cols.remove(col)
    final_df = pd.DataFrame(columns = class_cols)
    
    conditioned_df = general_df.drop(cols_to_remove, axis = 1)
    labels = general_df[condition].drop_duplicates().values.tolist()
    for label in labels:
        label_df = conditioned_df[getattr(conditioned_df,condition) == label]
        for criteria in ['RcmndClass', 'RcmndInstr', 'StudyHrs/wk', 'AvgGradeExpected', 'AvgGradeReceived']:
            label_df[criteria] = label_df[criteria] * label_df["EvalsMade"]
        label_avg = label_df.sum(axis=0)
        for criteria in ['RcmndClass', 'RcmndInstr', 'StudyHrs/wk', 'AvgGradeExpected', 'AvgGradeReceived']:
            label_avg[criteria] = label_avg[criteria]/label_avg['EvalsMade'] 
        label_avg[condition] = label
        final_df = final_df.append(label_avg, ignore_index = True)
        
    return final_df

def generate_cache():
    """This generates cached course, instructor, and term centric dataframes for
       each department csv at UCSD it populates the CAPES_Cache folder with .pkl files
       containing formatted pandas dataframes
    """

    cache_loc = "./CAPES_Cache"
    csv_loc = "../data/csv/cape"
    for root, dirs, files in os.walk(csv_loc):
        i=1
        for f in files:
            print(f)
            print("{}/{}".format(i,len(files)))
            df = csv_to_dataframe(os.path.join(csv_loc,f), True)
            df.to_pickle(os.path.join(cache_loc, f.replace(".csv","")+"_df.pkl"))
            class_df = general_to_conditioned_df(df, "Course")
            class_df.to_pickle(os.path.join(cache_loc, f.replace(".csv","")+"_df_class.pkl"))
            prof_df = general_to_conditioned_df(df,"Instructor")
            prof_df.to_pickle(os.path.join(cache_loc, f.replace(".csv","")+"_df_prof.pkl"))
            term_df = general_to_conditioned_df(df,"Term")
            term_df.to_pickle(os.path.join(cache_loc, f.replace(".csv","")+"_df_term.pkl"))
            i+=1

