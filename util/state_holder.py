from util.useful_lists import OpenWeb


def state_changer(page):
    for key,value in OpenWeb.items():
        if key == page:
            OpenWeb[page] += 1
        else:
            OpenWeb[key] = 0

