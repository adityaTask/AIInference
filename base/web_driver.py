from selenium import webdriver
from utilities.read_config import config

class WebDriver():

    def web_driver_instance(self):
        baseURL = (config['web']['url'])
        print("base url = " + baseURL)
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path = 'D:\\workspace_python\\drivers\\chromedriver.exe',options=options)
        driver.implicitly_wait(2)
        driver.maximize_window()
        driver.get(baseURL)
        return driver

