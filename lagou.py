from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv

driver = webdriver.Firefox()
driver.get('https://www.lagou.com')
driver.maximize_window()

#选择成都区
driver.find_element_by_css_selector("#changeCityBox > ul > li:nth-child(7)").click()
driver.implicitly_wait(15)

#搜索测试开发职位
driver.find_element_by_id("search_input").send_keys("测试开发")
driver.find_element_by_id("search_button").click()

#为了显示第一条职位信息，所以下拉滚动条
js = "window.scrollTo(0,180);"
driver.execute_script(js)
sleep(1)

def job_message():
    
    #获取职位名称
    jobs_name = driver.find_elements_by_xpath("//div[@class='p_top']/a/h3")
    #获取地址
    jobs_address = driver.find_elements_by_xpath("//span[@class='add']/em")
    #获取薪资/年限/学历
    jobs_require = driver.find_elements_by_xpath("//div[@class='p_bot']/div[@class='li_b_l']")

    return jobs_name,jobs_address,jobs_require

def open_new_window():

    #获取所有窗口句柄
    handles = driver.window_handles
    #跳转到新打开的页面
    driver.switch_to.window(handles[1])
    #获取职位详细信息
    job_advantage = driver.find_element_by_css_selector(".job-advantage").text
    job_bt = driver.find_element_by_css_selector(".job_bt").text
    sleep(1)
    #关闭当前页
    driver.close()
    #跳转到首页
    driver.switch_to.window(handles[0])

    return job_advantage,job_bt

def write_file(data):
    
    #写到csv文件中
    with open('output.csv','a',newline='')as csv_file:
        writer = csv.writer(csv_file)
        print(data)
        for n in data:
            writer.writerow(n)

def next_page():
    try:
        next_page = driver.find_element_by_xpath("//span[@class='pager_next ']")
    except NoSuchElementException:
        driver.quit()
    ActionChains(driver).move_to_element(next_page).perform()
    sleep(2)
    next_page.click()
    
a = 180
for page in range(2):
    jobs_name,jobs_address,jobs_require = job_message()
    for i in range(15):
        el = jobs_name[i]
        job_name = el.text      #职位
        job_address = jobs_address[i].text      #区域
        info = jobs_require[i].text.split(' ')
        job_salary = info[0]    #薪资
        job_exper = info[1]     #经验
        job_edu = info[3]       #学历

        el.click()
        job_advantage,job_bt = open_new_window()
        #将获取到的信息写到data 中
        data = [(job_name,job_address,job_salary,job_exper,job_edu,job_advantage,job_bt)]
        #每次滚动条下拉160
        a = a + 160
        js = "window.scrollTo(0,"+ str(a) +");"
        driver.execute_script(js)
        sleep(1)

        write_file(data)
    next_page()
      
driver.quit()

















