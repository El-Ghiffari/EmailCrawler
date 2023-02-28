import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd

def cariEmail(alamat):
    original_url = alamat 
    unscraped = deque([original_url])  
    scraped = set()  
    emails = set() 

    while len(unscraped) :
        url = unscraped.popleft()
        scraped.add(url)

        parts = urlsplit(url)

        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path :
            path = url[:url.rfind('/')+1]
        else :
            path = url

        print("Crawling URL %s" % url)
        try :
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) :
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, 'lxml')

        for anchor in soup.find_all('a') :
            if "href" in anchor.attrs :
                link = anchor.attrs['href']
            else :
                link = ''

                if link.startswith('/'):
                    link = base_url + link
            
                elif not link.startswith('http'):
                    link = path + link

                if not link.endswith(".gz"):
                    if not link in unscraped and not link in scraped:
                        unscraped.append(link)  

    df = pd.DataFrame(emails, columns=['Email'])
    #berkas=str(path)+"emails.csv"
    return df
    #df.to_csv(str(berkas), index=False)
    
if __name__ == "__main__":
    urls = ['https://www.signalhire.com/companies/telkomsel/employees']
    i=0
    for url in urls:
        #cariEmail(url)
        berkas = cariEmail(url)
        #nama=str(url)+"emails.txt"
        #with open(str(i), 'a') as file :
        #    file.write(berkas[i])
        #i=i+1
        berkas.to_csv("emails.csv", index=False)







#ref : https://medium.com/swlh/how-to-scrape-email-addresses-from-a-website-and-export-to-a-csv-file-c5d1becbd1a0