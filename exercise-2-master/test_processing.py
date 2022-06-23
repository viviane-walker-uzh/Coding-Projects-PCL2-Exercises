#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test_processing.py

# University of Zurich
# Department of Computational Linguistics

# Authors: Viviane Walker, Micha David Hess
# Matriculation Numbers: 18-719-070, 20-719-183


from unittest import TestCase, main
from processing import Joke, JokeGenerator
from os import path


class ProcessingTest(TestCase):
    """
    processing.py non functional tests
    includes the given test method "test_attributes"
    and the new test methods:
        - "test_MakeGenerator_types"
        - "test_Joke_dunder_methods"
    """

## FYI: we focused our own assertions on the newly introduced methods like a dunder method or the make_jokes_objects... :)

    def setUp(self):
        """setting up the input file as a class attribute"""
        self.gen = JokeGenerator("dadjokes_sample.csv")

    def test_attributes(self):
        """
        this test method was given by the tutors"""
        self.gen.make_jokes_objects()

        actual = self.gen.jokes[4]

        self.assertEqual(actual.author, "fredinNH")
        self.assertEqual(actual.link, "https://old.reddit.com/r/dadjokes/comments/rb1tys/why_do_the_numbers_3_and_5_make_such_a_great_team/")
        self.assertEqual(actual._raw_joke, "Why do the numbers 3 and 5 make such a great team? Because together they thrive.")
        self.assertEqual(actual.rating, 2578)
        self.assertEqual(actual.time, "2021-12-07 15:36:32\n")


    def test_MakeGenerator_types(self):
        """tests types in MakeGenerator class"""
        
        # first own assertion: make_jokes_objects()-method # check if the 11th element in the self.jokes list is a Joke class object:
        self.gen.make_jokes_objects()
        actual_2 = self.gen.jokes[6]
        self.assertIsInstance(actual_2, Joke, "Required type of list element is Joke object.")
        
        # second own assertion: make_jokes_objects()-method # check if the JokeGenerator instance attributes jokes is a list - as required:
        self.assertIsInstance(self.gen.jokes, list, "Required type is list.")


    # third own assertion: check output of dunder methods in the Joke class:
    def test_Joke_dunder_methods(self):
        """tests dunder methods __eq__ and __lt__ """

        self.gen.make_jokes_objects()
        A_actual_3 = self.gen.jokes[11] # rating=3951
        B_actual_3 = self.gen.jokes[21] # rating=7539

        # testing if __eq__ returns the desired output:
        self.assertEqual(A_actual_3==B_actual_3,
        ('My mom hired a handyman and gave him a list. \nWhen she got back home, only #1,3 &amp; 5 were completed. \nTurned out he only does odd jobs. ', 7534),
        "Since the rating of B is greater than A, it must repr return the B joke and its rating.")
        
        # testing if __lt__ returns the desired output:
        self.assertEqual(A_actual_3.rating<B_actual_3.rating, True, "Must return true, B has a greater rating than A: 3951 < 7539")


if __name__ == '__main__':
    main()
