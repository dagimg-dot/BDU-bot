from bot import bot
from util.useful_lists import grade_list


def gpa_calculator(message,credit,splitted_upper):
    tot_sum = 0
    credit_sum = 0
    for i in range(len(splitted_upper)):
        tot_sum += credit[i]*grade_list[splitted_upper[i]]
        credit_sum += credit[i]
    
    GPA = tot_sum / credit_sum
    sent_msg = "Your Predicted GPA is " + str(GPA)
    bot.send_message(message.chat.id,sent_msg)