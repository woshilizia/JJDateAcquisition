# selenium对jj的数据进行爬虫
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from enum import Enum, unique

# 文章类型
@unique
class ArticleType(Enum):
    BG_ANCIENT = 1
    BG_URBAN = 2
    BG_URBAN_FANTASY = 3
    BG_TIME_TRAVEL = 4
    BG_ANCIENT_FANTASY = 5
    BG_FUTURE = 6
    BL_URBAN = 7
    BL_URBAN_FANTASY = 8
    BL_ANCIENT = 9
    GL = 10
    NO_CP = 11
    BG_TWO_DIMENSIONAL_SPACE = 12
    BG_DERIVATION = 13
    BL_DERIVATION = 14

    @classmethod
    def value_str(cls, key):
        # 使用字典的方法模拟switch语句
        key_map = {
            cls.BG_ANCIENT.value: '古代言情',
            cls.BG_URBAN.value: '都市青春',
            cls.BG_URBAN_FANTASY.value: '幻想言情',
            cls.BG_TIME_TRAVEL.value: '古代穿越',
            cls.BG_ANCIENT_FANTASY.value: '奇幻言情',
            cls.BG_FUTURE.value: '未来游戏悬疑',
            cls.BL_URBAN.value: '现代都市纯爱',
            cls.BL_URBAN_FANTASY: '现代幻想纯爱',
            cls.BL_ANCIENT: '古代纯爱',
            cls.GL: '百合',
            cls.NO_CP: '无CP',
            cls.BG_TWO_DIMENSIONAL_SPACE: '二次元言情',
            cls.BG_DERIVATION: '衍生言情',
            cls.BL_DERIVATION: '衍生纯爱'
        }
        return key_map.get(key, '')


# 榜单
@unique
class ArticleList(Enum):
    EDITOR_RECOMMEND = 1
    VIP_NEW_ARTICLE = 2
    @classmethod
    def value_str(cls, key):
        key_map = {
            cls.EDITOR_RECOMMEND.value: '编辑推荐榜',
            cls.VIP_NEW_ARTICLE.value: 'VIP新文榜'
        }


# 存放文章信息
class Article(object):
    def __init__(self, link, name, author, click, recommend, collected, article_type, article_list, list_number):
        self.article_link = link
        self.article_name = name
        self.article_author = author
        self.count_click = click
        self.count_recommend = recommend
        self.count_collected = collected
        self.article_type = article_type
        self.article_list = article_list
        self.list_number = list_number


# 获得晋江数据类
class JJDateAcquire:
    def __init__(self):
        self.driver = webdriver.Chrome(options=self.set_web_option(), executable_path='E:/chromedriver_win32/chromedriver')

    # 配置浏览器信息
    @staticmethod
    def set_web_option():
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        # 不等待解析完毕就直接返回
        opt.set_capability('pageLoadStrategy', 'none')
        return opt

    def find_elements(self, link):
        return WebDriverWait(self.driver, 10, poll_frequency=0.05).until(
            EC.visibility_of_all_elements_located((By.XPATH, link)))

    def find_element(self, link):
        return WebDriverWait(self.driver, timeout=10, poll_frequency=0.05).until(
                EC.visibility_of_element_located((By.XPATH, link)))

    def acquire_article_type(self, jj_url):
        self.driver.get(jj_url)
        try:
            links = self.find_elements('//*[@id="sitehead"]/div[4]/div[2]/div[1]/a')
            link_list = dict()
            for link in links:
                link_list[link.text] = link.get_attribute('href')
            for article_type, article_type_url in link_list.items():
                if not article_type == '完结':
                    print(article_type, article_type_url)
        except Exception as e:
            print(e)

    # //*[@id="main"]/div[12]/div
    def acquire_article_list(self, article_type_url, article_type):
        self.driver.get(article_type_url)  # 'http://www.jjwxc.net/fenzhan/dm/bl.html'
        try:
            links = self.find_elements('//div[@class = "wrapper box_06 first"]/ul/li/a')
            link_list = [link.get_attribute('href') for link in links]
            for link in link_list:
                self.acquire_article(link, article_type, '1', '1')
        finally:
            self.driver.quit()

    def acquire_article(self, article_link, article_type, article_list, list_number):
        self.driver.get(article_link)
        try:
            result_list = dict()
            self.find_element(xpath_list['article_name'])
            for name, xpath in xpath_list.items():
                result_list[name] = self.driver.find_element_by_xpath(xpath).text

            print(' '.join(result for result in result_list.values()))
            print(' '.join([article_type, article_list, list_number]))
            print("--------------------")
        except Exception as e:
            print("--------------------", e)

    def get_date(self, jj_url):
        self.driver.get(jj_url)  # 'http://www.jjwxc.net/fenzhan/dm/bl.html'
        try:
            links = self.find_elements('//div[@class = "wrapper box_06 first"]/ul/li/a')
            link_list = [link.get_attribute('href') for link in links]
            for link in link_list:
                self.acquire_article(link, '1', '1', '1')
        finally:
            self.driver.quit()


xpath_list = dict()
xpath_list['article_name'] = '//*[@id="oneboolt"]/tbody/tr[1]/td/div/span/h1/span'
xpath_list['article_author'] = '//*[@id="oneboolt"]/tbody/tr[1]/td/div/h2/a/span'
xpath_list['count_collected'] = '//span[@itemprop="collectedCount"]'
xpath_list['count_click'] = '//*[@id="totleclick"]'
xpath_list['count_recommend'] = '//span[@itemprop="reviewCount"]'
# //*[@id="main"]/div[14]/div[1]
# //*[@id="main"]/div[14]/div[2]
date = JJDateAcquire()
# date.acquire_article_type('http://www.jjwxc.net/fenzhan/yq/')
date.get_date('http://www.jjwxc.net/fenzhan/dm/bl.html')