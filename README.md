# CrossWords
A python module with tools for generating various crossword puzzles.

------------------------------------------------------------------------------------------------------------------------
VERSION HISTORY :
------------------------------------------------------------------------------------------------------------------------

Change History
  v1.5
    *** check out demo function try_me_grid()
    - initially working grid crossword generator with multiline string grid definition
      (see try_me_2 for details)
    - bug fixes, various modifications
  v1.4.2
    - class GridCrossWord: initially working conversion from string to Word/Cell structure
       still fixing minor details
    - class Word: modified _cells_to_sequences function: only convert cells containing actual letters
      (more like a-z than %,& or _)
  v1.4.1
    - class GridCrossWord: working on conversion from string to Word/Cell structure
  v1.4
    - new class GridCrossWord for constrcting crosswords inside 2d array of Cells
      using Sequence, Dictionary, Cell and Word classes
      * check out function 'sample' inside this GridCrossWord class
  v1.3.1
    - class CrossWords: modified __cells_to_sequence - bugfix
    - minor fixes
    - - class CrossWords: renamed to Word
  v1.3 (kinda functional?)
    *** check out demo function try_me_2
    * this version SEEMS to be capable of generating simple grid crosswords
    - added demo function "try_me_2" for creating simple grid crossword
    - printing the grid containing (hopefully) crossword(s)
    - Working on defining Words in space, generating new type of crossword puzzle
  v1.2.1
    - class CrossWord: development of core structure
    - class Cell: development of core structure
  V1.2
    - started implementing new classes:
      -- Cell: a logical cell in a crosswords diagram (e.g. empty place for letter, huint, etc)
      -- CrossWord: single word in a crosswords diagram: contains Cell(s), Sequence(s)
  v1.1.1
    - Dictionary class: added 'session' attribute -
       for gathering meta-data or 'session' stats, eg. dict loading time, number of uses, etc
    - Dictionary class: match_words now works with no *args
    - minor changes
  v1.1
    - implemented function 'simple_crossword_2' which words like 'simple_crossword'
      but also accepts an iterable of lengths and letter positions for solution words.
      letter positions may be negative (from the end of a word)
      * sample usage in 'try_me_1' function
    - minor changes
    - modified and elaborated, metadata and comments. Clean up.
  v1.0(functional, actualy useful) <<<=====
    *** this version can actually generate a legit crossword - yey ^^
    *** see function try_me_1() for ane xample !
    - implemented simple crossword generator function
      take a look at: function 'simple_crossword'
    - class Dictionary: commented out sequences sorting code - not necessary atm
    - various changes
  ------------
  v0.3.5
    - layout changes to enable code to be imported as module
    - various changes
    - working on simple, sample crossword generator
  v0.3.4
    - various fixes
    - removed origin_words functions (merged into match_words)
    - Sequence class: added 'inWord' now accounting for negative position (from the end of a word)
  v0.3.3
    - Sequence class: added 'inWord' function that determines if sequence belong to a word (accounting position)
    - Sequence class: added match_words function that accepts arbitrary number of sequences and word length
  v0.3.2
    - Sequence class: working on 'origin_words_2' function that accepts 2 Sequence objects
    - Sequence class: added 'origin_words_1' functino - this one accepts a single Sequence object
    - Sequence class: added 'position' attribute - absttract sequence position in a virtual word,
                      changed init args
    - minor changes (printing, etc)
  v0.3.1
    - various considerable changes
  v0.3(functional)
    *** this version is fine for running in an interactive session
    *** run the code - this will load dictionary file and then play with 'origin_words' live
    - moved code to a new class Dictionary
    - implemented function "origin_words" that returns all words (of any or given length)
      that contain particular sequence (at any or given position)
    - generalized sorting code
    - whole words are no more in letter-sequences unless they are actually also a part of other words
    - various changes: structural, others
    - minor changes (e.g. removed plotly histogram examples code)
  v0.2.2
    - further implementation of Sequence class
    - implemented logical connections between Sequence objects
    - various changes: printing, structure, etc.
  v0.2.1
    - started implementing Sequence class
      this class will represent a sequence of letters (not necessarily a whole, legit word but also)
    - started creating sequence dictionaries with objects and conneting them together
  v0.2(functional)
    *** this version is fine for just statistical analysis of a word list
    *** namely: generate dictionaries of sequences of letters (different lengths)
    ***         together with information how many ocurrances of each sequence there are
  v0.1.4
    - generalized similar, repeating pieces of code for counting n-letter sequences
      (this seems to have worsened the performance by a bit, but makes it sooo much easie rto work with the code)
  v0.1.3
    - counting sequences up to 14 letters long
    - all sequences dictionaries sorted by number of occurances
    - minor changes in structure
  v0.1.2
    - counting sequences up to 12-letters long
    - various changes in code structure
  v0.1.1
    - counting sequences of 1-,2-,3-,4-,5-,6- and 7-letters
    - added memory info printout
    - added loading progress printout
  v0.1
    - added loading dictionary from txt file
    - added statistics: word count, words' lengths count, avg word len, letter count, 2-letter pairs count,
    - added histograms (plotly) - words' lengths and single letter occurances








