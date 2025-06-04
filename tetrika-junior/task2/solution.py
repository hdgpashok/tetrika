import csv
import requests
from bs4 import BeautifulSoup


def to_next_page(url):
    print('moving to next page')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.text, 'html.parser')
    next_page = soup.find('a', title= 'Категория:Животные по алфавиту', string='Следующая страница')

    return "https://ru.wikipedia.org" + next_page['href']


def get_animals_from_page(url: str, headers: dict) -> set:
    print('get new page animals list')
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.text, 'html.parser')
    my_category_group = soup.find_all('div', class_='mw-category-group')
    li_tags = []

    for li in my_category_group:
        li_tags.extend(li.find_all('li'))

    animals = set()
    for li in li_tags:
        a_tag = li.find('a')
        if a_tag.text and ('А' <= a_tag.text[0] <= 'Я'):
            animals.add(a_tag.text.strip())

    return animals



def to_dict(url) -> dict:

    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    russian_alphabet = {letter: 0 for letter in alphabet}
    base_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    current_url = base_url

    while True:
        animals = [letter[0].lower() for letter in get_animals_from_page(current_url, headers)]
        if len(animals) == 0:
            break
        for animal in animals:
            if animal in russian_alphabet.keys():
                russian_alphabet[animal] += 1
        current_url = to_next_page(current_url)

    return russian_alphabet


def write_to_csv(data):
    print('writing file')
    with open('result.csv', 'w', newline= '', encoding="utf-8") as file:
        writer = csv.writer(file)

        for key, value in data.items():
            writer.writerow([key, value])



if __name__ == '__main__':
    base_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    data = to_dict(base_url)
    write_to_csv(data)