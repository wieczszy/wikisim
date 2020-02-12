"""Doc2Vec model that can be trained and used to
measure the similarity of a given Wikipedia article
to Featured Articles divided into 30 categories.
"""

import collections
import gensim
import os
import time
from tqdm import tqdm
from wikisim import crawler
from wikisim.epoch_logger import EpochLogger

class WikiModel():
    def __init__(self):
        self.model = None

    def _tag_documents(self, top_directory):
        """For files in given directory, creates gensim
        TaggedDocuments with the file's bottom directory
        as tag.

        Arguments:
            top_directory {str} -- data directory

        Yields:
            gensim.models.doc2vec.TaggedDocument -- tokenized document
        """
        for root, _, files in tqdm(os.walk(top_directory)):
            for file in filter(lambda file: file.endswith('.txt'), files):
                document = open(os.path.join(root, file)).read()
                tokens = gensim.utils.simple_preprocess(document)
                document_class = root.split('/')[-1]
                yield gensim.models.doc2vec.TaggedDocument(tokens, [document_class])

    def _build_data(self, data_path):
        """Prepares data to be used for training or testing.

        Arguments:
            data_path {str} -- data directory

        Returns:
            list -- list of TaggedDocuments
        """
        data = list(self._tag_documents(data_path))
        return data

    def train(self, parameters, training_data_path):
        """Trains the Doc2Vec model using given parameters
        and training data.

        Arguments:
            parameters {dict} -- dictionary with training parameters:
                'vector_size': {int} -- model's size
                'min_count': {int} -- min number of word occurences
                'epochs': {int} -- number of training epochs
            training_data_path {str} -- training data directory
        """
        epoch_logger = EpochLogger()
        self.model = gensim.models.doc2vec.Doc2Vec(vector_size=parameters['vector_size'],
                                                   min_count=parameters['min_count'],
                                                   epochs=parameters['epochs'],
                                                   callbacks=[epoch_logger])
        print('=== BUILDING TRAINING DATA ===')
        training_data = self._build_data(training_data_path)
        self.model.build_vocab(training_data)
        print('=== TRAINING MODEL ===')
        start_time = time.time()
        self.model.train(training_data, total_examples=self.model.corpus_count, epochs=self.model.epochs)
        print("--- Training time: %s seconds ---" % (time.time() - start_time))

    def save(self, save_dir):
        """Saves the model to files.

        Arguments:
            save_dir {str} -- directory to save model's files in
        """
        assert self.model != None
        num_vectors = self.model.vector_size
        min_count = self.model.vocabulary.min_count
        epochs = self.model.epochs
        model_name = f"doc2vec_{num_vectors}_{min_count}_{epochs}.model"
        self.model.save(os.path.join(save_dir, model_name))
        print(f'Saved model as {os.path.join(save_dir, model_name)}')

    def load(self, model_path):
        """Loads model from files.

        Arguments:
            model_path {str} -- directory with saved model
        """
        self.model = gensim.models.doc2vec.Doc2Vec.load(model_path)

    def test(self, test_data_path):
        """Test the model. Prints model's accuracy.

        Arguments:
            test_data_path {str} -- directory with testing data
        """
        assert self.model != None
        print('=== BUILDING TESTING DATA ===')
        test_data = self._build_data(test_data_path)
        ranks = []
        print('=== TESTING MODEL ===')
        for doc_id in tqdm(range(len(test_data))):
            vector = self.model.infer_vector(test_data[doc_id].words)
            sims = self.model.docvecs.most_similar([vector], topn=len(self.model.docvecs))
            classified_as = sorted(sims, key=lambda s: s[1], reverse=True)[0][0]
            r = 1 if classified_as == test_data[doc_id].tags[0] else 0
            ranks.append(r)
        counter = collections.Counter(ranks)
        acc = round(counter[1] / len(test_data), 4)
        print(f"--- Testing accuracy: {acc} ---")

    def classify(self, article_name):
        """Classify a Wikipedia article.

        Arguments:
            article_name {str} -- The article's title (end of the URL)

        Returns:
            list -- list of tuples (category_name:str, similarity_measure:float)
        """
        assert self.model != None
        article  = crawler.Crawler.get_page_as_text(article_name)
        article = gensim.utils.simple_preprocess(article)
        vector = self.model.infer_vector(article)
        sims = self.model.docvecs.most_similar([vector], topn=len(self.model.docvecs))
        ranked = sorted(sims, key=lambda s: s[1], reverse=True)
        return ranked