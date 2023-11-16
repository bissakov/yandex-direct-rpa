from sqlalchemy import Column, NVARCHAR, Integer, ForeignKey, Date, BigInteger, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Campaigns(Base):
    __tablename__ = 'campaigns'
    __table_args__ = {'schema': 'dbo'}

    CampaignID = Column(Integer, primary_key=True)
    CampaignName = Column(NVARCHAR(255))


class CampaignData(Base):
    __tablename__ = 'campaign_data'
    __table_args__ = {'schema': 'dbo'}

    Campaign_data_ID = Column(Integer, autoincrement=True, primary_key=True)
    CampaignID = Column(Integer, ForeignKey('dbo.campaigns.CampaignID'), unique=True)
    CampaignType = Column(NVARCHAR(255))

    campaigns = relationship('Campaigns')


class AdGroups(Base):
    __tablename__ = 'ad_groups'
    __table_args__ = {'schema': 'dbo'}

    AdGroupID = Column(BigInteger, primary_key=True)
    CampaignID = Column(Integer, ForeignKey('dbo.campaigns.CampaignID'))
    AdGroupName = Column(NVARCHAR(255))

    campaigns = relationship('Campaigns')


class Ads(Base):
    __tablename__ = 'ads'
    __table_args__ = {'schema': 'dbo'}

    AdID = Column(BigInteger, primary_key=True)
    AdGroupID = Column(BigInteger, ForeignKey('dbo.ad_groups.AdGroupID'))

    adgroups = relationship('AdGroups')


class AdData(Base):
    __tablename__ = 'ad_data'
    __table_args__ = {'schema': 'dbo'}

    AdDataID = Column(Integer, primary_key=True, autoincrement=True)
    AdID = Column(BigInteger, ForeignKey('dbo.ads.AdID'))
    Impressions = Column(Integer)
    Clicks = Column(Integer)
    CTR = Column(Float)
    Cost = Column(Float)
    AvgCPC = Column(Float)
    AvgCPM = Column(Float)
    ImpressionReach = Column(Integer)
    AvgImpressionFrequency = Column(Float)
    ReportDate = Column(Date)

    ad = relationship('Ads')
