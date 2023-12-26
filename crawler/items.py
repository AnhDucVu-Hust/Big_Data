# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dataclasses import dataclass
import scrapy
from typing import Optional, List
@dataclass
class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
@dataclass
class ClimateItem():
    url: Optional[str]
    name: Optional[str]
    climate_day: List[Optional[str]]
    infor : List[Optional[str]]