------------------------------------------------------------------------------------------------------------------------
INITIAL DRAFT NOTES :
------------------------------------------------------------------------------------------------------------------------

A crosswords puzzle generator.

Standard crossword has a rectangular shape with square Fields and words go either up->down or left->right.
There are Empty Fields for entering letters and Clue Fields that contain hints
and also point in which neighbouring Empty Field the answers starts and what directions it goes.
- but this conditions can be extended.

The idea is to have a 'structure' of Fields connected in an arbitrary way.
This structure must not necessrily map onto a flat surface.
Fields could potentialy have different shapes, therefore different number of neighbours (e.g. triangular or pentagonal).
    What about following path while filling an aswer - will it be obvious or possible to be marked clearly?

A Clue Field has text inside it, which is a hint for guessing the answer (word).
A Clue Field may consist of one or more empty fields that form a closed shape
    (e.g. rectangle of 2 fields or square of foue)


-----------------------
- The TASK is to:

    The task is to take an empty structure and fill it completely with clues and answers.

    in general - fill a structure of empty Fields with Clues and Empty Fields, so that it can be solved as a crossword.
    in detail - adjust certain parameters and/or fill certain fields and let the program figure out the rest
                most likely by random choice using a provided list of words and their clues.

    This process can be random and have some dgrees of freedom, e.g.
        - how many field should become clue fields (how 'dense' crossword is)
          alternatively: possible lengths of answers (maybe favour shorter or longer words, which would impact 'density')
        - how big a clue field can get (could be usefull for filling 'inconvinient' spots)
        - what directions can answers be established (maybe its possible to write from right to left)
        - possibility of leaving some fileds unused (might be useful while having to fulfill other requirements)
        - which letter must or musn't be used (e.g. crossword which does not use the letter 'm')

    A structure can be partially filled, e.g.:
        - some words and hints could be defined beforehand
        - some particular fields could be filled with letters

    After filling the structure the answers can be left empty and only a geometrical, graphic representation of
        the structure together with hints is printed.
-------------
- Input:
    Dictionary -
        A list of Words and a list Clues.
        Each Word has one more more Clues associated with it.

    Surface -
        A structure of fields to be used.
        May be completely empty or contain any amount of relevant information.

    Constraints -
        A list of constraints regarding the final CrossWords.
-------------
- Output:
    The Surface filled as a crossword with Words and Clues from Dictionary, according to Constraints.


# Possible take - logical structure of CrossWords:
    A Field structure is a graph, basically.
    Each empty field is a graph's vertex.
    Each connection between two empty fields is a graph's edge.
    This way the geometrical structure can be planned beforehand (e.g. simple 2d rectangle or maybe 3d cylinder)
        and then an adequate graph can be created to accomodate it.

    A Clue Field kind of must contains info about:
        - which neigbouring, empty field contains the first letter of the answer.
        - which direction do remaining letters of the answer go (if there is more than one possible direction)
            (as in: 'standard', square crosswords would have at least 2 possibilities - down or right)

    In the simplest case every field has four heigbours (four squares around it)
        and while filling in an answer only a single direction is followed through.
        This direction, together with first field, is indicated by the clue field.


# Possible take - search algorithm
    Look at Words as:
    sequence of letters with additional 'letter' that is actually the hint that must be 'attached' to the Word.
        This 'hint letter' does not have to follow the line.
        This 'hint letter' could share a single space (Field or group of Fields) with one (or possibly many) more hints.
    (So initially it doesnt mater if words actually have their clues already-
      it only matters that there needs to be a space for a clue)
