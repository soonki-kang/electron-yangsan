from PySide6.QtCore import Signal, QThread
from browserload import browserLoad
from loginsite import loginSite
from datetime import datetime, timedelta
from time import time as timetime, sleep
import pause
import random
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# import threading
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.select import Select
from jointhread import joinThread

from myvar import myVar as mv


class procThread(QThread):
    browserproc_signal = Signal(str)
    endofjob_signal = Signal(str)

    def __init__(self):
        super().__init__()

    def return_mesg(self, mesg):
        self.browserproc_signal.emit(mesg)

    def browserload_n_login(self):
        # browser load
        try:
            before_time = datetime.now().strftime("%H%M%S%f")[:-3]
            self.bl = browserLoad()
            now_time = datetime.now().strftime("%H%M%S%f")[:-3]
            response_time = int((int(now_time) - int(before_time)) / 1000)
            self.browserproc_signal.emit(f'🌍 응답 시간 : {response_time} ms')
        except Exception as e:
            self.browserproc_signal.emit(e)
        self.bl.site_signal.connect(self.return_mesg)
        self.lg = loginSite()
        self.lg.login_signal.connect(self.return_mesg)
        self.lg.login()

    def callthread(self, e, selectTime):
        self.locals()['jt{}'.format(selectTime)] = joinThread(e, parent=self)
        self.locals()['jt{}'.format(selectTime)
                      ].joinsignal.connect(self.return_mesg)
        self.locals()['jt{}'.format(selectTime)].start()

    def callfunction(self, clickTee):
        # print('.........callfunction.................')
        try:
            # tee  click
            # clickTee.send_keys(Keys.ENTER)
            # 1. 신청 click
            clickTee.click()

            # 2. 예약 안내
            # 1번째 alert x월 x일 x코스 hh:mm타임을 예약하시겠습니까
            mv.DRIVER.find_element(
                By.XPATH, "//*[@id='cm_popup_content']/div[2]/div[1]/a/img").click()

            # 3. 예약 확정 안내
            # 예약이 확정되면 문자로 예약 내역이 발송됩니다.
            try:
                WebDriverWait(mv.DRIVER, 0.2).until(EC.alert_is_present())
                mesg = Alert(mv.DRIVER).text
                Alert(mv.DRIVER).accept()
                # Alert(mv.DRIVER).dismiss()
                self.browserproc_signal.emit(mesg)
            except:
                return False

            # 예약을 click했는데 "예약 내역이 발송됩니다" mesg가 없을 경우
            # 무조건 다시 select함"
            if mesg.find("발송") < 0:
                return False

            # 4. 동시 예약 등으로 예약이 불가한 안내
            # 예약하시겠습니까 accept후 다음 alert를 받았을 경우(동시예약등) 처리
            # 안내가 없을 경우 정상적으로 예약됨.
            try:
                WebDriverWait(mv.DRIVER, 0.2).until(EC.alert_is_present())
                mesg = Alert(mv.DRIVER).text
                Alert(mv.DRIVER).accept()
                self.browserproc_signal.emit(f"{mesg}")
                return False
            except:
                self.browserproc_signal.emit("예쓸!!!")
                return True

        except Exception as e:
            # print(f'...............error. : {e}')
            self.browserproc_signal.emit(e)
            return False

    # script를 실행하여  예약날자로 진입
    def peekDate(self):
        # 예약 일자 string 변환
        date_str = mv.USER_REVDATE.strftime("%Y%m%d")
        # mv.DRIVER.execute_script("timefrom_change('20220118','1','3','','00','T')")
        # print("예약일자 : ", date_str)
        holiday = "2" if (mv.REV_WEEK == 6 or mv.REV_WEEK == 7) else "1"
        week_no = 1 if (mv.REV_WEEK == 7) else mv.REV_WEEK + 1
        week_no_str = format(week_no, "1")

        # 날자 선택(javascript 실행)
        script_str = "timefrom_change('" + date_str + "','" + \
            holiday + "','" + week_no_str + "',',','00','T')"
        # print("script : ", script_str)
        # 날자 선택
        mv.DRIVER.execute_script(script_str)
        sleep(0.2)
        # print("date select :", mv.DRIVER.window_handles, datetime.today())

    def openandselect(self):
        # 예약 실패 후 loop 반복 지점
        setTimeOut = timetime() + (60 * 1)
        # tee가 나타날때까지 최대 1분 동안 loop
        self.browserproc_signal.emit(
            f"Open 대기 ..... " + datetime.today().strftime("%H:%M:%S"))

        isData = False
        while timetime() < setTimeOut:

            try:
                self.teeElements = WebDriverWait(mv.DRIVER, 0.1).until(
                    # EC.presence_of_all_elements_located((By.XPATH, "//*[@id=contains(text(), 'timeresbtn')]/img"))
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//*[starts-with(@id, 'timeresbtn')]"))
                )
                isData = True
                # self.current_window = mv.DRIVER.current_window_handle
                break
            except:
                # ActionChains(mv.DRIVER).click(mv.DRIVER.find_element(By.XPATH, tee_course_str2)).perform()
                self.browserproc_signal.emit(
                    f"Open 대기 ..... " + datetime.today().strftime("%H:%M:%S"))
                mv.DRIVER.refresh()
                # sleep(0.1)
                continue

        if (not isData):
            self.browserproc_signal.emit("예약일자 혹은 서버를 확인하세요!!!")
            mv.isRUN = False
            return mv.isRUN

        if len(self.teeElements) < 1:
            self.browserproc_signal.emit("제공된 tee가 없습니다.")
            mv.isRUN = False
            return mv.isRUN
        else:
            self.browserproc_signal.emit(
                f"총 {len(self.teeElements)} 개의 tee가 있습니다!")
            mv.isRUN = True
            return mv.isRUN

    def proc_tee(self):

        # 비즈니스 예약, 일반 예약 click
        if mv.USER_REV_ID == 0:
            # print('비즈니스........')
            mv.DRIVER.find_element(
                By.XPATH, '//*[@id="cm_reservation"]/ul/li[1]/a').click()
        elif mv.USER_REV_ID == 1:
            # print('일반........')
            mv.DRIVER.find_element(
                By.XPATH, '//*[@id="cm_reservation"]/ul/li[3]/a').click()
        else:
            pass

        # 날자를 넣고 script실행
        #print(f"peekDate ..... " + datetime.today().strftime("%H:%M:%S"))
        self.peekDate()
        #print(f"peekDate after ..... " + datetime.today().strftime("%H:%M:%S"))

        # 시간을 선택하기 위한 String value 설정
        # 05:00 ~ 07:00
        # strRevFmTime = '{:02d}'.format(mv.USER_FMTIME + 4) + '00'
        # strRevToTime = '{:02d}'.format(mv.USER_TOTIME + 4) + '59'
        # if mv.USER_TOTIME == 0:
        #     strRevToTime = '{:02d}'.format(19) + '00'
        strRevFmTime = (mv.USER_FMTIME + 4) * 100
        strRevToTime = (mv.USER_TOTIME + 4) * 100 + 59
        n = 0
        if mv.USER_TOTIME == 0:
            strRevToTime = 1959

        while True:
            isRetry = False
            if not self.openandselect():
                return mv.isRUN

            random.shuffle(self.teeElements)  # tee list를 random으로 섞음.
            for i, tee in enumerate(self.teeElements):
                # javascript의 내용에서 시간 추출
                selectTime = int(tee.get_attribute('href')[27:31])
                selectCourse = int(tee.get_attribute('href')[23:24])
                # 확인 print(f'time = {selectTime} index = {i}   length = {len(teeElements)}')
                if (mv.USER_COURSE != 0):
                    if (mv.USER_COURSE != selectCourse):
                        # sleep(0.2)
                        continue

                if (selectTime >= strRevFmTime and selectTime <= strRevToTime):
                    teeimage = tee.find_element(By.CSS_SELECTOR, 'img[src]')
                    n += 1
                    if self.callfunction(teeimage):
                        self.browserproc_signal.emit(f"🎆🎆🎆 예약이 성공하였습니다. 🎆🎆🎆")
                        mv.isRUN = False
                        return mv.isRUN
                    else:
                        self.browserproc_signal.emit("😥😥😥  재시도  😥😥😥")
                        isRetry = True
                        break

                    # sleep(0.01)
                # self.browserproc_signal.emit(f"outside - tee {selectTime} pass, {i} 회 시도 " )

            if isRetry:
                # print('이것은 retry continue')
                continue

            mv.isRUN = False
            break

        self.browserproc_signal.emit("😞😞😞예약이 실패했습니다.😞😞😞")
        return False

    # use pause until
    def run(self):
        # time to seconds 2분전을 세팅함
        base_date = datetime.combine(datetime.today(), mv.BASE_TIME)
        start_time = base_date - timedelta(minutes=2)
        pause.until(start_time)
        self.browserload_n_login()

        # 5초 전에 무조건 시작
        # start_time = base_date - timedelta(seconds=(4 + mv.DIFF_TIME))
        start_time = base_date - timedelta(seconds=10)
        #print(f"pause time ..... " + datetime.today().strftime("%H:%M:%S"))
        pause.until(start_time)
        #print(f"proc_tee start ..... " + datetime.today().strftime("%H:%M:%S"))
        self.proc_tee()
        mv.DRIVER.quit()
        self.endofjob_signal.emit("작업이 종료되었습니다.")
        self.stop()

    def stop(self):
        self.quit()
