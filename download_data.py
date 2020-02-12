from wikisim.crawler import Crawler

data_directory = 'wikisim/data2/featured_articles'

crawler = Crawler()
featured_articles = crawler.get_featured_articles()
crawler.save_featured_articles(featured_articles,
                               data_directory,
                               include_sub=False)