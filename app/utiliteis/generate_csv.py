import re
import requests
from bs4 import BeautifulSoup
import csv
import time



class GenerateCsv :

        def __init__(self, genre_id, search_name, file_name): # コンストラクタ
                self.genre_id = genre_id,
                self.search_name = search_name
                self.file_name = file_name


        def Execute(self):

                headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
                csvlist = [['落札年月','月内平均落札価格','落札価格','商品名']]
                genre_id = re.sub(r"['(,) ]", "", str(self.genre_id))

         
                def FetchMeanPrice(url):
                        r = requests.get(url,headers=headers)
                        r.encoding = r.apparent_encoding
                        soup = BeautifulSoup(r.text,'lxml')
                        return soup
                        

                for year in range(2015,2016):
                        for month in range(1,13):
                                if month <= 9:
                                        month = str(0) + str(month)
                                        url = f"https://aucfree.com/search?c={genre_id}&from={year}-{month}&o=t2&q={self.search_name}&to={year}-{month}"
                                        soup = FetchMeanPrice(url)
                                        time.sleep(3)
                                        mean_price = soup.findAll('strong',id='mean_price')
                                        item_title = soup.findAll('a',class_='item_title')
                                        item_price = soup.findAll('a',class_='item_price')
                                else:
                                        url = f"https://aucfree.com/search?c={genre_id}&from={year}-{month}&o=t2&q={self.search_name}&to={year}-{month}"
                                        soup = FetchMeanPrice(url)
                                        time.sleep(3)
                                        mean_price = soup.findAll('strong',id='mean_price')
                                        item_title = soup.findAll('a',class_='item_title')
                                        item_price = soup.findAll('a',class_='item_price')
                                for i in mean_price:
                                        i = i.text.replace(',','')
                                        #    .textでタグ型オブジェクトからテキストを取り出す
                                        if int(i) == 0:
                                                continue
                                        else:
                                                for k,l in zip(item_title,item_price):
                                                        k = k.text.replace(',','')
                                                        l = l.get_text().replace(',', '').replace('円', '')

                                                        csvlist.append([int(str(year)+str(month)),int(i),int(l),k]) 



                with open("./app/csv_files/%s.csv" % self.file_name, 'w' ) as f:
                        writecsv = csv.writer(f)
                        writecsv.writerows(csvlist)
                # with open('./csv_files/yotsuboshihinakabuto.csv', 'w') as f:
                # writecsv = csv.writer(f)
                # writecsv.writerows(csvlist)
