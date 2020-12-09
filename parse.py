#!/usr/bin/env python3
import requests
import locale
import platform
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

dnd_source = 'https://dungeon.su'
mob_html_group = dnd_source + '/bestiary/'

parse_mob1 = '/bestiary/305-umber_hulk/'
parse_mob2 = '/bestiary/84-imp/'

class Mob():
    def __init__(self,
            name,
            size,
            type_,
            alignment,
            strength,
            dexterity,
            constitution,
            intellegence,
            wisdom,
            chrarisma,
            ac,
            ):
        pass

    pass

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'}
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException,ValueError):
        print("Network err...")
        return False


def get_mobs():
    html = get_html(mob_html_group)
    soup = BeautifulSoup(html,'html.parser')
    if html:
        all_mobs = soup.find('ul', class_='list-of-items').findAll('li', class_='')
        print('List counts: {}'.format(len(all_mobs)))
        input('__________')
        for mob in all_mobs:
            title = mob.find('a').text
            mob_href = mob.find('a')['href']
            print('------'*30)
            print('Name: {}, Href: {}'.format(title, mob_href))
            parse_mob(mob_href)
            input()

def print_lis(params, block_descr):
    for param in params:
        li = param.findAll('li', recursive=False)
        if li:
            print_lis(li,'{}_sub'.format(block_descr))
        else:
            print('<<<<< :Parm: ({descr}) >>>>>\r\n{parm}\r\n<<<<< EndParm ({descr}) >>>>>\r\n'.format(parm=param.text, descr=block_descr))


def parse_mob(link):
    html = get_html(dnd_source+link)
    soup = BeautifulSoup(html,'html.parser')
    all_parms = soup.find('ul', class_='params').findAll('li', class_='', recursive=False)
    print_lis(all_parms,'main')
    all_parms = soup.find('ul', class_='params').findAll('li', class_='stats', recursive=False)
    print_lis(all_parms,'stats')
    all_parms = soup.find('ul', class_='params').findAll('li', class_='subsection', recursive=False)
    print_lis(all_parms,'subsection')


def main():
   get_mobs()

if __name__ == '__main__':
    main()
