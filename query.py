import sqlite3
import queries
from constants import *

conn = sqlite3.connect(DB_LOCATION)
c = conn.cursor()


def run():
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
            query_by_series_id()
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
        c.execute(queries.SELECT_RELEASE_DATE_BY_ITEM_ID, (query, ))
        item = c.fetchone()
        if item is not None:
            print(item)
        else:
            print('Item ID %s not found' % query)
    else:
        print('Invalid input')


def query_by_series_id():
    query = input('Enter Series ID: ').strip().replace(' ', '')
    if len(query) >= 5:
        c.execute(queries.SELECT_RELEASE_DATE_BY_SERIES, (query + '%', ))
        item_list = c.fetchall()
        if len(item_list) > 0:
            for item in item_list:
                print(item)
        else:
            print('Items with Series ID %s not matched' % query)
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


if __name__ == '__main__':
    run()
    conn.close()
