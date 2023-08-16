from datetime           import  datetime, timedelta, time
from PySide6.QtCore     import  QObject, Signal
from myvar              import  myVar  as mv

class signalFun(QObject):
    checkDisplay = Signal(str)

    def __init__(self):
         super().__init__()
   
    def check_date(self, tdate):
         # 요일 추출
         tdate = tdate.toPython()
         current_date = datetime.today()
         current_date = current_date.date()
         mv.REV_WEEK = datetime.isoweekday(tdate)    ##  요일을 1~7로 반환 weekday: 0~6반환
         if mv.REV_WEEK == 6 or mv.REV_WEEK == 7:
           cnt_date = tdate + timedelta(days = (-11 - mv.REV_WEEK))
           mv.BASE_TIME = time(10,0,0)
         else:
           cnt_date = tdate + timedelta(days = -14)
           mv.BASE_TIME = time(9,0,0)

         mv.isRUN = False
         curr_time  =  datetime.today().time()
         if current_date > cnt_date:
            self.checkDisplay.emit("예약 날자가 지났습니다.")
            return
         elif current_date != cnt_date :  
            self.checkDisplay.emit("예약 날자가 아닙니다.")
            return
         elif curr_time > mv.BASE_TIME:
            self.checkDisplay.emit("예약 시간이 지났습니다.")
            return
         mv.isRUN = True