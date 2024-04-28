import requests
from bs4 import BeautifulSoup
import pandas as pd

websites=['https://startupnation.com/tag/business-and-life-planning/',
          'https://startupnation.com/tag/e-commerce/',
          'https://startupnation.com/tag/funding/',
          'https://startupnation.com/category/start-your-business/get-inspired/',
          'https://startupnation.com/category/grow-your-business/leverage-business-technology/',
          'https://startupnation.com/tag/growth-hacks/',
          'https://startupnation.com/tag/side-hustle/']
articleCount = 0
articleList = []

for n in range(0,len(websites)):
    pages=0
    if n == 0 or n == 2 or n == 3 or n == 4:
        pages = 15
    elif n == 1 or n == 6:
        pages = 5

    for x in range(1,pages+1):
        if x == 1:
            url = websites[n]
        else:
            url = websites[n]+'/page-'+str(x)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, features='lxml')

        articles = soup.find_all('article', class_= 'post')
        error = ""

        for item in articles:
            #Getting the url link of the article from the home page. Then, we get the link each article to be able to access it.
            try:
                link = item.find({'a':'cs-overlay-link'})['href']

                url1 = link
                # print(link)

                headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

                r1 = requests.get(url1, headers=headers1)
                singleArticle = BeautifulSoup(r1.content, features='lxml')
                
                error="title"
                title = singleArticle.find({'h1':'cs-entry__title'}).text
                # print(title)

                error="author"
                author = singleArticle.find('span',class_='cs-author').text
                # print(author)

                error="date"
                date = singleArticle.find('div',class_='cs-meta-date').text
                # print(date)

                text = singleArticle.find('div', class_= 'entry-content').text
                # print(text)

                article = {
                    'articleNumber':articleCount,
                    'title': title,
                    'date': date,
                    'author': author,
                    'link': link,
                    'text': text
                }
                articleCount+=1
                articleList.append(article)
                print(articleCount, 'added article')
            except Exception as e:
                # By this way we can know about the type of error occurring
                print("The error is: ",e,articleCount) 

df = pd.DataFrame(articleList)
df.to_csv('StartUpNation.csv')
print( 'saved to csv')


