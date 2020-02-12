# wikisim
> Project for a class on search engines. Finds matching category for a given Wikipedia article.

Wikisim uses Gensim's Doc2Vec model to compare Wikipedia entry provided by the user to the base of [Featured Articles](https://en.wikipedia.org/wiki/Wikipedia:Featured_articles). The model is trained on all articles from the Featured Articles category (as of 12/02/2020). For demonstration purposes, Wikisim comes with a Flask-based interface but it is possible to make the classification in command line (using provied script) and/or import the model to use in other scripts. Training script for the model and tools to crawl training data are also provided.

There are 30 categories:
```
Art, architecture, and archaeology
Biology
Business, economics, and finance
Chemistry and mineralogy
Computing
Culture and society
Education
Engineering and technology
Food and drink
Geography and places
Geology and geophysics
Health and medicine
Heraldry, honors, and vexillology
History
Language and linguistics
Law
Literature and theatre
Mathematics
Media
Meteorology and climate
Music
Philosophy and psychology
Physics and astronomy
Politics and government
Religion, mysticism and mythology
Royalty and nobility
Sport and recreation
Transport
Video gaming
Warfare
```

## Installation
Clone the repository and install required libraries:

`git clone https://github.com/wieczszy/wikisim.git`

`pip install -r requirements.txt`.

## Usage
You can use Wikisim in two ways:
- in browser, by running `[TODO FLASK COMMAND]`
- using the classification script `python wikisim/classify.py wikisim/data/model/doc2vec_100_2_40.model Arthur_Sullivan
`

## Training the model
Using `train.py` you can train the model using your own data and/or hyperparameters. Provide paths to training and testing data, where to save the trained model and hyperparameters directly in the script. Testing returns model's accuracy understood as percentage of articles classified in the correct category. 

## Data
Featured articles can be downloaded in plain text using `crawler.py`. Downloaded articles are saved in a structure represented below.
```
├── data
│   ├── featured_articles
│   │   ├── Art, architecture, and archaeology
│   │   │   ├── 7 World Trade Center.txt
│   │   │   ├── Acra (fortress).txt
│   │   │   ├── Adolfo Farsari.txt
│   │   ├── Sport and recreation
│   │   │   ├── 1877 Wimbledon Championship.txt
│   │   │   ├── 1896 Summer Olympics.txt
│   │   │   ├── 1906 French Grand Prix.txt
│   │   │   ├── 1910 London to Manchester air race.txt
│   │   ├── Transport
│   │   │   ├── 1955 MacArthur Airport United Airlines crash.txt
│   │   │   ├── Air-tractor sledge.txt
│   │   │   ├── AirTrain JFK.txt
│   │   │   ├── Albert Bridge, London.txt
│   │   ├── Video games
│   │   │   ├── 32X.txt
│   │   │   ├── Agatha Christie: Murder on the Orient Express.txt
│   │   │   ├── Age of Empires.txt
│   │   │   ├── Alleyway (video game).txt
```
`split_data.py` can be used to move a number of articles from each category to separate directory `data/test_data` that has the same structure as above. This data can be used for testing the model. 
