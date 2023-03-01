# -*- coding: UTF-8 -*-
import getpass
import sys
import time
import traceback

from selenium.common import NoSuchElementException, NoAlertPresentException, ElementNotInteractableException, \
    StaleElementReferenceException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from constant import *
from login import Login


def main():
    # 装填参数
    username = ""
    password = ""

    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
    else:
        print("input username")
        while len(username.strip()) == 0:
            username = input("Please input your username: ")
        while len(password.strip()) == 0:
            password = getpass.getpass("and your password: ")

    url = DEFAULT_URL
    try:
        login = Login(url, username, password)
        login.login()

        driver = login.driver

        prepare_course(driver)

        learn_all_courses(driver)
    except StaleElementReferenceException:
        traceback.print_exc()


def get_seconds(text):
    # TODO：后续可以使用时间api直接解析
    time_array = text.split(":")
    array_len = len(time_array)
    second = 0
    dict = [1, 60, 3600]
    for i in range(array_len):
        try:
            time_parse = int(time_array[array_len - i - 1])
            second += time_parse * dict[i]
        except ValueError:
            print("解析时间失败")
            second = -1
    return second


def learn_all_courses(driver):
    print("learn_all_courses course begin")
    try:
        course_list = driver.find_elements(By.CSS_SELECTOR, "[class='courseDetail of ng-scope']")
        course_num = len(course_list)
        print("当前页面的课程数{}".format(course_num))

        course_index = 0

        while course_index < course_num:
            try:
                time.sleep(2)
                current_course_detail = driver.find_element(By.CSS_SELECTOR, "[class='courseDetail of ng-scope']")
                time.sleep(2)
                try:
                    current_course_detail = driver.find_elements(By.CSS_SELECTOR, "[class='courseDetail of ng-scope']")[
                        course_index]
                except IndexError:
                    print("current_course_detail is {}, courseIndex is {}".format(current_course_detail, course_index))
                current_course_detail.click()
                time.sleep(1)
                try:
                    video_list = current_course_detail.find_elements(By.CSS_SELECTOR,
                                                                     "[class='videoList of ng-scope']")
                    video_num = len(video_list)
                    video_index = 0
                    while video_index < video_num:
                        video = video_list[video_index]
                        video_title = video.find_element(By.CSS_SELECTOR, "[class='className ng-binding']")
                        video_player = video.find_element(By.CSS_SELECTOR, "[class='player']")
                        video_progress = video.find_element(By.CLASS_NAME, 'progress')
                        video_timer = video.find_element(By.CSS_SELECTOR, "[class='timer ng-binding']")

                        print("current video index {}, title {} progress {}, 时长 {} 分钟"
                              .format(str(video_index), video_title.text, video_progress.text,
                                      video_timer.text))
                        if video_progress.text == "0%":
                            print("未开始, 点击播放开始学习")
                        elif video_progress.text == "100%":
                            video_index += 1
                            print("已完成, 跳过")
                            continue
                        else:
                            print("正在学习，点击播放继续学习")
                        # 点击播放按钮
                        video_player.click()
                        # 切换控制到新打开到播放页面
                        handles = driver.window_handles
                        driver.switch_to.window(handles[-1])

                        while True:
                            print("进入死循环播放")
                            time.sleep(3)
                            try:
                                # 是否继续上次听课进度的弹窗(可能出现弹窗也可能不出现，但如果出现就必须先处理弹窗，
                                # 这里默认去处理下，没有弹窗也没关系，可以正常继续执行）
                                handle_alert(driver)
                            except NoAlertPresentException:
                                print("expected alert to continue play, but not found!")
                            except WebDriverException:
                                print("WebDriverException")
                            # 获取视频播放的当前时长(current_time)和视频总时长(duration)
                            time.sleep(3)
                            if check_element_exists(driver, By.CLASS_NAME, 'content-cL'):
                                hoverable = driver.find_element(By.CLASS_NAME, 'content-cL')
                                ActionChains(driver) \
                                    .move_to_element(hoverable) \
                                    .perform()
                            else:
                                print("content-CL not found!")
                            time.sleep(1)
                            duration_div = driver.find_element(By.CLASS_NAME, 'prism-time-display')
                            current_time = duration_div.find_element(By.CLASS_NAME, "current-time")
                            duration = duration_div.find_element(By.CLASS_NAME, "duration")
                            video_duration = get_seconds(duration.text) - get_seconds(current_time.text)
                            if get_seconds(duration.text) == -1:
                                video_duration = 3600 * 2
                                print("set max video duration 3600 * 2 seconds")
                            print("current time is {}, duration is {}, video_duration is {}".format(current_time.text,
                                                                                                    duration.text,
                                                                                                    video_duration))
                            time.sleep(3)
                            try:
                                double_rate(driver)
                                video_duration = video_duration / 2
                            except ElementNotInteractableException:
                                print("speed setting failed")
                            video_duration += 10
                            try:
                                # 休眠视频播放时间(video_duration),期间不断检测是否有已放完的弹窗
                                WebDriverWait(driver, timeout=video_duration, poll_frequency=5).until(
                                    AlertOrReLogin())
                            except:
                                AlertOrReLogin()(driver)
                            # time.sleep(10)
                            if EC.alert_is_present()(driver):
                                print("出现了连播弹窗")
                                if video_index < video_num - 1:
                                    print("继续播放下一讲")
                                    driver.switch_to.alert.accept()
                                    video_index += 1
                                else:
                                    print("最后一个视频了，取消")
                                    driver.switch_to.alert.dismiss()
                                    video_index += 1
                                    # 切换控制回之前的页面
                                    handles = driver.window_handles
                                    driver.close()
                                    driver.switch_to.window(handles[0])
                                    break
                            else:
                                print("未出现连播弹窗，video_index 加 1 后跳出死循环")
                                video_index += 1
                                break
                except NoSuchElementException:
                    print("获取视频失败{}".format(course_index))
            except NoSuchElementException:
                print("获取课程失败, course_index is {}".format(course_index))
            course_index += 1
    except NoSuchElementException:
        print("获取课程列表失败")
    print("learn_all_courses course end")


