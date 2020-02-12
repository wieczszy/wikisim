"""Training script for the WikiModel.
Put model parameters in the 'parameters' dictionary and
run the script to train, test and save trained model.
"""

from model import WikiModel


if __name__ == '__main__':
    training_data_dir = 'data/featured_articles'
    testing_data_dir = 'data/featured_articles'
    model_save_dir = 'data/model'

    parameters = {
        'vector_size': 100,
        'min_count': 2,
        'epochs': 40
    }

    model = WikiModel()
    model.train(parameters, training_data_dir)
    model.test(testing_data_dir)
    model.save(model_save_dir)