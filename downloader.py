import os
import requests
from urllib.parse import urljoin
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


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


crawler = SeleniumCrawler()

while True:
    url = input("URL을 입력하세요 (종료하려면 q를 입력하세요): ")

    if url.lower() == 'q':
        crawler.chrome_driver.quit()
        break

    try:
        crawler.chrome_driver.get(url)

        download_element = crawler.chrome_driver.find_element(
            By.XPATH, "//div[@class='engagement-item download ']//a")

        download_url = download_element.get_attribute('href')

        if download_url:
            download_url = urljoin(url, download_url)

            crawler.chrome_driver.get(download_url)

            image_size_header = crawler.chrome_driver.find_element(
                By.ID, "all-sizes-header")
            sizes_list = image_size_header.find_element(
                By.CLASS_NAME, 'sizes-list')
            all_size_items = sizes_list.find_elements(By.TAG_NAME, 'li')

            try:
                biggest_size = all_size_items[-1]
                biggest_size_link = biggest_size.find_element(
                    By.TAG_NAME, 'a').get_attribute('href')
            except:
                biggest_size = all_size_items[-2]
                biggest_size_link = biggest_size.find_element(
                    By.TAG_NAME, 'a').get_attribute('href')

            crawler.chrome_driver.get(biggest_size_link)

            image_element = crawler.chrome_driver.find_element(
                By.ID, "allsizes-photo").find_element(By.TAG_NAME, 'img')
            image_url = image_element.get_attribute('src')

            print(f"Image URL: {image_url}")

            image_response = requests.get(image_url)

            image_name = os.path.basename(image_url)
            with open(image_name, 'wb') as file:
                file.write(image_response.content)

            print(f"{image_name} 다운로드 완료.")
        else:
            print("다운로드 링크를 찾을 수 없습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
