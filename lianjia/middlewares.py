import pickle
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse

COOKIE_FILE = "cookies.pkl"


import undetected_chromedriver as uc

class SeleniumMiddleware:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        # options.add_argument('--headless')  # 如果你需要无头模式

        self.driver = uc.Chrome(options=options, headless=False)  # 或设置headless=True
        self.driver.implicitly_wait(5)



        # 这里示范用默认路径的chromedriver，如果你把chromedriver放在非默认路径，需要指定Service路径
        service = Service()  # 或者 Service(executable_path='/path/to/chromedriver')
        self.driver.maximize_window()

        self.load_cookies_if_exist()

    def load_cookies_if_exist(self):
        """从本地文件加载cookie"""
        if os.path.exists(COOKIE_FILE):
            self.driver.get("https://sh.lianjia.com")  # 必须先访问页面再设置cookie
            with open(COOKIE_FILE, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    if isinstance(cookie.get('expiry', None), float):
                        cookie['expiry'] = int(cookie['expiry'])
                    try:
                        self.driver.add_cookie(cookie)
                    except Exception:
                        continue
            print("[INFO] Cookie 加载完毕")

    def save_cookies(self):
        """保存当前cookie到本地文件"""
        with open(COOKIE_FILE, "wb") as f:
            pickle.dump(self.driver.get_cookies(), f)
        print("[INFO] Cookie 保存成功")

    def process_request(self, request, spider):
        if spider.name == "lianjia":
            try:
                self.driver.get(request.url)
                # 检查是否跳转到了登录/验证页面
                if "clogin.lianjia.com" in self.driver.current_url or "hip.lianjia.com" in self.driver.current_url:
                    print("[WARNING] 检测到跳转到登录页或验证页，请手动处理...")
                    input("处理完成后按回车继续...")
                    self.save_cookies()
                self.scroll_to_bottom()
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@class='sellListContent']"))
                )
                body = self.driver.page_source
                return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

            except Exception as e:
                spider.logger.warning(f"[ERROR] Selenium 加载失败: {e} URL: {request.url}")
                return HtmlResponse(url=request.url, status=500, request=request)

    def scroll_to_bottom(self, pause_time=0.4, max_scrolls=15):
        #向下滚动页面以加载更多数据
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(max_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(random.uniform(1.8, 2.2))#暂停随机时间

    def __del__(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception:
            pass
