#!/usr/bin/env python3
import requests
import re
from bs4 import BeautifulSoup

dnd_source = 'https://dungeon.su'
mob_html_group = dnd_source + '/bestiary/'

parse_mob1 = '/bestiary/305-umber_hulk/'
parse_mob2 = '/bestiary/84-imp/'


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'}
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Network err...")
        return False


def get_mobs():
    html = get_html(mob_html_group)
    soup = BeautifulSoup(html, 'html.parser')
    if html:
        all_mobs = soup.find('ul', class_='list-of-items').findAll('li', class_='')
        print('List counts: {}'.format(len(all_mobs)))
        input('__________')
        for mob in all_mobs:
            title = mob.find('a').text
            mob_href = mob.find('a')['href']
            print('------' * 30)
            print('Name: {}, Href: {}'.format(title, mob_href))
            parse_mob(mob_href)
            input()


def print_lis(params, block_descr):
    for param in params:
        li = param.findAll('li', recursive=False)
        if li:
            print_lis(li, '{}_sub'.format(block_descr))
        else:
            print(search_title(param.text))


def search_title(text):
    TITLES = (
        'Действия',
        'Действия логова',
        'Игровой персонаж',
        'Источник:',
        'Класс доспеха:',
        'Материал взят ',
        'Монстра добавил:',
        'Навыки:',
        'Опасность:',
        'Описание',
        'Реакции',
        'Спасброски:',
        'Способности',
        'Скорость:',
        'Легендарные действия',
        'Логово',
        'Хиты:',
        'Чувства:',
        'Эффекты логова',
    )
    for title in TITLES:
        result = re.findall(title+'(.*)', text)
        if result:
            return title + '::: ' + result[0] + '\r\n'

    # Undifined пишем в description
    return 'Undifined....' + text + '\r\n'


def parse_stats(params):
    STATS = (
        ('СИЛ', 'strength'),
        ('ЛОВ', 'dexterity'),
        ('ТЕЛ', 'constitution'),
        ('ИНТ', 'intellegence'),
        ('МДР', 'wisdom'),
        ('ХАР', 'chrarisma'),
    )

    for param in params:
        stats = param.findAll('div', class_='stat')
        for stat in stats:
            two_divs = stat.findAll('div')

            for stat_element in STATS:
                if stat_element[0] == two_divs[0].text:
                    key = stat_element[1]
                    print('Key: '+key)

                    val = re.findall(r'(\d{1,2})\s\(([+-]?\d)\)', two_divs[1].text)
                    print('Value: ', val)
                    break

            print(two_divs[1].text+'\r\n')


def parse_mob(link):
    html = get_html(dnd_source + link)
    soup = BeautifulSoup(html, 'html.parser')

    size_type_aligment = soup.find('ul', class_='params').find('li', class_='size-type-alignment', recursive=False)
    if size_type_aligment:
        sta = size_type_aligment.text.split(', ')
        print('Size: {}, Type: {}, Alignment: {}'.format(sta[0],sta[1],sta[2]))
    else:
        input('Size_Type_Alignment NOT FOUND')

    all_parms = soup.find('ul', class_='params').findAll('li', class_='', recursive=False)
    print_lis(all_parms, 'main')
    all_parms = soup.find('ul', class_='params').findAll('li', class_='stats', recursive=False)
    parse_stats(all_parms)
    all_parms = soup.find('ul', class_='params').findAll('li', class_='subsection', recursive=False)
    print_lis(all_parms, 'subsection')


def save_db(key, val, modifier=0):
    pass

def main():
    get_mobs()


if __name__ == '__main__':
    main()
