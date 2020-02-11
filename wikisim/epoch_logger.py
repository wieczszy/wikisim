import datetime
from gensim.models.callbacks import CallbackAny2Vec

class EpochLogger(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        t = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{t} -- Epoch #{self.epoch}")

    def on_epoch_end(self, model):
        self.epoch += 1