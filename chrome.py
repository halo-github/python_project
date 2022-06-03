from selenium import webdriver
import time
# 加启动配置

option = webdriver.ChromeOptions()
#option.add_argument('')

# 打开chrome浏览器
#driver = webdriver.Chrome()
driver = webdriver.Chrome(chrome_options=option)
#,executable_path="D:\Program Files\python3.9\chromedriver.exe"
#driver.get("www.baidu.com")
