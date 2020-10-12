import requests
from bs4 import BeautifulSoup

# pakai session karena adanya login
session = requests.Session()

def login():
    print('login...')
    datas = {
        'username': 'user',
        'password': 'user12345'
    }

    res = session.post('http://0.0.0.0:9999/login', data=datas)

    soup = BeautifulSoup(res.text, 'html5lib')

    page_item = soup.find_all('li', attrs={'class': 'page-item'})
    total_pages = len(page_item) - 2
    return total_pages


def get_urls(page):
    print('getting urls.........  page()', format(page))

    params = {
        'page': page
    }
    res = session.get('http://0.0.0.0:9999', params=params)

    # soup = BeautifulSoup(open('./res.html'), 'html5lib')

    soup = BeautifulSoup(res.text, 'html5lib')

    titles = soup.find_all('h4', attrs={'class': 'card-title'})
    urls = []              # untuk dijadikan satu
    for title in titles:
        url = title.find('a')['href']
        urls.append(url)

    return urls

    # sebagai result dari get_urls() page 1
    # f = open('./res.html', 'w+')
    # f.write(res.text)
    # f.close()

def get_detail():
    print('getting detail......')

def create_csv():
    print('csv generated...')

def run():
    # login()
    total_pages = login()
    total_urls = []
    for i in range(total_pages):    # in range biasa mulai dari 0 makanya di +1
        page = i + 1
        urls = get_urls(page)
        total_urls += urls   # total_urls = total_urls + urls

    print(total_urls)
    print(len(total_urls))

    get_detail()
    create_csv()

if __name__ == '__main__':
    run()