def double_rate(driver):
    time.sleep(1)
    if check_element_exists(driver, By.CLASS_NAME, 'content-cL'):
        hoverable = driver.find_element(By.CLASS_NAME, 'content-cL')
        ActionChains(driver) \
            .move_to_element(hoverable) \
            .perform()
    else:
        print("content-CL not found!")
    if check_element_exists(driver, By.CLASS_NAME, 'rate-components'):
        time.sleep(1)
        elem = driver.find_element(By.CLASS_NAME, 'rate-components')
        elem.click()
        time.sleep(1)
        if check_element_exists(driver, By.CLASS_NAME, 'current-rate'):
            time.sleep(1)
            elem = driver.find_element(By.CLASS_NAME, 'current-rate')
            elem.click()
            time.sleep(1)
        if check_element_exists(driver, By.CLASS_NAME, 'rate-list'):
            time.sleep(1)
            elem = driver.find_element(By.CLASS_NAME, 'rate-list')
            speed = elem.find_elements(By.TAG_NAME, 'li')
            speed[0].click()


def handle_alert(driver):
    # TODO: how to locate alert
    alert = driver.switch_to.alert  # 切换到alert
    print('alert text : ' + alert.text)  # 打印alert的文本
    alert.accept()  # 点击alert的【确认】按钮


def pause_for_debug():
    while True:
        word = input("continue or not?")
        if word.strip() == 'y':
            break


def check_element_exists(driver, by=By.ID, value=None):
    try:
        driver.find_element(by, value)
    except NoSuchElementException:
        print('not found {}'.format(value))
        return False
    return True


def prepare_course(driver):
    print("prepare course begin")
    # 进入课程列表页面，默认为全部标签到第一页
    try:
        elem = driver.find_element(By.XPATH, XPATH_COURSE_PAGE_HREF)
        elem.click()
        # flag 用来指示标签页
        #   0 代表默认全部标签，不作切换
        #   1 代表切换到正听标签
        #   2 代表切换到未听标签
        #   3 代表切换到已完成标签
        #   4 代表重新切换回全部标签
        flag = 1

        next_step = 0

        if flag == 1:
            # 进入正听标签
            try:
                elem = driver.find_element(By.XPATH, XPATH_COURSE_PAGE_LISTENING_TAB)
                elem.click()
            except NoSuchElementException:
                print("进入正听标签 失败")
        elif flag == 2:
            # 进入未听标签
            try:
                elem = driver.find_element(By.XPATH, XPATH_COURSE_PAGE_UNFINISHED_TAB)
                elem.click()
            except NoSuchElementException:
                print("进入未听标签 失败")
        elif flag == 3:
            # 进入已完成标签
            try:
                elem = driver.find_element(By.XPATH, XPATH_COURSE_PAGE_FINISHED_TAB)
                elem.click()
            except NoSuchElementException:
                print("进入已完成标签 失败")
        elif flag == 4:
            # 重新进入全部标签
            try:
                elem = driver.find_element(By.XPATH, XPATH_COURSE_PAGE_ALL_TAB)
                elem.click()
            except NoSuchElementException:
                print("进入全部标签 失败")

        # 下一页
        try:
            for i in range(0, next_step):
                page_num = driver.find_element(By.CLASS_NAME, 'skip')
                next_button = page_num.find_element(By.CLASS_NAME, 'skipDown')
                next_button.click()
                time.sleep(1)
            print("进入下一页触发{}次".format(next_step))
        except NoSuchElementException:
            print("下一页进入失败")
    except NoSuchElementException:
        print("进入课程列表【我要听课】页面失败")
    print("prepare course end")


class AlertOrReLogin:
    def __call__(self, driver):
        # 用来结合webDriverWait判断是否出现alert
        is_alert = bool(EC.alert_is_present()(driver))
        if is_alert:
            print("AlertOrReLogin call {}".format(is_alert))
        return is_alert


if __name__ == '__main__':
    main()
