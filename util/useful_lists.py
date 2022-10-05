import json

menu = ["Login", "Predict GPA"]
success_login = ["My Courses", "My Status", "My Grades", "My Dormitory"]
MyC = ["All Courses", "Courses given on a specific year",
       "Courses given on a specific semester"]
MyS = ["Cumulative GPA - CGPA", "Semester GPA - SGPA", "Semester Grades"]

Buttons = menu + success_login + MyC + MyS + ["Back", "Back to Menu"]

buttons_clicked = []

master_check = ['0']


cardinal_ordinal = {
    1: 'first',
    2: 'second',
    3: 'third',
    4: 'fourth',
    5: 'fifth',
    6: 'sixth',
    7: 'seventh',
}

with open('util\Dept\dept_list.json') as f:
    data = json.load(f)

dept_title =  []
for i in range(len(data)):
    dept_title.append(data[i]['Department Title'])