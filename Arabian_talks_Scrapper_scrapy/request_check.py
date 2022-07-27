import requests
from bs4 import BeautifulSoup as bs

cookies = {
    'ci_session': 'a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22ff442b702f37cd9532c6d3b66e3302c1%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A14%3A%2243.250.157.187%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A120%3A%22Mozilla%2F5.0+%28Linux%3B+Android+6.0%3B+Nexus+5+Build%2FMRA58N%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F103.0.0.0+Mobile+Sa%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1658421084%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D0236743f08d738ebc1e355fac1a68923d88bdb76',
}

headers = {
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

data = '------WebKitFormBoundaryGTwBQioroBCwnJyu\r\nContent-Disposition: form-data; name="start"\r\n\r\n0\r\n------WebKitFormBoundaryGTwBQioroBCwnJyu--\r\n'

response = requests.post('https://www.arabiantalks.com/ajax/load_content_categories', cookies=cookies, headers=headers, data=data)
x = bs(response.content, 'html.parser')
all_li = x.find_all("li")
# categories_title = (categories_title[0].select_one("a[href*='category'] > span")).text
categories_url = all_li[0].select_one("a[href*='category']")['href']
print(categories_url)