import re
from bot import bot
from functionalities.GPA_Prediction.reverse_gpa_calc import rev_gpa_calc
from util.interrupter import step_canceler
from util.message_cleaner import cleaner

def course_display(course_title,credit):
    course_list = {}
    for i in range(len(course_title)):
        temp_data = {course_title[i]: credit[i]}
        course_list.update(temp_data)

    full_str = "\n".join("{}\t\t{}".format(v, k)
                        for k, v in course_list.items())
    return full_str


def GPA_validator(message,course_title,credit,sent_msgR):
    if message.text == '/x':
        step_canceler(message)                                                                              
    else:
        sent_msgC = "Validating . . ."
        bot.edit_message_text(sent_msgC,sent_msgR.chat.id,sent_msgR.message_id)
        user_gpa = message.text
        cleaner(message)
        split_u_gpa = re.split(r'[,\s]',user_gpa)

        split_filter = list(filter(None,split_u_gpa))
        split_float = []

        if len(split_filter) != 2:
            sent_msgD = "Invalid number of GPAs, please enter two GPAs again"
            bot.edit_message_text(sent_msgD,sent_msgR.chat.id,sent_msgR.message_id)
            bot.register_next_step_handler(sent_msgR,GPA_validator,course_title,credit,sent_msgR)
        else:
            for i in range(len(split_filter)):
                if split_filter[i].replace('.','',1).isdigit() == True:
                    split_float.append(float(split_filter[i]))
        
                    if split_float[i] <= 0 or split_float[i] > 4:
                        sent_msgD = "The GPAs you entered should be 0 - 4, please enter GPAs again"
                        bot.edit_message_text(sent_msgD,sent_msgR.chat.id,sent_msgR.message_id)
                        bot.register_next_step_handler(sent_msgR,GPA_validator,course_title,credit,sent_msgR)
                    else:
                        if len(split_float) == 2:
                            sorted_gpa = sorted(split_float)
                            if sorted_gpa[1]-sorted_gpa[0] > 0.5:
                                sent_msgD = "The range is too broad, please enter GPAs again"
                                bot.edit_message_text(sent_msgD,sent_msgR.chat.id,sent_msgR.message_id)
                                bot.register_next_step_handler(sent_msgR,GPA_validator,course_title,credit,sent_msgR)
                            elif sorted_gpa[1] == sorted_gpa[0]:
                                sent_msgD = "It's not advisable to input equal GPAs, please enter GPAs again"
                                bot.edit_message_text(sent_msgD,sent_msgR.chat.id,sent_msgR.message_id)
                                bot.register_next_step_handler(sent_msgR,GPA_validator,course_title,credit,sent_msgR)
                            else:
                                rev_gpa_calc(message,course_title,credit,sorted_gpa)
                        else:
                            continue
                else:
                    sent_msgD = "Invalid GPAs, please enter GPAs again"
                    bot.edit_message_text(sent_msgD,sent_msgR.chat.id,sent_msgR.message_id)
                    bot.register_next_step_handler(sent_msgR,GPA_validator,course_title,credit,sent_msgR)
                    break
    