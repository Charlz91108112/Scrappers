import requests
from bs4 import BeautifulSoup as bs
import csv
import time

class ArabianScraper:
    def __init__(self):
        self.items = []
        self.company_links = []
        self.category_attr = ['Index','Title', 'URL', 'Regsitered Count']
        self.company_attr = ['Title', 'Email', 'Phone', 'Address', 'Fax Number', 'Website', 'Description']
        self.company_details = []
        self.category_index = 0
        self.cookies = {
            'ci_session': 'a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22ff442b702f37cd9532c6d3b66e3302c1%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A14%3A%2243.250.157.187%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A120%3A%22Mozilla%2F5.0+%28Linux%3B+Android+6.0%3B+Nexus+5+Build%2FMRA58N%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F103.0.0.0+Mobile+Sa%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1658421084%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D0236743f08d738ebc1e355fac1a68923d88bdb76',
        }
        self.headers = {
            'authority': 'www.arabiantalks.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryGTwBQioroBCwnJyu',
            # 'cookie': 'ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22ff442b702f37cd9532c6d3b66e3302c1%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A14%3A%2243.250.157.187%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A120%3A%22Mozilla%2F5.0+%28Linux%3B+Android+6.0%3B+Nexus+5+Build%2FMRA58N%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F103.0.0.0+Mobile+Sa%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1658421084%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D0236743f08d738ebc1e355fac1a68923d88bdb76',
            'origin': 'https://www.arabiantalks.com',
            'referer': 'https://www.arabiantalks.com/view-more-categories',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36',
        }

    def main(self):
        for i in range(10):
            all_li = self.category_scraper(i*12)
            for li in all_li:
                self.category_index += 1
                categories_title = ((li.select_one("a[href*='category'] > span")).text).split("Registered")[0]
                companies_registered = "Registered"+((li.select_one("a[href*='category'] > span")).text).split("Registered")[1]
                categories_url = li.select_one("a[href*='category']")['href']
                self.items.append({self.category_attr[0]:int(self.category_index), self.category_attr[1]:categories_title.strip(), self.category_attr[2]:categories_url.strip(), self.category_attr[3]:companies_registered.strip()})
                # yield items
            time.sleep(3)

        self.save_csv('Categories', self.category_attr, self.items)

        print('The Categories are saved in the file Categories.csv. Check the file.')
        print('Please input the category name to get details of companies in that category!\n\n')

        get_company_to_scrape_input = input("Either enter the category name or the index of the category: \n")

        if type(get_company_to_scrape_input) == int:
            get_company_to_scrape_input = get_company_to_scrape_input - 1
            link_to_further_scrape = self.items[get_company_to_scrape_input][self.category_attr[2]]
        elif type(get_company_to_scrape_input) == str:
            for item in self.items:
                if item[self.category_attr[1]] == get_company_to_scrape_input:
                    link_to_further_scrape = item[self.category_attr[2]]
                    break

        self.company_scrapper(link_to_further_scrape)

        for i in self.company_links:
            self.company_details_scrapper(i)
            time.sleep(2)
        self.save_csv('Companies', self.company_attr, self.company_details)


    def save_csv(self, filename, field_names, data):
        with open(f'{filename}.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            # for item in self.items:
            #     writer.writerow(item)
            writer.writerows(data)

    def company_scrapper(self, url):
        response = requests.post(url, cookies=self.cookies, headers=self.headers)
        x = bs(response.content, 'html.parser')
        all_item_props = x.select("span[itemprop='itemListElement']")
        for i in all_item_props:
            company_links = i.select_one("a[itemprop='item']")['href']
            self.company_links.append(company_links)

    def company_details_scrapper(self, url):
        response = requests.get(url, cookies=self.cookies, headers=self.headers)
        x = bs(response.content, 'html.parser')
        company_email = (x.select_one("h3[itemprop='email']").text).split(":")[1].strip()
        company_phone = (x.select_one("h3[itemprop='telephone']").text).split(":")[1].strip()
        company_address = (x.select_one("h3[itemprop='address']").text).split(":")[1].strip()
        company_faxNumber = (x.select_one("h3[itemprop='faxNumber']").text).split(":")[1].strip()
        company_website = ("Website:"+ x.select_one("h3 > a[itemprop='url']")['href']).split(":")[1].strip()
        company_title = x.select_one("h1[itemprop='Name']").text
        company_description = x.select_one("p[itemprop='description']").text
        self.company_details.append({self.company_attr[0]:company_title, self.company_attr[1]:company_email, self.company_attr[2]:company_phone, self.company_attr[3]:company_address, self.company_attr[4]:company_faxNumber, self.company_attr[5]:company_website, self.company_attr[6]:company_description})
        
        


    def category_scraper(self, initial_length):
        data = f'------WebKitFormBoundaryGTwBQioroBCwnJyu\r\nContent-Disposition: form-data; name="start"\r\n\r\n{initial_length}\r\n------WebKitFormBoundaryGTwBQioroBCwnJyu--\r\n'

        response = requests.post('https://www.arabiantalks.com/ajax/load_content_categories', cookies=self.cookies, headers=self.headers, data=data)
        x = bs(response.content, 'html.parser')
        all_li = x.find_all("li")
        return all_li