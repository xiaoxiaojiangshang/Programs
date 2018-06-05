#!/usr/bin/env  python
# coding=utf8

import os
import subprocess
import pytesseract
import urllib
from PIL import Image, ImageOps
import requests
import sys
import importlib
importlib.reload(sys)
ROOT = os.path.dirname(os.path.abspath(__file__))

MAX_RETRY_TIME = 3


def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/autojump.png')
    os.system('adb pull /sdcard/autojump.png .')

def run_command(cmd):
    retry = 0
    while retry < MAX_RETRY_TIME:
        status, output =  subprocess.getstatusoutput(cmd)
        if status != 0:
            retry += 1
            continue
        return status, output


# def capture():
#     cmd = "adb shell /system/bin/screencap -p {}".format(SCREEN_SHOT_PATH)
#     status, output = subprocess.getstatusoutput(cmd)
#     return status
#
#
# def transfer():
#     cmd = "adb pull {} {}".format(SCREEN_SHOT_PATH, LOCAL_SCREEN_PATH)
#     status, output = subprocess.getstatusoutput(cmd)
#     return status


def recognition():
    # file = Image.open(LOCAL_SCREEN_PATH)
    pull_screenshot()
    file = Image.open('autojump.png')
    question_box = file.crop((50, 205, 1100, 560))
    question = pytesseract.image_to_string(question_box, lang='chi_sim')
    question = question[question.index(u'.')+1:]

    """
        回答 TODO:
    """
    answers = []
    """"
    answer_box = file.crop((50, 560, 1100, 1300))
    answer_box = answer_box.convert("RGB")
    pixdata = answer_box.load()
    width, height = answer_box.size
    for y in xrange(height):
        for x in xrange(width):
            if pixdata[x, y] == (230, 235, 239):
                pixdata[x, y] = (255, 255, 255)
            item = pixdata[x, y]
            if (item[0]>=137 and item[0]<= 140) and (item[1]>=144 and item[1]<=185) and (item[2]>=148 and item[2]<=170):
                pixdata[x, y] = (0, 0, 0)
    answers = pytesseract.image_to_string(answer_box, lang='chi_sim')
    """

    return question, answers


def search(question):
    params = {'wd': question}
    url = u"https://www.baidu.com/s?"+urllib.urlencode(params)
    cmd = u'open "{}"'.format(url)
    run_command(cmd=cmd)


def analyze(question, answers):
    '''
    分析答案概率
    '''
    url = u"https://www.baidu.com/s?wd={}".format(question)
    res = requests.get(url)
    res.raise_for_status()

    all_pos = []
    answer_found = {}
    for answer in answers:
        offset = 0
        pos_list = []
        while True:
            pos = res.text.index(answer, start=offset)
            if pos >= 0:
                pos_list.append(pos)
                all_pos.append(pos)
            else:
                break
        answer_found[answer] = pos_list

    result = {}
    for answer, pos_list in answer_found.iteritems():
        result[answer] = float(len(pos_list))/len(all_pos) if all_pos else 0

    return result


def main():
    import time

    begin = time.time() * 1000
    question, answers = recognition()

    search(question)

    #analyze(question, answers)

    end = time.time() * 1000

    print ("cost time: ", (end-begin), " ms")


if __name__ == '__main__':
    main()