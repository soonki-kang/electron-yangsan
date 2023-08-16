from datetime               import datetime
from time                   import sleep
from PySide6.QtCore         import QThread, Signal
from myvar                  import myVar   as mv

class timeThread(QThread):
    timesignal  =  Signal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.base_datetime  =  datetime.combine(datetime.today(), mv.BASE_TIME)
        self.work_bool = True

    def run(self):
        while  self.work_bool:
            remainder_time =  int((self.base_datetime - datetime.today()).total_seconds())
            # print(" while remainder time", remainder_time, self.base_datetime, datetime.today())
            if remainder_time < 0:
                self.stop()
                continue
            self.timesignal.emit(remainder_time)
            sleep(1)

    def stop(self):
        self.work_bool = False
        self.quit()
