# selenium对jj的数据进行爬虫
from selenium import webdriver
from enum import Enum, unique

# 配置浏览器信息
opt = webdriver.ChromeOptions()
opt.add_argument("--headless")
driver = webdriver.Chrome(options=opt, executable_path='E:/chromedriver_win32/chromedriver')
driver.get('http://www.jjwxc.net/fenzhan/dm/bl.html')
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
    def __init__(self, link, name, author, click, review, collected, article_type, article_list, list_number):
        self.article_link = link
        self.article_name = name
        self.article_author = author
        self.count_click = click
        self.count_review = review
        self.count_collected = collected
        self.article_type = article_type
        self.article_list = article_list
        self.list_number = list_number


links = driver.find_elements_by_xpath("//div[@class = 'wrapper box_06 first']/ul/li/a")
link_list = [link.get_attribute('href') for link in links]
for link in link_list:
    driver.get(link)
    article_name = driver.find_element_by_xpath("//*[@id='oneboolt']/tbody/tr[1]/td/div/span/h1/span").text
    article_author = driver.find_element_by_xpath("//*[@id='oneboolt']/tbody/tr[1]/td/div/h2/a/span").text
    count_click = driver.find_element_by_xpath("//*[@id='totleclick']").text
    count_review = driver.find_element_by_xpath("//span[@itemprop='reviewCount']").text
    count_collected = driver.find_element_by_xpath("//span[@itemprop='collectedCount']").text
    print(' '.join([article_name, article_author, count_click, count_review, count_collected]))
    print("--------------------")
    driver.back()
