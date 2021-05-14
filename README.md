# CourseTableScraper
Scrapes Course Table from Graduate/Undergraduate Courses WebPage and generates output csv file of the specified format

## Download Chromedriver
To download this
1) Open Google Chrome and then open settings
2) Click on 'About Chrome' and check the version of your chrome
3) Then visit https://sites.google.com/a/chromium.org/chromedriver/downloads
4) Click on the link corresponding to your version of chrome
5) Click to download whichever zip file corresponds to your operating sytem. Mac users click on the mac link and the same for windows and linux users.
6) After downloading, copy the path of your chromedriver executable and use it for running the scrape_course_table.py script as mentioned in the instructions below.

## Download Python

To download python visit - https://www.python.org/ and the Downloads section
After download, decompress/unzip and run through the installations steps.

If you are using windows and have any issues downloading/running python then refer to -
1) https://docs.microsoft.com/en-us/windows/python/beginners\
2) https://docs.python.org/3/using/windows.html

Then install the following dependencies using pip command - 
1) Selenium (Link: https://selenium-python.readthedocs.io/)
```
pip install selenium
```
2) Pandas(This will also install numpy) (Link: https://pandas.pydata.org/docs/index.html)
```
pip install pandas
```

## Run the scrape_course_table.py script
To run the script, you need 3 arguments

Argument Number 1: Chromedriver path (The path of your chromedriver executable that you copied initally)
Argument Number 2: Link to Scrape (The link to the graduate courses or undergraduate courses webpage)
Argument Number 3: grad/undergrad (This flag tells the script whether the link_to_scrape is for graduate or undergraduate webpage)

```
python scrape_course_table.py <chromedriver_path> <link_to_scrape> <grad/undergrad>
```

Example run :
```
 python scrape_course_table.py /Users/aiuser/Desktop/chromedriver https://www.cs.stonybrook.edu/students/Graduate-Studies/courses grad
```

After this script is run, based on which flag you entered you will get an output csv file named scraped_course_table_grad.csv(Graduate Courses) or scraped_course_table_ugrad.csv(Undergraduate Courses)

You will need this and the Fall_2021.csv(This csv file will be replaced with the csv file with current semester. Example - Fall_2022.csv,Spring_2023.csv etc) to run the output_creation_script.py

##Running the output_creation_script.py file

To run the script, you need 4 arguments

Argument Number 1: Current Semester File Name - (Name of the info csv file for current semester(Fall_2021.csv or Spring_2022.csv etc.)
Argument Number 2: Scraped File Name - (The name of the file generated from the previous step(scraped_course_table_ugrad.csv or scraped_course_table_grad.csv)
Argument Number 3: Current Semester Name - (Name of the current semester(This is the name you want your ouptut file to go by)
Argument Number 4: grad/undergrad - (This flag tells the script whether the scraped file is for graduate or undergraduate webpage)

```
  python scrape_course_table.py <sem_file_name> <scraped_file_name> <current_sem_name> <grad/undergrad>'
```

Example run :
```
 python output_creation_script.py Fall_2021.csv scraped_course_table_grad.csv Fall_2021 grad 
```

After this script is run, based on which flag you entered you will get an output csv file named output_grad_<sem_name>.csv(Graduate Courses) or output_ugrad_<sem_name>.csv(Undergraduate Courses)

Note - If files are not in the same directory then make sure that you input the paths correctly
