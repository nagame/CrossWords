
# #####################################################################################################################
# Change History
#   v0.2.1
#     - started implementing Sequence class
#       this class will represent a sequence of letters (not necessarily a whole, legit word but also)
#     - started creating sequence dictionaries with objects and conneting them together
#   v0.2(functional)
#     *** this version is fine for just statistical analysis of a word list
#     *** namely: generate dictionaries of sequences of letters (different lengths)
#     ***         together with information how many ocurrances of each sequence there are
#   -------
#   v0.1.4
#     - generalized similar, repeating pieces of code for counting n-letter sequences
#       (this seems to have worsened the performance by a bit, but makes it sooo much easie rto work with the code)
#   v0.1.3
#     - counting sequences up to 14 letters long
#     - all sequences dictionaries sorted by number of occurances
#     - minor changes in structure
#   v0.1.2
#     - counting sequences up to 12-letters long
#     - various changes in code structure
#   v0.1.1
#     - counting sequences of 1-,2-,3-,4-,5-,6- and 7-letters
#     - added memory info printout
#     - added loading progress printout
#   v0.1
#     - added loading dictionary from txt file
#     - added statistics: word count, words' lengths count, avg word len, letter count, 2-letter pairs count,
#     - added histograms (plotly) - words' lengths and single letter occurances
#
# #####################################################################################################################


import os, psutil
import time
import plotly.express as px




class Sequence():
    def __init__(self, key):
        self.sequence = str(key)  # this particular sequence string
        self.word_source_ref = None
        self.count = None  # how many times this sequence appeared in the source data
        self.origin_words = None  # dictionary of words that contain this sequence







# report memory usage
mem_use_kb = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
print('Process memory, initial:', mem_use_kb, 'kb')

source_file = open("slowa2.txt", encoding="utf-8")

# data structure describing the dictionary loaded from source file
dictionary = {
    'words': {},  # list of words from the source file
    'count': 0,  # number of words in the dictionary
    'lengths': [0]*30,  # number of words of given length
    'len_max': 0,  # shortest word's length
    'len_min': 30,  # longest word's length
    'len_avg': 0,  # average word length
    'letters1': {},  # number of total occurances of given letters
    'letters2': {},  # number of total occurances of 2-letter pairs
    'letters3': {},  # number of total occurances of 3-letter pairs
    'letters4': {},  # number of total occurances of 4-letter pairs
    'letters5': {},  # number of total occurances of 5-letter pairs
    'letters6': {},  # number of total occurances of 6-letter pairs
    'letters7': {},  # number of total occurances of 7-letter pairs
    'letters8': {},  # number of total occurances of 8-letter pairs
    'letters9': {},  # number of total occurances of 9-letter pairs
    'letters10': {},  # number of total occurances of 10-letter pairs
    'letters11': {},  # number of total occurances of 11-letter pairs
    'letters12': {},  # number of total occurances of 12-letter pairs
    'letters13': {},  # number of total occurances of 13-letter pairs
    'letters14': {}  # number of total occurances of 14-letter pairs
}

# # start counting time of loading basic dictionary structure
# performance timer 'start'
timing = time.perf_counter()

# get total count for progress reference
dictionary['count'] = len(source_file.readlines())
source_file.seek(0)

