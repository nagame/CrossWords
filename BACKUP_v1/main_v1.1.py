# #####################################################################################################################
# Change History
#   v1.1
#     - implemented function 'simple_crossword_2' which words like 'simple_crossword'
#       but also accepts an iterable of lengths and letter positions for solution words.
#       letter positions may be negative (from the end of a word)
#       * sample usage in 'try_me_1' function
#     - minor changes
#     - modified and elaborated, metadata and comments. Clean up.
#   v1.0(functional, actualy useful) <<<=====
#     *** this version can actually generate a legit crossword - yey ^^
#     *** see function try_me_1() for ane xample !
#     - implemented simple crossword generator function
#       take a look at: function 'simple_crossword'
#     - class Dictionary: commented out sequences sorting code - not necessary atm
#     - various changes
#   ------------
#   v0.3.5
#     - layout changes to enable code to be imported as module
#     - various changes
#     - working on simple, sample crossword generator
#   v0.3.4
#     - various fixes
#     - removed origin_words functions (merged into match_words)
#     - Sequence class: added 'inWord' now accounting for negative position (from the end of a word)
#   v0.3.3
#     - Sequence class: added 'inWord' function that determines if sequence belong to a word (accounting position)
#     - Sequence class: added match_words function that accepts arbitrary number of sequences and word length
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
#   ------------
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
#   ------------
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

import os
import psutil
import random
import time
from random import randint


class Sequence:
    """
        A Sequence of letters that may represent a legit word or just a part of some word
    """
    def __init__(self, seq=None, pos=None):
        self.sequence = str(seq)  # this particular sequence string
        self.position = pos  # position of the sequence in a (virtual) word (negative count from the end of word)
        self.word_source_ref = None
        self.count = None  # how many times this sequence appeared in the source data
        self.origin_words = None  # dictionary of words that contain this sequence
        self.contained_sequences = None
        self.inWord = self.in_word  # check if this sequence fits a word (is contained and at position, if provided)

    def __len__(self):
        return len(self.sequence)

    def __str__(self):
        return self.sequence

    def __repr__(self):
        return self.sequence
        # return False

    def in_word(self, word):
        """
            Check if this sequence is contained in word (at all or at given position)
        :param word: word to be checked against
        :return: True or False
        """
        # sequence not in the word at all
        if word.find(self.sequence) == -1:
            return None
        # sequence was found in the word
        # if sequence does not specify position, return True
        if self.position is None:
            return word.find(self.sequence)

        # sequence specifies position, check it
        # if position negative, convert it in the context of provided word
        position_converted = self.position
        if self.position < 0:
            position_converted = len(word) + self.position

        w_strip = word
        pos_ok = None
        if position_converted == w_strip.find(self.sequence):
            pos_ok = True
        else:
            while position_converted >= w_strip.find(self.sequence) > -1:
                if w_strip.find(self.sequence) == position_converted:
                    pos_ok = True
                    break
                # translate position because current word got cut
                position_converted -= w_strip.find(self.sequence) + 1
                # update word
                w_strip = w_strip[w_strip.find(self.sequence) + 1:]
                pass
        return pos_ok


