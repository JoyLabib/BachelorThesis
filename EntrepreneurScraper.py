import requests
from bs4 import BeautifulSoup
import pandas as pd

websites=['https://www.entrepreneur.com/leadership/thought-leaders',
          'https://www.entrepreneur.com/leadership/innovation',
          'https://www.entrepreneur.com/starting-a-business/business-plans',
          'https://www.entrepreneur.com/starting-a-business/business-ideas',
          'https://www.entrepreneur.com/starting-a-business/business-models',
          'https://www.entrepreneur.com/starting-a-business/side-hustle',
          'https://www.entrepreneur.com/starting-a-business/branding',
          'https://www.entrepreneur.com/growing-a-business/operations-logistics',
          'https://www.entrepreneur.com/growing-a-business/marketing',
          'https://www.entrepreneur.com/growing-a-business/diversity',
          'https://www.entrepreneur.com/growing-a-business/collaboration',
          'https://www.entrepreneur.com/growing-a-business/culture',
          'https://www.entrepreneur.com/growing-a-business/business-process',
          'https://www.entrepreneur.com/growing-a-business/legal',
          'https://www.entrepreneur.com/business-news',
          'https://www.entrepreneur.com/science-technology/social-media',
          'https://www.entrepreneur.com/science-technology/business-solutions',
          'https://www.entrepreneur.com/science-technology/devices',
          'https://www.entrepreneur.com/science-technology/data-recovery',
          'https://www.entrepreneur.com/money-finance/accounting',
          'https://www.entrepreneur.com/money-finance/debt-loans-refinancing',
          'https://www.entrepreneur.com/money-finance/taxes',
          'https://www.entrepreneur.com/money-finance/cryptocurrency-blockchain',
          'https://www.entrepreneur.com/money-finance/buying-investing-in-business',
          'https://www.entrepreneur.com/money-finance/personal-finance',
          'https://www.entrepreneur.com/living/health-wellness',
          'https://www.entrepreneur.com/living/productivity',
          'https://www.entrepreneur.com/living/life-hacks',
          'https://www.entrepreneur.com/living/travel',
          'https://www.entrepreneur.com/living/celebrity-entrepreneurs',
          'https://www.entrepreneur.com/living/career',
          'https://www.entrepreneur.com/living/resumes-interviewing',
          'https://www.entrepreneur.com/living/making-a-change']
for n in range(0,len(websites)+1):
    articleList = []

    for x in range(1,11):
        if x == 1:
            url = websites[n]
        else:
            url = websites[n]+'/page-'+str(x)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, features='lxml')

        articles = soup.find_all('div', class_= 'flex flex-row-reverse mb-12')

        for item in articles:
            #Getting the url link of the article from the home page. Then, we get the link each article to be able to access it.
            try:
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
            except Exception as e:
                # By this way we can know about the type of error occurring
                print("The error is: ",e) 
    print("Moved to the next page",n)

    df = pd.DataFrame(articleList)
    df.to_csv('Entrepreneur3'+str(n)+'.com.csv')
    print(x, 'saved to csv')