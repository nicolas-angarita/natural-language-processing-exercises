import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import os 
import json

def acquire_codeup():
    
    if os.path.isfile('codeup_blogs.csv'):
        
        return pd.read_csv('codeup_blogs.csv')

    else:
        
        url = 'https://codeup.com/blog/'
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        links = [link['href'] for link in soup.select('.more-link')]

        articles = []

        for url in links:

            url_response = get(url, headers=headers)
            soup = BeautifulSoup(url_response.text)

            title = soup.find('h1', class_='entry-title').text
            content = soup.find('div', class_='entry-content').text.strip()

            article_dict = {
                'title': title,
                'content': content
            }

            articles.append(article_dict)
            
    blogs = pd.DataFrame(articles) 
    blogs.to_csv('blog_articles.csv', index=False)
    
    return blogs


def acquire_codeup_blog(links):
    
    file = 'blog_articles.json'
    
    if os.path.exists(file) and os.stat(file).st_size != 0:
        
        with open(file) as f:
            
             return json.load(f)
    
    headers = {'User-Agent': 'Codeup Data Science'}
    articles = []

    for url in links:

        response = get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1', class_='entry-title').text
        content = soup.find('div', class_='entry-content').text.strip()

        article_dict = {
            'title': title,
            'content': content
        }

        articles.append(article_dict)


    with open(file, 'w') as f:
        json.dump(articles, f)
            
    return articles


def scrape_one_page(topic):
    
    base_url = 'https://inshorts.com/en/read'
    
    response = get(base_url + '/' + topic)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    titles = soup.find_all('span', itemprop='headline')
    summaries =  soup.find_all('div', itemprop='articleBody')
    
    summary_list = []
    
    for i in range(len(titles)):
        
        temp_dict = {'category': topic,
                    'title': titles[i].text,
                    'content': summaries[i].text}
        
        summary_list.append(temp_dict)
 
    return summary_list

def get_news_articles(topic_list):
    
    file = 'news_articles.json'
    
    if os.path.exists(file):
        
        with open(file) as f:
            
            return json.load(f)
        
    final_list= []
    
    for topic in topic_list:
        
        final_list.extend(scrape_one_page(topic))
    with open(file, 'w') as f:
        
        json.dump(final_list, f)
        
    return final_list    

#topics = ['business', 'sports', 'technology', 'entertainment']----- final_list = get_news_articles(topics)


def get_news_blog_articles():
    
    if os.path.isfile('new_articles.csv'):
        
        return pd.read_csv('new_articles.csv')

    else:

        categories = ['business', 'sports', 'technology', 'entertainment]
        urls = ['https://inshorts.com/en/read/' + category for category in categories]

        inshorts = []

        for url, category in zip(urls, categories):
            response = get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            titles = [title.text for title in soup.find_all('span', itemprop='headline')]
            contents = [article.text for article in soup.find_all('div', itemprop='articleBody')]

            for i in range(len(titles)):
                article = {
                    'title': titles[i],
                    'content': contents[i],
                    'category': category,
                }

                inshorts.append(article)

    news_articles = pd.DataFrame(inshorts)
    
    news_articles.to_csv('new_articles.csv', index = False)

    return news_articles