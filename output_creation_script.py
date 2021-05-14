'''
This script uses three csv files to generate output csv files that can be directly uploaded to the course table importer
in order to update the course table on undergraduate and graduate courses page on cs.stonybrook.edu

The three csv files needed for this script need to be in the same directory as this script
1) Fall2021.csv - Now this csv is for all CSE/ISE ugrad and grad courses and their details for fall 2021 semester.
                  Make sure to replace this file with the file for current semester.

2) scraped_course_table_ugrad.csv - This file will be generated from the scrape_course_table.py script. The file initially
                  generated will be called scraped_course_table.csv. You should rename it to scraped_course_table_ugrad
                  if you assigned the undergraduate courses link to the link_to_scrape variable.

2) scraped_course_table_grad.csv - This file will be generated from the scrape_course_table.py script. The file initially
                  generated will be called scraped_course_table.csv. You should rename it to scraped_course_table_grad
                  if you assigned the graduate courses link to the link_to_scrape variable.

Author - Atharva Kadam
Date - 23rd April 2021
Contact me if you need help with setup. You can contact me at contact@atharvakadam.com

Library requirements:
1) Pandas - https://pandas.pydata.org/docs/index.html
2) Numpy - https://numpy.org/doc/stable/
'''
import pandas as pd
import numpy as np
import sys
import os


'''
Set the current_sem_filename variable to the name of the csv file containing all the details about the courses
that are being taught this current semester. You can check if format is correct by comparing your file with the
Fall2021.csv semester file.

This step is important as it will NOT work if - 
1) you dont have the file in the same directory
2) you dont have assign the name of the file correctly
3) Format of the file is incorrect.
'''

# current_sem_filename = 'Fall_2021.csv'
def get_courses_arr(current_sem_filename):
    upcom_sem_df = pd.read_csv(current_sem_filename)
    upcom_sem_df['course_num'] = upcom_sem_df['Subj'] + upcom_sem_df['CRS']
    courses = upcom_sem_df['course_num'].unique()
    courses = np.delete(courses, np.where(courses == '  '))

    '''
    The three variables:
    1) undergrad_cs_courses - names of all undergrad CSE courses being taught this semester
    2) grad_cs_courses - names of all grad CSE courses being taught this semester
    3) ise_courses - names of all ISE courses being taught this semester
    '''
    undergrad_cs_courses = []
    grad_cs_courses = []
    ise_courses = []
    for course in courses:
      if 'CSE' in course:
        if int(course.split()[1]) > 500:
            grad_cs_courses.append(course)
        else:
            undergrad_cs_courses.append(course)
      else:
        ise_courses.append(course)

    return undergrad_cs_courses, grad_cs_courses, ise_courses

'''
This function takes in two variables:
1) undergrad_cs_courses - the undergrad_cs_courses variable created above
2) current_sem - A string of the name of current sem (examples - 'Fall2021.csv', 'Spring2022.csv')
This function when ran uses the scraped_course_table_ugrad.csv to generate the output file.This file will be generated 
from the scrape_course_table.py script. The file initially generated will be called scraped_course_table.csv. You should 
rename it to scraped_course_table_ugrad if you assigned the undergraduate courses link to the link_to_scrape variable

It will generate the output file in the same directory as this script.

The output file will be called output_ugrad_currentsem.csv where currentsem will be replaced by the value of the
parameter you pass in for 'current_sem'.
'''
def undergrad(undergrad_cs_courses, current_sem, file_name):
    scraped_course_table_df = pd.read_csv(file_name)
    all_ugrad_courses = scraped_course_table_df['course_name']
    undergrad_cs_courses = [x.split()[0] + x.split()[1] for x in undergrad_cs_courses]

    semester_5 = []
    for course in all_ugrad_courses:
        # print(course)
        if course == 'CSE390-394':
            if 'CSE390' in undergrad_cs_courses or 'CSE391' in undergrad_cs_courses or 'CSE392' in undergrad_cs_courses or 'CSE393' in undergrad_cs_courses or 'CSE394' in undergrad_cs_courses:
                semester_5.append('✔')
            else:
                semester_5.append(' ')
        elif course == 'CSE190-192':
            if 'CSE190' in undergrad_cs_courses or 'CSE191' in undergrad_cs_courses or 'CSE192' in undergrad_cs_courses:
                semester_5.append('✔')
            else:
                semester_5.append(' ')
        else:
            if course in undergrad_cs_courses:
                semester_5.append('✔')
            else:
                semester_5.append(' ')

    scraped_course_table_df['semester_5'] = semester_5
    # print(scraped_course_table_df)
    scraped_course_table_df.drop('semester_0', axis=1, inplace=True)
    scraped_course_table_df.rename(columns={'semester_1': 'semester_0',
                                            'semester_2': 'semester_1',
                                            'semester_3': 'semester_2',
                                            'semester_4': 'semester_3',
                                            'semester_5': 'semester_4'}, inplace=True)

    scraped_course_table_df.fillna(' ', inplace=True)
    scraped_course_table_df.replace('✔', '&#10004', inplace=True)
    # print(scraped_course_table_df)
    departments = []
    course_number = []
    course_id = []
    for course in scraped_course_table_df['course_name']:
        if course == 'CSE390-394':
            # print('CSE390-394	')
            departments.append('CSE')
            course_number.append('390')
            course_id.append('CSE390 - CSE 394ROW')
            # course_id.append('CSE39XROW')
        elif course == 'CSE190-192':
            # print('CSE190-192')
            departments.append('CSE')
            course_number.append('190')
            course_id.append('CSE190 - CSE 192ROW')
            # course_id.append('CSE19XROW')
        else:
            departments.append('CSE')
            course_num = course[3:]
            course_number.append(course_num)
            course_id.append('CSE' + course_num + 'ROW')
    # print(course_number)
    # print(course_id)
    # print(len(course_number))
    scraped_course_table_df['Course ID'] = course_id
    scraped_course_table_df['Department'] = departments
    scraped_course_table_df['Course Number'] = course_number
    scraped_course_table_df.rename(columns={'course_name': 'Course Name',
                                            'course_description': 'Course Description',
                                            'semester_0': 'Semester 0',
                                            'semester_1': 'Semester 1',
                                            'semester_2': 'Semester 2',
                                            'semester_3': 'Semester 3',
                                            'semester_4': 'Semester 4',
                                            }, inplace=True)
    scraped_course_table_df = scraped_course_table_df[['Course ID', 'Department', 'Course Number', 'Course Name', 'Course Description', 'Semester 0', 'Semester 1',
         'Semester 2', 'Semester 3', 'Semester 4']]
    # scraped_course_table_df.to_csv('output_ugrad_Fall2021.csv', index=False)
    output_file_name = 'output_ugrad_' + current_sem + '.csv'
    scraped_course_table_df.to_csv(output_file_name, index=False)
    # print(scraped_course_table_df)
    print('Created output_ugrad_' + current_sem + '.csv file in current directory.')


