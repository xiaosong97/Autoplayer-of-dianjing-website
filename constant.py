# website url
DEFAULT_URL = "http://www.zfwx.com/wxqt/"

# constant define
XPATH_LOGIN_LABEL = r"/html/body/div[3]/div[1]/div[1]/div/div[2]/a[1]"
XPATH_LOGIN_USERNAME_INPUT = r"//*[@id='username']"
XPATH_LOGIN_PASSWORD_INPUT = r"//*[@id='password']"
XPATH_LOGIN_BUTTON = r"//*[@id='login-form']/p[5]/input"
XPATH_COURSE_PAGE_HREF = r'/html/body/div[3]/div[3]/div[1]/div[1]/ul/li[2]/a'  # 我要听课

XPATH_COURSE_PAGE_ALL_TAB = r'//*[@id="ng-app"]/body/div[3]/div[3]/div[2]/div/div/div[2]/ul/li[1]'
XPATH_COURSE_PAGE_LISTENING_TAB = r'//*[@id="ng-app"]/body/div[3]/div[3]/div[2]/div/div/div[2]/ul/li[2]'
XPATH_COURSE_PAGE_UNFINISHED_TAB = r'//*[@id="ng-app"]/body/div[3]/div[3]/div[2]/div/div/div[2]/ul/li[3]'
XPATH_COURSE_PAGE_FINISHED_TAB = r'//*[@id="ng-app"]/body/div[3]/div[3]/div[2]/div/div/div[2]/ul/li[4]'
