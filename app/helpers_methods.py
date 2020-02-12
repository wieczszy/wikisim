import pandas as pd
from wikisim.model import WikiModel
from wikisim.cloud import CloudGenerator
import os
import matplotlib.pyplot as plt
import matplotlib



def process_article(article_name):
    cat = get_categories(article_name=article_name)
    save_response_as_fig(cat,article_name)
    get_wc(article_name)
    return cat[0][0].replace(' ','_')

def get_categories(article_name):
    m = WikiModel()
    m.load("data/model/doc2vec_100_2_40.model")
    r = m.classify(article_name=article_name)
    return r

def save_response_as_fig(r,article_name):
    matplotlib.use('Agg')
    f = pd.DataFrame(r, columns=['category', 'similarity']).sort_values(by='similarity').plot(x='category', y='similarity', kind='barh')
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f'img/{article_name}.png')
    # filename = os.path.join(dirname, f'img/result.png')

    if os.path.exists(filename):
        os.remove(filename)

    f.get_figure().savefig(filename,bbox_inches='tight')

def get_wc(article_name):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f'img/{article_name}_wc.png')
    g = CloudGenerator()
    plt.imsave(filename,g.get_cloud_for_article(article_name))