class Dictionary:
    """
        Wrapper for dictionary structure
    """
    def __init__(self, source_file=None, depth=None):
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
        self.load = self._load_dictionary
        # load dictionary
        # source_file = open("small.txt", encoding="utf-8")
        if source_file is not None and depth is not None:
            self._load_dictionary(source_file, depth)

    def _load_dictionary(self, source_file, depth):
        """
            Load dictionary from file.
            Create dict structures that ontain words and letter sequences of all possible lengths.
            Create Sequence objects and link words with sequences.
        :param source_file: dictionary source file: expecting txt file with one entry (preferably single word) per line
        :return: nothing
        """
        # count Sequence objects
        sequence_objects_num = 0

        # # report memory usage
        # mem_use_kb_1 = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
        # print('Process memory, initial:', mem_use_kb_1, 'kb')

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
                            except TypeError:
                                # word doesnt yet have contained_sequences dictionary
                                # initialize it
                                word_obj.contained_sequences = \
                                    {seq_key: self.dictionary['letters'+str(seq_len)][seq_key]}
                        # no entry yet, create it
                        except KeyError:
                            # create Sequence object, assign actual letter sequence
                            sequence_objects_num += 1
                            seq_obj = Sequence(seq_key)
                            seq_obj.count = 1
                            # add current word as first origin
                            seq_obj.origin_words = {line: word_obj}
                            # also update word object with reference to this sequence
                            try:
                                # word already has contained_sequences dictionary
                                word_obj.contained_sequences[seq_key] = seq_obj
                            except TypeError:
                                # word doesnt yet have contained_sequences dictionary
                                # initialize it
                                word_obj.contained_sequences = {seq_key: seq_obj}
                            # put object into dictionary
                            self.dictionary['letters'+str(seq_len)][seq_key] = seq_obj
                    # no more sequences in current word
                    except IndexError:
                        pass

        # calculate average word length for dict_stats
        self.dictionary['len_avg'] = \
            sum([self.dictionary['lengths'][i] * i
                 for i in range(len(self.dictionary['lengths']))]) / self.dictionary['count']
        # 'progress print ending (and new line symbol)
        print('Loading source file... 100% - '+str(self.dictionary['count'])+' words loaded.')
        # # stop counting time of loading basic dictionary structure
        # performance timer 'stop' and print
        print(f'Depth {depth} dictionary structure loading time:   ', time.perf_counter() - timing)

        # # # sort letters sequences dictionaries by number of occurances
        # # performance timer 'start'
        # timing = time.perf_counter()
        # for seq_len in range(seq_len_min, seq_len_max + 1):
        #     self.dictionary[f'letters{seq_len}'] = \
        #         {k: v for k, v in
        #          sorted(self.dictionary[f'letters{seq_len}'].items(), key=lambda item: item[1].count, reverse=True)}
        # # performance timer 'stop' and print
        # print('Sorting time:', time.perf_counter() - timing)

        # # report memory usage
        # mem_use_kb_2 = psutil.Process(os.getpid()).memory_info()[0]/1024  # memory usage by the process [kb]
        # print('Process memory after loading:', mem_use_kb_2, 'kb')

        # print dictionary info
        # number of words
        print(f'Words: {len(self.dictionary["words"])}')

        # print number of sequences for each length and number of Sequence objects created
        # for seq_len in range(1, 19):
        #     # construct sequence key - basically a sequence of letters from current word
        #     print(f' Letters{seq_len}: {len(self.dictionary[f"letters{seq_len}"])} ')

        print(f'Sequence objects: {sequence_objects_num}')
        # print(f'Dictionary ~size in memory: {(mem_use_kb_2-mem_use_kb_1)/1024}Mb')

    def match_words(self, *args, length=None):
        """
        :param args: 1 or more sequence(s) objects
                        sequence object contains string
                        and possibly a position of the sequence(s) in a word (any if None)
        :param length: length of words (any if None)
        :return: dictionary of words (of given length or all lengths) that contain the sequence
        (at given or any position)
        """
        # 1. check qhich sequence gives the shortest list of origin words and start with it
        #     this way the rest of filtering is done on the smallest initial set
        # 2. filter shortest_seq_words by length provided
        # 3. check all sequences against 'words'
        #    for every word check if:
        #       - every sequence in this word at certain position
        # * variable 'words' always holds words filtered in previous step

        # find the sequence that yields the least amount of words
        # this is an optimization step - not functional
        shortest_seq_arg_idx = 0
        for arg_idx in range(len(args)):
            key = f'letters{len(args[arg_idx])}'
            if len(self.dictionary[key][str(args[arg_idx])].origin_words) < \
                len(self.dictionary
                    [f'letters{len(args[shortest_seq_arg_idx])}'][str(args[shortest_seq_arg_idx])].origin_words):
                shortest_seq_arg_idx = arg_idx

        # get sequence words (of which sequence yields the least amount of words)
        key = f'letters{len(args[shortest_seq_arg_idx])}'
        # gett origin words directly from an appropriate letter-sequence dictionary
        words = self.dictionary[key][str(args[shortest_seq_arg_idx])].origin_words
        # also check if this sequence isnt a word by itself
        if args[shortest_seq_arg_idx] in self.dictionary['words']:
            words[str(args[shortest_seq_arg_idx])] = self.dictionary[key][str(args[shortest_seq_arg_idx])]

        # filter by length, if provided
        words_filtered = {}
        if length is not None:
            for w in words:
                if len(w) == length:
                    words_filtered[w] = words[w]
            # update words dictionary
            words = words_filtered

        # # filter by all sequences and their positions
        # for every sequence provided
        words_filtered = {}
        # for every word check if sequence is contained and if position is ok
        for w in words:
            # filtering result
            word_ok = True
            # go through all sequences for this particular word w
            for arg_idx in range(len(args)):
                # get current sequence
                s = args[arg_idx]
                # check if sequence fits the word
                if s.in_word(w) is None:
                    word_ok = False
                    break
            if word_ok is True:
                words_filtered[w] = words[w]
        words = words_filtered
        return words


def load_dictionary(filename, depth):
    source_file = open(filename, encoding="utf-8")
    return Dictionary(source_file, depth)


# if __name__ == '__main__':


D = None


