import requests
from bs4 import BeautifulSoup
import pandas as pd

articleList = []
articleCount=1

for x in range(1,201):
    if x == 1:
        url = 'https://seths.blog'
    else:
        url = 'https://seths.blog/page/'+str(x)+'/'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, features='lxml')
    articles = soup.find_all('div',class_='post')

    for item in articles:
        error=''
        try:
            #Getting the url link of the article from the home page. Then, we get the link each article to be able to access it.
            link = item.find({'h2'}).a['href']
            # print(link)

            error="title"
            title = item.find('h2').text
            # print(title)

            error="date"
            date = item.find('span', class_ = 'date').text
            # print(date)

            error="text"
            texts = item.find_all('p')
            # print(texts)

            length=len(texts)-1
            text=""

            for p in range(0,length):
                # print(length)
                text = text + texts[p].text + " "

            # print(text)

            article = {
                'title': title,
                'date': date,
                'author': "Seth Godin",
                'link': link,
                'text': text
            }

            articleList.append(article)

            print(articleCount,'added post')
            articleCount=articleCount+1
        except Exception as e:
            # By this way we can know about the type of error occurring
            print("The error is: ",e,error,articleCount) 

df = pd.DataFrame(articleList)
df.to_csv('SethBlog.csv')
print('saved to csv')