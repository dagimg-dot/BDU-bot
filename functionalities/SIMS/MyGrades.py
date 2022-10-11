from bot import bot
from selenium.webdriver.common.by import By
from util.keyboard_buttons import buttons
from util.message_cleaner import cleaner

# web = driver_transfer()

def My_Grades(message,sent_msg,web):
    # print(type(web))
    try:
        web.find_element(
            By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt63").click()

        courseTitle = web.find_elements(
            By.XPATH, "//div[1]/table/tbody/tr/td[2]/div")
        grade = web.find_elements(
            By.XPATH, "//div[1]/table/tbody/tr/td[4]/div")

        grade_list = {}
        for i in range(1,len(courseTitle)):
            temp_data = {courseTitle[i].text: grade[i].text}
            grade_list.update(temp_data)

        full_str = "\n".join("{}\t\t{}".format(v, k)
                            for k, v in grade_list.items())
        bot.send_message(message.chat.id, full_str,reply_markup=buttons("s_login"))
        cleaner(sent_msg)
        # bot.delete_message(sent_msg.chat.id,sent_msg.message_id)
    except Exception:
        sent_msg_error = "The database is being updated, please try agian later"
        bot.send_message(message.chat.id,sent_msg_error,reply_markup=buttons("s_login"))
        cleaner(sent_msg)
        # bot.delete_message(sent_msg.chat.id,sent_msg.message_id)