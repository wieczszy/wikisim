import collections
import datetime
import gensim
import os
import time
from tqdm import tqdm
from gensim.models.callbacks import CallbackAny2Vec
from crawler import get_page_as_text

class EpochLogger(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        t = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f'{t} -- Epoch #{self.epoch}')

    def on_epoch_end(self, model):
        self.epoch += 1

def iter_documents(top_directory):
    for root, dirs, files in tqdm(os.walk(top_directory)):
        for file in filter(lambda file: file.endswith('.txt'), files):
            document = open(os.path.join(root, file)).read()
            yield gensim.utils.tokenize(document, lower=True)

def make_dictionary(top_directory):
    return gensim.corpora.Dictionary(iter_documents(top_directory))

def tag_documents(top_directory):
    for root, dirs, files in tqdm(os.walk(top_directory)):
        for file in filter(lambda file: file.endswith('.txt'), files):
            document = open(os.path.join(root, file)).read()
            tokens = gensim.utils.simple_preprocess(document)
            document_class = root.split('/')[-1]
            yield gensim.models.doc2vec.TaggedDocument(tokens, [document_class])

def test_model(model, data):
    ranks = []
    for doc_id in tqdm(range(len(data))):
        vector = model.infer_vector(data[doc_id].words)
        sims = model.docvecs.most_similar([vector], topn=len(model.docvecs))
        classified_as = sorted(sims, key=lambda s: s[1], reverse=True)[0][0]
        r = 1 if classified_as == data[doc_id].tags[0] else 0
        ranks.append(r)
    counter = collections.Counter(ranks)
    acc = counter[1] / len(data)
    return acc, counter


if __name__ == '__main__':
    VECTOR_SIZE = 100
    MIN_COUNT = 5
    NUM_EPOCHS = 80
    TRAIN = True
    SAVE = True
    WIKI_TEST = False
    ASSESS = False
    TEST = True

    if TRAIN or ASSESS:
        print('=== BUILDING TRAINING DATA ===')
        training_data = list(tag_documents('data/featured_articles'))

    if TRAIN:
        epoch_logger = EpochLogger()
        model = gensim.models.doc2vec.Doc2Vec(vector_size=VECTOR_SIZE,
                                            min_count=MIN_COUNT,
                                            epochs=NUM_EPOCHS,
                                            callbacks=[epoch_logger])
        model.build_vocab(training_data)
        print('=== TRAINING MODEL ===')
        start_time = time.time()
        model.train(training_data, total_examples=model.corpus_count, epochs=model.epochs)
        end_time = time.time()
        print("--- Training time: %s seconds ---" % (time.time() - start_time))
        if SAVE:
            model.save('data/model/doc2vec_80_epochs.model')
    else:
        model = gensim.models.doc2vec.Doc2Vec.load('data/model/doc2vec.model')

    if WIKI_TEST:
        print('=== WIKI ARTICLE TEST ===')
        article_name = 'Copenhagen interpretation'
        test_art  = get_page_as_text(article_name)
        test_art = gensim.utils.simple_preprocess(test_art)
        vector = model.infer_vector(test_art)
        sims = model.docvecs.most_similar([vector], topn=len(model.docvecs))
        ranked = sorted(sims, key=lambda s: s[1], reverse=True)

        print(article_name)
        for r in ranked:
            print(r)

    if ASSESS:
        print('=== ASSESSING MODEL ===')
        acc, _ = test_model(model, training_data)
        acc = round(acc, 4)
        print(f"--- Assessment accuracy: {acc} ---")

    if TEST:
        print('=== BUILDING TESTING DATA ===')
        test_data = list(tag_documents('data/test_data'))
        print('=== TESTING MODEL ===')
        acc, _ = test_model(model, test_data)
        acc = round(acc, 4)
        print(f"--- Testing accuracy: {acc} ---")

