'''
madison_property.py

Summary: Code for finding words in a given dictionary
that satisfy the "madison" properpty.

Author: David Abel, david-abel.github.io
Date: October 2018
'''


# Python imports.
import random
import operator
from collections import defaultdict

def _is_bad_word(word):
	return not word.isalpha() or len(word) == 1 and word not in ["a", "i"]

def _remove_non_alpha(line):
	'''
	Args;
		line (str)

	Returns:
		(str)

	Summary:
		Removes all non-alpha symbols and replaces them with spaces.
	'''
	line = line.lower()
	line = line.strip()
	bad_symbols = ["\n", "\t", ",", ".", "-", "!", "?", "'", ":", "-", "_", "[", "]", '"', '`', '(', ')', ';']
		
	for sym in bad_symbols:
		line = line.replace(sym, " ")

	return line

def convert_to_corpus(file_name, out_file_name):
	'''
	Args:
		file_name (str)
		out_file_name (str)

	Summary:
		Takes a given txt file and turns it into a file that
		contains all unique words in @file_name, one word per line.
	'''

	# Get unique words in text.
	word_dict = defaultdict(int)
	for line in file(file_name, "r").readlines():
		line = _remove_non_alpha(line)
		line = line.split(" ")
		for word in line:
			if _is_bad_word(word):
				continue
			# out_file.write(word + "\n")
			word_dict[word] += 1

	sorted_words = sorted(word_dict.keys())

	# Write all words to out file.
	out_file = file(out_file_name, "w+")
	for word in sorted_words:
		out_file.write(word + "\n")
	out_file.close()

def load_words_to_dict(file_name="words.txt"):
	'''
	Returns:
		(defaultdict(int)): Loads all words in @file_name into a word dict with:
			Key-->word
			Val-->1
	'''
	word_dict = defaultdict(int)
	for word in file(file_name, "r").readlines():
		word_dict[word.strip().lower()] = 1
	return word_dict

def is_madison_property(word, all_words, original_word_len=None):
	'''
	Args:
		word (str)
		all_words (list)

	Returns:
		(bool)
		(int)
		(list)
	'''

	if original_word_len is None:
		original_word_len = len(word)

	# Base case.
	if len(word) < original_word_len and word in all_words:
		return True, 1, [word]

	if len(word) == 1 and len(word) < original_word_len and word not in all_words:
		return False, 0, []

	# Recursive case.
	for i in range(1, len(word)):
		sub_word = word[:i]
		remainder = word[i:]

		# print sub_word, remainder

		is_sub_madison, num_sub_words, sub_words = is_madison_property(sub_word, all_words, original_word_len)
		is_rem_madison , num_rem_sub_words, rem_words = is_madison_property(remainder, all_words, original_word_len)
		if is_sub_madison and is_rem_madison:
			return True, num_sub_words + num_rem_sub_words, sub_words + rem_words

	return False, 0, []

def get_all_madison_words(word_dict):
	'''
	Args:
		word_dict (dict)

	Returns:
		(dict)
	'''
	all_madison_words = defaultdict(int)
	for i, word in enumerate(word_dict.keys()):
		is_mad_word, num_sub_words, sub_words = is_madison_property(word, word_dict)
		if is_mad_word:
			all_madison_words[word] = num_sub_words, sub_words

	return all_madison_words

def display_results(madison_words, all_words):
	'''
	Args:
		madison_words (dict)
	'''

	sorted_by_madison_density_words = sorted(madison_words.items(), key=operator.itemgetter(1))
	sorted_by_len_madison_words = sorted(madison_words.keys(), key=len)

	# Display results.
	print "Shortest:", sorted_by_len_madison_words[0], madison_words[sorted_by_len_madison_words[0]][1]
	print "Longest:", sorted_by_len_madison_words[-1], madison_words[sorted_by_len_madison_words[-1]][1]
	print "Highest Density:", sorted_by_madison_density_words[-1]
	print "Madison ratio:", round(float(len(madison_words.keys())) / len(all_words.keys()), 3)
	print "Madison words:", len(madison_words.keys())
	print "Total words:", len(all_words.keys())

def main():

	# Use alice.
	out_file = "alice_corpus.txt"
	convert_to_corpus("alice.txt", out_file)

	# Load words.
	all_words = load_words_to_dict(file_name=out_file)

	# Get all madison words.
	all_madison_words = get_all_madison_words(all_words)

	# Show results.
	display_results(all_madison_words, all_words)

if __name__ == "__main__":
	main()