'''
This function takes in two variables:
1) grad_cs_courses - the grad_cs_courses variable created above
2) current_sem - A string of the name of current sem (examples - 'Fall2021.csv', 'Spring2022.csv')
This function when ran uses the scraped_course_table_grad.csv to generate the output file.This file will be generated 
from the scrape_course_table.py script. The file initially generated will be called scraped_course_table.csv. You should 
rename it to scraped_course_table_grad if you assigned the undergraduate courses link to the link_to_scrape variable

It will generate the output file in the same directory as this script.

The output file will be called output_grad_currentsem.csv where currentsem will be replaced by the value of the
parameter you pass in for 'current_sem'.
'''
def grad(grad_cs_courses, current_sem, file_name):
    scraped_course_table_df = pd.read_csv(file_name)
    all_grad_courses = scraped_course_table_df['course_name']
    grad_cs_courses = [x.split()[0] + x.split()[1] for x in grad_cs_courses]
    semester_5 = []
    for course in all_grad_courses:
        if course in grad_cs_courses:
            semester_5.append('✔')
        else:
            semester_5.append(' ')
    scraped_course_table_df['semester_5'] = semester_5
    scraped_course_table_df.drop('semester_0', axis=1, inplace=True)
    scraped_course_table_df.rename(columns={'semester_1': 'semester_0',
                                            'semester_2': 'semester_1',
                                            'semester_3': 'semester_2',
                                            'semester_4': 'semester_3',
                                            'semester_5': 'semester_4'}, inplace=True)
    scraped_course_table_df.fillna(' ', inplace=True)
    scraped_course_table_df.replace('✔', '&#10004', inplace=True)
    departments = []
    course_number = []
    course_id = []
    for course in scraped_course_table_df['course_name']:
        departments.append('CSE')
        course_num = course[3:]
        course_number.append(course_num)
        course_id.append('CSE' + course_num + 'ROW')

    scraped_course_table_df['Course ID'] = course_id
    scraped_course_table_df['Department'] = departments
    scraped_course_table_df['Course Number'] = course_number

    scraped_course_table_df.rename(columns={'course_name': 'Course Name',
                                            'course_description': 'Course Description',
                                            'semester_0': 'Semester 0',
                                            'semester_1': 'Semester 1',
                                            'semester_2': 'Semester 2',
                                            'semester_3': 'Semester 3',
                                            'semester_4': 'Semester 4',
                                            }, inplace=True)
    scraped_course_table_df = scraped_course_table_df[['Course ID', 'Department', 'Course Number', 'Course Name', 'Course Description', 'Semester 0', 'Semester 1',
         'Semester 2', 'Semester 3', 'Semester 4']]
    output_file_name = 'output_grad_' + current_sem + '.csv'
    scraped_course_table_df.to_csv(output_file_name, index=False)
    print('Created output_grad_' + current_sem + '.csv file in current directory.')

'''
Simple two calls to the functions created above with the current semester passed in generates expected output files
for any given current semester.

Replace the second parameter with the current semester name (examples - Spring2022, Fall2023 etc.)
'''


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) < 5:
        print('Please run the script again after providing all three arguments in the correct order: \n'
              'Argument Number 1: Current Semester File Name\n'
              'Argument Number 2: Scraped File Name \n'
              'Argument Number 3: Current Semester Name \n'
              'Argument Number 4: grad/undergrad \n'
              'Example : python scrape_course_table.py <sem_file_name> <scraped_file_name> <current_sem_name> <grad/undergrad>')
    else:
        if os.path.isfile(arguments[1]):
            undergrad_cs_courses, grad_cs_courses, ise_courses = get_courses_arr(arguments[1])
            if arguments[4] == 'grad':
                if os.path.isfile(arguments[2]):
                    grad(grad_cs_courses, arguments[3], arguments[2])
                else:
                    print("No such file: ", arguments[2], '! Please check and run the script again.')
            elif arguments[4] == 'undergrad':
                if os.path.isfile(arguments[2]):
                    undergrad(undergrad_cs_courses, arguments[3], arguments[2])
                else:
                    print("No such file: ", arguments[2], '! Please check and run the script again.')
            else:
                print("Check your input and run the program again")
        else:
            print("No such file: ", arguments[1], '! Please check and run the script again.')