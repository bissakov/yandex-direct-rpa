import os
from datetime import datetime

import dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from models import Campaigns, CampaignData, AdGroups, Ads, AdData, Base
from src.settings import CONNECTION_URL


def df_to_dict(df: pd.DataFrame) -> list[dict[str, any]]:
    data_types = {
        'Date': lambda x: datetime.strptime(x, '%Y-%m-%d').date() if x != '--' else None,
        'CampaignType': lambda x: str(x) if x != '--' else None,
        'CampaignName': lambda x: str(x) if x != '--' else None,
        'CampaignId': lambda x: int(x) if x != '--' else None,
        'AdGroupName': lambda x: str(x) if x != '--' else None,
        'AdGroupId': lambda x: int(x) if x != '--' else None,
        'AdId': lambda x: int(x) if x != '--' else None,
        'Impressions': lambda x: int(x) if x != '--' else None,
        'Clicks': lambda x: int(x) if x != '--' else None,
        'Ctr': lambda x: float(x) if x != '--' else None,
        'Cost': lambda x: float(x) if x != '--' else None,
        'AvgCpc': lambda x: float(x) if x != '--' else None,
        'AvgCpm': lambda x: float(x) if x != '--' else None,
        'ImpressionReach': lambda x: int(x) if x != '--' else None,
        'AvgImpressionFrequency': lambda x: float(x) if x != '--' else None,
    }

    rows = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc='Converting data types'):
        new_row = {}
        for col, dtype_fn in data_types.items():
            new_row[col] = dtype_fn(row[col])
        rows.append(new_row)
    return rows


def populate_db():
    # Set echo to True if you want logs
    engine = create_engine(CONNECTION_URL, use_setinputsizes=False, echo=False)
    Base.metadata.create_all(engine)

    data = pd.read_csv('Report.csv', encoding='utf-16')
    df = pd.DataFrame(data)

    if len(df) == 0:
        print('CSV is empty. Finishing process.')
        return

    rows = df_to_dict(df)

    with sessionmaker(bind=engine)() as session:
        for index, row in tqdm(enumerate(rows), total=len(rows), desc='Populating database'):
            try:
                campaign = Campaigns(CampaignID=row['CampaignId'], CampaignName=row['CampaignName'])
                if not session.query(Campaigns).filter_by(CampaignID=campaign.CampaignID,
                                                          CampaignName=campaign.CampaignName).first():
                    session.add(campaign)

                campaign_data = CampaignData(CampaignID=campaign.CampaignID, CampaignType=row['CampaignType'])
                if not session.query(CampaignData).filter_by(CampaignID=campaign.CampaignID,
                                                             CampaignType=campaign_data.CampaignType).first():
                    session.add(campaign_data)

                ad_group = AdGroups(AdGroupID=row['AdGroupId'], CampaignID=campaign.CampaignID,
                                    AdGroupName=row['AdGroupName'])
                if not session.query(AdGroups).filter_by(AdGroupID=ad_group.AdGroupID, CampaignID=ad_group.CampaignID,
                                                         AdGroupName=ad_group.AdGroupName).first():
                    session.add(ad_group)

                ad = Ads(AdID=row['AdId'], AdGroupID=ad_group.AdGroupID)
                if not session.query(Ads).filter_by(AdID=ad.AdID, AdGroupID=ad.AdGroupID).first():
                    session.add(ad)

                ad_data = AdData(AdID=ad.AdID, Impressions=row['Impressions'], Clicks=row['Clicks'], CTR=row['Ctr'],
                                 Cost=row['Cost'], ImpressionReach=row['ImpressionReach'], AvgCPC=row['AvgCpc'],
                                 AvgCPM=row['AvgCpm'], AvgImpressionFrequency=row['AvgImpressionFrequency'],
                                 ReportDate=row['Date'])
                if not session.query(AdData).filter_by(AdID=ad_data.AdID, Impressions=ad_data.Impressions,
                                                       Clicks=ad_data.Clicks, CTR=ad_data.CTR,
                                                       Cost=ad_data.Cost, ImpressionReach=ad_data.ImpressionReach,
                                                       AvgCPC=ad_data.AvgCPC, AvgCPM=ad_data.AvgCPM,
                                                       AvgImpressionFrequency=ad_data.AvgImpressionFrequency,
                                                       ReportDate=ad_data.ReportDate).first():
                    session.add(ad_data)

                session.commit()
            except (IntegrityError, DataError) as error:
                print(f'Error inserting row {index}: {str(error)}')
                session.rollback()
                raise error


if __name__ == '__main__':
    populate_db()
