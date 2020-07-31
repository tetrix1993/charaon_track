import sqlite3
import queries
import os
from constants import *

conn = sqlite3.connect(DB_LOCATION)
c = conn.cursor()


def run():
    item_ids = get_item_ids()
    print_intro_message()
    choice = input('Enter choice: ')
    while True:
        if choice == '0':
            print('Exiting...')
            return
        elif choice == '1':
            list_items(True)
        elif choice == '2':
            list_items(False)
        elif choice == '3':
            query_by_item_id()
        elif choice == '4':
            query_by_series_id(item_ids)
        else:
            print('Invalid choice. Exiting...')
            return
        print_intro_message()
        choice = input('Enter choice: ')


def print_intro_message():
    print('Make your choice:\n' +
          '1 - List all items by Release Date\n' +
          '2 - List all items by Item ID\n' +
          '3 - Query by Item ID\n' +
          '4 - Query by Series ID\n' +
          '0 - Exit')


def query_by_item_id():
    query = input('Enter Item ID: ').strip().replace(' ', '')
    if len(query) > 0:
        c.execute(queries.SELECT_RELEASE_DATE_BY_ITEM_ID, (query.upper(), ))
        item = c.fetchone()
        if item is not None:
            print(item)
        else:
            print('Item ID %s not found' % query.upper())
    else:
        print('Invalid input')


def query_by_series_id(item_ids):
    query = input('Enter Series ID: ').strip().replace(' ', '')
    if len(query) >= 5:
        c.execute(queries.SELECT_RELEASE_DATE_BY_SERIES, (query.upper() + '%', ))
        item_list = c.fetchall()
        if len(item_list) > 0:
            has_print_item = False
            for item in item_list:
                if item[0] in item_ids:
                    has_print_item = True
                    print(item)
            if not has_print_item:
                print('Items with Series ID %s matched but not found in ' % query.upper() + INPUT_FILE_PATH)
        else:
            print('Items with Series ID %s not matched' % query.upper())
    else:
        print('Invalid input')


def list_items(by_release_dt=True):
    if by_release_dt:
        c.execute(queries.SELECT_ALL_ITEMS_ORDER_BY_RELEASE_DATE)
    else:
        c.execute(queries.SELECT_ALL_ITEMS_ORDER_BY_ITEM_ID)
    item_list = c.fetchall()
    for item in item_list:
        print(item)


def get_item_ids():
    item_ids = []
    if not os.path.exists(INPUT_FILE_PATH):
        pass
    else:
        with open(INPUT_FILE_PATH, 'r') as f:
            line = f.readline()
            while line:
                if len(line.strip()) > 0:
                    item_ids.append(line.strip())
                line = f.readline()
    return item_ids


if __name__ == '__main__':
    run()
    conn.close()
