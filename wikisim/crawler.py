import mwclient
import os
import re
import requests
from tqdm import tqdm

# Helper script used to crawl text of Wikipedia's featured articles
# Gets titles and categories of articles mentioned on
# https://en.wikipedia.org/wiki/Wikipedia:Featured_article
# then saves the plain text versions of the articles in text files
# stored in structured catalogues.
#
# e.g Engineering and technology is a category and
# Engineering and technology_Engineering and technology biographies is
# it's subcategory. Subcategories are not stored in tree structure to
# make further processing easier.

class Crawler():
    def __init__(self):
        pass

    @staticmethod
    def get_page_as_text(title):
        """
        Returns plain text version of given Wikipedia article.

        Arguments:
            title {str} -- title of the article to acces

        Returns:
            str -- plain text version of the article
        """
        response = requests.get(
            'https://en.wikipedia.org/w/api.php',
            params={
                'action': 'query',
                'format': 'json',
                'titles': title,
                'prop': 'extracts',
                'explaintext': True
        }).json()

        page = next(iter(response['query']['pages'].values()))
        text = page['extract']
        return text

    @staticmethod
    def get_featured_articles():
        """
        Crawls categories and titles of featured articles from
        https://en.wikipedia.org/wiki/Wikipedia:Featured_article

        Returns:
            list -- list of tuples with articles data: (category, subcategory, title)
        """
        site = mwclient.Site("en.wikipedia.org")
        page = site.pages['Wikipedia:Featured_articles']
        page_content = page.text().split('\n')

        featured_articles = []

        category, subcategory, title = '', '', ''
        for line in page_content:
            if line.startswith('==='):
                subcategory = line.replace('=', '')
            elif line.startswith('=='):
                category = line.replace('=', '')
                subcategory = ''
            elif line.startswith('*'):
                if '{FA/' in line:
                    title = re.search(r'\[\[(.*?)\]\]', line)
                    title = title.group(1)
                    title = title.split('|')[0]
            if title == '':
                pass
            else:
                entry = (category, subcategory, title)
                featured_articles.append(entry)

        featured_articles = sorted(list(set(featured_articles)), key=lambda a: (a[0], a[1], a[2]))

        return featured_articles

    @staticmethod
    def save_featured_articles(featured_articles, data_dir='data/featured_articles', include_sub=True):
        """
        Saves crawled articles in text files in given directory
        in catalogues organized by categories and sub categories.

        Arguments:
            featured_articles {list} -- list returned by get_featured_articles()

        Keyword Arguments:
            data_dir {str} -- main directory for files to save (default: {'data/featured_articles'})
        """
        for article in tqdm(featured_articles):
            try:
                if (article[1] != '' and include_sub):
                    category = article[0] + '_' + article[1]
                else:
                    category = article[0]
                title = article[2]
                directory = os.path.join(data_dir, category)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file_path = os.path.join(directory, title) + '.txt'
                if not os.path.exists(file_path):
                    article_text = Crawler.get_page_as_text(article[2])
                    with open(file_path, 'w') as f:
                        f.write(article_text)
            except Exception:
                pass

if __name__ == '__main__':
    crawler = Crawler()
    featured_articles = crawler.get_featured_articles()
    crawler.save_featured_articles(featured_articles, include_sub=False)
