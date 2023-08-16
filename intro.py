# from multiprocessing    import Process, Queue
import urllib
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QDate, Slot
from PySide6 import QtCore
from datetime import datetime, timedelta, date
import pytz
from dateutil import parser
from myvar import myVar as mv
from yangsanform import Ui_YangsanForm
from signalfun import *
import myfunc as mf
from timethread import timeThread
from loginsite import loginSite
from procthread import procThread
from inputpickle import inputPickle


# UI File이 아닌 경우 주석처리
# form_class = uic.loadUiType


class Intro(QMainWindow, Ui_YangsanForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.setWindowTitle("Macro booking of Yangsan CC Ver : v2.1")

        # 해상도별 글자 크기 강제(일정한 크기)
        mf.suppress_qt_warnings()

        self.sf = signalFun()
        self.inputpick = inputPickle()
        self.inputpick.read_input()
        self.iid.setText(mv.USER_ID)
        self.ipassword.setText(mv.USER_PASSWORD)
        self.rev_id.setCurrentIndex(mv.USER_REV_ID)

        # 기초 자료 setting 및 connect
        # 날자 검증
        self.idate.setDate(QDate.currentDate().addDays(14))
        self.idate.dateChanged.connect(self.sf.check_date)
        self.sf.checkDisplay.connect(self.result_display)
        self.idate.setCalendarPopup(True)

        # 시간 선택시 간격 설정
        self.ifm_time.currentIndexChanged.connect(self.set_ifm_time)
        self.ito_time.currentIndexChanged.connect(self.set_ito_time)

        # 표준시 Check
        mesg = mf.time_check("time.windows.com")
        if not mesg == "":
            self.iresult.setText(mesg)

        # Proc button click
        self.iproc.clicked.connect(self.start_proc)

    def closeEvent(self, event):

        event.accept()

    @Slot(str)
    def result_display(self, mesg):
        self.iresult.append(mesg)
        QApplication.processEvents()

    @Slot(int)
    def time_display(self, remainder_time):
        # str_remainder_time =  "{0:>8}".format(str(timedelta(seconds=remainder_time)))
        # print("def time_display", remainder_time)
        str_remainder_time = str(timedelta(seconds=remainder_time))
        if remainder_time < 30:
            self.ilcdNumber.setStyleSheet("color: red;")
        elif remainder_time > 600:
            self.ilcdNumber.setStyleSheet("color: #FCF6F5;")
        else:
            rest_time = (255 * remainder_time) // 600
            ct = 255 - rest_time
            f_color = f"color:rgb({ct}, {rest_time}, {rest_time});"
            self.ilcdNumber.setStyleSheet(f_color)

        self.ilcdNumber.display(str_remainder_time)
        # QApplication.processEvents()

    def count_down_tee_time(self):
        '''
            # count down tee time thread create
        '''
        # print("count_down")
        self.iproc.setDisabled(True)
        # self.time_frame.show()
        # QWidget.update()

        self.tt = timeThread(parent=self)
        self.tt.timesignal.connect(self.time_display)
        self.tt.start()

    def move_global_data(self):
        '''
          입력 data를 global 변수에 넣음
        '''
        mv.USER_ID = self.iid.text()
        mv.USER_PASSWORD = self.ipassword.text()
        mv.USER_REVDATE = self.idate.date().toPython()
        mv.USER_FMTIME = self.ifm_time.currentIndex()
        mv.USER_TOTIME = self.ito_time.currentIndex()
        mv.USER_COURSE = self.icourse.currentIndex()
        mv.USER_REV_ID = self.rev_id.currentIndex()

    # def member_toggle(self, status):
    #     mv.USER_MEMBER = status
    #     self.imember.setStyleSheet("background-color:%s"%({True:"#7b9a3c",False: "#7b9acc"}[status]))
    #     self.imember.setText({True:"지정회원", False:"정회원"}[status])

    def set_ifm_time(self, status):
        if status > self.ito_time.currentIndex():
            self.ito_time.setCurrentIndex(status)

    def set_ito_time(self, status):
        if status < self.ifm_time.currentIndex():
            self.ifm_time.setCurrentIndex(status)

    def nearestmonday(self):
        week_no = 8 - datetime.isoweekday(datetime.today())
        return week_no

    def switchbtn(self, mesg):
        # self.time_frame.hide()
        self.iproc.setEnabled(True)
        self.result_display(mesg)

    def get_server_time(self):
        local_tz = pytz.timezone("Asia/Seoul")
        svr_str_time = urllib.request.urlopen(mv.USER_URL).headers['Date']
        svr_time = parser.parse(svr_str_time)
        local_conv_time = svr_time.replace(
            tzinfo=pytz.utc).astimezone(local_tz)
        return local_conv_time

    def start_proc(self):

        # move to global variable
        self.move_global_data()

        # date check  #  test 종료시 remarks 해제
        self.sf.check_date(self.idate.date())
        if not mv.isRUN:
            return

        self.lg = loginSite()
        self.lg.login_signal.connect(self.result_display)

        # test date move
        # n = datetime.now()
        # mv.USER_REVDATE = date(n.year, n.month, n.day + 1)
        # mv.BASE_TIME = time(hour=n.hour, minute=n.minute + 1, second=0)

        # id & password check
        self.pt = procThread()
        self.pt.browserproc_signal.connect(self.result_display)
        self.pt.endofjob_signal.connect(self.switchbtn)
        self.pt.browserload_n_login()

        if not mv.isRUN:
            mv.DRIVER.quit()
            return

        self.lg.logout()
        mv.DRIVER.quit()

        # input data save
        self.inputpick.save_input()

        # count down
        self.count_down_tee_time()

        # get mv.USER_URL datetime
        local_svr_time = self.get_server_time()
        pc_time = datetime.today()
        mv.DIFF_TIME = (int(local_svr_time.strftime("%H%M%S%f")[
                        :-6]) - int(pc_time.strftime("%H%M%S%f")[:-6]))
        self.result_display(
            "server ⏲️ : " + local_svr_time.strftime("%H:%M:%S"))
        self.result_display(
            "pc      🕰️ : " + pc_time.strftime("%H:%M:%S") + "   격차 : " + str(mv.DIFF_TIME) + "초")

        # scraping thread start
        self.iproc.setEnabled(False)
        self.result_display("✨ 예약을 시작합니다!!! ✨")
        self.pt.start()

        return
