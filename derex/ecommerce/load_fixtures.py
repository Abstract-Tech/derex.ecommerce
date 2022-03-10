from path import Path as path

import os


FIXTURES_DIR = path("/openedx/fixtures/")


def main():
    if FIXTURES_DIR.isdir():
        # We sort lexicographically by file name
        # to make predictable ordering possible
        files = " ".join(map(str, sorted(FIXTURES_DIR.listdir())))
        print('Loading fixtures "{}"'.format(files))
        path("/openedx/ecommerce").chdir()
        res = os.system("./manage.py loaddata {}".format(files))
        if res != 0:
            raise RuntimeError


if __name__ == "__main__":
    main()
