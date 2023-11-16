import json
from io import BytesIO
from os.path import join
from time import sleep
from typing import Optional, Union

import pandas as pd
import requests
from requests import Response

from src.settings import HEADERS, REPORT_CONFIG, Report, YANDEX_API_URL


def handle_http_response(response: Response) -> Union[bool, None]:
    request_id = response.headers.get('RequestId', None)
    status_code = response.status_code

    if status_code in [201, 202]:
        retry_in = int(response.headers.get('retryIn', 60))
        print(f'Retrying in {retry_in} seconds. RequestId: {request_id}')
        sleep(retry_in)
        return True
    elif status_code == 200:
        process_report(response, request_id)
    else:
        print(f'Error {status_code}: {response.json()}. RequestId: {request_id}')
        return False


def process_report(response: Response, request_id: Optional[str], report: Report = REPORT_CONFIG) -> None:
    df = pd.read_csv(BytesIO(response.content), delimiter='\t')
    df.to_csv(join(report.folder, report.name), encoding='utf-16')
    print(f'Report {report.name} created successfully. RequestId: {request_id}. Rows: {len(df)}')


def download_report(report: Report = REPORT_CONFIG, date_from: str = None, date_to: str = None):
    body = {
        'params': {
            'SelectionCriteria': {},
            'FieldNames': report.fields,
            'ReportName': report.name,
            'ReportType': report.type,
            'DateRangeType': report.date_range,
            'Format': 'TSV',
            'IncludeVAT': 'NO',
            'IncludeDiscount': 'NO'
        }
    }

    if report.date_range == 'CUSTOM_DATE' and isinstance(date_from, str) and isinstance(date_to, str):
        body['params']['SelectionCriteria']['DateFrom'] = date_from
        body['params']['SelectionCriteria']['DateTo'] = date_to

    body_json = json.dumps(body, indent=4)

    while True:
        response = requests.post(YANDEX_API_URL, body_json, headers=HEADERS, timeout=60)
        response.encoding = 'utf-8'

        if not handle_http_response(response):
            break
