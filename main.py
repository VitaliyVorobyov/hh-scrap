import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import fake_headers
import requests


class MyParser:
    def __init__(self, url: str, driver: any, headers: any):
        self.url = url
        self.driver = driver
        self.headers = headers

    def get_links_vacancy(self, url: str) -> list:
        self.driver.get(url)
        links = self.driver.find_elements(By.CLASS_NAME, 'vacancy-serp-item-body__main-info')
        return list(map(lambda x: x.find_element(By.TAG_NAME, 'a').get_attribute('href'), links))

    def parser(self) -> list:
        links = self.get_links_vacancy(self.url)
        list_vacancy = []
        for link in links:
            response = requests.get(link, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.h1.get_text()
            company = soup.find('a', {'data-qa': 'vacancy-company-name'}).get_text()
            city = soup.find('p', {'data-qa': 'vacancy-view-location'})
            description = soup.find('div', {'data-qa': 'vacancy-description'}).get_text()
            stack = soup.find('div', {'class': 'vacancy-section'}).get_text()
            salary = soup.find('span', {'data-qa': 'vacancy-salary-compensation-type-net'})
            salary = salary.get_text() if salary else None
            city = city.get_text() if city else soup.find('span', {'data-qa': 'vacancy-view-raw-address'}).get_text()
            if 'Python' and 'Django' in description or 'Python' and 'Flask' in stack:
                dict_vacancy = {'name': name, 'company': company, 'city': city.split(",")[0], 'salary': salary}
                list_vacancy.append(dict_vacancy)
        return list_vacancy


def start():
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    driver = webdriver.Chrome()
    headers = fake_headers.Headers(os="win", browser="chrome").generate()
    parser = MyParser(url, driver, headers)
    vacancy = parser.parser()
    driver.close()
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(vacancy, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    start()
