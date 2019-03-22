import os
import re
from Parser import Message
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='nltk')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns


def person_count_word_cloud(df, root=''):

    count = df.groupby('First_Name')['Msg'].count()
    wc = WordCloud(background_color='white', max_font_size=50, max_words=20)
    wc.fit_words(count.to_dict())
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(root+'wc.png')
    return fig, ax


def person_count_bar_chart(df, root=''):

    count = df.groupby('First_Name')['Msg'].count()
    count = count.sort_values(ascending=False)

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    sns.set(style="whitegrid")
    sns.barplot(y=count.index.values, x=count.values, palette="Blues_d", ax=ax)
    ax.set_xlabel('Number of Messages')
    plt.savefig(root+'count_bar.png')

    return fig, ax


def rolling_count(df, root=''):
    g = df.groupby('date')['Msg'].count()
    r = g.rolling(5).mean()
    r.index = pd.to_datetime(r.index)
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.plot(r.index, r.values)
    ax.set_ylabel('# Messages (5-day moving avg)')
    plt.savefig(root+'rolling_count.png')

    return fig, ax


def sentiment_time(df, root=''):
    g = df.groupby('date')['sentiment'].mean()
    r = g.rolling(5).mean()
    r.index = pd.to_datetime(r.index)
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.plot(r.index, r.values)
    ax.set_ylabel('Approximate Sentiment')
    plt.savefig(root+'sentiment_time.png')

    return fig, ax


def create_df(filename, root=''):
    # add try/except pattern here or confirm file exists
    # regex pattern is date, time, name, sentence
    pattern = r'(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2} [APM]+) - ([a-zA-Z\s]+): (.+)'
    sia = SentimentIntensityAnalyzer()
    msgs = list()
    with open(root+filename, 'r') as fp:
        for line in fp:
            # line = fp.readline()
            lst = re.findall(pattern, line)  # date, time, person
            if len(lst) > 0:
                tup = lst[0]
                if len(tup) == 4:
                    msgs.append(Message(tup, sia))
                elif len(tup) == 0:
                    msgs[-1].msg.append(line)
                else:
                    None  # need error handling

    dct = {}
    dct['media'] = [m.is_media for m in msgs]
    dct['First_Name'] = [m.name_first for m in msgs]
    dct['date'] = [m.date for m in msgs]
    dct['time'] = [m.time for m in msgs]
    dct['sentiment'] = [m.sentiment for m in msgs]
    dct['Msg'] = [m.msg for m in msgs]

    df = pd.DataFrame(dct)
    #df.to_pickle(root+'temp')
    #print(df.head())

    return df
