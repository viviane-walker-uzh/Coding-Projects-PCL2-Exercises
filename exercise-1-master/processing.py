#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# processing.py

# University of Zurich
# Department of Computational Linguistics

# Authors: # Viviane Walker, Micha David Hess
# Matriculation Numbers: 18-719-070, 20-719-183

from typing import List, Tuple
import re

def split_into_sentences(post_str: str) -> List[str]:
	#remove emoji:
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
	no_emojis = emoji_pattern.sub(r'', post_str)

	
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
	no_emojis = re.sub(r"(?<=\s)\"", "\"\b", no_emojis)
	no_emojis = re.sub(r"(?=\s)\"", "\b\"", no_emojis)
	no_emojis = re.sub(r"(?<=\w)\.\s\.\s\.", " …", no_emojis)
	no_emojis = re.sub(r"(?<=\w)\.\.\.?", " …", no_emojis)
	
	#second, we filter (remove) all empty strings (empty strings emerge when we sub "\n" for " \n ")
	#third, we split the sentences at .?!)… or \n
	return list(filter(lambda x: x != "",re.split(r"(?<=\.|\?|\!|\"|…)\s|(?<=\n)\s", no_emojis)))


def tokenize(sentences_str: List) -> List[List[str]]:
	result = []
	for ele in sentences_str:
		# add spaces before punctuation
		if ele[-1] == "?":
			no_questionmark = re.sub(r"\?", " ?", ele)
			result += [no_questionmark.split()]
		elif ele[-1] == "!":
			no_exclamationmark = re.sub(r"!", " !", ele)
			result += [no_exclamationmark.split()]
		elif ele[-1] == ".":
			no_dot = re.sub(r"\.", " .", ele)
			result += [no_dot.split()]
		elif ele == "\n":
			if ele is not sentences_str[-1]:
				result += [[ele]]
		else:
			result += [ele.split()]
	return result

def filter_profanity(tokenized: List[List[str]], filename: str) -> Tuple[List[List[str]], int]:
	prof_count = 0
	new_lista = []
	result_tokenized = []
	# list of suffixes that often co-occur with the given profanities
	suffixes = {'s', 'es','er','ers', 'in','ing', 'ings', 'ed', 'ly', 'al', 'ally', 'able', '-ass', 'ass'}
	with open(filename, 'r', encoding="utf-8") as f1:
		f1 = tuple(f1.read().split("\n"))
		#print(repr(f1))
		for lista in tokenized:
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
							# 
							currentwordissafe = False
					# if not an inflected profanity
					if currentwordissafe is True:
						new_lista.append(tok)
			result_tokenized.append(new_lista)
			new_lista = []

	res = []
	res = tuple([result_tokenized] + [prof_count])
	return res

def pretty_print(processed: List[List[str]]) -> None:
	for sent in processed:
		# ignores new-line sentences or profanity count
		if sent == '\n' or type(sent) is int:
			continue
		for token in sent:
			try:
				# if a token is the second last element, i.e. in most cases just before the punctuation... 
				if token is sent[-2]:
					# ... it won't have a space after it, but be directly followed by the punctuation
					print(token, end='')
				else:
					# end with a space (instead of a newline)
					print(token, end=' ')
			# to avoid indexErrors in elements with less than two elements
			except IndexError: continue
		# just because yes :)
		print('\n', end='')
	# just because yes, again (: 
	print('\n', end='')

if __name__ == '__main__':
	with open('dadjokes_samples.txt', 'r', encoding='utf-8') as f:
		for line in f.readlines():
			# have fun reviewing our output & leave a positive rating on script-advisor ;)
			pretty_print(filter_profanity(tokenize(split_into_sentences(line)), 'profanities.txt')[0])

# Here be dragons: