# import logging
# import sqlite3
# import re
#
# global DB
# DB = dict()
#
#
# def connect():
#     global DB
#     c = sqlite3.connect('DB/billionaires', check_same_thread=False)
#     c.row_factory = sqlite3.Row
#     DB['conn'] = c
#     DB['cursor'] = c.cursor()
#     # logging.info('Connected to DB')
#
#
# def execute(sql, args=None):
#     global DB
#     c = sqlite3.connect('DB/billionaires', check_same_thread=False)
#     c.row_factory = sqlite3.Row
#     DB['conn'] = c
#     DB['cursor'] = c.cursor()
#     sql = re.sub('\s+', ' ', sql)
#     logging.info('SQL: {} Args: {}'.format(sql, args))
#     return c.cursor().execute(sql, args) \
#         if args is not None else c.cursor().execute(sql)
#
#
# def close():
#     global DB
#     DB['conn'].close()
