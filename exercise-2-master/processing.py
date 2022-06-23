#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# processing.py

# University of Zurich
# Department of Computational Linguistics

# Authors: Viviane Walker, Micha David Hess
# Matriculation Numbers: 18-719-070, 20-719-183


from lib2to3.pgen2 import token
import time
from typing import List, Tuple
import re
import random
import csv


class Joke:
    """
    pre-processing of jokes:
    - #TODO handle .csv, .txt, str, ... as input
    - sentence splitting
    - tokenization within each sentence
    - covering up profanities in sentences

    printing processed jokes:
    - printing joke with build up
    - printing joke in a "pretty" way
    - implementation of various dunder methods:
        - 
    """

    def __init__(self, raw_joke: str) -> None:
        try:
            self.author, self.link, raw_joke = raw_joke.split(',', 2)
            self._raw_joke, score, self.time = raw_joke.rsplit(',', 2)
        except ValueError:
            self._raw_joke = raw_joke
            score, self.author, self.link, self.time = 0,'','',''
        self._sentence_split = self._split_into_sentences()
        self._tokenized = self._tokenize()
        self._profanityless = self._filter_profanity()
        self.joke = ''
        self.rating = int(float(score))

    def _split_into_sentences(self) -> List[str]:
        """removes emojis and
        splits sentences """
        # remove emoji(s):
        if len(self._raw_joke) == 0:
            raise ValueError('must have a string to construct a joke')
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002500-\U00002BEF"  # chinese char
                            u"\U00002702-\U000027B0"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            u"\U0001f926-\U0001f937"
                            u"\U00010000-\U0010ffff"
                            u"\u2640-\u2642"
                            u"\u2600-\u2B55"
                            u"\u200d"
                            u"\u23cf"
                            u"\u23e9"
                            u"\u231a"
                            u"\ufe0f"  # dingbats
                            u"\u3030"
                            "]+", flags=re.UNICODE)
        no_emojis = emoji_pattern.sub(r'', self._raw_joke)
        
        # split sentences:
        #first, we sub "\n" for " \n " to that our re.split pattern works:
        no_emojis = re.sub(r"\n", " \n ", no_emojis)

        # if the last element (besides whitespaces/newlines) is a letter or digit, i.e. if punctuation is missing: 
        if no_emojis.rstrip(' \n')[-1].isalnum() is True:
            # remove whitespaces and newlines...
            no_emojis = no_emojis.rstrip(' \n')
            # ... and add a period and a newline
            no_emojis = f'{no_emojis}. \n'
        # inserting whitespace before/after quotation marks (if missing),
        # turning all multi-period punctuation (../.../. . .) into the single character ' …' 
        
        # turning "word" into 'word' for the sake of quotation-mark disambiguation:
        no_emojis = re.sub(r"\"(\w+)\"", r"'\1'", no_emojis)
        # double quotation-mark pretokenization:
        no_emojis = re.sub(r"(?<=\s)\"", "\"\b", no_emojis)
        no_emojis = re.sub(r"(?=\s)\"", "\b\"", no_emojis)
        no_emojis = re.sub(r"(?=\s)\"", "\b\"", no_emojis)
        # no_emojis = re.sub(r"(?=\w+\b\")\"\b", "\"", no_emojis)
        # triple-dot unification/correction/standardization:
        no_emojis = re.sub(r"(?<=\w)\.\s\.\s\.", " …", no_emojis)
        no_emojis = re.sub(r"(?<=\w)\.\.\.?", " …", no_emojis)
        
        #second, we filter (remove) all empty strings (empty strings emerge when we sub "\n" for " \n ")
        #third, we split the sentences at .?!)… or \n
        # self._sentence_split = list(filter(lambda x: x != "",re.split(r"(?<=\.|\?|\!|\"|…)\s|(?<=\n)\s", no_emojis)))     
        return list(filter(lambda x: x != "",re.split(r"(?<=\.|\?|\!|\"|…)\s|(?<=\n)\s", no_emojis))) # --> self._sentence_split

    def _tokenize(self) -> List[List[str]]:
        """
        tokenizes splitted sentences into tokens
        ?,! and . count as a seperate token.
        """
        result = []
        for ele in self._sentence_split:
            # add spaces before punctuation
            try:
                if ele[-1] == "?":
                    no_questionmark = re.sub(r"\?", " ?", ele)
                    result += [no_questionmark.split()]
                elif ele[-1] == "!":
                    no_exclamationmark = re.sub(r"!", " !", ele)
                    result += [no_exclamationmark.split()]
                elif ele[-1] == ".":
                    no_dot = re.sub(r"\.", " .", ele)
                    result += [no_dot.split()]
                elif ele[-2:] in ('."','!"','?"','…"'):
                    no_dot = re.sub(r'([\.\?!…]")', r' \1', ele)
                    result += [no_dot.split()]
                elif ele == "\n":
                    if ele is not self._sentence_split[-1]:
                        result += [[ele]]
                else:
                    result += [ele.split()]
            except IndexError:
                continue
        return result #--> self._tokenized


    def _filter_profanity(self, filename="profanities.txt") -> Tuple[List[List[str]], int]:
        """
        filters profanities (including version with suffixes) and covers each character in a profanity
        with a "#".
        """
        if self._tokenized == []:
            raise Warning('Joke isn\'t tokenized yet')
        prof_count = 0
        new_lista = []
        result_tokenized = []
        # list of suffixes that often co-occur with the given profanities
        suffixes = {'s', 'es','er','ers', 'in','ing', 'ings', 'ed', 'ly', 'al', 'ally', 'able', '-ass', 'ass'}
        with open(filename, 'r', encoding="utf-8") as f1:
            f1 = tuple(f1.read().split("\n"))
            for lista in self._tokenized:
                for tok in lista:
                    # if token is in the profanity-list (tuple, technically)
                    if tok in f1:
                        prof_count += 1
                        covered_tok = len(tok) * "#"
                        new_lista.append(covered_tok)
                        continue
                    # non-lemma profanity filtering
                    else:
                        currentwordissafe = True
                        for profanity in f1:
                            if (profanity in tok) and (tok[tok.index(profanity)+len(profanity):] in suffixes):
                                prof_count += 1
                                covered_tok = len(tok) * "#"
                                new_lista.append(covered_tok)
                                currentwordissafe = False
                                break
                        # if not an inflected profanity
                        if currentwordissafe is True:
                            new_lista.append(tok)
                result_tokenized.append(new_lista)
                new_lista = []

        profanity_filtered = tuple([result_tokenized] + [prof_count])
        return profanity_filtered # self._profanityless

    def tell_joke(self) -> None:
        """
        Assuming an intellectual such as ourselves is able to read on average 4 words per seconds (240 words/minute),
        this function tells a joke and takes into account the length of the joke's setup in defining the waiting time before revealing the punchline.
        """
        # if it's a one-sentence joke:
        if self._profanityless[0][0] is self._profanityless[0][-1]:
            for token in self._profanityless[0][0]:    
                        if token is sentence[-1]:
                                print(token, end='')
                        else:
                            print(token, end=' ')
            print('')
        
        else:
            for sentence in self._profanityless[0]:
                # if it is the last sentence:
                if sentence is self._profanityless[0][-1]:
                    # calculates the number of words in the setup
                    n_of_words = sum(len(ls) for ls in self._tokenized if ls is not self._tokenized[-1])
                    # sets the punchline-waiting-time according to our estimated reading speed and the length of the setup 
                    time.sleep(n_of_words/4)
                    for token in sentence:
                        if token is sentence[-1]:
                            print(token, end='')
                        else:
                            print(token, end=' ')
                else:
                    for token in sentence:    
                        if token is sentence[-1]:
                                print(token, end='')
                        else:
                            print(token, end=' ')
                print('')

    @staticmethod
    def pretty_print(joke) -> str:
        """
        returns the joke after being processed in a readable format
        """
        return repr(Joke(joke))

    def __repr__(self):
        """
        returns a nicely formated string of a Joke.
        """
        jokestring = ''
        
        for sent in self._profanityless[0]:
            for token in sent:
                try:
                    # if a token is the second last element, i.e. in most cases just before the punctuation... 
                    if token is sent[-2]:
                        # ... it won't have a space after it, but be directly followed by the punctuation
                        jokestring += token
                    else:
                        # end with a space (instead of a newline)
                        jokestring += token + ' '
                # to avoid indexErrors in elements with less than two elements
                except IndexError: continue
            # add a newline except at the end
            if sent is not self._profanityless[0][-1]:
                jokestring += '\n'
        return jokestring

    def __eq__(self, other):
        """
        compares two objects of type(joke), returns the joke with the higher score and its score
        """
        if self.rating > other.rating:
            return self.__repr__(), self.rating
        elif self.rating < other.rating:
            return other.__repr__(), other.rating
        elif self.rating == other.rating:
            return 'both jokes are equally hilarious, much haha lmao rofl! \n', self.__repr__(), self.rating, other.__repr__(), other.score

    def __lt__(self, other):
        """
        compares two jokes' scores A < B, returns True 
        if joke A's score is lower than joke B's score, else returns False.
        """
        if self.rating < other.rating:
            return True
        return False

    def __gt__(self, other):
        """
        compares two jokes' scores A > B, returns True 
        if joke A's score is higher than joke B's score, else returns False.
        """
        if self.rating > other.rating:
            return True
        return False

    def __le__(self, other):
        """
        compares two jokes' scores A <= B, returns True 
        if joke A's score is lower than or equal to joke B's score, else returns False.
        """
        if self.rating <= other.rating:
            return True
        return False

    def __ge__(self, other):
        """
        compares two jokes' scores A >= B, returns True 
        if joke A's score is higher than or equal to joke B's score, else returns False.
        """
        if self.rating >= other.rating:
            return True
        return False


