import wordcloud
from . import crawler
import numpy as np
import os
from tqdm import tqdm
from matplotlib import pyplot as plt


class CloudGenerator():
    def __init__(self):
        pass

    def _get_article(self, article):
        return crawler.Crawler.get_page_as_text(article)

    def get_cloud_from_text(self, text):
        cloud = wordcloud.WordCloud(max_words=100, background_color='white').generate(text)
        return np.array(cloud)

    def get_cloud_for_article(self, article):
        text = self._get_article(article)
        return self.get_cloud_from_text(text)

if __name__ == "__main__":
    cg = CloudGenerator()

    if not os.path.exists('data/c'):
        os.makedirs('data/c')

    for root, dirs, files in os.walk('data/featured_articles'):
        for d in tqdm(dirs):
            text = ''
            for file in os.listdir(os.path.join(root, d)):
                fname = os.path.join(root, d, file)
                text += open(fname, 'r').read()
            cloud = cg.get_cloud_from_text(text)
            plt.imsave(f'data/c/{d}.png', cloud)
