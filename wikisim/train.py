from model import WikiModel

if __name__ == '__main__':
    parameters = {
        'vector_size': 10,
        'min_count': 2,
        'epochs': 5
    }

    model = WikiModel()
    model.train(parameters, 'data/test_data')
    model.test('data/test_data')
    model.save('data')