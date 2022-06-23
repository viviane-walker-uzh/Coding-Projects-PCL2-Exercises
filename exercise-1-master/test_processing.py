#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test_processing.py

# University of Zurich
# Department of Computational Linguistics

# Authors: # Viviane Walker, Micha David Hess
# Matriculation Numbers: 18-719-070, 20-719-183


# Test Units for dad_jokes Analyzer Engine
# Module for functional and non functional testing of dad_jokes_processor module

# Import Statements
from unittest import TestCase, main
import processing
from os import path


class LpTest(TestCase):
    """
    dad_jokes_processor non functional tests
    """

    def test_output_split_into_sentences_function(self):
        # examplary test assertion (given by tutors): type ->list
        dad_joke_1 = "Want to hear a construction joke?\nI'm working on it."
        result_1 = processing.split_into_sentences(dad_joke_1)
        self.assertIsInstance(result_1, list, "Required type of output is list")
        #TODO: 2 own test assertions
        # 1st own test assertion: no emojis
        dad_joke_2 = "Pig in a blanket. 😄☝😭🐷" #cut off for controlling removal of emojis only (without considering sentence splitting)
        result_2 = processing.split_into_sentences(dad_joke_2)
        self.assertEqual(result_2, ["Pig in a blanket."], "Did not remove emoji(s)")
        # 2nd own test assertion: \n
        dad_joke_3 = "Want to hear a construction joke?\nI'm working on it 🏗 🛠."
        result_3 = processing.split_into_sentences(dad_joke_3)
        self.assertIsInstance(result_3, list, "Required type of output is list")

    def test_output_tokenize_function(self):
        # examplary test assertion (given by tutors):
        split_dad_joke_1 = ["Want to hear a construction joke?", "\n", "I'm working on it."]
        result_1 = processing.tokenize(split_dad_joke_1)
        target_1 = [["Want", "to", "hear", "a", "construction", "joke", "?"], ["\n"], ["I'm", "working", "on", "it", "."]]
        self.assertEqual(result_1, target_1)
        #TODO: 2 own test assertions, we did 3:
        # 1st own test assertion: with ?
        split_dad_joke_2 = ["What do you call a cop in a bed?", "(Lord help me) Pig in a blanket"]
        result_2 = processing.tokenize(split_dad_joke_2)
        target_2 = [["What", "do", "you", "call", "a", "cop", "in", "a", "bed", "?"], ["(Lord", "help", "me)", "Pig", "in", "a", "blanket"]]
        self.assertEqual(result_2, target_2, "tokenization did not work correctly.")
        # 2nd own test assertion: with …
        split_dad_joke_3 = ["I ate the Scrabble tiles O, U, O, N, Y and T", "…", "I shit you not."]
        result_3 = processing.tokenize(split_dad_joke_3)
        target_3 = [["I", "ate", "the", "Scrabble", "tiles", "O,", "U,", "O,", "N,", "Y", "and", "T"], ["…"], ["I", "shit", "you", "not", "."]]
        self.assertEqual(result_3, target_3)
        # 3rd own test assertion: with . . .
        split_dad_joke_3 = ["Vampires.", ".", ".", "sure are a pain in the neck!"]
        result_3 = processing.tokenize(split_dad_joke_3)
        target_3 = [["Vampires", "."], ["."], ["."], ["sure", "are", "a", "pain", "in", "the", "neck", "!"]]
        self.assertEqual(result_3, target_3, "Something did not work with the tokenization of three dots in a row with space.")

    def test_output_filter_profanity_function(self):
        # examplary test assertion (given by tutors): fuck
        tokenized_dad_joke_1 = [["Want", "to", "fuck", "a", "construction", "joke", "?"], ["\n"], ["I'm", "working", "on", "it", "."]]
        result_1 = processing.filter_profanity(tokenized_dad_joke_1,"profanities.txt")
        target_1 = ([["Want", "to", "####", "a", "construction", "joke", "?"], ["\n"], ["I'm", "working", "on", "it", "."]], 1)
        self.assertEqual(result_1, target_1, "Covering up Fluchwörtner does not work..")
        #TODO: 2 own test assertions
        # # 1st own test assertion: type -> tuple:
        tokenized_dad_joke_2 = [["I", "ate", "the", "Scrabble", "tiles", "O,", "U,", "O,", "N,", "Y", "and", "T"], ["…"], ["I", "shit", "you", "not", "."]]
        result_2 = processing.filter_profanity(tokenized_dad_joke_2, "profanities.txt")
        self.assertIsInstance(result_2, tuple, "The profanity function output is not a tuple.")
        # # 2nd own test assertion: with two profanities (one profanity which is in the profanity file and another which has the suffix -ass)
        tokenized_dad_joke_3 = [["Want", "to", "fuck", "a", "motherfucker-ass", "joke", "?"], ["\n"], ["I'm", "working", "on", "it", "."]]
        result_3 = processing.filter_profanity(tokenized_dad_joke_3,"profanities.txt")
        target_3 = ([["Want", "to", "####", "a", "################", "joke", "?"], ["\n"], ["I'm", "working", "on", "it", "."]], 2)
        self.assertEqual(result_3, target_3, "Covering up Fluchwörtner does not work..")

if __name__ == '__main__':
    main()
