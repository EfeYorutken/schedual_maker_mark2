from course import *
import sys
import inspect

#anything from here to the get_crits function can be changed

def program_begins_after_10(p):
    
    for c in p:
        for day in c.times:
            if c.times[day][0] < 10:
                return False
    return True

def program_ends_before_17(p):
    for c in p:
        for day in c.times:
            if c.times[day][1] > 17:
                return False
    return True

def program_has_a_break_of_length_1(program):
    mo = [c.times["Mo"] for c in program if "Mo" in c.times]
    tu = [c.times["Tu"] for c in program if "Tu" in c.times]
    we = [c.times["We"] for c in program if "We" in c.times]
    th = [c.times["Th"] for c in program if "Th" in c.times]
    fr = [c.times["Fr"] for c in program if "Fr" in c.times]

    days = [mo,tu,we,th,fr]

    for day in days:
        day.sort(key = lambda x : x[0])

    for day in days:
        for i in range(len(day)-1):
            if day[i+1][0] - day[i][1] > 0:
                return True

    return False

# this function will return all the functions defined in this module
def get_crits():
    fns = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    return [f[1] for f in fns if f[0] != "get_crits"]
