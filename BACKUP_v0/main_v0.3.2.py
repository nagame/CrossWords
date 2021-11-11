
# #####################################################################################################################
# Change History
#   v0.3.2
#     - Sequence class: working on 'origin_words_2' function that accepts 2 Sequence objects
#     - Sequence class: added 'origin_words_1' functino - this one accepts a single Sequence object
#     - Sequence class: added 'position' attribute - absttract sequence position in a virtual word,
#                       changed init args
#     - minor changes (printing, etc)
#   v0.3.1
#     - various considerable changes
#   v0.3(functional)
#     *** this version is fine for running in an interactive session
#     *** run the code - this will load dictionary file and then play with 'origin_words' live
#     - moved code to a new class Dictionary
#     - implemented function "origin_words" that returns all words (of any or given length)
#       that contain particular sequence (at any or given position)
#     - generalized sorting code
#     - whole words are no more in letter-sequences unless they are actually also a part of other words
#     - various changes: structural, others
#     - minor changes (e.g. removed plotly histogram examples code)
#   ----------
#   v0.2.2
#     - further implementation of Sequence class
#     - implemented logical connections between Sequence objects
#     - various changes: printing, structure, etc.
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
import time, curses
from pprint import pprint


class Sequence:
    """
        A Sequence of letters that may represent a legit word or just a part of some word
    """
    def __init__(self, seq=None, pos=None):
        self.sequence = str(seq)  # this particular sequence string
        self.position = pos  # position of the sequence in a (virtual) word
        self.word_source_ref = None
        self.count = None  # how many times this sequence appeared in the source data
        self.origin_words = None  # dictionary of words that contain this sequence
        self.contained_sequences = None

    def __len__(self):
        return len(self.sequence)

    def __str__(self):
        return self.sequence

    def __repr__(self):
        return self.sequence


