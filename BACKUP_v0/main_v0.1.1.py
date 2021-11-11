
# #####################################################################################################################
# Change History
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

# # # timing stuff
# # performance timer 'start'
# timing = time.perf_counter()
# # [thing to do]
# # performance timer 'stop' and print
# timing = time.perf_counter() - timing
# print('_____ time:   ', timing)

# # # memory usage stuff
# process = psutil.Process(os.getpid())
# print(process.memory_info()[0])  # used memory in bytes

# report memory usage
mem_use_kb = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
print('Process memory, initial:', mem_use_kb, 'kb')


dict_file = open("slowa2.txt", encoding="utf-8")
dict = {}
dict_stats = {
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
    'letters7': {}  # number of total occurances of 7-letter pairs
}

timing = time.perf_counter()
# get total count for progress reference
dict_stats['count'] = len(dict_file.readlines())
dict_file.seek(0)

# current word sequence number
word_counter = 0
# detector for progress update notification
# [0] - next milestone progress, [1] - current progress
progress_tick = [0, -1]
# progress print begining
print('[', end='')
# take each line - word from a file
for line in dict_file:
    # update loading progress
    word_counter += 1
    progress_tick[1] = (word_counter / dict_stats['count']) * 100
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
    dict[line] = line

    # update lengths information in dict_stats
    if len(line) > dict_stats['len_max']:
        dict_stats['len_max'] = len(line)
    if len(line) < dict_stats['len_min']:
        dict_stats['len_min'] = len(line)
    try:
        dict_stats['lengths'][len(line)] += 1
    except IndexError as e:
        print(e)
        raise e

    # update occurances of single letters
    for letter in line:
        try:
            dict_stats['letters'][letter] += 1
        except KeyError as e:
            dict_stats['letters'][letter] = 1

    # convert str into list
    letters = [x for x in line]

    # update occurances of 2-letters groups
    # iterate through list of letters
    for idx in range(len(letters)):
        # try getting current letter and the following - 2-letters pair
        try:
            key = letters[idx] + letters[idx + 1]
            # try updating entry in dict_stats['letters2']
            try:
                dict_stats['letters2'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dict_stats['letters2'][key] = 1
        # no more pairs in current word
        except IndexError as e:
            pass

    # update occurances of 3-letters groups
    # iterate through list of letters
    for idx in range(len(letters)):
        # try getting current letter and the following - 3-letters pair
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2]
            # try updating entry in dict_stats['letters3']
            try:
                dict_stats['letters3'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dict_stats['letters3'][key] = 1
        # no more pairs in current word
        except IndexError as e:
            pass

    # update occurances of 4-letters groups
    # iterate through list of letters
    for idx in range(len(letters)):
        # try getting current letter and the following - 4-letters pair
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3]
            # try updating entry in dict_stats['letters4']
            try:
                dict_stats['letters4'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dict_stats['letters4'][key] = 1
        # no more pairs in current word
        except IndexError as e:
            pass

    # update occurances of 5-letters groups
    # iterate through list of letters
    for idx in range(len(letters)):
        # try getting current letter and the following - 5-letters pair
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4]
            # try updating entry in dict_stats['letters5']
            try:
                dict_stats['letters5'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dict_stats['letters5'][key] = 1
        # no more pairs in current word
        except IndexError as e:
            pass

    # update occurances of 6-letters groups
    # iterate through list of letters
    for idx in range(len(letters)):
        # try getting current letter and the following - 6-letters pair
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5]
            # try updating entry in dict_stats['letters6']
            try:
                dict_stats['letters6'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dict_stats['letters6'][key] = 1
        # no more pairs in current word
        except IndexError as e:
            pass

    # update occurances of 7-letters groups
    # iterate through list of letters
    for idx in range(len(letters)):
        # try getting current letter and the following - 7-letters pair
        try:
            key = letters[idx] + letters[idx + 1] + letters[idx + 2] + letters[idx + 3] + letters[idx + 4] \
                  + letters[idx + 5] + letters[idx + 6]
            # try updating entry in dict_stats['letters7']
            try:
                dict_stats['letters7'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dict_stats['letters7'][key] = 1
        # no more pairs in current word
        except IndexError as e:
            pass

# 'progress print ending (and new line symbol)
print('100%]')

# calculate average word length for dict_stats
dict_stats['len_avg'] = \
    sum([dict_stats['lengths'][i] * i for i in range(len(dict_stats['lengths']))]) / dict_stats['count']

# report memory usage
mem_use_kb = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
print('Process memory, after loading dict structures:', mem_use_kb, 'kb')





# # draw stats
# fig_letters = px.bar(x=[letter for letter in dict_stats['letters']],
#               y=[dict_stats['letters'][letter] for letter in dict_stats['letters']], title="Letters")
# fig_letters.show()
#
# fig_lengths = px.bar(x=[i for i in range(len(dict_stats['lengths']))],
#               y=[dict_stats['lengths'][i] for i in range(len(dict_stats['lengths']))], title="Lengths")
# fig_lengths.show()

