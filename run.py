import requests
from bs4 import BeautifulSoup

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


def get_urls():
    print('getting urls.........')

    params = {
        'page': 1
    }
    res = session.get('http://0.0.0.0:9999', params=params)

    f = open('./res.html', 'w+')
    f.write(res.text)
    f.close()

def get_detail():
    print('getting detail......')

def create_csv():
    print('csv generated...')

def run():
    login()
    get_urls()
    get_detail()
    create_csv()

if __name__ == '__main__':
    run()