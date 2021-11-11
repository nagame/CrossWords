
# #####################################################################################################################
# Change History
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
    'letters': {},  # number of total occurances of given letters
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
    # update loading progress
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
    dictionary['words'][line] = line

    # update lengths information in dict_stats
    if len(line) > dictionary['len_max']:
        dictionary['len_max'] = len(line)
    if len(line) < dictionary['len_min']:
        dictionary['len_min'] = len(line)
    try:
        dictionary['lengths'][len(line)] += 1
    except IndexError as e:
        print(e)
        raise e

    # update occurances of single letters
    for letter in line:
        try:
            dictionary['letters'][letter] += 1
        except KeyError as e:
            dictionary['letters'][letter] = 1

    # convert str into list
    letters = [x for x in line]

    # update occurances of 2-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 2-letters sequences
        try:
            key = letters[idx] + letters[idx + 1]
            # try updating entry in dict_stats['letters2']
            try:
                dictionary['letters2'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters2'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 3-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 3-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2]
            # try updating entry in dict_stats['letters3']
            try:
                dictionary['letters3'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters3'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 4-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 4-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3]
            # try updating entry in dict_stats['letters4']
            try:
                dictionary['letters4'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters4'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 5-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 5-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4]
            # try updating entry in dict_stats['letters5']
            try:
                dictionary['letters5'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters5'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 6-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 6-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5]
            # try updating entry in dict_stats['letters6']
            try:
                dictionary['letters6'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters6'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 7-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 7-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5] + letters[idx + 6]
            # try updating entry in dict_stats['letters7']
            try:
                dictionary['letters7'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters7'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 8-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 8-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5] + letters[idx + 6] + letters[idx + 7]
            # try updating entry in dict_stats['letters8']
            try:
                dictionary['letters8'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters8'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 9-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 9-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5] + letters[idx + 6] + letters[idx + 7] + letters[idx + 8]
            # try updating entry in dict_stats['letters9']
            try:
                dictionary['letters9'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters9'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 10-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 10-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5] + letters[idx + 6] + letters[idx + 7] + letters[idx + 8] + letters[idx + 9]
            # try updating entry in dict_stats['letters10']
            try:
                dictionary['letters10'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters10'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 11-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 11-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5] + letters[idx + 6] + letters[idx + 7] + letters[idx + 8] + letters[idx + 9] \
                  + letters[idx + 10]
            # try updating entry in dict_stats['letters11']
            try:
                dictionary['letters11'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters11'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update occurances of 12-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 12-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5] + letters[idx + 6] + letters[idx + 7] + letters[idx + 8] + letters[idx + 9] \
                  + letters[idx + 10] + letters[idx + 11]
            # try updating entry in dict_stats['letters12']
            try:
                dictionary['letters12'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters12'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update ocurrances of 13-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 13-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5] + letters[idx + 6] + letters[idx + 7] + letters[idx + 8] + letters[idx + 9] \
                  + letters[idx + 10] + letters[idx + 11] + letters[idx + 12]
            # try updating entry in dict_stats['letters13']
            try:
                dictionary['letters13'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters13'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

    # update ocurrances of 14-letters sequences
    for idx in range(len(letters)):
        # try getting current letter and the following - 14-letters sequences
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5] + letters[idx + 6] + letters[idx + 7] + letters[idx + 8] + letters[idx + 9] \
                  + letters[idx + 10] + letters[idx + 11] + letters[idx + 12] + letters[idx + 13]
            # try updating entry in dict_stats['letters14']
            try:
                dictionary['letters14'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dictionary['letters14'][key] = 1
        # no more sequences in current word
        except IndexError as e:
            pass

# 'progress print ending (and new line symbol)
print('100%]')

# # stop counting time of loading basic dictionary structure
# performance timer 'stop' and print
print('Dictionary level 14 basic structure loading time:   ', time.perf_counter() - timing)


# calculate average word length for dict_stats
dictionary['len_avg'] = \
    sum([dictionary['lengths'][i] * i for i in range(len(dictionary['lengths']))]) / dictionary['count']

# report memory usage
mem_use_kb = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
print('Process memory, after loading dictionary level 14 basic structures:', mem_use_kb, 'kb')






# # # timing stuff
# # performance timer 'start'
# timing = time.perf_counter()
# # [thing to do]
# # performance timer 'stop' and print
# timing = time.perf_counter() - timing
# print('_____ time:   ', timing)

# performance timer 'start'
timing = time.perf_counter()
# sort letters sequences dictionaries by number of occurances
dictionary['letters'] = {k: v for k, v in sorted(dictionary['letters'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters2'] = {k: v for k, v in sorted(dictionary['letters2'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters3'] = {k: v for k, v in sorted(dictionary['letters3'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters4'] = {k: v for k, v in sorted(dictionary['letters4'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters5'] = {k: v for k, v in sorted(dictionary['letters5'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters6'] = {k: v for k, v in sorted(dictionary['letters6'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters7'] = {k: v for k, v in sorted(dictionary['letters7'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters8'] = {k: v for k, v in sorted(dictionary['letters8'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters9'] = {k: v for k, v in sorted(dictionary['letters9'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters10'] = {k: v for k, v in sorted(dictionary['letters10'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters11'] = {k: v for k, v in sorted(dictionary['letters11'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters12'] = {k: v for k, v in sorted(dictionary['letters12'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters13'] = {k: v for k, v in sorted(dictionary['letters13'].items(), key=lambda item: item[1], reverse=True)}
dictionary['letters14'] = {k: v for k, v in sorted(dictionary['letters14'].items(), key=lambda item: item[1], reverse=True)}
# performance timer 'stop' and print
print('L1 through L13 sorting time:', time.perf_counter() - timing)

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