# current word sequence number
word_counter = 0
# detector for progress update notification
# [0] - next milestone progress, [1] - current progress
progress_tick = [0, -1]
# progress print begining
print('[', end='')
# take each line - word from a file
for line in source_file:
    # # update loading progress
    word_counter += 1
    progress_tick[1] = (word_counter / dictionary['count']) * 100
    # current progress exceeds current milestone
    if progress_tick[1] > progress_tick[0]:
        # notify user of achieved milestone
        print(str(progress_tick[0])+'%', end='|')
        # set next milestone
        progress_tick[0] += 5

    # remove endline character
    if line[-1] == '\n':
        line = line[0:len(line)-1]

    # assign 'value' to the word
    # TODO: this value is now just a sequence number - an object could reside here instead
    word_obj = Sequence(line)
    word_obj.word_source_ref = word_counter
    dictionary['words'][line] = word_obj

    # # update lengths information in dict_stats
    # max and min lengths
    if len(line) > dictionary['len_max']:
        dictionary['len_max'] = len(line)
    if len(line) < dictionary['len_min']:
        dictionary['len_min'] = len(line)
    # lengths histogram data
    try:
        dictionary['lengths'][len(line)] += 1
    except IndexError as e:
        print(e)
        raise e

    # # update occurances of [s1..s2) letters sequences
    # convert str into list
    letters = [x for x in line]
    s1, s2 = 1, 15
    for seq_len in range(s1, s2):
        for idx in range(len(letters)):
            # try getting current letter and the following - 2-letters sequences
            try:
                seq_key = ''
                for seq_pos in range(seq_len):
                    seq_key += letters[idx+seq_pos]
                # try updating entry in dict_stats['lettersX']
                try:
                    # increase sequence ocurrnace counter
                    dictionary['letters'+str(seq_len)][seq_key].count += 1
                    # add current word to origins dictionary
                    dictionary['letters' + str(seq_len)][seq_key].origin_words[line] = word_obj
                # no entry yet, create it
                except KeyError as e:
                    # create Sequence object, assign actual letter sequence
                    seq_obj = Sequence(seq_key)
                    seq_obj.count = 1
                    # add current word as first origin
                    seq_obj.origin_words = {line: word_obj}
                    # put object into dictionary
                    dictionary['letters'+str(seq_len)][seq_key] = seq_obj
            # no more sequences in current word
            except IndexError as e:
                pass
# calculate average word length for dict_stats
dictionary['len_avg'] = \
    sum([dictionary['lengths'][i] * i for i in range(len(dictionary['lengths']))]) / dictionary['count']
# 'progress print ending (and new line symbol)
print('100%]')


# # stop counting time of loading basic dictionary structure
# performance timer 'stop' and print
print('Dictionary basic structure loading time:   ', time.perf_counter() - timing)
# report memory usage
mem_use_kb = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
print('Process memory, after loading dictionary basic structures:', mem_use_kb, 'kb')



# # sort letters sequences dictionaries by number of occurances
# performance timer 'start'
timing = time.perf_counter()
# try sorting letters dictionaries
try:
    dictionary['letters1'] = {k: v for k, v in sorted(dictionary['letters1'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters2'] = {k: v for k, v in sorted(dictionary['letters2'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters3'] = {k: v for k, v in sorted(dictionary['letters3'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters4'] = {k: v for k, v in sorted(dictionary['letters4'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters5'] = {k: v for k, v in sorted(dictionary['letters5'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters6'] = {k: v for k, v in sorted(dictionary['letters6'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters7'] = {k: v for k, v in sorted(dictionary['letters7'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters8'] = {k: v for k, v in sorted(dictionary['letters8'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters9'] = {k: v for k, v in sorted(dictionary['letters9'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters10'] = {k: v for k, v in sorted(dictionary['letters10'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters11'] = {k: v for k, v in sorted(dictionary['letters11'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters12'] = {k: v for k, v in sorted(dictionary['letters12'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters13'] = {k: v for k, v in sorted(dictionary['letters13'].items(), key=lambda item: item[1].count, reverse=True)}
    dictionary['letters14'] = {k: v for k, v in sorted(dictionary['letters14'].items(), key=lambda item: item[1].count, reverse=True)}
except Exception as e:
    print(e)
    pass
# performance timer 'stop' and print
print('Sorting time:', time.perf_counter() - timing)
# report memory usage
mem_use_kb = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
print('Process memory, after sorting sequence dictionaries:', mem_use_kb, 'kb')












# # draw stats
# data = dictionary['letters']
# fig_letters = px.bar(x=[letter for letter in data],
#               y=[data[letter] for letter in data], title="Letters")
# fig_letters.show()
#
# fig_lengths = px.bar(x=[i for i in range(len(dictionary['lengths']))],
#               y=[dictionary['lengths'][i] for i in range(len(dictionary['lengths']))], title="Lengths")
# fig_lengths.show()

