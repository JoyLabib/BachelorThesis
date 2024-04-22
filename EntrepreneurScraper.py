import requests
from bs4 import BeautifulSoup
import pandas as pd

articleList = []

for x in range(1,11):
    if x == 1:
        url = 'https://www.entrepreneur.com/starting-a-business/fundraising'
    else:
        url = 'https://www.entrepreneur.com/starting-a-business/fundraising/page-'+str(x)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, features='lxml')

    articles = soup.find_all('div', class_= 'flex flex-row-reverse mb-12')

    for item in articles:
        #Getting the url link of the article from the home page. Then, we get the link each article to be able to access it.
        link = item.find({'a':'block hover:underline'})['href']
        link = 'https://www.entrepreneur.com'+link

        url1 = link
        headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

        r1 = requests.get(url1, headers=headers1)
        singleArticle = BeautifulSoup(r1.content, features='lxml')
        
        title = singleArticle.find({'h1':'tracking-tight'}).text
        title = title.split('\n')[1].strip()
        # print(title)

        authorDate = singleArticle.find('p', class_='font-normal').text
        author = authorDate.split('\n')[2].strip()
        date = authorDate.split('\n')[7].strip()
        #print(date)

        x = x+1
        text = singleArticle.find('div', class_= 'first-letter:float-left')
        if type(text) is type(None):
            text = singleArticle.find('article', class_= 'max-w-3xl').text
        else:
            text = text.text

        article = {
            'title': title,
            'date': date,
            'author': author,
            'link': link,
            'text': text
        }

        articleList.append(article)
        print(x, 'added article')

df = pd.DataFrame(articleList)
df.to_csv('Entrepreneur.com.csv')
print(x, 'saved to csv')