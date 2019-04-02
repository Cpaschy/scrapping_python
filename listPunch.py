import requests
from bs4 import BeautifulSoup
import json
import os

class RapPunchLine (object) :

        def __init__(self,page):
                self.url = 'https://www.punchLine.fr/page/' + str(page) 
                 

        def getData(self):
                html = requests.get(self.url).text
                self.soup = BeautifulSoup(html, 'lxml')

        def parseList(self):

                punch = self.soup.find_all('div',{'class': 'post'})
                
                punchList = []
                for punchLineEl in punch:        
                        punchLine = punchLineEl.find('h2', {'class': 'post-title entry-title'}) 
                        descPunch = punchLineEl.find('div',{'class': 'post-meta'})  
                        votePunch = punchLineEl.find('div',{'class':'gdt-size-32 gdthumbtext'})
                        detail = {
                                'punchLine': punchLine.text,
                                'description':descPunch.text,
                                'vote':votePunch.text
                        } 
                        meta = descPunch.find_all("a")
                        try:
                                detail['artist'] = meta[0].text
                        except Exception as e:
                                pass
                        try:
                                detail['album'] = meta[1].text
                        except Exception as e:
                                pass
                        try:
                                detail['titre'] = meta[2].text
                        except Exception as e:
                                pass
                        try:
                                detail['vote'] = votePunch.text
                        except Exception as e:
                                pass
                        punchList.append(detail)  

                return punchList

if __name__ == '__main__':
        punchLine = [] 
        for page in xrange(1, 10):
                ln = RapPunchLine(page)

                ln.getData()
                punchLine.append(ln.parseList())
               

        f = open("monJson.json", "w")
        f.write(json.dumps(sum(punchLine, [])))
        f.close()

