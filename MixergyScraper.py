import requests
from bs4 import BeautifulSoup
import pandas as pd

articleList = []
articleCount=1


for x in range(1,136):
    
    if x == 1:
        url = 'https://mixergy.com/interviews/'
    else:
        url = 'https://mixergy.com/interviews/page/'+str(x)+'/'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, features='lxml')
    articles = soup.find_all('div',class_='col-sm-4')
    for item in articles:
        error=''
        try:
            #Getting the url link of the article from the home page. Then, we get the link each article to be able to access it.
            link = item.find({'div','content'}).a['href']
            print(link)

            url1 = link
            headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

            r1 = requests.get(url1, headers=headers1)
            singleArticle = BeautifulSoup(r1.content, features='lxml')

            error="title"
            title = singleArticle.find('h1', class_ = 'article-title entry-title').text

            error="author"
            author = singleArticle.find('span',class_ = 'guest-name').text
            author1 = author.split(' ',1)[0]
            length=len(author.split(' '))

            error="company"
            companyName = singleArticle.find('span',class_ = 'company-name').text
            companyName = companyName[2:]

            error="date"
            date = singleArticle.find('div', class_ = 'post-date').text
            date = date.split(' ',1)[1]

            error="text"
            wholetext2 = singleArticle.find('article',class_ = 'transcript-view')
            wholeText = wholetext2.find_all('p')
            text=''
            guest = False
            condition = author1+':'

            for p in wholeText:
                p = p.text
                if 'Andrew:' in p or 'Andrew Warner' in p:
                    guest = False
                elif condition in p or 'Interviewee:' in p:
                    article = {
                        'articleNumber':articleCount,
                        'title': title,
                        'date': date,
                        'author': author,
                        'company': companyName,
                        'link': link,
                        'text': text
                    }
                    
                    articleList.append(article)
                    text=''
                    textToBeAdded = p
                    textToBeAdded = textToBeAdded.split(' ',1)[1]
                    text = text + textToBeAdded + ' '
                    guest = True
                elif author+':' in p:
                    article = {
                        'articleNumber':articleCount,
                        'title': title,
                        'date': date,
                        'author': author,
                        'company': companyName,
                        'link': link,
                        'text': text
                    }
                    
                    articleList.append(article)
                    text=''
                    textToBeAdded = p
                    textToBeAdded = textToBeAdded.split(' ',length)[length]
                    # if length == 2:
                    #     textToBeAdded = textToBeAdded.split(' ',2)[2]
                    # elif length == 3:
                    #     textToBeAdded = textToBeAdded.split(' ',3)[3]
                    text = text + textToBeAdded + ' '
                    guest = True
                elif guest == True:
                    text = text + p + ' '
            

            print(articleCount,'added article')
            articleCount=articleCount+1
        except Exception as e:
            # By this way we can know about the type of error occurring
            print("The error is: ",e,error,articleCount) 

df = pd.DataFrame(articleList)
df.to_csv('Mixergy.csv')
print('saved to csv')





