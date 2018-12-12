import requests
import json
from bs4 import BeautifulSoup

with open('source.html') as file:
    source = file.read()

soup = BeautifulSoup(source, 'html.parser')

datas = []
counter = 0
for child in soup.find_all("tbody")[0].children:
    counter += 1
    if counter % 2 == 0:
        data = {}
        td = child.find_all('td')
        data['kode_saham'] = td[1].find('a').contents[0].strip()
        if td[2].contents[0] != ' ':
            data['nama_perusahaan'] = td[2].contents[0].strip()
        else:
            data['nama_perusahaan'] = td[2].contents[1].contents[0].strip()
        
        data['sektoral'] = []
        for sektoral in td[3].find_all('a'):
            data['sektoral'].append(sektoral.contents[0].strip())
        datas.append(data)
        print(data['nama_perusahaan'])        

with open('data.json', 'w') as file:
    file.write(json.dumps(datas))