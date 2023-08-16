from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtCore import Signal, QObject
from time import sleep
from myvar import myVar as mv


class loginSite(QObject):
    login_signal = Signal(str)

    def __init__(self):
        super().__init__()

    def login(self):
        loginid = mv.DRIVER.find_element(By.XPATH, '//*[@id="login_id"]')
        loginpassword = mv.DRIVER.find_element(By.XPATH, '//*[@id="login_pw"]')
        loginbtn = mv.DRIVER.find_element(
            By.XPATH, '//*[@id="login"]/div/a/img')

        actions = ActionChains(mv.DRIVER)
        actions.click(loginid)
        actions.send_keys(mv.USER_ID)
        actions.click(loginpassword)
        actions.send_keys(mv.USER_PASSWORD)
        # actions.move_to_element(loginbtn)
        actions.click(loginbtn)
        actions.perform()
        sleep(1)
        # actions.reset_actions()
        n = 0

        while True:
            try:
                WebDriverWait(mv.DRIVER, 1).until(EC.alert_is_present())
                mesg = Alert(mv.DRIVER).text
                if not mesg.find("환영") < 0:
                    mv.isRUN = True
                    Alert(mv.DRIVER).accept()
                    break
                elif not mesg.find("변경") < 0:
                    mv.isRun = True
                    Alert(mv.DRIVER).accept()
                    changebtn = mv.DRIVER.find_element(
                        By.XPATH, '//*[@id="content_body"]/div[2]/a[2]')
                    actions = ActionChains(mv.DRIVER)
                    actions.click(changebtn)
                    actions.perform()
                    break
                elif not mesg.find("일치") < 0:
                    mv.isRUN = False
                    self.login_signal.emit(mesg)
                    Alert(mv.DRIVER).accept()
                    return
                else:
                    self.login_signal.emit(mesg)
                    Alert(mv.DRIVER).dismiss()
                    n += 1
                    if n > 5:
                        mv.isRUN = False
                        return
                    else:
                        continue
            except Exception as e:
                self.login_signal.emit("popup nothing")
                mv.isRUN = False
                return

        self.login_signal.emit(mesg)

    def logout(self):
        logoutbtn = mv.DRIVER.find_element(By.XPATH, '//*[@id="head"]/div/a')
        actions = ActionChains(mv.DRIVER)
        actions.click(logoutbtn)
        actions.perform()
        # Alert(mv.DRIVER).accept()
