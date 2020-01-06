# selenium对jj的数据进行爬虫
import time
from selenium import webdriver

# 配置浏览器信息
opt = webdriver.ChromeOptions()
opt.add_argument("--headless")
driver = webdriver.Chrome(options=opt, executable_path='E:/chromedriver_win32/chromedriver')
driver.get('http://www.jjwxc.net/fenzhan/dm/bl.html')

driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1)

links = driver.find_elements_by_xpath("//div[@class = 'wrapper box_06 first']/ul/li/a")
link_list = []
for link in links:
	link_list.append(link.get_attribute('href'))
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


