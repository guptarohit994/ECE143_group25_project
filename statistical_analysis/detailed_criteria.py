
import helper
import os
import pandas as pd



def calculate_detailed_corr(dept_list):
    """Calculates the correlation of all the criteria with the overall professor rating, using all
    departments specificied in dept_list. This information is printed. Additionally, 
    A dataframe containing the averaged criteria (used as an intermediate tool during calculation)
    is returned.
    
    Arguments:
        dept_list {[String]} -- A list of departments to use
    
    Returns:
        [DataFrame] -- The dataframed containing the averaged criteria
    """
    
    # all the general values we will use
    relevant_general_cols = [
                    "Instructor",
                    "Course",
                    "Term",
                    "Enroll",
                    "EvalsMade",
                    "RcmndClass",
                    "RcmndInstr"
                    ]

    # all the detailed criteria we will use
    relevant_detailed_cols = [
                    "course_material_intellectually_stimulating",
                    "assignments_promote_learning",
                    "required_reading_useful",
                    "course_difficult_relative_others",
                    "exams_representative_course_material",
                    "instructor_displays_proficient_command_material",
                    "instructor_well_prepared_classes",
                    "instructors_speech_clear_audible",
                    "instructor_explains_course_material_well",
                    "lectures_hold_attention",
                    "instructor’s_lecture_style_facilitates_notetaking",
                    "instructor_shows_concern_students_learning",
                    "instructor_promotes_appropriate_questionsdiscussion",
                    "instructor_accessible_outside_class",
                    "instructor_starts_finishes_class_time",
                    "instructor_effective_promoting_academic_integrity",
                    "instructor_practiced_effective_teaching_strategies_acknowledged_valued_differences_among_students_including_differences_race_gender_identity"
                    ]

    # the question levels for CAPES
    question_levels = ["Strongly_Disagree",
                    "Disagree",
                    "Neither_Agree_nor_Disagree",
                    "Agree",
                    "Strongly_Agree",
                    "Not_Applicable"]
    
    detailed_capes_dir = "../data/csv/cape_detailed"
    dept_list_to_use = dept_list
    # minimum evaluations to use (otherwise, the course is discarded)
    min_evals_threshold = 20

    total_corrs = pd.DataFrame(columns=["Criteria", "Corr", "Dept"])
    total_avg_df = pd.DataFrame()

    for dept in dept_list_to_use:
        csv_path = os.path.join(detailed_capes_dir, "cape_{}_auto.csv".format(dept))
        if os.path.exists(csv_path):
            df = pd.read_csv(os.path.join(csv_path))
            
            # generating a dataframe that contains averages of the detailed survey questions
            avg_df = df[relevant_general_cols]
            for detailed_col in relevant_detailed_cols:
                mean_col = df[[detailed_col+"_"+level for level in question_levels]]
                mean_col = (mean_col*[1,2,3,4,5,0]).sum(axis=1)/(mean_col*[1,1,1,1,1,0]).sum(axis=1)
                avg_df[detailed_col+"_mean"] = mean_col
            
            total_avg_df = total_avg_df.append(avg_df)
            
            # computing the correlations between RcmndInstr and all the relevant detailed column means to see which detailed criteria have the strongest correlation with overall instructor recommendation
            dept_corrs = pd.DataFrame(columns=["Criteria", "Corr"])
            for detailed_col in relevant_detailed_cols:
                df = (avg_df[avg_df["EvalsMade"]>min_evals_threshold])[["RcmndInstr",detailed_col+"_mean"]].dropna()
                # converting from percent to float
                df["RcmndInstr"]=  df["RcmndInstr"].apply(lambda x:float(x[:-1]))
                if len(df!=0):
                    dept_corrs = dept_corrs.append({"Criteria":detailed_col,"Corr":df.corr().values[0][1]},ignore_index=True)
            dept_corrs["Dept"] = dept
            total_corrs = total_corrs.append(dept_corrs, ignore_index=True)
    
    print(total_corrs.groupby(['Criteria']).mean().sort_values("Corr"))

    return total_avg_df


def plot_corr_scatter(dept_list):
    """Plots a scatterplot for averaged detailed data
    
    Arguments:
        dept_list {[String]} -- A list of departments to use
    """
    avg_df = calculate_detailed_corr(dept_list)
    criterion = "instructor_starts_finishes_class_time"
    plot_df = avg_df[["RcmndInstr",criterion+"_mean"]]
    plot_df["RcmndInstr"] = plot_df["RcmndInstr"].apply(lambda x:float(x[:-1]))
    ax = plot_df.plot.scatter(x = criterion+"_mean", y = "RcmndInstr")
    ax.set_xlabel("Mean Punctuality Rating", fontsize = 15)
    ax.set_ylabel("Mean Instructor Rec. %", fontsize = 15)
    ax.set_title("ECE Courses", fontsize = 17)
