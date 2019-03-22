import pandas as pd
import numpy as np
import re
import random


def generate_text(sentences):
    names = ['Alice', 'Bob', 'Chuck', 'Debra', 'Evan']
    dates = pd.date_range('1/1/2018', '12/31/2018')
    cluster_num = np.random.poisson(4, size=len(dates))  # on each date, this many clusters of convs
    burst_num = np.random.poisson(4, size=len(dates))  # for each cluster, this many bursts
    times = pd.date_range('00:01', '23:59', freq="30s")
    lst_times = list(times)


    txt = ''

    for cluster, burst, date in zip(cluster_num, burst_num, dates):
        t = random.sample(lst_times, cluster)
        t.sort()
        line = ''
        for t_ in t:
            idx = lst_times.index(t_)
            for b_ in range(burst):
                if idx+b_ < len(lst_times):
                    t_msg = lst_times[idx+b_] # messages every 30s
                    line += date.strftime('%m/%d/%y') + ', '
                    line += t_msg.strftime('%I:%M %p') + ' - '
                    line += random.choice(names) + ': '
                    comment = random.choice(sentences)
                    for ch in '"*”“':
                        comment = comment.replace(ch, '')
                    line += comment
                    line += '\n'
        txt += line

    return txt


def main():
    filename = 'war_and_peace.txt'
    sentences = list()
    num_sentences = 50
    with open(filename) as fn:
        sentences += re.findall(r'.*?[\.\!\?]+', fn.read())
    sentences = sentences[100:]

    txt = generate_text(sentences)

    with open('chat_war_peace.txt', 'w+') as txt_file:
        txt_file.write(txt)


main()