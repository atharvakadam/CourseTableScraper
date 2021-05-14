'''
This script uses Selenium(with Chromedriver) to scrape course table from the Stony Brook Computer Science website
You can use it to generate a course table csv file for each of the tables scraped. Run it separately for the undergrad
and the grad course tables.

Author - Atharva Kadam
Date - 23rd April 2021
Contact me if you need help with setup. You can contact me at contact@atharvakadam.com

Library requirements:
1) Selenium - https://selenium-python.readthedocs.io/
2) Pandas - https://pandas.pydata.org/docs/index.html
'''
from selenium import webdriver
import pandas as pd
import time
import sys

def scrape_table(chromedriver_path, link_to_scrape):
    '''
    Make sure the path for your chromedriver is correct. You will need Chromedriver corresponding to your own
    machine. If you dont have a chromedriver install it here - https://sites.google.com/a/chromium.org/chromedriver/downloads

    After downloading, make sure the chromedriver_link variable has the correct path
    '''
    mydriver = webdriver.Chrome(chromedriver_path)


    '''
    The link_to_scrape variable will have the link from which we want to scrape the course table. Try to avoid unsecure
    links. But if you do work with it then add a time.sleep() command so that you can get enough time to bypass the security
    option on your browser 
    
    As you can see there are two different links we can work with. So we can do either -
    1) Uncomment the first one and comment the second one if you want to scrape undergraduate CSE courses.
    OR
    2) Uncomment the second one and comment the first one if you want to scrape undergraduate CSE courses.
    
    Default is set to grad CSE courses link.
    '''
    mydriver.get(link_to_scrape)

    '''
    Uncomment next line(time.sleep) if you are accessing a link which isnt secure. this way it will give you time
    to proceed to the site from the unsecure warning that is prompted in the browser.
    '''
    # time.sleep(10)

    '''
    Make sure that it is working correctly by printing the title. If it doesnt print it correctly, something is wrong.
    '''
    # print(mydriver.title)

    '''
    Extract the tbody - table body element and then extract all rows(tr). Then iterate over these
    tr elements and extract by class name. Do this for every element you want to extract. In this case, we need
    1) course_names - name of the course
    2) course_description - description of the course
    3) semester_0s - if the course was taught in semester 0 then ✔ else nothing.
    4) semester_1s - if the course was taught in semester 1 then ✔ else nothing.
    5) semester_2s - if the course was taught in semester 2 then ✔ else nothing.
    6) semester_3s - if the course was taught in semester 3 then ✔ else nothing.
    7) semester_4s - if the course was taught in semester 4 then ✔ else nothing.
    So we will create a list for each of the above listed attributes and add to it as we iterate through all the rows.
    '''
    tbody_tag = mydriver.find_element_by_tag_name('tbody')
    # tr_xpath = mydriver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/div[1]/div/div/div/div/div[2]/table/tbody/tr[1]')
    child_elements = tbody_tag.find_elements_by_xpath('.//tr')

    course_names = []
    course_descriptions = []
    semester_0s = []
    semester_1s = []
    semester_2s = []
    semester_3s = []
    semester_4s = []

    for child_elem in child_elements:
        # tds = child_elem.find_elements_by_xpath('.//td')
        course_name = child_elem.find_element_by_xpath(".//*[@class='views-field views-field-field-course-name']").text
        course_description = child_elem.find_element_by_xpath(".//*[@class='views-field views-field-field-course-description']").text
        semester_0 = child_elem.find_element_by_xpath(".//*[@class='views-field views-field-field-semester-0']").text
        semester_1 = child_elem.find_element_by_xpath(".//*[@class='views-field views-field-field-semester-1']").text
        semester_2 = child_elem.find_element_by_xpath(".//*[@class='views-field views-field-field-semester-2']").text
        semester_3 = child_elem.find_element_by_xpath(".//*[@class='views-field views-field-field-semester-3']").text
        semester_4 = child_elem.find_element_by_xpath(".//*[@class='views-field views-field-field-semester-4']").text
        course_names.append(course_name)
        course_descriptions.append(course_description)
        semester_0s.append(semester_0)
        semester_1s.append(semester_1)
        semester_2s.append(semester_2)
        semester_3s.append(semester_3)
        semester_4s.append(semester_4)


    '''
    These are verification print statements. Comment them out if you want.
    '''
    # print(tbody_tag)
    # # print(tr_xpath)
    # print(len(child_elements))
    # print(child_elements)

    '''
    Let us create a dataframe and add these lists as columns in our dataframe
    '''
    scraped_df = pd.DataFrame()
    scraped_df['course_name'] = course_names
    scraped_df['course_description'] = course_descriptions
    scraped_df['semester_0'] = semester_0s
    scraped_df['semester_1'] = semester_1s
    scraped_df['semester_2'] = semester_2s
    scraped_df['semester_3'] = semester_3s
    scraped_df['semester_4'] = semester_4s
    return scraped_df

'''
Make sure your dataframe is printed correctly. The output csv file will be in the same directory as this script.
Remember to change the name of the csv file to indicate whether it is for undergrad or grad.
For undergrad - change the name of the file to scraped_course_table_ugrad.csv
For grad - change the name of the file to scraped_course_table_grad.csv
'''
if __name__ == '__main__':
    # chromedriver_link = '/Users/atharvakadam/Desktop/chromedriver'
    # # link_to_scrape = "https://www.cs.stonybrook.edu/students/Undergraduate-Studies/csecourses"
    # link_to_scrape = "https://www.cs.stonybrook.edu/students/Graduate-Studies/courses"
    # print("Args: ", sys.argv)
    arguments = sys.argv
    if len(arguments) < 4:
        print('Please run the script again after providing all three arguments in the correct order: \n'
              'Argument Number 1: Chromedriver path \n'
              'Argument Number 2: Link to Scrape \n'
              'Argument Number 3: grad/undergrad \n' 
              'Example : python scrape_course_table.py <chromedriver_path> <link_to_scrape> <grad/undergrad>')
    else:
        scraped_df = scrape_table(arguments[1], arguments[2])
        print(scraped_df)
        output_file_name = 'scraped_course_table_'
        if arguments[3] == 'grad':
            output_file_name += 'grad.csv'
        elif arguments[3] == 'undergrad':
            output_file_name += 'ugrad.csv'
        print("Scraped table saved to ", output_file_name)
        scraped_df.to_csv(output_file_name, index=False)