def simple_crossword(solution):
    """
    Construct a simple crossword with questions in rows and answer in a single column.
    There are as many question as there are letters in the solution.
    :param solution: string representing the solution
    :return: a crossword in string format
    """
    global D
    print(f'Solution: {solution}\n{"- "*10}')
    crossword_string = ''
    # go through every letter of solution and figure out a question for it
    offset = 20
    for letter in solution:
        if letter is ' ':
            crossword_string_line = ' ' * offset + '| |'  # just an empty line, a space in solution
        else:
            tries_left = 100  # this many tries to randomly find matching word
            while tries_left is not 0:
                word_length = randint(3, 15)
                letter_position = randint(1, word_length-1)  # which letter in answer belongs to solution
                possible_words = D.match_words(Sequence(letter, letter_position), length=word_length)
                tries_left -= 1
                if len(possible_words) is not 0:
                    break  # possible words found! break the try loop and go choose a word
            else:
                raise(LookupError(f'Couldnt find matching words for letter: {letter}'))

            # random selection from the set of matching words
            chosen_word = random.choice(list(possible_words.keys()))
            # offset for pretty printing
            word_offset = offset-letter_position
            # crossword prettyprint line for the letter
            crossword_string_line = ' '*word_offset + ''.join([
                f'|{chosen_word[n].upper()}|' if n == letter_position else chosen_word[n]
                for n in range(len(chosen_word))
            ])
        crossword_string += crossword_string_line + '\n'
    print(crossword_string)


def simple_crossword_2(solution, lengths=None, positions=None):
    """
    Construct a simple crossword with questions in rows and answer in a single column.
    There are as many question as there are letters in the solution.
    Each word length can be specified (or not - then random).
    Each solution letter's position in its word can be specified (or not - then random)
    :param solution: string representing the solution
    :param lengths: iterable of lengths of words
    :param positions: iterable of solutions' letters' positions in words
    :return: a crossword in string format
    """
    global D
    print(f'Solution: {solution}\n{"- "*10}')
    crossword_string = ''
    # go through every letter of solution and figure out a question for it
    offset = 20
    letter_cnt = 0
    for letter in solution:
        if letter is ' ':
            crossword_string_line = ' ' * offset + '| |'  # just an empty line, a space in solution
        else:
            # are position and length provided for current word or will it be random
            if positions is not None and lengths is not None:
                # if position and length of the word is provided there will only be one 'match_words' call
                tries_left = 1
            else:
                tries_left = 100   # this many tries to randomly find matching word

            while tries_left is not 0:
                # get expected word length from argument or generate random
                try:
                    word_length = lengths[letter_cnt]
                except TypeError or IndexError:
                    word_length = randint(3, 15)
                # get expected letter position from argument or generate random
                try:
                    letter_position = positions[letter_cnt]
                except TypeError or IndexError:
                    letter_position = randint(3, 15)
                # get matching words
                possible_words = D.match_words(Sequence(letter, letter_position), length=word_length)
                # if no tries left
                tries_left -= 1
                if len(possible_words) is not 0:
                    # random selection from the set of matching words
                    chosen_word = random.choice(list(possible_words.keys()))
                    # if position negative, convert it in the context of provided word
                    position_converted = letter_position
                    if letter_position < 0:
                        position_converted = len(chosen_word) + letter_position
                    # offset for pretty printing
                    word_offset = offset - position_converted
                    # crossword prettyprint line for the letter
                    crossword_string_line = ' ' * word_offset + ''.join([
                        f'|{chosen_word[n].upper()}|' if n == position_converted else chosen_word[n]
                        for n in range(len(chosen_word))
                    ])
                    break  # possible words found! go to the next letter
            else:
                # # no matching word found
                # raise(LookupError(f'Couldnt find matching words for letter: {letter}'))
                # construct crossword line without a word
                crossword_string_line = \
                    ' ' * (offset-2) + '_' * 2 + '|'+letter.upper()+'|' + '_' * 2  # a space in solution

        crossword_string += crossword_string_line + '\n'
        letter_cnt += 1
    print(crossword_string)


def try_me_1():
    """
    Demo function showing how to
        - use Dictionary class
        - use Sequence class
        - create a simple crossword
    :return:
    """
    global D

    # # print some stuff and initiate things
    print('*'*30)

    # open source text file - one entry per line (preferably one word)
    # source_file = open("slowa2.txt", encoding="utf-8")
    source_file = open("small.txt", encoding="utf-8")

    S = Sequence  # class alias
    D = Dictionary(source_file, depth=(1, 18))  # Dictionary module root object
    d = D.dictionary

    # get words starting with 'a' and ending with 'ing', containing letter b, with length 8
    D.match_words(S('a', 1), S('ing', -3), S('i'), length=8)

    # report memory usage
    mem_use_kb_2 = psutil.Process(os.getpid()).memory_info()[0] / 1024  # memory usage by the process [kb]
    print('Process memory after loading:', mem_use_kb_2, 'kb')
    print('*' * 30)

    # # generate sample crosswords
    simple_crossword('python rocks')
    simple_crossword_2('python', lengths=[10 for x in range(15)], positions=[x for x in range(15)])
    # simple_crossword_2('adrian iwonka', positions=[x for x in range(15)])
    simple_crossword_2('python', lengths=[x for x in range(3, 15, 2)], positions=[-x for x in range(2, 15)])


try_me_1()
