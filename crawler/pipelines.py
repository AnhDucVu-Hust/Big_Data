# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import dataclasses
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

class CrawlerPipeline:
    def process_item(self, item, spider):
        #print(os.getcwd())
        name = item.url.split("/")[4]
        path_now = os.path.dirname(__file__)
        x = "/".join(item.infor)
        #if os.path.exists(os.path.join(os.getcwd(),x)) != True:
        #        os.makedirs(os.path.join(os.getcwd(),x))
        #with open(os.path.join(os.getcwd(),x)+"/"+name+".txt","w",encoding="UTF-8") as f:
        #    f.write(item.climate_day)
        def call_back(err,msg):
            if err is not None:
                print(f"Failed:{err}")
            else:
                print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
        spider.producer.poll(0)
        print(json.dumps(dataclasses.asdict(item)).encode('utf-8'))
        spider.producer.produce(spider.name,json.dumps(dataclasses.asdict(item)).encode('utf-8'),callback=call_back)

        spider.producer.flush()
if __name__=="__main__":
    with open(f"./data_climate/test.txt", "w", encoding="UTF-8") as f:
        f.write('test')