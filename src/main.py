import sys
from os.path import abspath, dirname

if sys.version_info < (3,):
    raise Exception('Python 2 is not supported')

sys.path.append(dirname(dirname(abspath(__file__))))


if __name__ == '__main__':
    from src.report import download_report
    from src.db import populate_db

    download_report()
    populate_db()
