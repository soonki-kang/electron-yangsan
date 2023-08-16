from datetime               import datetime
from time                   import sleep
from PySide6.QtCore         import QThread, Signal
from selenium.webdriver.common.keys      import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from myvar                  import myVar   as mv

class joinThread(QThread):
    joinsignal  =  Signal(int)

    def __init__(self, clickTee, parent=None):
        super().__init__()
        self.main = parent
        self.clickTee = clickTee

    def run(self):
        try:
            # tee  click
            self.clickTee.send_keys(Keys.ENTER)

            # 'xxx님 예약하시겠습니까?'
            WebDriverWait(mv.DRIVER, 1).until(EC.alert_is_present())
            # alert_event = mv.DRIVER.switch_to.alert
            mesg = Alert(mv.DRIVER).text
            Alert(mv.DRIVER).accept()
            if mesg.find('예약하시겠습니까') < 1:
                self.joinsignal.emit('실.....패')
                self.stop()

            # '성공적으로 예약되었습니다'
            WebDriverWait(mv.DRIVER, 1).until(EC.alert_is_present())
            mesg = Alert(mv.DRIVER).text
            Alert(mv.DRIVER).accept()
            # alert_event = mv.DRIVER.switch_to.alert
            if mesg.find('성공적으로') > 0:
                self.joinsignal.emit(mesg)
                mv.isThreadRun = False
        except: 
            self.stop()




        while  mv.isThreadRun:
            remainder_time =  int((self.base_datetime - datetime.today()).total_seconds())
            # print(" while remainder time", remainder_time, self.base_datetime, datetime.today())
            if remainder_time < 0:
                self.stop()
                continue
            self.joinsignal.emit(remainder_time)
            sleep(1)

    def stop(self):
        self.quit()
