from typing import Any
import re
import requests
from bs4 import BeautifulSoup
import scrapy
from confluent_kafka import Producer
import json
from crawler import settings as my_settings
from scrapy.settings import Settings
from requests import Response
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from confluent_kafka import Producer
from crawler.items import ClimateItem
from confluent_kafka.admin import AdminClient, NewTopic
class Climate_Data(scrapy.Spider):

    start_urls= ['https://en.tutiempo.net/climate/asia.html']
    def __init__(self):
        self.kafka={'bootstrap.servers':'localhost:9092'}
        self.name = 'climate_data_expand'
        self.producer=Producer(**self.kafka)


    def parse(self, response: Response,month=None,year=None, **kwargs: Any) -> Any:
        new_urls=response.css('.mlistados li a')
        for new_url in new_urls:
            new_url_link = new_url.css('::attr(href)').get()
            pattern = r'\b\d{1,2}-\d{4}\b'
            match = re.search(pattern, new_url_link)
            if bool(match):
                yield response.follow(response.urljoin(new_url_link), callback=self.parse_climate)
            else:
                yield response.follow(response.urljoin(new_url_link), callback=self.parse)

    def parse_climate(self,response,month=None,year=None):
        #print("Crawl climate")
        html_content = response.text
        soup= BeautifulSoup(html_content,'html.parser')
        name= soup.find('div',class_="titulo").find('h2').get_text()
        name = name.replace("Climate","")
        year = name.split('-')[-1].strip()
        month = name.split('-')[-2]
        country, month = ' '.join(month.split()[:-1]),month.split()[-1]
        table = soup.find('table',class_="medias mensuales numspan")
        infor = soup.find(attrs={'id':'UrlTopScroll'}).find_all('td')[2:]
        infor = [x.get_text() for x in infor]
        #print("Path:",infor)
        #print(table)

        rows = table.find_all('tr')
        cell_out=''

        for row in rows:
            # Lấy ra tất cả các ô (cells) trong dòng
            cells = row.find_all(['th', 'td'])
            # Xử lý nội dung của từng ô
            cell_data = [cell.text.strip() for cell in cells]
            cell_out += ','.join(cell_data)+","
            cell_out += country +","+month +","+year+"\n"
        cell_out = cell_out.strip("\n")
        item = ClimateItem(url=response.request.url,climate_day=cell_out,infor=infor,name=name)
        yield item

    def send_to_kafka(self, data):
        # Thay đổi các thông số Kafka theo cấu hình của bạn
        kafka_bootstrap_servers = 'localhost:9092'
        #kafka_topic = 'crawled'
        #try:st
        #    producer = KafkaProducer(
        #    bootstrap_servers=kafka_bootstrap_servers,
        #    value_serializer=lambda v: json.dumps(v).encode('utf-8')
        #)
        #except:
        #    print("Wrong")

        #producer.send(kafka_topic, value=data)
        #producer.flush()

        #self.log(f"Sent to Kafka: {data}")
if __name__ == '__main__':
    pattern = r'\b\d{1,2}-\d{4}\b'
    match = re.search(pattern, "https://en.tutiempo.net/climate/06-1970/ws-488675.html")
    #print(bool(match))
    setting = Settings()
    setting.setmodule(my_settings)
    process = CrawlerProcess(setting)
    process.crawl(Climate_Data)
    process.start()