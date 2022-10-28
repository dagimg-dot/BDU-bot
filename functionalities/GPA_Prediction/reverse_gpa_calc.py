import itertools as it
import math
import random
from functionalities.GPA_Prediction.display_reverse import display_final
from util.useful_lists import rev_grade_list
from util.user_database import users



def random_grade_generator(course_title):
    rand_grade_list = []
    for i in range(len(course_title)):
        grade = random.choice(list(rev_grade_list.keys()))
    # grade = random.choice(list(it.combinations_with_replacement(list(rev_grade_list.keys()), len(course_title))))
        rand_grade_list.append(grade)
    return rand_grade_list
    # return grade

def rev_gpa_calc(message,course_title,credit,sorted_u_gpa):
    global count, count2
    count = -1
    count2  = 0
    while count < 5:
        credit_sum = sum(credit)
        tot_sum = 0
        rand_gr = random_grade_generator(course_title)
        for i in range(len(rand_gr)):
            tot_sum += credit[i]*rev_grade_list[rand_gr[i]]

        tot_sum_rounded = round(tot_sum, 2)
        finder(message,tot_sum_rounded,credit_sum, rand_gr, course_title,sorted_u_gpa)


def finder(message,tot_sum_rounded,credit_sum, rand_gr, course_title,u_gpa):
    
    global count, count2
    count2 += 1
    if tot_sum_rounded >= u_gpa[0]*credit_sum and tot_sum_rounded <= u_gpa[1]*credit_sum:
        count += 1
        gpa = tot_sum_rounded/credit_sum
        collector(message,rand_gr,course_title,gpa,count)
    else:
        max_perm = math.pow(len(rev_grade_list),len(course_title))
        if count == 0 and count2 == max_perm:
            print("Nothing Found try again with different GPA")
            exit()

def collector(message,rand_gr,course_title,gpa,count):
    users[message.from_user.id].gpa_list.append(gpa)
    users[message.from_user.id].possibility_dict[count] = {}
    for j in range(len(course_title)):
        temp_data = {course_title[j]: rand_gr[j]}
        users[message.from_user.id].possibility_dict[count].update(temp_data)

    if len(users[message.from_user.id].possibility_dict) == 5:
        display_final(message)


