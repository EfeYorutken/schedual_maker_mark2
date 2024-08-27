# What Is schedual_maker_mark2
It is an CLI tool for creating and sorting scheduals basend on user defined
criteria.

# How to Use It
Run the command `python main.py fix` to get the config file, `config.json`. This
is the file which will allow the user to configure how the data regarding different
courses.

> NOTE : schedual_maker was made for student use in mind. Hence, while the application can bu used for any kind of schedualing work, the terms in this readme will be focused on students

## Config
### config.json
- the collumn names in the CSV file can be indicated in the config file. Find the key in the JSON file that corresponds to the collumn and change the value it is mapped to in order to do so
- file name
    - this is the name of the file that contains the data for the events
    - the file needs to be in the CSV format
- wanted_cols
    - stands for wanted collumns
    - allows the user to indicate the collumns that will be involved in the schedual creation and sorting process
    - Code : for the code of the course, CMPE123, BA330, ECON101 etc
    - schedual: for the times the course will take place in a given day. The schedual must be given in the format of DayOfTheWeek begin - end DayOfTheWeek begin - end
    - section: for the section of the course
    - extras are for collumns that you want used in the sorting process
    - each filed under extras follows the same convetion as the other keys, the name by which you want to refer to them mapped to the collumn name in the CSV file
- out_file : when the scheduals are created and sorted, whey will be logged into an output file, this field dictates the name of that file
- needed_courses : this is a list of courses that you have to take. Scheduals that will be created will have all of these courses
    - if no course is indicated to be needed, all the courses in the courses, all of the given courses will be considered as needed
- wanted_courses : courses that would be nice to have like electives

### functions.py
- this is the file where you can represent the criteria for a good schedual
- you can write python functions here which take in a list of courses which will represent your schedual.
- each course have the following fields
    - code : code of the course
    - times : a dictionary that maps from the day of the week (in 2 letter format, Mo, We etc)
    - section : section code of the course
    - extra_fileds : a dictionary that maps from the names of the attributes you have specified in the extras filed in the config.json to their values
- you can access all of these fileds in the functions.py file
- all the functions you write here must return a boolean value. At the sorting phase, all of the functions in this file will be called and each time a function, given a schedual, returns true the scedual will have another point. Based on their points, the scheduals will be sorted

# Example Use
1. downloaded the courses that will offered this semester and made sure the files is in csv format
1. in the config.json file make sure to indicate the code, schedual and section columns in the CSV file along with the file that has the data about the courses
```json
{
	"file_name":"corses.csv",
	"wanted_cols":{
		"Code": "Code",
		"Schedule" : "Schedule",
		"Section" : "Section",
```
1. There are a few collumns outside of the ones that are required that I want to use during the sorting process, I indicate them in the extras field
```json
		"extras": {
			"prof" : "Lecturer",
			"success" : "Succesfull"
		}
```
1. I indicate the name of the output file
```json

	"out_file" : "programs.txt",
```
1. Finally indicate the courses you have to take and the courses you would like to take
```json
	"needed_courses":[
		"CMEP123",
		"CMEP345",
		"PRoG442"
	],
	"wanted_courses":[
		"CMPE 492-O"
	]
```
1. Now that the cofiguration is done, go the the functions.py file. Lets say you want courses that are given by the professors John Doe and Jane Doe. We can write a function that itterates over the list of courses and returns true if all the courses are given by one of these 2
```python
def given_by_does(program):
    for course in program:
        if course.extra_fileds["prof"] not in ["John Doe", "Jane Doe"]:
            return False
    return True
```
1. You also might want not to have any courses on Tuesdays, you can check for that too
```python
def no_cours_on_tu(program):
    for course in program:
        if "Tu" in list(course.times.keys()):
            return False
    return True
```
1. Once you have written the functions for your criteria and written the configs, run `python main.py` and you will have your schedules
