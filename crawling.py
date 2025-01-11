import os
import requests
from urllib.parse import urljoin
from crawler import SeleniumCrawler
from selenium.webdriver.common.by import By

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

            image_size_header = crawler.chrome_driver.find_element(By.ID, "all-sizes-header")
            sizes_list = image_size_header.find_element(By.CLASS_NAME, 'sizes-list')
            all_size_items = sizes_list.find_elements(By.TAG_NAME, 'li')

            try:
                biggest_size = all_size_items[-1]
                biggest_size_link = biggest_size.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                biggest_size = all_size_items[-2]
                biggest_size_link = biggest_size.find_element(By.TAG_NAME, 'a').get_attribute('href')

            crawler.chrome_driver.get(biggest_size_link)

            image_element = crawler.chrome_driver.find_element(By.ID, "allsizes-photo").find_element(By.TAG_NAME, 'img')
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
