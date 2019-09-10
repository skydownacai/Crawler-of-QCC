import time
import os
from requests.cookies import RequestsCookieJar
import traceback
import colorlog
import logging
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json
import pandas as pd
from bs4 import BeautifulSoup
import sys
from requests_toolbelt import SSLAdapter
import requests
adapter = SSLAdapter('TLSv1')
class NeedLogin(Exception):
    def __init__(self):
        pass
class OperationTooOfen(Exception):
    def __init__(self):
        pass
class Noresult(Exception):
    def __init__(self):
        pass
class Unexpected(Exception):
    def __init__(self):
        pass
class Log:
    def __init__(self, fileName):
        log_colors_config = {
            'DEBUG': 'fg_yellow',
            'INFO': 'fg_green',
            'WARNING': 'fg_red',
            'ERROR': 'fg_red',
            'CRITICAL': 'fg_red',
        }
        RESET_SEQ = "\033[0m"
        COLOR_SEQ = "\033[1;%dm"
        BOLD_SEQ = "\033[1m"
        self.filename = fileName
        self.logger = logging.getLogger("VeChain LJC")
        self.logger.setLevel(logging.DEBUG)
        #self.fileformatter = colorlog.ColoredFormatter(
        #    '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
        #    log_colors=log_colors_config)  # 日志输出格式
        self.consleformatter = colorlog.ColoredFormatter(
               '\033[7m%(asctime)s\033[0m%(log_color)s[%(levelname)-7s] : %(message)s',
            log_colors=log_colors_config)  # 日志输出格式
        fh = logging.FileHandler(filename=self.filename, mode='a',
                                 encoding='utf-8')  # 使用RotatingFileHandler类，滚动备份日志
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.consleformatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = colorlog.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.consleformatter)
        self.logger.addHandler(ch)
    @property
    def debug(self):
        return self.logger.debug
    @property
    def info(self):
        return self.logger.info
    @property
    def warning(self):
        return self.logger.warning
    @property
    def error(self):
        return self.logger.error
    @property
    def critical(self):
        return self.logger.critical
def TimeStamp(TIME,timeShuff = False):
    '''返回时间字符串的时间戳
       timeShuff:时间字符串是否包含 时分秒
    '''
    if timeShuff:
        return int(time.mktime(time.strptime(str(TIME),'%Y-%m-%d %H:%M:%S')))
    else:
        return int(time.mktime(time.strptime(str(TIME)+' 08:00:00','%Y-%m-%d %H:%M:%S')))
