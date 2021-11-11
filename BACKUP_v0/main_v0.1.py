# #####################################################################################################################
# Change History
#   v0.1
#     - added loading dictionary from txt file
#     - added statistics: word count, words' lengths count, avg word len, letter count, 2-letter pairs count,
#     - added histograms (plotly) - words' lengths and single letter occurances
#
# #####################################################################################################################



import plotly.express as px

dict_file = open("slowa2.txt", encoding="utf-8")
dict = {}
dict_stats = {
    'count': 0,  # number of words in the dictionary
    'lengths': [0]*30,  # number of words of given length
    'len_max': 0,  # shortest word's length
    'len_min': 30,  # longest word's length
    'len_avg': 0,  # average word length
    'letters': {},  # number of total occurances of given letters
    'letters2': {}  # number of total occurances of 2-letter pairs
}



# take each line - word from a file
for line in dict_file:
    # remove endline character
    if line[-1] == '\n':
        line = line[0:len(line)-1]
    # assign 'value' to the word
    # TODO: this value is now just a sequence number - an object could reside here instead
    dict[line] = dict_stats['count']
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
    # update occurances of 2-letters groups
    # convert str into list
    letters = [x for x in line]
    # iterate through list of letters
    for idx in range(len(letters)):
        # try getting current letter and the following - 2-letters pair
        try:
            key = letters[idx] + letters[idx+1]
            # try updating entry in dict_stats['letters2']
            try:
                dict_stats['letters2'][key] += 1
            # no entry yet, create it
            except KeyError as e:
                dict_stats['letters2'][key] = 1
        # no more pairs in current word
        except IndexError as e:
            pass
    # increase word counter
    dict_stats['count'] += 1

# calculate average word length for dict_stats
dict_stats['len_avg'] = \
    sum([dict_stats['lengths'][i] * i for i in range(len(dict_stats['lengths']))]) / dict_stats['count']
# # 1. array of all quantities from dict_stats['lengths']
# [dict_stats['lengths'][i] for i in range(len(dict_stats['lengths']))]
# # 2. array of all quatities from dict_stats['lengths'] multiplied by their values
# [dict_stats['lengths'][i] * i for i in range(len(dict_stats['lengths']))]
# # 3. sum of array of all quatities from dict_stats['lengths'] multiplied by their values
# sum([dict_stats['lengths'][i] * i for i in range(len(dict_stats['lengths']))])
# # 4. sum of array of all quatities from dict_stats['lengths'] multiplied by their values divided by number of lengths
# sum([dict_stats['lengths'][i] * i for i in range(len(dict_stats['lengths']))]) / dict_stats['count']





# # draw stats
# fig_letters = px.bar(x=[letter for letter in dict_stats['letters']],
#               y=[dict_stats['letters'][letter] for letter in dict_stats['letters']], title="Letters")
# fig_letters.show()
#
# fig_lengths = px.bar(x=[i for i in range(len(dict_stats['lengths']))],
#               y=[dict_stats['lengths'][i] for i in range(len(dict_stats['lengths']))], title="Lengths")
# fig_lengths.show()
