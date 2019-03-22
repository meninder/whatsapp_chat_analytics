

class Message(object):

    def __init__(self, tup, sia=None):

        self.sia = sia # sentiment analyzer
        self.name = tup[2]
        self.name_first = tup[2].split()[0]
        self.date = tup[0]
        self.time = tup[1]
        self.msg = tup[3]

        if self.sia is not None:
            self.sentiment = self.get_sentiment(self.msg)
        else:
            self.sentiment = None

        self.is_media = True if 'Media omitted' in tup[3] else False

    def get_sentiment(self, msg):

        score = self.sia.polarity_scores(msg)

        return score['compound']
