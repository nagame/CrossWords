# CrossWords
A python module with tools for generating various crossword puzzles.








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
