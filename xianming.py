import requests
from bs4 import BeautifulSoup
def text_save(content, filename, mode='a'):
    file = open(filename, mode)
    file.write(str(content))
    file.close()

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'}
all_url = 'https://beijing.8684.cn/'
start_html = requests.get(all_url,headers=headers)

Soup = BeautifulSoup(start_html.text,'html.parser')
all_a = Soup.find('div', class_="bus-layer depth w120").find_all('a')

for a in all_a:
    Network_list = []
    href = a['href']
    html = all_url + href
    second_html = requests.get(html,headers=headers)
    Soup2 = BeautifulSoup(second_html.text,'html.parser')
    try:
        all_a2 = Soup2.find('div',class_='list clearfix').find_all('a')
    except:
        continue
    for a2 in all_a2:
        title1 = a2.get_text()
        Network_list.append(title1)
    text_save(Network_list,'Network_bus.txt');
print("爬取完成")