#!/usr/bin/env python
from django.conf import settings
from path import Path as path

import logging
import bz2
import MySQLdb
import os


DUMP_FILE_PATH = "/openedx/empty_dump.sql.bz2"
FIXTURES_DIR = path("/openedx/fixtures/")


def get_dump_file_contents():
    print('Reading dump file "{}"'.format(DUMP_FILE_PATH))
    return bz2.BZ2File(DUMP_FILE_PATH).read()


def get_connection(include_db=True):
    kwargs = dict(
        host=settings.DATABASES["default"]["HOST"],
        port=int(settings.DATABASES["default"].get("PORT", 3306)),
        user=settings.DATABASES["default"]["USER"],
        passwd=settings.DATABASES["default"]["PASSWORD"],
    )
    if include_db:
        kwargs["db"] = settings.DATABASES["default"]["NAME"]
    return MySQLdb.connect(**kwargs)


def restore_dump():
    admin_cursor = get_connection(include_db=False).cursor()
    database_name = settings.DATABASES["default"]["NAME"]
    print('Resetting mysql database "{}"'.format(database_name))
    admin_cursor.execute(
        "DROP DATABASE IF EXISTS {}".format(database_name)
    )
    admin_cursor.execute(
        "CREATE DATABASE {} CHARACTER SET utf8".format(database_name)
    )
    sql = get_dump_file_contents()
    cursor = get_connection().cursor()
    cursor.execute(sql)


def run_fixtures():
    if FIXTURES_DIR.isdir():
        # We sort lexicographically by file name
        # to make predictable ordering possible
        for file in sorted(FIXTURES_DIR.listdir()):
            print('Loading fixture "{}"'.format(file))
            path("/openedx/ecommerce").chdir()
            os.system("./manage.py loaddata {}".format(file))


def main():
    restore_dump()
    run_fixtures()


if __name__ == "__main__":
    main()
