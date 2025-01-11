from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC


class SeleniumCrawler:
    def __init__(self):
        self.chrome_driver_path = ChromeDriverManager().install()

        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument("--single-process")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument(
            f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (HTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_driver = webdriver.Chrome(
            options=self.chrome_options,
            service=Service(executable_path=self.chrome_driver_path)
        )

        self.chrome_driver.implicitly_wait(5)

    def scroll_to_end(self):
        self.chrome_driver.find_element(
            By.TAG_NAME,
            'body'
        ).send_keys(
            Keys.END
        )

    def get_response(self, url: str):
        self.chrome_driver.get(url=url)

        return self.chrome_driver.page_source
