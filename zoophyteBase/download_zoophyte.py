import os
from selenium import webdriver

home = "http://bioserv7.bioinfo.pbf.hr/Zoophyte/registration/login.jsp"
NUM_OF_PAGE = 10  # All sequences can be downloaded,check how many pages it has.
username = "your_user_name" 
passwd = "your_password"
query_dir = "download_path"

#setting
IMPLICIT_WAIT_TIME = 10 
chromeoptions = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups':0,'download.default_directory': query_dir}
chromeoptions.add_experimental_option('prefs',prefs)
# chromedriver has to be in system path.
chromedriver = "/Users/jc502059/local/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

#let's go
driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=chromeoptions)
driver.implicitly_wait(IMPLICIT_WAIT_TIME)

#An account is needed for this database.

def site_login():
    
    driver.get(home)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(passwd)
    driver.find_element_by_name("submit").click()


site_login()

# I need genes involve in all function available.
driver.find_element_by_link_text("Zoophy (text search)").click()
driver.find_element_by_id("q").send_keys("*")
driver.find_element_by_id("querySubmit").click()

#There are hundreds of pages. select all and download!
for i in range(NUM_OF_PAGE):
    driver.find_element_by_link_text('Select All').click()
    driver.find_element_by_link_text('Download Sequences').click()
    if i != NUM_OF_PAGE - 1:
        driver.find_element_by_link_text('next').click()


