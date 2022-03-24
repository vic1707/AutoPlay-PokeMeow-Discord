from decimal import Decimal
from sys import platform, stdout
from time import sleep

from pyotp import TOTP
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CustomDriver( webdriver.Firefox, 
                    webdriver.Opera,  
                    webdriver.Chrome,
                    webdriver.Edge):
    
    URL_VOTE_POKEMEOW = 'https://top.gg/bot/664508672713424926/vote'
    URL_LOGIN_TOP_GG = 'https://top.gg/login'
    AUTHORIZE_BUTTON_XPATH = "//button[@class='button-38aScr lookFilled-1Gx00P colorBrand-3pXr91 sizeMedium-1AC_Sl grow-q77ONN']"
    VOTE_BUTTON_XPATH = '//input[@class="voting btn btn-orange btn-4x vote-button"]'
    # <input id="votingvoted" type="button" class="voting btn btn-orange btn-4x vote-button" value="Vote">
    # MODIFIER = Keys.COMMAND if platform == "win32" or platform == 'linux' else Keys.COMMAND

    SEND_MSG_BAR_XPATH: str = "//div[@class='markup-eYLPri slateTextArea-27tjG0 fontSize16Padding-XoMpjI']"
    SEND_MSG_BAR = None
    LAST_MSG = None
    NBR_MAX_RECURSION: int = 4

    MSG_XPATH: str = "//div[contains(@class,'message-2qnXI6 cozyMessage-3V1Y8y')]"
    POKEMEOW_USERNAME: str = 'PokéMeow'

    def __init__(self, ARGUMENTS):
        self.CHANNEL = ARGUMENTS.C
        self.USERNAME = ARGUMENTS.U
        self.MAIL = ARGUMENTS.M
        self.PASSWD = ARGUMENTS.P
        self.TOKENFA = ARGUMENTS.FA
        self.BACKWARDS = ARGUMENTS.BACKWARDS
        if ARGUMENTS.D == 'Firefox': 
            path_binary = r'./webdrivers/Firefox/linux_geckodriver' if platform == 'linux' else r"webdrivers\Firefox\geckodriver.exe" if platform == "win32" else r"webdrivers/Firefox/mac_geckodriver"
            options = FirefoxOptions()
            if ARGUMENTS.H: options.headless = True
            webdriver.Firefox.__init__(self, executable_path=path_binary, options=options)
        elif ARGUMENTS.D == 'Chrome': 
            path_binary = r'./webdrivers/Chrome/linux_chromedriver' if platform == 'linux' else r"webdrivers\Chrome\chromedriver.exe" if platform == "win32" else r"webdrivers/Chrome/mac_chromedriver"
            options = ChromeOptions()
            if ARGUMENTS.H: options.add_argument('headless')
            webdriver.Chrome.__init__(self, executable_path=path_binary, chrome_options=options)
        elif ARGUMENTS.D == 'Opera': 
            path_binary = r'./webdrivers/Opera/linux_operadriver' if platform == 'linux' else r"webdrivers\Opera\operadriver.exe" if platform == "win32" else r"webdrivers/Opera/mac_operadriver"
            options = OperaOptions()
            if ARGUMENTS.H: options.add_argument('headless')
            webdriver.Opera.__init__(self, executable_path=path_binary, options=options)
        elif ARGUMENTS.D == 'Edge': 
            if platform == "win32": 
                # options = EdgeOptions()
                # options.use_chromium = True
                path = r"webdrivers\Edge\msedgedriver.exe"
                # if ARGUMENTS.H: options.headless = True
                webdriver.Edge.__init__(self, path)
            else: raise Exception("Edge is only supported on Windows ! ")
        else: 
            print('Unsupported driver, please use only "Firefox", "Opera", "Edge" or "Chrome".')
            raise Exception('BROWSER NOT SUPPORTED !')

        self.DiscordLogin(self.CHANNEL)
        self.SEND_MSG_BAR = self.FindOneByXPATH(self.SEND_MSG_BAR_XPATH, 'Discord sending bar')
        self.LAST_MSG = self.FindMessages('find last message')[0]

    def DiscordLogin(self, CHANNEL: str):
        self.get(CHANNEL)
        self.find_element_by_name("email").send_keys(self.MAIL)
        pwd = self.find_element_by_name("password")
        pwd.send_keys(self.PASSWD)
        pwd.send_keys(Keys.RETURN)
        if self.TOKENFA: input( f"Please type this code : '{ TOTP(self.TOKENFA).now() }' and then come back to this console to type enter." )

    def FindOneByCLASS(self, _class: str, item: str, 
                          timeout: int = 30):
        try:
            return WebDriverWait(self, timeout=timeout).until(lambda driver: driver.find_element_by_class_name(_class))
        except TimeoutException: raise Exception(f'"{ item }" took too much time to apear, dev can\'t really do anything to fix it')

    def FindOneByID(self, _id: str, item: str, 
                          timeout: int = 30):
        try:
            return WebDriverWait(self, timeout=timeout).until(EC.element_to_be_clickable((By.ID,_id)))
        except TimeoutException: raise Exception(f'"{ item }" took too much time to apear, dev can\'t really do anything to fix it')

    def FindOneByXPATH(self, PATH, item: str, 
                          timeout: int = 30):
        try:
            return WebDriverWait(self, timeout=timeout).until(EC.element_to_be_clickable((By.XPATH, PATH))) 
        except TimeoutException: raise Exception(f'"{ item }" took too much time to apear, dev can\'t really do anything to fix it')

    def FindMessages(self, item: str, 
                           timeout: int = 30):
        try:
            return WebDriverWait(self, timeout=timeout).until(lambda driver: driver.find_elements_by_xpath(self.MSG_XPATH))[::-1] 
        except TimeoutException: raise Exception(f'"{ item }" took too much time to apear, dev can\'t really do anything to fix it')

    def SendMessage(self, keys: str):
        if self.BACKWARDS : keys = keys[::-1]
        try: 
            self.SEND_MSG_BAR.send_keys(keys)
        except:
            self.SEND_MSG_BAR = self.FindOneByXPATH(self.SEND_MSG_BAR_XPATH, 'Discord sending bar')
            self.SEND_MSG_BAR.send_keys(keys)

        self.SEND_MSG_BAR.send_keys(Keys.RETURN)

    def CheckLast(self,
                  contains: str = ''):
        msgList = self.FindMessages('find all messages')
        for message in msgList[:msgList.index(self.LAST_MSG)]:
            try:
                sender, text = message.text.split('\n', 1)
                if self.POKEMEOW_USERNAME in sender and \
                   self.USERNAME in text and \
                   (all(contain in text for contain in contains) if type(contains) == list else contains in text):
                    self.LAST_MSG = message
                    return message 
            except: pass

    def WaitNew(self, to_send: str, contains, # contains can be a str or a list of str
                      retry: int = NBR_MAX_RECURSION, message_orig_txt = None, number_of_sleep: Decimal = Decimal(4) ):

        if not message_orig_txt: message_orig_txt = self.LAST_MSG.text
        # send le message
        self.SendMessage(to_send)

        # recupere une nouvelle fois le text du dernier embed
        new_message = self.CheckLast(contains)
        
        # tant que les deux messages sont egaux et que retry n'est pas passé
        while not new_message and number_of_sleep:
            sleep(0.1)
            number_of_sleep -= Decimal('0.1')
            new_message = self.CheckLast(contains)

        # si les deux embeds sont effectivement diffs
        if new_message and message_orig_txt != new_message.text: return new_message

        if retry :
            # sinon recur
            self.attente(6, 'trying again this action')
            return self.WaitNew(to_send, contains, retry - 1, message_orig_txt)
        else: raise RecursionError('MAX RECURSION REACHED')

    def attente(self, time: int, arg: str):
        for remaining in range(time, 0, -1):
            print(f"{remaining:2d}/{ time } seconds remaining before { arg }.", end = '\r')
            sleep(1)
        if platform != 'win32':
            stdout.write("\033[K")
            stdout.flush()
        else: print(' ' * 25)

    def WaitChangesOnMessage(self, to_send: str, message, 
                                   retry: int = NBR_MAX_RECURSION, number_of_sleep: Decimal = Decimal(4)) -> bool:
        bak_text = message.text
        self.SendMessage(to_send)
 
        while message.text == bak_text and number_of_sleep:
            sleep(0.1)
            number_of_sleep -= Decimal('0.1')

        if message.text != bak_text: return '\nCongratulations' in message.text

        if retry : 
            # sinon recur
            self.attente(6, 'trying again this action')
            return self.WaitChangesOnMessage(to_send, message, retry -1)
        else: raise RecursionError('MAX RECURSION REACHED')

    def Vote(self):
        print('Going to vote for you.')
        self.get(self.URL_LOGIN_TOP_GG)
        self.FindOneByXPATH(self.AUTHORIZE_BUTTON_XPATH, 'Discord Authorize button on top.gg').click()
        self.FindOneByCLASS('logo', 'Top.gg main logo')
        self.get(self.URL_VOTE_POKEMEOW)
        try: sleep(5); self.FindOneByXPATH("//a[@class='btn' and text() = 'No thanks']", 'No tanks button', 15).click()
        except: pass
        sleep(5)
        self.FindOneByXPATH(self.VOTE_BUTTON_XPATH, 'Vote button', 120).click()
        self.FindOneByID('rememberReminder', 'Vote has been validated', 120)
        self.get(self.CHANNEL)
        self.LAST_MSG = self.FindMessages('find last message')[0]
        print('I voted for you.')
