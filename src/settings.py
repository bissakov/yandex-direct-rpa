import os
from os.path import abspath, dirname, join
from datetime import date
from dataclasses import dataclass

import dotenv

# Load environment variables
dotenv.load_dotenv()

# Time Configurations
TODAY = date.today().strftime('%d.%m.%Y')

# Folder paths
PROJECT_ROOT = dirname(dirname(abspath(__file__)))


# Report Configurations
@dataclass
class Report:
    folder: str
    name: str
    date_range: str
    type: str
    fields: list[str]


REPORT_CONFIG = Report(folder=join(PROJECT_ROOT, 'reports'),
                       name=f'Report_{TODAY}.csv',
                       date_range='TODAY',
                       type='REACH_AND_FREQUENCY_PERFORMANCE_REPORT',
                       fields=['Date', 'CampaignType', 'CampaignName',
                               'CampaignId', 'AdGroupName', 'AdGroupId',
                               'AdId', 'Impressions', 'Clicks', 'Ctr',
                               'Cost', 'AvgCpc', 'AvgCpm', 'ImpressionReach',
                               'AvgImpressionFrequency'])

# API Configurations
YANDEX_API_URL = 'https://api.direct.yandex.com/json/v5/reports'
YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')
CLIENT_LOGIN = 'brands-rg'

# API Headers
HEADERS = {
    'Authorization': f'Bearer {YANDEX_TOKEN}',
    'Client-Login': CLIENT_LOGIN,
    'Accept-Language': 'ru',
    'processingMode': 'auto',
    'returnMoneyInMicros': 'false',
    'skipReportHeader': 'true',
    'skipColumnHeader': 'false',
    'skipReportSummary': 'true'
}

# Database Configurations
CONNECTION_URL = (
    'mssql+pyodbc://{user}:{password}@{host}:{port}/{database}?driver={driver}'
    .format(
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        database=os.getenv('DATABASE'),
        driver=os.getenv('DRIVER')
    )
)