class antidriver:
    def __init__(self):
        pass
    def chrome(self):
        option = webdriver.ChromeOptions()
        option.add_argument(
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"')
        option.add_experimental_option('excludeSwitches',['enable-automation',"ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
        #option.add_argument('--headless')
        #username = os.getenv("USERNAME")
        #userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        #option.add_argument("user-data-dir={}".format(userProfile))
        option.add_argument('disable-infobars')
        localpath = "Google Chrome\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = localpath
        self.driver = webdriver.Chrome(chrome_options=option,executable_path= localpath)
        self.driver.delete_all_cookies()
        return self.driver
    def firefox(self,data = {"ip":"221.225.91.175","port":43301}):
        '以代理的形式启动一个firefox'
        self.location = 'C:\Program Files\Mozilla Firefox\\firefox.exe'
        self.profile = FirefoxProfile()
        self.profile.set_preference("network.proxy.type", 1)
        self.profile.set_preference('network.proxy.http', data['ip'])
        self.profile.set_preference('network.proxy.http_port', data['port'])  # int
        self.profile.update_preferences()
        self.driver = webdriver.Firefox(firefox_profile=self.profile, firefox_binary=self.location)
        return self.driver
def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track
class qcc():
    def __init__(self):
        #self.getproxy()
        self.header= {
        'Host': 'www.qichacha.com',
        'Connection': 'keep-alive',
        'Accept': r'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        "Referer": "https://www.qichacha.com/search?key=",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1'}
        self.log = Log("log")
        sys.exitfunc = self.exitfun
    @property
    def proxy(self):
        try:
            return  self._proxy
        except:
            self._proxy = {}
            return self._proxy
    @proxy.setter
    def proxy(self,value):
        self._proxy = value
    @property
    def driver(self):
        try:
            return self._driver
        except:
            self._driver = antidriver().chrome()
            return self._driver
    @driver.setter
    def driver(self,value):
        self._driver = value

    @property
    def requestcookiejar(self):
        try:
            return self._cookiejar
        except:
            self._cookiejar = RequestsCookieJar()
            return self._cookiejar
    @requestcookiejar.setter
    def requestcookiejar(self,value):
        if type(value) != type(RequestsCookieJar()):
            raise TypeError()
        self._cookiejar = value
    def getEnterUrlRequest(self,name):
        self.header["Referer"] = "https://www.qichacha.com"
        #self.getproxy()
        res =BeautifulSoup(requests.get("https://www.qichacha.com/search?key={}".format(name),headers=self.header,cookies = self.requestcookiejar,proxies = self.proxy).text,'html.parser')
        if res.text.startswith("window.location.href='https://www.qichacha.com/index_verify?"):
            raise OperationTooOfen
        if res.text[8:].startswith("会员登录"):
            raise NeedLogin
        try:
            company = res.find(attrs={"class":"ma_h1"})
            href = "https://www.qichacha.com" + company['href']
            return (company.text,href)
        except TypeError:
            try:
                res.find(attrs={"class": "noresult"})
            except:
                raise Unexpected
            raise Noresult
    def getEnterUrl(self,name):
        self.log.debug('尝试获取'+ name +'的详细信息url')
        headerKey = self.driver.find_element_by_id("headerKey")
        headerKey.clear()
        headerKey.send_keys(name)
        self.driver.find_element_by_class_name("top-searchbtn").click()
        if  "/index_verify?" in self.driver.current_url:
            raise OperationTooOfen
        if "user_login?" in self.driver.current_url:
            raise NeedLogin
        try:
            company = WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "ma_h1")))
            href = company.get_attribute('href')
            return (company.text, href)
        except:
            try:
                WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "noresult")))
                raise  Noresult
            except:
                raise NeedLogin
    def getDetail(self,url):
        "获得企业的具体信息"
        keys = {'统一社会信用代码': "null", '所属行业': "null", '经营范围': "null",'宗旨和业务范围':"null"}
        res = requests.get(url.replace("firm","cbase"), headers=self.header,cookies = self.requestcookiejar,verify=True)
        self.page = BeautifulSoup(res.text, 'html.parser')
        page = self.page
        if page.text.startswith("window.location.href='https://www.qichacha.com/index_verify?") or "function setCookie" in page.text:
            raise OperationTooOfen
        if page.text[8:].startswith("会员登录"):
            raise NeedLogin
        page = page.find(attrs={"id": "Cominfo"})
        if page == None:
            raise Noresult
        tds = page.find_all('td')
        self.tds = []
        for j in range(len(tds)):
            td = tds[j].text.replace(" ", "").replace("\n", '')
            self.tds.append(td)
            if td in keys or ("业务范围" in td and len(td) <= 10):
                if "业务范围" in td:
                    td = "宗旨和业务范围"
                keys[td] = tds[j + 1].text.replace(" ", "").replace("\n", '')

        ready = [keys[key] != "null" for key in keys]
        if any(ready):
            return {'code':1,'data':keys}
        else:
            raise Unexpected
    def getserachpage(self,driver:webdriver.Chrome = None):
        if driver == None:
            driver = self.driver
        while True:
            try:
                driver.get('https://www.qichacha.com/')
                driver.maximize_window()
                try:
                    s = WebDriverWait(driver, 10, 0.05).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="searchkey"]')))
                    s.send_keys("上海驷客信息科技有限公司")
                except:
                    print(traceback.format_exc())
                    driver.find_element_by_xpath('/html/body/div[3]/div/div/div/button/span[1]').click()
                    driver.find_element_by_xpath('//*[@id="searchkey"]').send_keys("上海驷客信息科技有限公司")
                break
            except:
                continue
        driver.find_element_by_xpath('//*[@id="V3_Search_bt"]').click()
        time.sleep(1)
        if  "/index_verify?" in driver.current_url:
            raise OperationTooOfen
        if "user_login?" in driver.current_url:
            raise NeedLogin
    def getcookie(self):
        pass
    def getproxy(self):
        api = "http://http.tiqu.qingjuhe.cn/getip?num=1&type=2&pack=36102&port=11&city=320500&yys=100017&pro=320000&lb=1&pb=5&regions="
        while True:
            try:
                raw = json.loads(requests.get(api, timeout=1).text)
            except:
                print('重新获取代理ip重连中')
                time.sleep(2)
                continue
            if raw['msg'] == '请2秒后再试' or len(raw['data']) == 0:
                print('重新获取代理ip重连中')
                time.sleep(2)
                continue
            data = raw['data'][0]
            print('update proxy:',data)
            proxies = {
                # "http": "http://202.121.96.33:8086",
                "http": "http://{}:{}".format(data['ip'], data['port']),
            }
            return (proxies,data)
    def handletoooften(self,driver:webdriver.Chrome):
        #verifyURL :https://www.qichacha.com/index_verify?type=companysearch
        self.log.debug("尝试解决操作过频繁问题中...")
        #driver.maximize_window()
        driver.get("https://www.qichacha.com/index_verify?type=companysearch")
        time.sleep(3)
        try:
            driver.maximize_window()
        except:
            pass
        if not "/index_verify?" in driver.current_url:
            cookies = driver.get_cookies()
            with open("cookies.txt", "w") as fp:
                json.dump(cookies, fp)
            self.log.debug("try to handle problem of <too often> and save cookie  done!")
            return 0
        while True:
            slider = WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "btn_slide")))
            action = ActionChains(driver)
            action.click_and_hold(slider).perform()
            action.reset_actions()  # 清除之前的action
            track = [4, 20,40,65,95,130,173,213,240,250]
            #track = get_track(250)
            for i in track:
                action.move_by_offset(xoffset=i, yoffset=0).perform()
                #action.reset_actions()
                time.sleep(0.1)
            action.release().perform()
            try:
                fresh = driver.find_element_by_xpath('//*[@id="dom_id"]/div/span/a')
                fresh.click()
                input("请手动操作,输入任意键继续")
                break
            except:
                break

        driver.find_element_by_class_name("btn-lg").click()
        time.sleep(1)
        cookies = driver.get_cookies()
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)
        self.log.debug("try to handle problem of <too often> and save cookie  done!")
    def simulateLogin(self,driver:webdriver.Chrome):
        # 打开登录页面
        #driver.maximize_window()
        self.log.debug("模拟登陆中...")
        while True:
            try:
                # 单击用户名密码登录的标签
                driver.get("https://www.qichacha.com/user_login")
                time.sleep(1)
                if "user_login" not in driver.current_url:
                    self.log.debug("No need to login")
                    return 0
                driver.find_element_by_id("normalLogin").click()
                time.sleep(1)
                input = driver.find_element_by_id('nameNormal')
                input.clear()
                input.send_keys('18011167319')
                input = driver.find_element_by_id('pwdNormal')
                input.clear()
                input.send_keys('ljc971124')
                break
            except:
                time.sleep(1)
                continue
        while True:
            slider = WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "btn_slide")))
            time.sleep(1)
            # 开始拖动 perform()用来执行ActionChains中存储的行为
            distance = 310
            action = ActionChains(driver)
            action.click_and_hold(slider).perform()
            action.reset_actions()  # 清除之前的action
            track = [3,14,20,30,42,70,95,126,146,186,223,-100,258,290,308]
            for i in track:
                action.move_by_offset(xoffset=i, yoffset=0).perform()
                #action.reset_actions()
                time.sleep(0.1)
            action.release().perform()
            try:
               fresh = driver.find_element_by_xpath('//*[@id="dom_id_one"]/div/span/a')
               fresh.click()
               time.sleep(1)
            except:
                break
        # 单击登录按钮
        btn = driver.find_element_by_xpath('//*[@id="user_login_normal"]/button')
        btn.click()
        driver.get("https://www.qichacha.com/firm_45c5e76df53d5d0e1e21dc6e9c393ebc.html")
        time.sleep(3)
        "下面要检查是否出现操作过于频繁的界面"
        check = driver.find_element_by_class_name("col-sm-12").text
        if "操作过于频繁" in check:
            self.log.error("操作频繁!")
            self.handletoooften(driver)
        cookies = driver.get_cookies()
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)

        self.log.debug('try to simulate login and save cookie done!')
    def updatecookie(self):
        with open("cookies.txt", "r") as fp:
            cookies = json.load(fp)
            for cookie in cookies:
                self.requestcookiejar.set(cookie['name'], cookie['value'])
        self.log.info("Load local cookie:" + str(self.requestcookiejar))
    def changeproxyandcookie(self):
        #(proxy,data) = self.getproxy()
        self.driver = antidriver().firefox()
        self.driver.get("http://httpbin.org/ip")
        time.sleep(2)
        self.driver.get("https://www.qichacha.com")
        time.sleep(1)
        self.driver.get("https://www.qichacha.com/firm_45c5e76df53d5d0e1e21dc6e9c393ebc.html")
        time.sleep(1)
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.requestcookiejar.set(cookie['name'], cookie['value'])
        self.log.debug('try to fix problem and save cookie done!')
    def getAllEnterUrlV2(self,file):
        data = pd.read_excel(file)
        names = data["单位详细名称"].values
        num = len(names)
        names = (name for name in names)
        outcome = {
            "name":[],
            "href":[],
            "searchname":[]
        }

        name = names.__next__()

        self.driver.set_window_size(500,600)#设定固定大小
        counter = 1
        while True:
            try:
                self.getserachpage()
                while True:
                    outcome['name'].append(name)
                    (companyname, url) = self.getEnterUrl(name)
                    outcome['href'].append(url)
                    outcome['searchname'].append(companyname)
                    self.log.info("Get[{}/{}]:<{}/{}>".format(counter,num,name,companyname) + url)
                    name = names.__next__()
                    time.sleep(self.interval)
                    counter += 1
            except OperationTooOfen:
                self.log.error("操作频繁!")
                self.handletoooften(self.driver)
            except NeedLogin:
                self.log.error("需要登陆!")
                self.simulateLogin(self.driver)
                continue
            except Noresult:
                self.log.error("没有想要的结果!")
            except Unexpected:
                self.log.error("未知错误!")
                exit()
            except StopIteration:
                self.log.info("所有任务完成!")
                break
        pd.DataFrame(outcome).to_csv("企业网页地址.csv",encoding='utf_8_sig')
    def getAllEnterUrl(self,file):
        data = pd.read_excel(file)
        if os.path.exists("1W企业网页地址.csv"):
            with open("1w企业网页地址.csv",encoding='utf_8_sig') as f:
                have = pd.read_csv(f)
            outcome = {
                "name":list(have['name'].values),
                "href":list(have['href'].values),
                "searchname":list(have['searchname'].values)
            }
        else:
            outcome = {
                "name":[],
                "href":[],
                "searchname":[]
            }
        names = data["单位详细名称"].values[len(outcome['name']):9813]

        num = len(names)
        names = (name for name in names)
        self.updatecookie()
        name = names.__next__()
        counter = 1 + len(outcome['name'])
        HadTooOfen = False
        while True:
            try:
                while True:
                    self.log.debug('Try<{}/{}>:'.format(counter, 9812) + name)
                    (companyname, url) = self.getEnterUrlRequest(name)
                    outcome['name'].append(name)
                    outcome['href'].append(url)
                    outcome['searchname'].append(companyname)
                    self.log.info("Autosaving")
                    pd.DataFrame(outcome).to_csv("1W企业网页地址.csv", encoding='utf_8_sig')
                    self.log.info("Get[{}/{}]:<{}/{}>".format(counter,num,name,companyname) + url)
                    name = names.__next__()
                    HadTooOfen = False
                    time.sleep(0.5)
                    counter += 1
            except OperationTooOfen:
                self.log.error("操作频繁!")
                if HadTooOfen == False:
                    self.log.debug("等待十秒尝试解决")
                    time.sleep(10)
                    HadTooOfen = True
                else:
                    self.handletoooften(self.driver)
                    self.updatecookie()
            except NeedLogin:
                self.log.error("需要登陆!")
                self.simulateLogin(self.driver)
                self.updatecookie()
                continue
            except Noresult:
                self.log.error("没有想要的结果!")
                outcome['name'].append(name)
                outcome['href'].append('无')
                outcome['searchname'].append("无")
                name = names.__next__()
            except Unexpected:
                self.log.error("未知错误!")
                print(traceback.format_exc())
                exit()
            except StopIteration:
                self.log.info("所有任务完成!")
                pd.DataFrame(outcome).to_csv("1w企业网页地址.csv", encoding='utf_8_sig')
                break
    def getAllEnterDetail(self):
        self.log.info('starting geting detail infromation')
        keys = ['统一社会信用代码', '所属行业', '经营范围', '宗旨和业务范围']
        if os.path.exists("1wdata.csv"):
            with open("1wdata.csv",encoding='utf_8_sig') as f:
                data = pd.read_csv(f)
            g = lambda x: max([i + 1 if type(x[i]) == type("a") and len(x[i]) >= 5 else 0 for i in range(len(x))])
            self.counter = max(g(data['所属行业']),g(data['经营范围']),g(data['宗旨和业务范围']))
        else:
            self.counter = 0
            for file in os.listdir():
                if "企业网页地址" in file:
                    with open(file, encoding='utf_8_sig') as f:
                        data = pd.read_csv(f)
                    break
            for key in keys:
                data[key] = 'null'
        for column in data.columns:
            if "Unnamed:" in column:
                data = data.drop(columns=column)
        data.reset_index(drop=True)
        self.simulateLogin(self.driver)
        self.updatecookie()
        for i in range(self.counter,len(data['href'])):
            url = str(data['href'][i])
            name = str(data['name'][i])
            self.log.debug('尝试获取 <{}>:'.format(i)+name+" url:"+url)
            if  len(url) <= 10:
                self.log.debug('跳过\n')
                for key in keys:
                    data[key][i]= "null"
                continue
            while True:
                try:
                    detail = self.getDetail(url)
                    self.log.info("download:"+str(detail['data']))
                    for key in detail['data']:
                        data[key][i] = detail['data'][key]
                    self.log.info("Autosaving...")
                    data.to_csv("1wdata.csv",encoding="utf_8_sig")
                    break
                except NeedLogin:
                    self.log.error("需要登录!")
                    self.simulateLogin(self.driver)
                    self.updatecookie()
                except OperationTooOfen:
                    self.log.error("操作频繁!")
                    self.handletoooften(self.driver)
                    self.updatecookie()
                except Noresult:
                    self.log.error("没有数据!跳过!")
                    for key in keys:
                        data[key][i] = "Need Manual Check"
                    break
                except Unexpected:
                    self.log.error("未知错误 跳过!")
                    print(traceback.format_exc())
                    for key in keys:
                        data[key][i] = "Need Manual Check"
                    break
            self.counter += 1
        self.log.info("All detail infromation have been downloaded!")
        data.to_csv("data.csv",encoding="utf_8_sig")
        #print(res.text)
    def getAllEnterDetailV2(self):
        stime = time.time()
        self.log.info('starting geting detail infromation')
        keys = ['统一社会信用代码', '所属行业', '经营范围', '宗旨和业务范围']
        if os.path.exists("data.csv"):
            with open("data.csv",encoding='utf_8_sig') as f:
                data = pd.read_csv(f)
        else:
            with open('企业网页地址.csv', encoding='utf_8_sig') as f:
                data = pd.read_csv(f)
            for key in keys:
                data[key] = 'null'
        for column in data.columns:
            if "Unnamed:" in column:
                data = data.drop(columns=column)
        data.reset_index(drop=True)
        self.counter = 1046
        self.changeproxyandcookie()
        self.driver = antidriver().firefox()
        HadTooOfen = False
        for i in range(self.counter,len(data['href'])):
            url = str(data['href'][i])
            name = str(data['name'][i])
            self.log.debug('尝试获取 <{}>:'.format(i)+name+" url:"+url)
            if  len(url) <= 10:
                self.log.debug('跳过\n')
                for key in keys:
                    data[key][i]= "null"
            while True:
                try:
                    detail = self.getDetail(url)
                    self.log.info("download:"+str(detail['data']))
                    HadTooOfen = False
                    for key in detail['data']:
                        data[key][i] = detail['data'][key]
                    self.log.info("Autosaving...")
                    data.to_csv("data.csv",encoding="utf_8_sig")
                    break
                except NeedLogin:
                    self.log.error("需要登录!")
                    self.simulateLogin(self.driver)
                    self.getproxy()
                    self.updatecookie()
                except OperationTooOfen:
                    self.log.error("操作频繁!")
                    if HadTooOfen == False:
                        self.log.debug("等待十秒尝试解决")
                        time.sleep(10)
                    else:
                        HadTooOfen = True
                        self.handletoooften(self.driver)
                        self.updatecookie()
                except Noresult:
                    self.log.error("没有数据!")
                    for key in keys:
                        data[key][i] = "Need Manual Check"
                    break
                except Unexpected:
                    self.log.error("未知错误 跳过!")
                    for key in keys:
                        data[key][i] = "Need Manual Check"
                    break
            self.counter += 1
        self.log.info("All detail infromation have been downloaded!")
        data.to_csv("data.csv",encoding="utf_8_sig")
        #print(res.text)
    def exitfun(self):
        print('hellow')
app = qcc()
#app.handletoooften(antidriver().get_driver())
app.getAllEnterDetail()