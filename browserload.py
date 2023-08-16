from PySide6.QtCore import Signal, QObject
from selenium import webdriver
from subprocess import CREATE_NO_WINDOW
from time import sleep
from fake_useragent import UserAgent
import shutil
# from user_agent                         import (InvalidOption, generate_user_agent)
# import chromedriver_autoinstaller

from myvar import myVar as mv


class browserLoad(QObject):
    site_signal = Signal(str)

    def __init__(self):
        super().__init__()

        mv.isRUN = True
        if mv.USER_BROWSER == "Chrome":
            self.chrome_driver()
        elif mv.USER_BROWSER == "Firefox":
            self.firefox_driver()
        else:
            mv.DRIVER = None
            mv.isRUN = False
            return
        self.loadsite()

    def loadsite(self):
        loop_cnt = 1

        mv.DRIVER.set_page_load_timeout(20)

        while loop_cnt < 10:
            try:
                mv.DRIVER.get(mv.USER_URL)
                assert mv.USER_SITE in mv.DRIVER.title
                # assert "No results found." not in mv.DRIVER.page_source
                mv.isRUN = True
                return
            except:
                sleep(10)
                self.site_signal.emit(f"site가 응답하지 않습니다. 재시도 {loop_cnt}회")
                loop_cnt += 1
                continue
        self.site_signal.emit(f"site가 {loop_cnt}회 응답하지 않아 종료합니다!")
        mv.DRIVER.quit()
        mv.isRUN = False

    def chrome_driver(self):
        '''
        Chrome Driver load
        '''
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        # from webdriver_manager.core.utils import ChromeType
        from selenium.webdriver.chrome.options import Options

        try:
            shutil.rmtree(r"c\chrometemp")    # 쿠키 / 캐쉬 파일 삭제
        except FileNotFoundError:
            pass
            # print('not found c:\chrometemp shutil.rmtree')

        # 수동으로 실행한 것 처럼 실행
        # subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
        # subprocess.Popen(f'./{chrome_ver}/chromedriver.exe --remote-debugging-port=9515 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
        weboptions = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_value':  {'cookies':   2,  # 1: enable 2:disable
                                                            'images':   2,
                                                            'plugins':   2,
                                                            'popups':   2,
                                                            'geolocation':   2,
                                                            'notifications':   2,
                                                            'auto_select_certificate':   2,
                                                            'fullscreen':   2,
                                                            'mouselock':   2,
                                                            'mixed_script':   2,
                                                            'media_stream':   2,
                                                            'media_stream_mic':   2,
                                                            'media_stream_camera':   2,
                                                            'protocol_handlers':   2,
                                                            'ppapi_broker':   2,
                                                            'automatic_downloads':   2,
                                                            'midi_sysex':   2,
                                                            'push_messaging':   2,
                                                            'ssl_cert_decisions':   2,
                                                            'metro_switch_to_descktop':   2,
                                                            'protected_media_identifier':   2,
                                                            'app_banner':   2,
                                                            'site_engagement':   2,
                                                            'durable_storage':   2,
                                                            'detach': 1,
                                                            'excludeSwitches': 1
                                                            }}
        # weboptions.add_experimental_option('prefs', prefs)

        # user-agent를 랜덤으로 설정함
        # fake-useragent가 안되므로  user-agent로 변경 2022.12.23
        # ua = UserAgent(verify_ssl=False)
        # ua = UserAgent(browsers=['chrome', 'firefox'], user_local_file=False, verify_ssl=False)
        # ua = UserAgent(user_local_file=False, verify_ssl=False)
        # ua.verify_ssl=False
        # ua.cache = False
        # ua.use_local_file=False
        # ua.user_cache_server=False
        # ua = UserAgent(verify_ssl=False, user_cache_server=True)
        # userAgent = ua.random
        # userAgent = ua.data_randomize
        # user-agent로 변경
        # userAgent = generate_user_agent(device_type='desktop')
        # print(userAgent)
        # weboptions.add_argument(f'user-agent={userAgent}')
        # end
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") # 수동으로 실행한 것 처럼 실행

        weboptions.add_argument('--disable-extensions')
        weboptions.add_argument('--profile-directory=Default')
        weboptions.add_argument('--incognito')
        weboptions.add_argument('--disable-plugins-discovery')
        weboptions.add_argument('--start-maximized')
        weboptions.add_experimental_option(
            'excludeSwitches', ['enable-logging'])  # 에라로그 없앰
        weboptions.add_argument('disable-gpu')
        weboptions.add_argument('disable-infobars')
        weboptions.add_argument(
            "app-version=Mozilla/5.0 (Windows NT 10.0;Win64l x64) AppeWeKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
        weboptions.add_argument("--headless")               # browser hidden

        # weboptions.add_argument('window-size=1920,1080')
        # options.headless = True
        # # options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'
        # bot를 피해가기 위한 user-agent 수정
        # weboptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
        # options.add_argument('--sandbox')                  #selenium-common-exceptions-webdriverexception-message-unknown-error-unable-to
        # weboptions.add_experimental_option(
        # "excludeSwitches", ["enable-logging"])           # 시스템에 부착된 장치가 작동하지 않습니다. 방지
        # weboptions.add_experimental_option('detach', True)   # 브라우저 바로 닫힘 방지
        # weboptions.add_experimental_option("debuggerAddress","127.0.0.1:9515") # 시스템에 부착된 장치가 작동하지 않습니다. 방지

        # chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        # chromedriver Console  display 억제 ver 3.141.0 에서 안됨

        # print('pass ChromeServide.....')
        # 2023.08.03 selenium 4.1.3에서  4.11.2 upgrade
        # chromedriver_autoinstaller.install()
        chrome_service = ChromeService(
            ChromeDriverManager().install()
            # executable_path=ChromeDriverManager(
            #     version="114.0.5735.90"
            # ).install()
        )
        # executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        # # chrome_service = ChromeService(executable_path='chromedriver')
        # print('aa20.....')
        chrome_service.creation_flags = CREATE_NO_WINDOW
        # # chromedriver Console End

        try:
            # print('enter webdriver.......')
            mv.DRIVER = webdriver.Chrome(
                service=chrome_service,
                options=weboptions
            )
            #     # mv.DRIVER = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options = weboptions)
            #     # mv.DRIVER = webdriver.Chrome(f'./chromedriver.exe', options = weboptions, service=chrome_service)
            #     # driver = webdriver.Chrome('./chromedriver.exe', options=weboptions)
            # mv.DRIVER = webdriver.Chrome(ChromeDriverManager().install())
            # chrome_service = ChromeService()
            # options = Options()
            # options.add_argument('start-maximized')
            # # mv.DRIVER = webdriver.Chrome(
            # #     service=chrome_service, options=options)
            # mv.DRIVER = webdriver.Chrome()
            # pass
        except Exception as e:
            print(f"Web Browser install fail {str(e)}")

        # print('pass webdriver........')
        # mv.DRIVER = webdriver.Chrome(ChromeDriverManager(
        #     chrome_type=ChromeType.CHROMIUM).install())

        mv.DRIVER.implicitly_wait(0.1)

    def firefox_driver(self):
        '''
        Firefox driver load
        '''
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager
        mv.DRIVER = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()))
