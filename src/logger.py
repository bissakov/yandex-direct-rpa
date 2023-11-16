import datetime
import logging
import os
from os.path import join
from src.settings import PROJECT_ROOT


def setup_logger() -> None:
    log_folder = join(PROJECT_ROOT, 'logs')
    os.makedirs(log_folder, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_format = '%(asctime).19s %(levelname)s %(name)s %(filename)s %(funcName)s : %(message)s'
    formatter = logging.Formatter(log_format)

    today = datetime.date.today()
    year_month_folder = join(log_folder, today.strftime('%Y/%B'))
    os.makedirs(year_month_folder, exist_ok=True)

    file_handler = logging.FileHandler(
        join(year_month_folder, f'{today.strftime("%d.%m.%y")}.log'),
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    httpcore_logger = logging.getLogger('httpcore')
    httpcore_logger.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
