import sqlite3
import os
import requests
from bs4 import BeautifulSoup as bs

import queries
from constants import *

conn = sqlite3.connect(DB_LOCATION)
c = conn.cursor()


def run():
    create_schema()
    item_ids = get_item_ids()
    for item_id in item_ids:
        release_dt = get_release_date_from_webpage(item_id)
        if release_dt is not None:
            update_item(item_id, release_dt)


def create_schema():
    c.execute(queries.CREATE_TABLE_ITEMS)


def get_item_ids():
    item_ids = []
    if not os.path.exists(INPUT_FILE_PATH):
        print(INPUT_FILE_PATH + ' not found')
    else:
        with open(INPUT_FILE_PATH, 'r') as f:
            line = f.readline()
            while line:
                if len(line.strip()) > 0:
                    item_ids.append(line.strip())
                line = f.readline()
    return item_ids


def get_release_date_from_webpage(item_id):
    item_url = ITEM_URL_TEMPLATE % item_id
    release_dt = None
    try:
        r = requests.get(item_url)
        soup = bs(r.content.decode(), 'html.parser')
        sections = soup.find_all('section', id='itemDetail-wrap')
        if len(sections) > 1:
            text = sections[1].find('b').text
            year = '0000'
            month = '00'
            day = '00'
            if '年' in text:
                split1 = text.split('年')
                year = split1[0][-4:]
                if len(split1) > 1 and '月' in split1[1]:
                    split2 = split1[1].split('月')
                    month = split2[0].zfill(2)
                    if len(split2) > 1 and '日' in split2[1]:
                        day = split2[1].split('日')[0].zfill(2)
            release_dt = year + month + day
    except:
        release_dt = None
    return release_dt


def update_item(id, release_dt):
    c.execute(queries.SELECT_RELEASE_DATE_BY_ITEM_ID, (id,))
    item = c.fetchone()
    if item is None:
        c.execute(queries.INSERT_INTO_TABLE_ITEMS, (id, release_dt))
        conn.commit()
        print('Inserted %s with date %s' % (id, release_dt))
    elif item[0] != release_dt:
        c.execute(queries.UPDATE_RELEASE_DATE_BY_ITEM_ID, (release_dt, id))
        conn.commit()
        print('Updated %s: %s -> %s' % (id, item[0], release_dt))


if __name__ == '__main__':
    run()
    conn.close()
