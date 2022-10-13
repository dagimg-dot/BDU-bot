import json

menu = ["Login", "Predict GPA"]
success_login = ["My Courses", "My Status", "My Grades", "My Dormitory"]
MyC = ["All Courses", "Courses given on a specific year",
       "Courses given on a specific semester"]
MyS = ["Cumulative GPA - CGPA", "Semester GPA - SGPA", "Semester Grades"]

Buttons = menu + success_login + MyC + MyS + ["Back", "Back to Menu"]


OpenWeb = {
    "My Courses": 0,
    "My Status": 0,
    "My Grades": 0,
    "Semester Grades": 0
}
# for i in range(len (Login_func)):
#     temp_data = {Login_func[i]:'0'}
#     OpenWeb.update(temp_data)

Grades = ['A+','a+','A','a','A-','a-','B+','b+','B','b','B-','b-','C+','c+','C','c','C-','c-','D','d','F','f']

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

grade_list = {
    "A+": 4,
    "A": 4,
    "A-": 3.75,
    "B+": 3.5,
    "B": 3,
    "B-": 2.75,
    "C+": 2.5,
    "C": 2,
    "C-": 1.75,
    "D": 1,
    "F": 0
}

with open('util\Dept\dept_list.json') as f:
    data = json.load(f)

dept_title =  []
for i in range(len(data)):
    dept_title.append(data[i]['Department Title'])

