import requests
from bs4 import BeautifulSoup
import pandas as pd

articleList = []

for x in range(1,18):
    if x == 1:
        url = 'https://www.theelpodcast.com/blog/'
    else:
        url = 'https://www.theelpodcast.com/blog/page/'+str(x)+'/'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, features='lxml')

    articles = soup.find_all('div', class_= 'blog-holder')

    for item in articles:
        #Getting the url link of the article from the home page. Then, we get the link each article to be able to access it.
        link = item.find({'a':'more-link'})['href']

        url1 = link
        headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

        r1 = requests.get(url1, headers=headers1)
        singleArticle = BeautifulSoup(r1.content, features='lxml')

        title = singleArticle.find('h1', class_ = 'headline').text
        date = singleArticle.find('p', class_ = 'align-left').text
        text = singleArticle.find('div', class_= 'article').text

        splitted = date.split()
        date = splitted[2]+' '+splitted[3]+' '+splitted[4]
        author = splitted[6] +' '+  splitted[7]

        article = {
            'title': title,
            'date': date,
            'author': author,
            'link': link,
            'text': text
        }
        
        articleList.append(article)
        print(x,'added article')

df = pd.DataFrame(articleList)
df.to_csv('TheelPodcast.csv')
print(x,'saved to csv')