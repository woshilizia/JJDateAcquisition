# selenium对jj的数据进行爬虫
from selenium import webdriver
from enum import Enum, unique

# 配置浏览器信息
opt = webdriver.ChromeOptions()
opt.add_argument("--headless")
driver = webdriver.Chrome(options=opt, executable_path='E:/chromedriver_win32/chromedriver')
driver.get('http://www.jjwxc.net/fenzhan/dm/bl.html')
@unique
class ArticleType(Enum):
    bg_ancient = 1
    bg_urban = 2
    bg_urban_fantasy = 3
    bg_time_travel = 4
    bg_ancient_fantasy = 5
    bg_future = 6
    bl_urban = 7
    bl_urban_fantasy = 8
    bl_ancient = 9
    gl = 10
    no_cp = 11
    bg_two_dimensional_space = 12
    bg_derivation = 13
    bl_derivation = 14


class Article(object):
    def __init__(self, link, name, author, click, review, collected, type: ArticleType):
        self.article_link = link
        self.article_name = name
        self.article_author = author
        self.count_click = click
        self.count_review = review
        self.count_collected = collected
        self.article_type = type


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
