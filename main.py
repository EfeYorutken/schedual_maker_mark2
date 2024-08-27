from course import *
import pandas as p
import json
import functions
from tabulate import *
from graph import *
import sys

print(sys.argv)

if sys.argv[1] == "fix":
    configs = """
{
	"file_name":"corses_csv.csv",
	"wanted_cols":{
		"Code": "Code",
		"Schedule" : "Schedule",
		"Section" : "Section",
		"extras": {
			"prof" : "Lecturer",
			"room" : "Room"
		}
	},
	"out_file" : "programs.txt",
	"needed_courses":[
		"CMPE 399",
		"CMPE 421",
		"CMPE 472",
		"CMPE 491"
	],
	"wanted_courses":[
		"CMPE 492-O"
	]
}
    """
    with open("config.json", "w") as f:
        f.write(configs)
    exit(0)

def impossiblity_termination(msg="exiting due to unconstructable program"):
    sys.stderr.write(msg)
    exit(0)

def find_same(arr):
    m = {}
    for i in range(len(arr)):
        if not arr[i] in m:
            m[arr[i]] = i
        else:
            return [m[i], i]
    return []

def seperate(arr, i, j):
    r1 = [x for x in arr if arr.index(x) != i]
    r2 = [x for x in arr if arr.index(x) != j]

    return [r1,r2]


#converts a list of courses into a string which looks like a table
#school_begin and school_end are the hours (in army time) for which the table will span
#in other words school_begin should be the time of the earliest possible class
#and school_end should be the latest houre a course can begin + 1 (due to how range function works)
def show(program, school_begin=9, school_end=21):

    res = []

    #seperate the courses in the list based on the days they are on
    mapping = {
            "Mo" : [x for x in program if "Mo" in x.times.keys()],
            "Tu" : [x for x in program if "Tu" in x.times.keys()],
            "We" : [x for x in program if "We" in x.times.keys()],
            "Th" : [x for x in program if "Th" in x.times.keys()],
            "Fr" : [x for x in program if "Fr" in x.times.keys()]
            }

    #convertin the map to a 2d list so it can be converted into a string
    #for each day in mapping
    for day in mapping.keys():
        #add the day to the end of the list
        res.append([day])
        last = len(res) - 1 #index of the latest added day
        for i in range(school_begin,school_end):
            res[last].append("X")#fill the rest of the list with Xs for each hour a course can begin
        for c in mapping[day]: # for each course in a given day
            #get when the course starst and ends on that day
            begin = c.times[day][0]
            end = c.times[day][1]

            #take the begin time, substract the school_begin time to get how many hours after school begins this course will takes place
            #this number should be the index in the list, but the first element is the day, so time the course begins/ends
            #-begin time + 1 (for the extra element of day at the begining) will give us which "cell" in the table should be filled with the course
            for i in range(begin-school_begin+1,end+1-school_begin):
                res[last][i] = c.code #write the code of the course to the index calculated
    time_headders = ["day"] + [str(x) for x in range(school_begin, school_end)] #clreating the top "label" of the table
    return tabulate(res, headers = time_headders) #return the table formated string

configs = {}
config_file = "config.json"
#wanted courses is also an option

fn_list = functions.get_crits()

print("getting configurations")
try:
    with open(config_file, "r") as f:
        configs = json.loads(f.read())
except Exception as e:
    impossiblity_termination(f"config file named {config_file} not found or is malformed . Rename the existing file or create the default")

file_name = "corses_csv.csv" if configs["file_name"] == None else configs["file_name"]

out_file = "out.txt" if configs["out_file"] == None else configs["out_file"]

config_cols = configs["wanted_cols"]
extra_cols = configs["wanted_cols"]["extras"]
wanted_cols = []

wanted_cols.append(config_cols["Code"])

wanted_cols.append(config_cols["Schedule"])

for col in [x for x in list(extra_cols.values())]:
    wanted_cols.append(col)

print("configurations got")

print(f"reading csv file : {file_name}")
try:
    data = p.read_csv(file_name)
except:
    impossiblity_termination(f"csv file named {file_name} is not found")

print(f"extracting relevant columns : {', '.join([x for x in wanted_cols])}")
data = data.drop([c for c in data.columns if c not in wanted_cols], axis = 1)

all_courses = [course(r[wanted_cols[0]], r[wanted_cols[1]], r[wanted_cols[2]], extra_cols) for _, r in data.iterrows()]

print("extracting relevant courses (all if not stated in the configs)")
needed_courses = configs["needed_courses"]
nice_to_have_courses = configs["wanted_courses"]
wanted_courses = nice_to_have_courses + needed_courses
if len(wanted_courses) != 0:
    all_courses = [x for x in all_courses if x.code in wanted_courses]


#might put this part and the connect_courses_w_fn part to graph
def check(prim, sec):
    return (not course.intersect(prim,sec)) and (not prim.code == sec.code)

g = graph()

print("adding courses to the graph")
g.add_courses(all_courses)

print("constructing all possible programs")
g.connect_courses_w_fn(check)

programs = g.get_progs()
if len(programs) == 0:
    impossiblity_termination("no programs could be created")

print("all possible programs created")

#due to how the get_progrs function works some programs might end up with
#the same course in 2 different sections
#these casese are appropriate time wise, meaning all other courses in the program
#can be taken with either section. for the sake of completeness, multiple programs
#each having one section of the same course need to be created
l = len(programs)
print("seperating programs with duplicate courses")
#while the amount ofdefective programs, which are programs that have the same 
#course in different sections
while len([defective for defective in programs if len(find_same(defective)) > 0]) > 0:
    print(f"\tcurrent program count : {len(programs)}")
    #simplfy this with list comprehension
    for program in programs:
        fs = find_same(program)
        if len(fs) != 0: #to make sure non-defective programs are skipped over
            i = fs[0]#indecies of the courses with the same doce
            j = fs[1]
            s = seperate(program,i,j)
            r1 = s[0]#variatons of the program with no duplicate courses
            r2 = s[1]

            #remove the defective program and add in the non defective one
            programs.remove(program)
            programs.append(r1)
            programs.append(r2)


temp = []
#filter the programs that dont have all the needed courses
if len(needed_courses) != 0:
    print("filtering incomplete programs")
    for program in programs:
        in_prog = [x.code for x in program]
        if all((should in in_prog) for should in needed_courses):
            temp.append(program)

programs = temp

if len(programs) == 0:
    impossiblity_termination("no programs that have all the needed courses could be created the needed courses")

print("all programs ready")

print(f"there are {len(programs)} possible porgrams")

print("sorting programs according to the criteria")

programs.sort(key=lambda x : graph.score_program(x, fn_list))

print(f"best program with a score of {graph.score_program(programs[0],fn_list)} out of {len(fn_list)}")
print(show(programs[0]))

print(f"alternative courses are printed into {out_file}")

with open(out_file, "w") as f:
    for program in programs:
        title = f"Program #{programs.index(program)} : {graph.score_program(program, fn_list)}/{len(fn_list)}\n"
        f.writelines(title + show(program) + "\n"*3)

print(f"all programs writeen to {out_file}")