class Dictionary:
    """
        Wrapper for dictionary structure
    """
    def __init__(self, source_file=None, depth=(1, 5)):
        # data structure describing the dictionary loaded from source file
        self.dictionary = {
            'words': {},  # list of words from the source file
            'count': 0,  # number of words in the dictionary
            'lengths': [0] * 30,  # number of words of given length
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
            'letters14': {},  # number of total occurances of 14-letter pairs
            'letters15': {},  # number of total occurances of 15-letter pairs
            'letters16': {},  # number of total occurances of 16-letter pairs
            'letters17': {},  # number of total occurances of 17-letter pairs
            'letters18': {},  # number of total occurances of 18-letter pairs
        }
        # load dictionary
        source_file = open("small.txt", encoding="utf-8")
        self._load_dictionary(source_file, depth)

    def _load_dictionary(self, source_file, depth):
        """
            Load dictionary from file.
            Create dict structures that ontain words and letter sequences of all possible lengths.
            Create Sequence objects and link words with sequences.
        :param source_file: dictionary source file: expecting txt file with one entry (preferably single word) per line
        :return: nothing
        """
        # report memory usage
        mem_use_kb = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
        print('Process memory, initial:', mem_use_kb, 'kb')

        # source_file = open("slowa2.txt", encoding="utf-8")
        # source_file = open("small.txt", encoding="utf-8")

        # # start counting time of loading basic dictionary structure
        # performance timer 'start'
        timing = time.perf_counter()
        # get total count for progress reference
        self.dictionary['count'] = len(source_file.readlines())
        source_file.seek(0)

        # # ======================================================
        # # build sequences database and link sequences with words
        seq_len_min, seq_len_max = 1, 2
        # current word number
        word_counter = 0
        # detector for progress update notification
        # [0] - next milestone progress, [1] - current progress
        progress_tick = [0, -1]
        # min and max sequence length to build (mostly for testing purposes - speed)
        seq_len_min, seq_len_max = depth[0], depth[1]
        # take each line - word from a file
        for line in source_file:
            # # update loading progress
            word_counter += 1
            progress_tick[1] = (word_counter / self.dictionary['count']) * 100
            # current progress exceeds current milestone
            if progress_tick[1] > progress_tick[0]:
                # notify user of achieved milestone
                print('Loading source file... '+str(progress_tick[0])+'%' +
                      ' ['+str(word_counter)+'/'+str(self.dictionary['count'])+']', end='\r')
                # set next milestone
                progress_tick[0] += 1

            # remove endline character
            line = line.rstrip()

            # assign a word object
            word_obj = Sequence(line)
            word_obj.word_source_ref = word_counter
            self.dictionary['words'][line] = word_obj

            # # update lengths information in dict_stats
            # max and min lengths
            if len(line) > self.dictionary['len_max']:
                self.dictionary['len_max'] = len(line)
            if len(line) < self.dictionary['len_min']:
                self.dictionary['len_min'] = len(line)
            # lengths histogram data
            try:
                self.dictionary['lengths'][len(line)] += 1
            except IndexError as e:
                print(e)
                raise e

            # # update occurances of [s1..s2)-letters sequences
            # # create Sequence objects wor words and letter-sequences, 'connect' objects
            # convert str into list
            letters = [x for x in line]

            # check all sequence lengths
            for seq_len in range(seq_len_min, seq_len_max+1):
                for idx in range(len(letters)):
                    # try getting current letter and the following - 2-letters sequences
                    try:
                        # construct sequence key - basically a sequence of letters from current word
                        seq_key = ''
                        for seq_pos in range(seq_len):
                            seq_key += letters[idx+seq_pos]

                        # dont add current word as a sequence
                        # words that are not parts of any other words will not be included as letter sequences
                        # they will only be wisible in 'words' dictionary
                        # if seq_key == line:
                        #     continue

                        # try updating entry in dict_stats['lettersX']
                        try:
                            # increase sequence ocurrnace counter
                            self.dictionary['letters'+str(seq_len)][seq_key].count += 1
                            # add current word to origins dictionary
                            self.dictionary['letters' + str(seq_len)][seq_key].origin_words[line] = word_obj
                            # also update word object with reference to this sequence
                            try:
                                # word already has contained_sequences dictionary
                                word_obj.contained_sequences[seq_key] = self.dictionary['letters'+str(seq_len)][seq_key]
                            except TypeError as e:
                                # word doesnt yet have contained_sequences dictionary
                                # initialize it
                                word_obj.contained_sequences = {seq_key: self.dictionary['letters'+str(seq_len)][seq_key]}
                        # no entry yet, create it
                        except KeyError as e:
                            # create Sequence object, assign actual letter sequence
                            seq_obj = Sequence(seq_key)
                            seq_obj.count = 1
                            # add current word as first origin
                            seq_obj.origin_words = {line: word_obj}
                            # also update word object with reference to this sequence
                            try:
                                # word already has contained_sequences dictionary
                                word_obj.contained_sequences[seq_key] = seq_obj
                            except TypeError as e:
                                # word doesnt yet have contained_sequences dictionary
                                # initialize it
                                word_obj.contained_sequences = {seq_key: seq_obj}
                            # put object into dictionary
                            self.dictionary['letters'+str(seq_len)][seq_key] = seq_obj
                    # no more sequences in current word
                    except IndexError as e:
                        pass

        # calculate average word length for dict_stats
        self.dictionary['len_avg'] = \
            sum([self.dictionary['lengths'][i] * i for i in range(len(self.dictionary['lengths']))]) / self.dictionary['count']
        # 'progress print ending (and new line symbol)
        print('Loading source file... 100% - '+str(self.dictionary['count'])+' words loaded.')
        # # stop counting time of loading basic dictionary structure
        # performance timer 'stop' and print
        print(f'Depth {depth} dictionary structure loading time:   ', time.perf_counter() - timing)

        # # sort letters sequences dictionaries by number of occurances
        # performance timer 'start'
        timing = time.perf_counter()
        for seq_len in range(seq_len_min, seq_len_max + 1):
            self.dictionary[f'letters{seq_len}'] = \
                {k: v for k, v in
                 sorted(self.dictionary[f'letters{seq_len}'].items(), key=lambda item: item[1].count, reverse=True)}
        # performance timer 'stop' and print
        print('Sorting time:', time.perf_counter() - timing)

        # report memory usage
        mem_use_kb = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
        print('Process memory after loading:', mem_use_kb, 'kb')

        # print dictionary info
        # number of words
        print(f'Words: {len(self.dictionary["words"])}')
        # number of sequences for each length
        for seq_len in range(1,19):
            # construct sequence key - basically a sequence of letters from current word
            print(f' Letters{seq_len}: {len(self.dictionary[f"letters{seq_len}"])} ')

    def origin_words(self, sequence=None, pos=None, length=None):
        """
        :param sequence: sequence of letters
        :param pos: position of the sequence in words (any if None)
        :param length: length of words (any if None)
        :return: dictionary of words (of given length or all lengths) that contain the sequence (at given or any position)
        """

        # if sequence is provided then get origin words for it
        if sequence is not None:
            # get all words that contain this sequence
            key = f'letters{len(sequence)}'
            # gett origin words directly from an appropriate letter-sequence dictionary
            words = self.dictionary[key][sequence].origin_words
            # also check if this sequence isnt a word by itself
            if sequence in self.dictionary['words']:
                words[sequence] = self.dictionary[key][sequence]
        # no sequence provided - use words list
        else:
            words = self.dictionary['words']

        # filter words (length, sequence position)
        if pos is not None or length is not None:
            words_filtered = {}
            for w in words:
                # check if sequence is at particular position in current word
                pos_ok = None
                if pos is not None:
                    # # the sequence will be searched using builtin 'find' -so from the beginning to end
                    # # is sequence is found at position smaller then requested then must check the rest od the word
                    # sequence found at the position
                    if w.find(sequence) == pos:
                        pos_ok = True
                    # sequence found after requested position or not found at all
                    elif w.find(sequence) == -1 or w.find(sequence) > pos:
                        pos_ok = False
                    # sequence found earlier - keep searching
                    elif w.find(sequence) < pos:
                        w_strip = w
                        pos_ok = False
                        while pos > w_strip.find(sequence) > -1:
                            w_strip = w_strip[w_strip.find(sequence)+1:]
                            # translate position because current word got cut
                            pos -= w_strip.find(sequence)+1
                            if w_strip.find(sequence) == pos:
                                pos_ok = True
                                break
                # check if current word has requested length
                len_ok = None
                if length is not None:
                    if len(w) == length:
                        len_ok = True
                    else:
                        len_ok = False
                if not(pos_ok is False or len_ok is False):
                    words_filtered[w] = words[w]
            words = words_filtered
        return words

    def origin_words_1(self, sequence=None, length=None):
        """
        :param sequence: 1 sequence object
                        sequence object contains string
                        and possibly a position of the sequence in a word (any if None)
        :param length: length of words (any if None)
        :return: dictionary of words (of given length or all lengths) that contain the sequence (at given or any position)
        """

        # if sequence is provided then get origin words for it
        if sequence is not None:
            # get all words that contain this sequence
            key = f'letters{len(sequence)}'
            # gett origin words directly from an appropriate letter-sequence dictionary
            words = self.dictionary[key][str(sequence)].origin_words
            # also check if this sequence isnt a word by itself
            if sequence in self.dictionary['words']:
                words[str(sequence)] = self.dictionary[key][str(sequence)]
        # no sequence provided - use words list
        else:
            words = self.dictionary['words']

        # filter words (length, sequence position)
        if sequence.position is not None or length is not None:
            words_filtered = {}
            for w in words:
                # check if sequence is at particular position in current word
                pos_ok = None
                if sequence.position is not None:
                    # # the sequence will be searched using builtin 'find' -so from the beginning to end
                    # # is sequence is found at position smaller then requested then must check the rest od the word
                    # sequence found at the position
                    if w.find(str(sequence)) == sequence.position:
                        pos_ok = True
                    # sequence found after requested position or not found at all
                    elif w.find(str(sequence)) == -1 or w.find(str(sequence)) > sequence.position:
                        pos_ok = False
                    # sequence found earlier - keep searching
                    elif w.find(str(sequence)) < sequence.position:
                        w_strip = w
                        pos_ok = False
                        while sequence.position > w_strip.find(str(sequence)) > -1:
                            w_strip = w_strip[w_strip.find(str(sequence))+1:]
                            # translate position because current word got cut
                            sequence.position -= w_strip.find(str(sequence))+1
                            if w_strip.find(str(sequence)) == sequence.position:
                                pos_ok = True
                                break
                # check if current word has requested length
                len_ok = None
                if length is not None:
                    if len(w) == length:
                        len_ok = True
                    else:
                        len_ok = False
                if not(pos_ok is False or len_ok is False):
                    words_filtered[w] = words[w]
            words = words_filtered
        return words

    def origin_words_2(self, sequence=None, sequence2=None, length=None):
        """
        :param sequence: 1 or more sequence(s) objects
                        sequence object contains string
                        and possibly a position of the sequence(s) in a word (any if None)
        :param length: length of words (any if None)
        :return: dictionary of words (of given length or all lengths) that contain the sequence (at given or any position)
        """


        # get all words that contain this sequence
        key = f'letters{len(sequence)}'
        # gett origin words directly from an appropriate letter-sequence dictionary
        words = self.dictionary[key][str(sequence)].origin_words
        # also check if this sequence isnt a word by itself
        if sequence in self.dictionary['words']:
            words[str(sequence)] = self.dictionary[key][str(sequence)]

        # words_filtered = {}
        # for w in words:
        #     if w.find(str(sequence2)) != -1:
        #         words_filtered[str(w)] = w
        # words = words_filtered

        # # filter according to first sequence
        words_filtered = {}
        # filter words (length, sequence position)
        if sequence2.position is not None or length is not None:
            for w in words:
                # check if sequence is at particular position in current word
                pos_ok = None
                if sequence2.position is not None:
                    # # the sequence will be searched using builtin 'find' -so from the beginning to end
                    # # is sequence is found at position smaller then requested then must check the rest od the word
                    # sequence found at the position
                    if w.find(str(sequence2)) == sequence2.position:
                        pos_ok = True
                    # sequence found after requested position or not found at all
                    elif w.find(str(sequence2)) == -1 or w.find(str(sequence2)) > sequence2.position:
                        pos_ok = False
                    # sequence found earlier - keep searching
                    elif w.find(str(sequence2)) < sequence2.position:
                        w_strip = w
                        pos_ok = False
                        while sequence2.position > w_strip.find(str(sequence2)) > -1:
                            w_strip = w_strip[w_strip.find(str(sequence2)) + 1:]
                            # translate position because current word got cut
                            sequence2.position -= w_strip.find(str(sequence2)) + 1
                            if w_strip.find(str(sequence2)) == sequence2.position:
                                pos_ok = True
                                break
                # check if current word has requested length
                len_ok = None
                if length is not None:
                    if len(w) == length:
                        len_ok = True
                    else:
                        len_ok = False
                if not (pos_ok is False or len_ok is False):
                    words_filtered[w] = words[w]
            words = words_filtered

        # # filter according to second sequence
        words_filtered = {}
        # filter words (length, sequence position)
        if sequence.position is not None or length is not None:
            for w in words:
                # check if sequence is at particular position in current word
                pos_ok = None
                if sequence.position is not None:
                    # # the sequence will be searched using builtin 'find' -so from the beginning to end
                    # # is sequence is found at position smaller then requested then must check the rest od the word
                    # sequence found at the position
                    if w.find(str(sequence)) == sequence.position:
                        pos_ok = True
                    # sequence found after requested position or not found at all
                    elif w.find(str(sequence)) == -1 or w.find(str(sequence)) > sequence.position:
                        pos_ok = False
                    # sequence found earlier - keep searching
                    elif w.find(str(sequence)) < sequence.position:
                        w_strip = w
                        pos_ok = False
                        while sequence.position > w_strip.find(str(sequence)) > -1:
                            w_strip = w_strip[w_strip.find(str(sequence))+1:]
                            # translate position because current word got cut
                            sequence.position -= w_strip.find(str(sequence))+1
                            if w_strip.find(str(sequence)) == sequence.position:
                                pos_ok = True
                                break
                # check if current word has requested length
                len_ok = None
                if length is not None:
                    if len(w) == length:
                        len_ok = True
                    else:
                        len_ok = False
                if not(pos_ok is False or len_ok is False):
                    words_filtered[w] = words[w]
            words = words_filtered
        return words



D = Dictionary(depth=(1, 10))
d = D.dictionary

D.origin_words('home')
# =======================================================================================
"""
Construct a simple crossword with questions in rows and answer in a single column.
There are as many question as there are letters in the solution.
input: string representing the solution
output: a crossword (in what form?)
"""

# solution = 'aberration'
#
# # go through every letter of solution and figure out a question for it
# for letter in solution:
#     possible_words = D.origin_words()
#     print(letter)