import os
import sqlite3
import datetime as dt


DEFAULT_LOG_LOC = '../../reddit-engagement-files/log.txt'


def update_database(generator, mode, db_path):
    # connect to DB, table creation may be needed
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    table_args = 'id TEXT PRIMARY KEY, title TEXT, subreddit TEXT, access_time TIMESTAMP, action TEXT'
    create_table = '''CREATE TABLE IF NOT EXISTS activity (%s);''' % table_args
    cursor.execute(create_table)

    # for every submission, create sql entry
    for item in generator:
        current_time = dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        values = (item.id, item.title, item.subreddit.display_name, current_time, mode)
        insert_into = '''INSERT OR IGNORE INTO activity VALUES (?,?,?,?,?);'''
        cursor.execute(insert_into, values)
        connection.commit()

    # log and finish
    logger('Inserted into DB for %s mode' % mode)
    cursor.close()
    connection.close()


def logger(info, log_path=DEFAULT_LOG_LOC):
    # create current log entry
    timestamp = dt.datetime.now()
    entry = '%s | %s' % (timestamp, info)

    # log to end of file if exists, else make
    write_mode = 'a' if os.path.exists(log_path) else 'w'
    log_file = open(log_path, write_mode)
    log_file.write(entry)
    log_file.close()