import os

from path import Path as path

FIXTURES_DIR = path("/openedx/fixtures/")


def main():
    if FIXTURES_DIR.isdir():
        # We sort lexicographically by file name
        # to make predictable ordering possible
        for file in sorted(FIXTURES_DIR.listdir()):
            print('Loading fixture "{}"'.format(file))
            path("/openedx/ecommerce").chdir()
            os.system("./manage.py loaddata {}".format(file))


if __name__ == "__main__":
    main()
