import glob
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

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


def get_detail(url):
    print('getting detail......{}'.format(url))
    res = session.get('http://0.0.0.0:9999'+url)

    # sebagai results dari get_urls() page 1
    f = open('./res.html', 'w+')
    f.write(res.text)
    f.close()

    # Metode Python Strip () digunakan untuk menghapus kepala dan ekor string karakter yang ditentukan (default adalah spasi).
    # Metode replace () mengembalikan salinan string di mana semua kemunculan substring diganti dengan substring lain.
    soup = BeautifulSoup(res.text, 'html5lib')
    title = soup.find('title').text.strip()
    price = soup.find('h4', attrs={'class': 'card-price'}).text.strip()
    stock= soup.find('span', attrs={'class': 'card-stock'}).text.strip().replace('stock: ', '')
    category = soup.find('span', attrs={'class': 'card-category'}).text.strip().replace('category: ', '')
    description = soup.find('p', attrs={'class': 'card-text'}).text.strip().replace('Description: ', '')

    dict_data = {
        'title': title,
        'price': price,
        'stock': stock,
        'category': category,
        'description': description,
    }

    #generate file JSON setiap produk kedalam folder
    with open('./results/{}.json'.format(url.replace('/', '')), 'w') as outfile:
        json.dump(dict_data, outfile)


def create_csv():
    # fungsi glob untuk print file
    files = sorted(glob.glob('./results/*.json'))

    datas = []
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

     #generate pakai pandas
    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)
    # df.to_excel('results.xlsx', index=False)

    print('csv generated...')

def run():

    total_pages = login()

    options = int(input('Input option number:\n1.Collecting all urls\n2.Get detail all product\n3.Create csv :\n '))
    if options == 1:
        total_urls = []
        for i in range(total_pages):    # in range biasa mulai dari 0 makanya di +1
            page = i + 1
            urls = get_urls(page)
            total_urls += urls   # total_urls = total_urls + urls

        # print(total_urls)
        # print(len(total_urls))

        # write JSON file
        with open('all_urls.json', 'w') as outfile:
            json.dump(total_urls, outfile)

    # NOTE : ketika sudah mendapatkan urlsnya tinggal dibaca saja karena memakan waktu untuk kasus memiliki urls ribuan

    # BISA DIKOMENTARI KETIKA SUDAH MENDAPATKAN FILENYA
    if options == 2:
        # reading from JSON file
        with open('all_urls.json') as json_file:
            all_url = json.load(json_file)

        # cara dibawah looping lama karena semua yang dilooping
        for url in all_url:
            get_detail(url)

        # get_detail('/takoyakids-lyla-racer-back-dress-terracota')
    if options == 2:
        create_csv()

if __name__ == '__main__':
    run()