class JokeGenerator:
    """
    creates a list of Jokes from a .csv file.
    """

    def __init__(self, filename) -> None:
        self.jokes = []
        self.filename = filename


    def make_jokes_objects(self) -> List:
        """
        turns jokes from a .csv file into Joke objects, appends them to the JokeGenerator's list of jokes
        """
        with open(self.filename, 'r', encoding='utf-8') as f:
            # skips the first line
            f.readline()
            self.jokes.extend([Joke(joke)for joke in f.readlines()])
                # author, link, jokestr = line.split(',', 2)
                # jokestr, score, date = jokestr.rsplit(',', 2)
                # joke = Joke(jokestr)
                # joke.rating = float(score)
                # joke.author = author
                # joke.link = link
                # joke.time = date
                # self.jokes.append(joke)

    def generate_jokes(self) -> None:
        """
        tells a random joke if it is longer than one sentence
        """
        viable_joke = False
        while viable_joke == False:
            randomjoke = self.jokes[random.randint(0, len(self.jokes)-1)]
            if len(randomjoke._sentence_split) > 1:
                viable_joke = True
        randomjoke.tell_joke()


    def random_joke(self) -> Joke:
        """
        Only accepts and pretty prints jokes which are longer than one sentence len(self._split) > 1:
        """
        # a random joke of the JokeGenerator's List retrieved with a random index of the list (delimited by the length of the joke-list)
        randomjoke = self.jokes[random.randint(0, len(self.jokes)-1)]
        print(repr(randomjoke))
        return randomjoke

# BONUS:
def find_highest_score(jokes: JokeGenerator):
    sorted_jokes = sorted(jokes.jokes, key=lambda x: x.rating, reverse=True)
    return sorted_jokes[0]

# feel free to use the (un-)commented function calls below to test our code :)
if __name__ == '__main__':
    
    # reading in the dadjokes csv file and making joke objects:
    dad_jokes = JokeGenerator('dadjokes_sample.csv')
    dad_jokes.make_jokes_objects()

    print(find_highest_score(dad_jokes))
    # Joke.tell_joke(dad_jokes.jokes[22]) # prints punchline with delay based on an average readers reading speed.
    # print(dad_jokes.jokes) # prints list of joke objects
    # dad_jokes.generate_jokes() # prints jokes
    # dad_jokes.random_joke() # prints a random joke
    # print(dad_jokes.jokes[44]) # == print(find_highest_score(dad_jokes)) # test the bonus method
    # print(Joke.pretty_print('What do you call a cop in a bed? (Lord help me) Pig in a blanket 😄☝😭🐷')) #prints the output of a single string as input
