import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

'''
目的：
- 抓取 FB公開社團名單

'''


def main():
    # --- import class ---
    run = FaceBookCrawler()

    # --- 初始化作業 ---
    run.初始化()
    # --- loading ---
    run.loading()
    # --- go to page ---
    run.goToSide()
    # --- crawler data ---
    run.getData()


class FaceBookCrawler:
    def __init__(self):
        # --- 登入帳號註冊信箱 ---
        self.userName = 'YOUR ACCOUNT'
        # --- 登入帳號註冊密碼 ---
        self.userPassword = 'YOUR PASSWORD'
        # --- 要抓取的社團url, "members 就是該社團的成員清單頁面" ---
        self.page = 'https://www.facebook.com/groups/603588537221545/members'  # 直播 主播 粉絲 感情 詐騙
        # --- facebook url ---
        self.baseUrl = 'https://www.facebook.com'

    # --- web driver 初始化 ---
    def 初始化(self):
        # ------- selenium webdriver 初始化 -------
        # (以下註解開發人員選項部分, 若需要使用該功能再自行打開)
        opts = Options()  # use 開發人員模式
        path = 'C:/Users/user/python/crawler/chromedriver_v101/chromedriver.exe'  # FilePath_chromedriver.
        # ------- 開發人員選項 -------
        opts.add_argument("--incognito")  # 使用無痕模式開啟 browser.
        # opts.add_argument("--headless")  # 不開啟實體瀏覽器, 背景執行.
        # opts.add_argument("--disable-plugins")  # 禁止載入外掛, 增加速度。可以透過about: plugins 頁面檢視效果.
        opts.add_argument("--incognito")  # 隱身模式啟動.
        # ------- 偽造user-agent -------
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        opts.add_argument(f'user-agent={ua}')  # 偽造 user-agent
        # ------- 啟動/定義 driver -------
        self.driver = webdriver.Chrome(executable_path=path,
                                       chrome_options=opts)

    def loading(self):
        # ------- login account -------
        self.driver.get('https://zh-tw.facebook.com')  # facebook login URL
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.NAME, 'email')))  # 頁面加載緩衝
        username = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))  # 帳號註冊信箱
        password = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "pass")))   # 帳號註冊密碼
        login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))
        # --- execute login account ---
        username.clear()  # username 欄位清空，避免input多餘的value.
        password.clear()  # password 欄位清空，避免input多餘的value.
        username.send_keys(self.userName)  # input username.
        password.send_keys(self.userPassword)  # input password.
        login.click()  # click login按鍵.
        time.sleep(5)  # 等待兩秒

    def goToSide(self):
        self.driver.get(self.page)  #
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rq0escxv d2edcug0 ecyo15nh k387qaup r24q5c3a hv4rvrfc dati1w0a")))
        time.sleep(3)

    def getData(self):
        nameList = []  # 抓取帳號名稱
        accountUrl = []  # 抓取該帳號個人頁面.

        print('-'*127)
        print('抓取社團名單準備作業中...\n請以滑鼠滾輪往下加載成員名單(最多加載時間x分鐘)')
        ready = input('完成請輸入\"y\"繼續交由程式執行, 或輸入其他任意建取消:\n')

        if ready == 'y':
            print('抓取社團名單...')
            print('-127')
            bs = BeautifulSoup(self.driver.page_source, 'html.parser')
            for link in bs.findAll('a', {'class':'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p'}):
                # print(link)
                if 'href' in link.attrs:
                    # print(f'User Name: {link.text}\nurl:\n', self.baseUrl + link.attrs['href'])
                    nameList.append(link.text)  # 裝載user name
                    accountUrl.append(self.baseUrl + link.attrs['href'])  # 裝載 user 個人檔案連結.

        print('-'*127)
        print('--- 輸出 name list ---')
        for name in nameList:
            print(name)

        print('-'*127)
        print('--- 輸出url ---')
        for url in accountUrl:
            print(url)

        return nameList, accountUrl

    # --- connect database ---
    def save(self, nameList, accountUrl):
        pass


if __name__ == '__main__':
    main()


